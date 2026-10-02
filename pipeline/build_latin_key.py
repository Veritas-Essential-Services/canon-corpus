#!/usr/bin/env python3
# prov: 2026-10-02 claude-opus-5-5 drafted
# fable_review: pending
"""
build_latin_key.py -- Lewis & Short as the key for Latin words, linked to the
Clementine Vulgate's words through Whitaker's WORDS.

    python3 pipeline/build_latin_key.py --fetch   # the pinned Lewis & Short XML (once)
    python3 pipeline/build_latin_key.py           # build data/lemmas/latin-key/
    python3 pipeline/build_latin_key.py --check   # rebuild in memory: byte-identical

The Latin twin of build_strongs.py. Strong's number is the key for a Hebrew
or Greek word, and BDB, Thayer and LSJ hang off it as witnesses. For Latin
there is no numbered concordance, so the key is the entry Lewis & Short
(1879) gives the word, cited `lewis-short:<key>` with Perseus's own entry
key (`adoro`, `malus1`, `malus3`: a homograph carries L&S's number). Whitaker's
WORDS, the house Latin analyzer (README-lemma-spine.md), gets from a form as
written to its dictionary lemma; this build gets from that lemma to the L&S
entry. Rules and reasons: pipeline/README-latin-key.md.

WHAT IT WRITES (data/lemmas/latin-key/, all committed)
    lewis-short.jsonl     THE TABLE. One row per L&S entry (51,645): its key,
                          citation, Perseus entry id, homograph number, entry
                          type, folded headword, and word class as L&S marks
                          it. Facts and pointers only: no definition text.
    whitaker-ls.jsonl     One row per Whitaker lemma: the L&S key it is, and
                          how that was decided (s.3), or why there is none.
    vulgate-forms.jsonl   One row per distinct form of the Vulgate as written
                          (lower-cased): its token count, Whitaker lemmas and
                          L&S keys. No running text.
    vulgate-concordance.jsonl
                          One row per L&S key the Vulgate uses: the verses
                          where a form can only be that word (`sure`), and
                          where it is one reading of several (`possible`).
    manifest.json         Sources, pins, rights, counts, what is not claimed.

NO MINTING
    Nothing goes into data/uids/. A Vulgate verse is cited in the Vulgate's
    own numbering (`Ps.50.3` = vulgate:Ps.50.3); its KJV verse and uid are in
    convert_vulgate's `kjv` field, not repeated here.

A PARTIAL RUN NEVER DELETES
    Without the L&S XML, the Whitaker files or the Vulgate, the committed
    files are carried forward unchanged, so --check passes anywhere.
"""

import collections
import hashlib
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import structure_texts as S  # noqa: E402
import whitaker as W  # noqa: E402

OUT = os.path.join(ROOT, "data", "lemmas", "latin-key")

LS = {
    "repo": "https://github.com/PerseusDL/lexica",
    "commit": "56061ca127f4a2844980baffc5f2b6d1332897b3",
    "path": "CTS_XML_TEI/perseus/pdllex/lat/ls/lat.ls.perseus-eng2.xml",
    "sha256": "a21c3799f42d33931b463c19a036b0e5c4a6504ccbd81ee55a262421a9e1836c",
    "edition": "Lewis & Short, A Latin Dictionary (Oxford: Clarendon Press, 1879)",
}
LS_URL = f"https://raw.githubusercontent.com/PerseusDL/lexica/{LS['commit']}/{LS['path']}"
LS_FILE = os.path.join(S.CORPUS, "lewis-short", LS["commit"][:12], "lat.ls.perseus-eng2.xml")
LS_RIGHTS = {
    "work": "public-domain (1879)",
    "license": "CC BY-SA 4.0 (Perseus's machine-readable text)",
    "attribution": ("Text provided under a CC BY-SA license by Perseus Digital Library, "
                    "http://www.perseus.tufts.edu, with funding from The National Endowment "
                    "for the Humanities. Data accessed from https://github.com/PerseusDL/lexica/ "
                    "[2026-10-02]."),
    "source_url": "https://github.com/PerseusDL/lexica/tree/master/CTS_XML_TEI/perseus/pdllex/lat/ls",
    "committed": "entry keys, Perseus entry ids, homograph numbers, entry types and the "
                 "word-class tags only; no definition text",
    "redistribute_whole": False,
}

# ---------------------------------------------------------------------------
# Lewis & Short
# ---------------------------------------------------------------------------

RE_ENTRY = re.compile(r"<entryFree ([^>]*)>(.*?)</entryFree>", re.S)
RE_ATTR = re.compile(r'(\w+)="([^"]*)"')
RE_POS = re.compile(r"<pos>([^<]*)</pos>")
RE_GEN = re.compile(r"<gen>([^<]*)</gen>")
RE_ORTH = re.compile(r"<orth [^>]*>([^<]*)</orth>")
HEAD_CHARS = 800          # the word class is printed in an entry's opening line


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fetch():
    if os.path.exists(LS_FILE) and sha256_file(LS_FILE) == LS["sha256"]:
        print(f"  have {os.path.relpath(LS_FILE, ROOT)}")
        return
    os.makedirs(os.path.dirname(LS_FILE), exist_ok=True)
    print(f"  fetch {LS_URL}")
    with urllib.request.urlopen(LS_URL, timeout=300) as r:
        blob = r.read()
    got = hashlib.sha256(blob).hexdigest()
    if got != LS["sha256"]:
        raise SystemExit(f"HARD STOP: Lewis & Short sha256 {got} != pinned {LS['sha256']}")
    with open(LS_FILE + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(LS_FILE + ".tmp", LS_FILE)


CLASS_WORDS = (("prep", "PREP"), ("conj", "CONJ"), ("interj", "INTERJ"), ("pron", "PRON"),
               ("subst", "N"), ("num", "NUM"))


def ls_class(pos, gen):
    """The word class L&S prints, in Whitaker's terms; None where it prints none."""
    if gen:
        return "N"
    if not pos:
        return None
    p = pos.lower()
    if p.startswith("v."):
        return "V"
    if p.startswith("adv"):
        return "ADV"
    if "adj" in p or p == "p. a.":
        return "ADJ"
    for k, c in CLASS_WORDS:
        if p.startswith(k):
            return c
    return None


RE_ITAL = re.compile(r'<hi rend="ital">([^<]*)</hi>')
RE_TAG = re.compile(r"<[^>]+>")


def sense_class(first_sense):
    """Where L&S tags no <pos>, the class it writes in italics at the head of
    the first sense (cum2: "conj."; qui2: "adv. interrog."). A hint only."""
    for t in RE_ITAL.findall(first_sense)[:2]:
        t = t.strip().lower()
        if t.startswith("adv"):
            return "ADV"
        for k, c in CLASS_WORDS:
            if t.startswith(k):
                return c
    return None


def ls_fold(s):
    """Folded as Whitaker folds. Dropped: hyphens (L&S's ăd-ōro), Perseus's
    quantity marks ^ and _ (a^credula), the dagger and the full stop. The
    Cyrillic ў the Perseus text has for y in a few Greek names reads as y."""
    return W.fold(s.replace("ў", "y")).translate(LS_STRIP).strip()


LS_STRIP = str.maketrans("", "", "-^_†.")


def is_affix(o):
    return o.startswith("-") or o.endswith("-")


def read_ls():
    """One row per entry. The headword is the first spelling L&S prints, NOT
    the key: Perseus keys some compounds by their prefix (super10 is
    super-fio). An entry printed as an affix (sum-, "for sub before m") keeps
    its hyphen, so it never takes a whole word. A pointer entry -- nothing but
    a cross-reference ("sum = eum, v. is") -- is marked, and loses to a real
    entry of the same headword (s.3)."""
    with open(LS_FILE, encoding="utf-8") as f:
        s = f.read()
    rows = []
    for m in RE_ENTRY.finditer(s):
        a = dict(RE_ATTR.findall(m.group(1)))
        body = m.group(2)
        head = body[:HEAD_CHARS]
        pos, gen = RE_POS.search(head), RE_GEN.search(head)
        pos = pos.group(1).strip() if pos else None
        gen = gen.group(1).strip() if gen else None
        key = a["key"]
        lead, _, rest = body.partition("<sense")
        orths = [o.strip() for o in RE_ORTH.findall(lead) if o.strip()]
        first = orths[0] if orths else re.sub(r"\d+$", "", key)
        hw = (ls_fold(first.replace("-", "~")).replace("~", "-") if is_affix(first) else ls_fold(first))
        # the other spellings printed before the first sense: rursus, rursum;
        # reverto, revertor. A partial spelling (-vort-) is not a headword.
        alts = []
        for o in orths[1:]:
            f = ls_fold(o)
            if not is_affix(o) and " " not in f and f != hw and f not in alts:
                alts.append(f)
        cls = ls_class(pos, gen)
        hint = None if cls else sense_class(rest[:400])
        plain = RE_TAG.sub("", body)
        pointer = len(plain) < 120 and bool(re.search(r"\bv\. ", plain)) and not gen and not pos
        rows.append({"key": key, "citation": f"lewis-short:{key}", "perseus_id": a["id"],
                     "homograph": int(a["n"]) if a.get("n", "").isdigit() else None,
                     "type": a.get("type"), "headword": hw, "spellings": alts,
                     "class": cls or hint, "class_by": "tag" if cls else "sense" if hint else None,
                     "pointer": pointer})
    keys = [r["key"] for r in rows]
    if len(set(keys)) != len(keys):
        raise SystemExit("HARD STOP: Lewis & Short keys are not unique")
    return rows


# ---------------------------------------------------------------------------
# Whitaker lemma -> L&S key
# ---------------------------------------------------------------------------

# Whitaker's part of speech -> the L&S classes that can print it
WCLASS = {"N": {"N"}, "V": {"V"}, "VPAR": {"V", "ADJ"}, "SUPINE": {"V"}, "ADJ": {"ADJ", "NUM"},
          "NUM": {"NUM", "ADJ", "ADV"}, "ADV": {"ADV"}, "PREP": {"PREP"}, "CONJ": {"CONJ"},
          "INTERJ": {"INTERJ"}, "PRON": {"PRON", "ADJ"}, "PACK": {"PRON", "ADJ"}}
SKIP_TYPES = {"spur"}     # L&S's own "spurious" entries never take a word


def _choose(cands, pos):
    """Narrow same-headword entries: real entries over pointers; then the one
    whose class fits; then, if every other entry prints a class that does
    not fit, the one entry that prints none."""
    real = [r for r in cands if not r["pointer"]] or cands
    if len(real) == 1:
        return "one", [real[0]["key"]]
    want = WCLASS.get(pos, set())
    fit = [r for r in real if r["class"] in want]
    if len(fit) == 1:
        return "class", [fit[0]["key"]]
    if not fit:
        blank = [r for r in real if r["class"] is None]
        if len(blank) == 1:
            return "class", [blank[0]["key"]]
    return "ambiguous", [r["key"] for r in (fit or real)]


def voice_variants(headword, pos):
    """reverto/revertor, dominor/domino: L&S and WORDS do not always agree on
    whether a verb is deponent, so a verb is also looked for in the other voice."""
    if pos != "V":
        return []
    if headword.endswith("or"):
        return [headword[:-1]]
    if headword.endswith("o"):
        return [headword + "r"]
    return []


def link(headword, pos, by_head, by_spelling):
    """(status, [L&S keys]) for one Whitaker lemma. Statuses, s.3 of the README:
    headword -- one L&S entry prints this headword first;
    class    -- several do, and exactly one has this word class;
    spelling -- none does, but one prints it as another spelling before its
                first sense (rursum under rursus);
    voice    -- only the other voice is there (WORDS domino, L&S dominor);
    ambiguous-- several remain; all are listed, none is chosen;
    none     -- L&S has none of these."""
    tries = [(by_head, headword, "headword"), (by_spelling, headword, "spelling")]
    tries += [(ix, v, "voice") for v in voice_variants(headword, pos) for ix in (by_head, by_spelling)]
    for index, hw, tag in tries:
        cands = [r for r in index.get(hw, []) if r["type"] not in SKIP_TYPES]
        if not cands:
            continue
        how, keys = _choose(cands, pos)
        if how == "ambiguous":
            return "ambiguous", keys
        if tag == "headword":
            return ("headword" if how == "one" else "class"), keys
        return tag, keys
    return "none", []


LINKED = ("headword", "class", "spelling", "voice")


def indexes(ls_rows):
    by_head, by_spelling = collections.defaultdict(list), collections.defaultdict(list)
    for r in ls_rows:
        by_head[r["headword"]].append(r)
        for f in r["spellings"]:
            by_spelling[f].append(r)
    return by_head, by_spelling


def whitaker_links(X, ls_rows):
    by_head = indexes(ls_rows)
    out = {}
    for i, e in enumerate(X.entries):
        form, _ = X.form(i)
        if not form:
            continue
        if form in out:
            continue
        st, keys = link(W.headword_of(form), e["part"]["pos"], *by_head)
        out[form] = {"whitaker": form, "headword": W.headword_of(form), "pos": e["part"]["pos"],
                     "status": st, "ls": keys}
    return out, by_head


def describe_key(a, links, by_head):
    """The L&S link for one analysis: lemma rows from DICTLINE are in `links`;
    UNIQUES, the names table and the house supplement are linked by headword."""
    k = a["key"]
    if k in links:
        return links[k]
    if a["form_by"] == "whitaker-roman":
        return {"whitaker": k, "headword": a["headword"], "pos": "NUM", "status": "none", "ls": []}
    st, keys = link(a["headword"], a["parse"]["pos"], *by_head)
    row = {"whitaker": k, "headword": a["headword"], "pos": a["parse"]["pos"], "status": st, "ls": keys}
    links[k] = row
    return row


# ---------------------------------------------------------------------------
# The Vulgate
# ---------------------------------------------------------------------------

WORD = re.compile(r"[^\W\d_]+")


def vulgate_units():
    import fetch_sources as F
    return S.convert_vulgate(os.path.join(S.CORPUS, "vulgate"), F.VULGATE["books"],
                             F.VULGATE["pin"])["units"]


def cased(t):
    import unicodedata
    s = unicodedata.normalize("NFD", t)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.replace("Æ", "Ae").replace("æ", "ae").replace("Œ", "Oe").replace("œ", "oe")


def build_vulgate(X, links, by_head):
    units = vulgate_units()
    seen = {}                                   # cased form -> (whitaker keys, ls sure set, ls all)
    forms = collections.defaultdict(lambda: {"tokens": 0, "whitaker": set(), "ls": set(),
                                             "ambiguous": False})
    sure = collections.defaultdict(list)
    possible = collections.defaultdict(list)
    for u in units:
        vid = u["id"].split(":", 1)[1]
        s_here, p_here = set(), set()
        for t in WORD.findall(u["text"]):
            c = cased(t)
            if c not in seen:
                # never taken: WORDS's two-words guesses (README-lemma-spine s.3),
                # and its abbreviations (Non., A.): the text has none, its
                # words are cut at every stop
                A = [a for a in X.analyze(c)
                     if not any(v["kind"] == "TWO_WORDS" for v in a.get("via") or [])
                     and not a["key"].split("  ")[0].endswith(", abb.")]
                wk = sorted({a["key"] for a in A})
                ls_all, clean = set(), True
                for a in A:
                    row = describe_key(a, links, by_head)
                    ls_all.update(row["ls"])
                    if row["status"] not in LINKED:
                        clean = False
                seen[c] = (wk, ls_all, clean and len(ls_all) == 1)
            wk, ls_all, is_sure = seen[c]
            f = forms[c.lower()]
            f["tokens"] += 1
            f["whitaker"].update(wk)
            f["ls"].update(ls_all)
            if not is_sure:
                f["ambiguous"] = True
            (s_here if is_sure else p_here).update(ls_all)
        for k in s_here:
            sure[k].append(vid)
        for k in p_here - s_here:
            possible[k].append(vid)
    form_rows = []
    for form in sorted(forms):
        f = forms[form]
        st = ("unread" if not f["whitaker"] else "no-ls" if not f["ls"]
              else "sure" if not f["ambiguous"] else "several")
        form_rows.append({"form": form, "tokens": f["tokens"], "status": st,
                          "whitaker": sorted(f["whitaker"]), "ls": sorted(f["ls"])})
    conc = [{"key": k, "sure": sure.get(k, []), "possible": possible.get(k, [])}
            for k in sorted(set(sure) | set(possible))]
    return form_rows, conc, len(units)


# ---------------------------------------------------------------------------
# Build, write, check
# ---------------------------------------------------------------------------

def jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def read_committed(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def build():
    have = os.path.exists(LS_FILE) and W.have_cache() and os.path.isdir(os.path.join(S.CORPUS, "vulgate"))
    if not have:
        prior = {n: read_committed(n) for n in FILES}
        if any(v is None for v in prior.values()):
            raise SystemExit("missing sources and no committed files: run with --fetch, "
                             "build_lemma_spine.py --fetch and fetch_sources.py first")
        print("  sources missing here: committed files carried forward unchanged")
        return prior
    if sha256_file(LS_FILE) != LS["sha256"]:
        raise SystemExit("HARD STOP: Lewis & Short file differs from the pin")
    import proper_names
    ls_rows = read_ls()
    X = W.Whitaker(house_supplement=True)
    X.names = proper_names.load()
    links, by_head = whitaker_links(X, ls_rows)
    form_rows, conc, n_units = build_vulgate(X, links, by_head)
    wl = [links[k] for k in sorted(links, key=lambda k: (W.fold(k), k))]
    tok = collections.Counter()
    for r in form_rows:
        tok[r["status"]] += r["tokens"]
    import fetch_sources as F
    manifest = {
        "schema": "wordhoard/latin-key/v1",
        "key": "Lewis & Short's own entry key (Perseus `key`), cited lewis-short:<key>",
        "sources": {
            "lewis-short": {**LS, "rights": LS_RIGHTS},
            "whitaker": {"commit": W.COMMIT, "license": "free-grant (README-lemma-spine.md s.1)",
                         "house_supplement": True, "proper_names": True},
            "vulgate": {"pin": F.VULGATE["pin"], "license": "public-domain",
                        "verses": n_units, "cited_as": "vulgate:<id>, the Vulgate's own numbering"},
        },
        "counts": {
            "lewis_short_entries": len(ls_rows),
            "whitaker_lemmas": len(wl),
            "whitaker_lemmas_by_status": dict(sorted(collections.Counter(r["status"] for r in wl).items())),
            "vulgate_forms": len(form_rows),
            "vulgate_forms_by_status": dict(sorted(collections.Counter(r["status"] for r in form_rows).items())),
            "vulgate_tokens_by_status": dict(sorted(tok.items())),
            "vulgate_keys": len(conc),
        },
        "not_claimed": [
            "A Whitaker lemma is matched to L&S by headword, then by word class; never by meaning.",
            "`possible` lists every reading WORDS allows; the build does not choose among them.",
            "Words L&S does not have (Church Latin coinages, many names) keep their Whitaker lemma only.",
            "No uid is proposed or minted.",
        ],
        "files": {},
    }
    out = {"lewis-short.jsonl": jsonl(ls_rows), "whitaker-ls.jsonl": jsonl(wl),
           "vulgate-forms.jsonl": jsonl(form_rows), "vulgate-concordance.jsonl": jsonl(conc)}
    for n, text in out.items():
        manifest["files"][n] = {"rows": text.count("\n"),
                                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    out["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return out


FILES = ("lewis-short.jsonl", "whitaker-ls.jsonl", "vulgate-forms.jsonl",
         "vulgate-concordance.jsonl", "manifest.json")


def write(out):
    os.makedirs(OUT, exist_ok=True)
    for n, text in out.items():
        p = os.path.join(OUT, n)
        with open(p + ".tmp", "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(p + ".tmp", p)                # atomic: a killed run never truncates


def main():
    args = sys.argv[1:]
    if "--fetch" in args:
        fetch()
        return
    out = build()
    if "--check" in args:
        bad = [n for n in FILES if read_committed(n) != out[n]]
        for n in FILES:
            print(f"  {'DIFFERS' if n in bad else 'same':8} {n}")
        if bad:
            raise SystemExit(1)
        return
    write(out)
    m = json.loads(out["manifest.json"])
    for k, v in m["counts"].items():
        print(f"  {k:28} {v}")


if __name__ == "__main__":
    main()
