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

WHAT IT WRITES (build/latin-key/, gitignored; only data/lemmas/latin-key/manifest.json is committed)
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

OUT = os.path.join(ROOT, "data", "lemmas", "latin-key")      # committed: manifest.json only
# Every file that carries Lewis & Short's keys is built from Perseus's CC BY-SA
# text, so it is built here, gitignored, until Adam rules; the committed
# manifest records each one's sha256 and the rights block (README s.5).
LOCAL = os.path.join(ROOT, "build", "latin-key")

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
    if pos and pos.lower().startswith("v."):
        return "V"      # comitio, "v. n. and a.": a gender further on is a later sense's
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


RE_ITYPE = re.compile(r"<itype>([^<]*)</itype>")
RE_VERB_BEFORE = re.compile(r"\bv\.\s*(dep\.\s*)?(a\.?\s*)?(and\s*)?$")


def verb_neuter(head, gen, gen_at, pos):
    """Perseus tags L&S's "v. n." (verbum neutrum, an intransitive verb) as a
    <gen>n.</gen>, so miror, vereor and abstineo would read as neuter nouns.
    The n. is a verb's when L&S prints a verb class (<pos>v. dep. a.</pos>), a
    conjugation number in the inflection (miror "ātus, 1"), or "v. a. and"
    just before it."""
    if gen != "n.":
        return False
    if pos and pos.lower().startswith("v."):
        return True
    it = RE_ITYPE.search(head)
    if it and re.search(r"(^|,)\s*[1-4]\s*$", it.group(1)):
        return True
    return bool(RE_VERB_BEFORE.search(RE_TAG.sub("", head[:gen_at])[-40:]))


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
        gen_at = gen.start() if gen else None
        pos = pos.group(1).strip() if pos else None
        gen = gen.group(1).strip() if gen else None
        if gen and verb_neuter(head, gen, gen_at, pos):
            gen = None      # "v. dep. a. and n.": n. is neuter (intransitive), not a gender
            pos = pos or "v."
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
        if cls == "V":
            gen = None
        hint = None if cls else sense_class(rest[:400])
        plain = RE_TAG.sub("", body)
        pointer = len(plain) < 120 and bool(re.search(r"\bv\. ", plain)) and not gen and not pos
        rows.append({"key": key, "citation": f"lewis-short:{key}", "perseus_id": a["id"],
                     "homograph": int(a["n"]) if a.get("n", "").isdigit() else None,
                     "type": a.get("type"), "headword": hw, "spellings": alts,
                     "class": cls or hint, "class_by": "tag" if cls else "sense" if hint else None,
                     "gen": gen, "pointer": pointer})
    keys = [r["key"] for r in rows]
    if len(set(keys)) != len(keys):
        raise SystemExit("HARD STOP: Lewis & Short keys are not unique")
    return rows


# ---------------------------------------------------------------------------
# Whitaker lemma -> L&S key
# ---------------------------------------------------------------------------

# Whitaker's part of speech -> the L&S classes that can print it
# (WORDS files the conjunction cum, "when", as an ADV; L&S prints it conj.)
WCLASS = {"N": {"N"}, "V": {"V"}, "VPAR": {"V", "ADJ"}, "SUPINE": {"V"}, "ADJ": {"ADJ", "NUM"},
          "NUM": {"NUM", "ADJ", "ADV"}, "ADV": {"ADV", "CONJ"}, "PREP": {"PREP"}, "CONJ": {"CONJ"},
          "INTERJ": {"INTERJ"}, "PRON": {"PRON", "ADJ"}, "PACK": {"PRON", "ADJ"}}
# A verb and a noun, or a pronoun and an adverb, are never one entry. When the only entry of that spelling
# is the other class, it is another word (WORDS's vis, "you want", is not
# L&S's vis, "force"; canto, cantonis is not canto, to sing): left unlinked.
CLASHES = ({"V", "N"}, {"PRON", "ADV"})   # eadem the pronoun is not L&S's adverb eadem
SKIP_TYPES = {"spur"}     # L&S's own "spurious" entries never take a word


LS_GEN = {"M": ("m.",), "F": ("f.",), "N": ("n.",), "C": ("comm.", "com.")}


def _choose(cands, pos, gender=None, proper=None):
    """Narrow same-headword entries, each step only if it leaves one or more:
    real entries over pointers; the class that fits (or, if none fits, the
    one entry printing no class); a proper name to a capitalised key and a
    common word to a lower-case one (rex1, not Rex2); a noun's gender (populus
    the people is m., populus the poplar f.). Returns (how, keys): how is the
    step that left one entry, "one" if no step was needed."""
    pool = [r for r in cands if not r["pointer"]] or cands
    if len(pool) == 1:
        if {pos, pool[0]["class"]} in CLASHES:
            return "clash", []
        return "one", [pool[0]["key"]]
    want = WCLASS.get(pos, set())
    fit = [r for r in pool if r["class"] in want]
    if not fit:
        blank = [r for r in pool if r["class"] is None]
        fit = blank if len(blank) == 1 else []
    steps = [("class", fit)]
    if proper is not None:
        steps.append(("case", lambda P: [r for r in P if r["key"][:1].isupper() == proper]))
    if gender in LS_GEN and pos == "N":
        steps.append(("gender", lambda P: [r for r in P if r["gen"] in LS_GEN[gender]]))
    for how, step in steps:
        nxt = step if isinstance(step, list) else step(pool)
        if nxt:
            pool = nxt
        if len(pool) == 1:
            return how, [pool[0]["key"]]
    return "ambiguous", [r["key"] for r in pool]


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


def link(headword, pos, by_head, by_spelling, gender=None, proper=None):
    """(status, [L&S keys]) for one Whitaker lemma. Statuses, s.3 of the README:
    headword -- one L&S entry prints this headword first;
    class    -- several do, and exactly one has this word class;
    case     -- ... and exactly one is capitalised as the lemma is (rex1, Rex2);
    gender   -- ... and exactly one noun has the lemma's gender (populus1, 2);
    spelling -- none does, but one prints it as another spelling before its
                first sense (rursum under rursus);
    voice    -- only the other voice is there (WORDS domino, L&S dominor);
    ambiguous-- several remain; all are listed, none is chosen;
    clash    -- the only entry is a noun for a verb or a verb for a noun
                (WORDS's vis "you want", L&S's vis "force"): another word;
    none     -- L&S has none of these."""
    tries = [(by_head, headword, "headword"), (by_spelling, headword, "spelling")]
    tries += [(ix, v, "voice") for v in voice_variants(headword, pos) for ix in (by_head, by_spelling)]
    clash = False
    for index, hw, tag in tries:
        cands = [r for r in index.get(hw, []) if r["type"] not in SKIP_TYPES]
        if not cands:
            continue
        how, keys = _choose(cands, pos, gender, proper)
        if how == "clash":
            clash = True
            continue
        if how == "ambiguous":
            return "ambiguous", keys
        if tag == "headword":
            return ("headword" if how == "one" else how), keys
        return tag, keys
    return ("clash" if clash else "none"), []


LINKED = ("headword", "class", "case", "gender", "spelling", "voice")


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
        st, keys = link(W.headword_of(form), e["part"]["pos"], *by_head,
                        gender=e["part"].get("gender"), proper=form[:1].isupper())
        out[form] = {"whitaker": form, "headword": W.headword_of(form), "pos": e["part"]["pos"],
                     "status": st, "ls": keys}
    return out, by_head


NUM_LINKS = {}
NUM_PART = {"ORD": (1, "ADJ"), "DIST": (2, "ADJ"), "ADVERB": (3, "ADV")}


def num_link(k, sort, links, by_head):
    """WORDS keeps a number's four words in one entry: "septem, septimus -a
    -um, septeni -ae -a, septie (n)s". L&S gives the ordinal, distributive and
    adverb their own entries, so each is linked by its own word: septimo is
    septimus, tertio tertius, never septem or tres."""
    if (k, sort) in NUM_LINKS:
        return NUM_LINKS[(k, sort)]
    idx, pos = NUM_PART[sort]
    parts = k.split("  ")[0].split(", ")
    word = re.sub(r"\s*\((n)\)\s*", r"\1", parts[idx]).split()[0] if idx < len(parts) else "-"
    hw = W.fold(word)
    st, keys = link(hw, pos, *by_head) if hw != "-" else ("none", [])
    row = {"whitaker": f"{k} ({sort})", "headword": hw, "pos": pos, "status": st, "ls": keys}
    NUM_LINKS[(k, sort)] = row
    return row


def describe_key(a, links, by_head):
    """The L&S link for one analysis: lemma rows from DICTLINE are in `links`;
    UNIQUES, the names table and the house supplement are linked by headword."""
    k = a["key"]
    sort = a["parse"].get("sort")
    if a["parse"]["pos"] == "NUM" and sort in NUM_PART and ", " in k:
        return num_link(k, sort, links, by_head)
    if k in links:
        return links[k]
    if a["form_by"] == "whitaker-roman":
        return {"whitaker": k, "headword": a["headword"], "pos": "NUM", "status": "none", "ls": []}
    proper = a["form_by"] == "house-names" or k[:1].isupper()
    st, keys = link(a["headword"], a["parse"]["pos"], *by_head,
                    gender=a["parse"].get("gender"), proper=proper)
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


# ---------------------------------------------------------------------------
# One word in its verse: the context rules (README-latin-key s.4b)
# ---------------------------------------------------------------------------

FREQ_RANK = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "I": 6, "M": 6, "N": 6}
COMMON_INFLECTION = {"A", "B"}
CASED_POS = {"N", "ADJ", "PRON", "VPAR", "NUM", "SUPINE"}
PUNCT = re.compile(r"[,.;:?!]")
INDEF_AFTER = {"si", "ne", "num"}       # after these, quis is indefinite (not nisi: nisi qui is relative)
RULES = ("idem-dem", "proper-lower", "possessive-agrees", "whole-word", "rare-inflection", "rare-entry",
         "prep-object", "no-prep-object", "si-quis")
# particles the Vulgate puts second in a clause (itaque and igitur by its own habit)
POSTPOSITIVE = {"vero", "autem", "enim", "itaque", "igitur", "ergo", "quoque", "quidem"}
PRIORS = {"rare-entry", "rare-inflection", "whole-word"}   # WORDS's grades and conventions, not grammar
FAMILY = {"VPAR": "V", "SUPINE": "V"}      # a participle or supine is its verb's
# Forms where WORDS grades the word whose lemma IS the form two or more grades
# below a commoner word that also reads it, and the Vulgate means the rarer
# one: rare-entry stands aside and they stay null. Each was read in its
# verses (capitium is not caput, praecipito is not praecipio, genus is not
# genu, merces is not merx, sacerdotium is the priesthood, not sacerdos,
# mentum is the chin, not mens). A list, not a rule: as a rule ("never against
# the form's own lemma") it un-resolved 1,412 tokens, mostly rightly resolved
# (populus, omne, medium, pedum, pane), reviewer round 4, 2026-10-03.
OWN_LEMMA_STANDS = frozenset({"capitium", "praecipito", "genus", "merces", "sacerdotium", "mentum"})
POSSESSIVES = {"meus", "tuus", "suus", "noster", "vester"}
NOMINAL = {"N", "ADJ", "PRON", "NUM"}


def _agree(a, b):
    """Case, number and gender agree (X any; C, common, is m or f)."""
    def eq(x, y):
        return x == y or "X" in (x, y) or None in (x, y)

    def geq(x, y):
        return eq(x, y) or (x == "C" and y in "MF") or (y == "C" and x in "MF")
    return eq(a["case"], b["case"]) and eq(a["number"], b["number"]) and geq(a["gender"], b["gender"])


def flag_tables(X):
    """DICTLINE line -> entry flags, INFLECTS line -> (age, freq): WORDS's own
    frequency marks, which this port reads but never used to drop anything."""
    entry = {}
    for e in X.entries:
        for n in e.get("lines") or []:
            entry[f"DICTLINE.GEN:{n}"] = e["flags"]
        if e.get("synthetic"):
            entry[e["synthetic"]] = e["flags"]
    infl = {}
    with open(os.path.join(X.cache, "INFLECTS.LAT"), encoding="latin-1") as f:
        for n, raw in enumerate(f, 1):
            t = raw.split("--", 1)[0].split()
            if len(t) >= 3:
                infl[f"INFLECTS.LAT:{n}"] = (t[-2], t[-1])
    return entry, infl


def readings(X, c, links, by_head, flags):
    """Every WORDS reading of one form as written, with its L&S target.
    Never taken: WORDS's two-words guesses (README-lemma-spine s.3), and its
    abbreviations (Non., A.): the text has none, its words are cut at every stop."""
    entry_flags, infl_flags = flags
    out = []
    for a in X.analyze(c):
        if any(v["kind"] == "TWO_WORDS" for v in a.get("via") or []):
            continue
        if a["key"].split("  ")[0].endswith(", abb."):
            continue
        row = describe_key(a, links, by_head)
        ef = entry_flags.get(a["source"])
        age, ifreq = infl_flags.get(a.get("inflect") or "", (None, None))
        target = tuple(row["ls"]) if row["ls"] else ("~" + a["key"],)
        out.append({"target": target, "linked": row["status"] in LINKED, "wkey": a["key"],
                    "pos": a["parse"]["pos"], "case": a["parse"].get("case"),
                    "number": a["parse"].get("number"), "gender": a["parse"].get("gender"),
                    "efreq": FREQ_RANK.get(ef["freq"]) if ef else None,
                    "ifreq": ifreq, "iage": age, "enclitic": a.get("enclitic"),
                    "own": W.fold(a["headword"]) == W.fold(c),
                    "proper": a["form_by"] == "house-names" or a["key"][:1].isupper()})
    return out


def _keep(groups, keep, rule, used):
    """Drop the groups `keep` rejects, only if at least one is left."""
    nxt = {t: R for t, R in groups.items() if keep(t, R)}
    if nxt and len(nxt) < len(groups):
        used.append(rule)
        return nxt
    return groups


def resolve(tok, nxt_tok, prev_form, prev_tok=None, nxt2_tok=None):
    """(L&S key or None, [rule ids]) for one token. `tok`/`nxt_tok`:
    {"form", "cased", "R": readings, "punct_after"}. A rule only removes
    readings; it never adds one, and it never removes them all."""
    groups = collections.OrderedDict()
    for r in tok["R"]:
        groups.setdefault(r["target"], []).append(r)
    used = []

    def done():
        if len(groups) == 1:
            (t, R), = groups.items()
            if len(t) == 1 and not t[0].startswith("~") and all(r["linked"] for r in R):
                return t[0]
        return None

    if done():
        return done(), []
    form = tok["form"]
    # idem: WORDS's own entry says "w/-dem ONLY"
    groups = _keep(groups, lambda t, R: not all(r["wkey"].startswith("idem,") for r in R)
                   or "dem" in form, "idem-dem", used)
    # a word written lower-case is not a name: drop readings that are names in
    # L&S (a capitalised key: Pan for panes, Leo3 for leo), or, where L&S has
    # no entry, in WORDS (the names table)
    if tok["cased"][:1].islower():
        def common(t, R):
            if t[0].startswith("~"):
                return not all(r["proper"] for r in R)
            return not all(k[:1].isupper() for k in t)
        groups = _keep(groups, common, "proper-lower", used)
    # a possessive beside it that can only be a possessive (meus, tuum) needs a
    # noun or adjective to agree with: salutare tuum is "thy salvation", not
    # the verb's infinitive. Only readings that agree with it are kept.
    for nb in (prev_tok, nxt_tok):
        if not nb or not nb["R"] or not all(r["target"] in {(p,) for p in POSSESSIVES} for r in nb["R"]):
            continue
        groups = _keep(groups, lambda t, R: any(r["pos"] in NOMINAL and any(_agree(r, q) for q in nb["R"])
                                                for r in R), "possessive-agrees", used)
    # a word printed whole in the dictionary is not split off an enclitic:
    # absque is the preposition "without", not abs + -que
    if any(not r["enclitic"] for R in groups.values() for r in R):
        groups = _keep(groups, lambda t, R: any(not r["enclitic"] for r in R), "whole-word", used)
    # an ending WORDS marks less than common (dominum as domina's genitive plural)
    groups = _keep(groups, lambda t, R: any(r["ifreq"] in COMMON_INFLECTION or r["ifreq"] is None
                                            for r in R), "rare-inflection", used)
    # an entry two or more of WORDS's frequency grades below the commonest reading
    ranks = [min((r["efreq"] for r in R if r["efreq"] is not None), default=None)
             for R in groups.values()]
    known = [x for x in ranks if x is not None]
    if known and min(known) <= 1:
        best = min(known)
        # only between readings of one word class (est: edo or sum, both
        # verbs). A noun never loses to a verb of its own stem by frequency:
        # peccata is peccatum, not pecco's participle; tribus is the tribe as
        # often as the number three.
        best_cls = {FAMILY.get(r["pos"], r["pos"]) for R, x in zip(groups.values(), ranks) if x == best
                    for r in R}
        # and never against the form's own lemma where that was measured
        # (OWN_LEMMA_STANDS)
        own_stands = W.fold(form) in OWN_LEMMA_STANDS
        groups = _keep(groups, lambda t, R: min((r["efreq"] for r in R if r["efreq"] is not None),
                                                 default=best) < best + 2
                       or (own_stands and any(r.get("own") for r in R))
                       or not ({FAMILY.get(r["pos"], r["pos"]) for r in R} <= best_cls), "rare-entry", used)
    # a preposition takes an object in its case, next in the clause
    preps = {t: {r["case"] for r in R if r["pos"] == "PREP"} for t, R in groups.items()}
    if any(preps.values()) and len(groups) > 1:
        nxt_cases = set()
        if nxt_tok and not tok["punct_after"]:
            # a name from the names table carries no case: it could be any
            nxt_cases = {r["case"] or "X" for r in nxt_tok["R"] if r["pos"] in CASED_POS}
        governs = any(c in nxt_cases or "X" in nxt_cases for P in preps.values() for c in P)
        # Quod cum David rescisset: a name with no case, then a verb, may be the
        # subject of a cum-clause, not the object of cum "with": left null
        name_then_verb = ("X" in nxt_cases and nxt_tok["cased"][:1].isupper() and nxt2_tok and nxt2_tok["R"]
                          and not nxt_tok["punct_after"]
                          and all(r["pos"] == "V" for r in nxt2_tok["R"]))
        # cum vero, cum itaque: a postpositive particle stands second in its
        # clause and never between a preposition and its object, so the word
        # before it opened the clause on its own: not a preposition
        if nxt_tok and not tok["punct_after"] and nxt_tok["form"] in POSTPOSITIVE:
            groups = _keep(groups, lambda t, R: not preps[t], "no-prep-object", used)
        elif governs and name_then_verb:
            pass
        elif governs:
            groups = _keep(groups, lambda t, R: bool(preps[t] & (nxt_cases | {"X"})) or
                           ("X" in nxt_cases and preps[t]), "prep-object", used)
        elif tok["punct_after"] or (nxt_tok and nxt_tok["R"] and nxt_tok["cased"][:1].islower()
                                    and not any(r["pos"] == "ADV" for r in nxt_tok["R"])):
            # only when the clause ends (a, a, a), or the next word is read,
            # written lower-case, has no case and is no adverb (cum autem): a
            # capitalised word may be a name WORDS misreads (a Sidone, read as
            # sido), and a preposition can take an adverb (a longe, from afar)
            groups = _keep(groups, lambda t, R: not preps[t], "no-prep-object", used)
    # si quis: after si, ne, num, quis is the indefinite (L&S quis2)
    # (the WORDS lemma "quis, quid" links to both quis1 and quis2; this rule
    # is what picks between them)
    if prev_form in INDEF_AFTER and any("quis2" in t for t in groups):
        groups = _keep(groups, lambda t, R: "quis2" in t, "si-quis", used)
        if "si-quis" in used and len(groups) == 1:
            (t, R), = groups.items()
            groups = {("quis2",): [dict(r, linked=True) for r in R]}
    return done(), used


def build_vulgate(X, links, by_head, units):
    flags = flag_tables(X)
    seen = {}
    forms = collections.defaultdict(lambda: {"tokens": 0, "whitaker": set(), "ls": set(),
                                             "ambiguous": False, "resolved": collections.Counter(),
                                             "unresolved": 0})
    sure = collections.defaultdict(list)
    by_rule = collections.defaultdict(lambda: collections.defaultdict(list))
    possible = collections.defaultdict(list)
    token_rows = []
    rule_tokens = collections.Counter()
    for u in units:
        vid = u["id"].split(":", 1)[1]
        text = u["text"]
        toks, prev_end = [], 0
        ms = list(WORD.finditer(text))
        for i, m in enumerate(ms):
            c = cased(m.group(0))
            if c not in seen:
                seen[c] = readings(X, c, links, by_head, flags)
            after = text[m.end():ms[i + 1].start()] if i + 1 < len(ms) else ""
            toks.append({"form": c.lower(), "cased": c, "R": seen[c],
                         "punct_after": bool(PUNCT.search(after))})
        s_here, r_here, p_here = set(), {}, set()
        row = []
        for i, t in enumerate(toks):
            f = forms[t["form"]]
            f["tokens"] += 1
            f["whitaker"].update(r["wkey"] for r in t["R"])
            targets = {k for r in t["R"] for k in r["target"] if not k.startswith("~")}
            f["ls"].update(targets)
            key, used = resolve(t, toks[i + 1] if i + 1 < len(toks) else None,
                                toks[i - 1]["form"] if i else None, toks[i - 1] if i else None,
                                toks[i + 2] if i + 2 < len(toks) else None)
            if key and not used:
                s_here.add(key)
            elif key:
                f["ambiguous"] = True
                f["resolved"]["+".join(used)] += 1
                rule_tokens["+".join(used)] += 1
                r_here.setdefault(key, set()).add("+".join(used))
            else:
                if targets:
                    f["ambiguous"] = True
                    f["unresolved"] += 1
                p_here.update(targets)
            row.append([t["form"], key, "+".join(used) if key and used else None])
        token_rows.append({"verse": vid, "tokens": row})
        for k in s_here:
            sure[k].append(vid)
        for k, rules in r_here.items():
            if k in s_here:
                continue
            for rule in sorted(rules):
                by_rule[k][rule].append(vid)
        for k in p_here - s_here - set(r_here):
            possible[k].append(vid)
    form_rows = []
    for form in sorted(forms):
        f = forms[form]
        st = ("unread" if not f["whitaker"] else "no-ls" if not f["ls"]
              else "sure" if not f["ambiguous"] else "several")
        r = {"form": form, "tokens": f["tokens"], "status": st,
             "whitaker": sorted(f["whitaker"]), "ls": sorted(f["ls"])}
        if st == "several":
            r["resolved"] = dict(sorted(f["resolved"].items()))
            r["unresolved"] = f["unresolved"]
        form_rows.append(r)
    keys = sorted(set(sure) | set(by_rule) | set(possible))
    conc = [{"key": k, "sure": sure.get(k, []),
             "resolved": {rule: v for rule, v in sorted(by_rule[k].items())} if k in by_rule else {},
             "possible": possible.get(k, [])} for k in keys]
    return form_rows, conc, len(units), token_rows, rule_tokens


# ---------------------------------------------------------------------------
# Strong's number -> the Vulgate's Latin for it (README-latin-key s.4c)
# ---------------------------------------------------------------------------

KJV_TAGS = os.path.join(ROOT, "build", "strongs", "kjv-tags.jsonl")   # local too (README-strongs s.6)
EQ_MIN_VERSES = 3          # a pair seen in fewer verses is not evidence
EQ_MIN_DICE = 0.10
EQ_OF_TOP = 0.40           # a second word must score at least 40% of the first
EQ_MAX = 5
EQ_MUTUAL = 3              # ... and the number must be among the word's own top 3
EQ_THIN = 10               # a number in fewer KJV verses: marked "thin" (H4 "fruit", 3 verses,
                           # pairs with ramus and subter: one passage's other words)


def strongs_latin(units, token_rows):
    """Which L&S entries stand in the Vulgate where each Strong's number
    stands in the KJV, by verse co-occurrence. A Vulgate verse is paired with
    the KJV verse(s) its map names (convert_vulgate's `kjv`); a KJV verse
    brings its Strong's tags (build/strongs/kjv-tags.jsonl), a Vulgate verse
    the L&S keys of its sure and resolved words. Score: Dice, 2c / (n_s + n_l).
    Kept: the pairs strong on both sides (EQ_* above). Statistical: a pair is
    evidence that two words translate each other, never a reading of a verse."""
    tags = {}
    with open(KJV_TAGS, encoding="utf-8") as f:
        for l in f:
            r = json.loads(l)
            tags[r["citation"]] = {t[1] for t in r["tags"]}
    latin = {"vulgate:" + v["verse"]: {k for _, k, _ in v["tokens"] if k} for v in token_rows}
    pairs = collections.defaultdict(lambda: (set(), set()))
    for u in units:
        t = u.get("kjv") or {}
        if not t.get("resolved"):
            continue
        ks = sorted({t["target"]} | {x for x in t.get("spans", []) if x.startswith("kjv:")})
        S, L = pairs[tuple(ks)]
        L |= latin.get(u["id"], set())
        for k in ks:
            S |= tags.get(k, set())
    ns, nl, c = collections.Counter(), collections.Counter(), collections.Counter()
    for S, L in pairs.values():
        ns.update(S)
        nl.update(L)
        for s_ in S:
            for l_ in L:
                c[(s_, l_)] += 1
    dice = {sl: 2 * n / (ns[sl[0]] + nl[sl[1]]) for sl, n in c.items() if n >= EQ_MIN_VERSES}
    by_l = collections.defaultdict(list)
    for (s_, l_), d in dice.items():
        by_l[(l_, s_[0])].append((-d, s_))
    mutual = set()
    for (l_, _), v in by_l.items():
        for _, s_ in sorted(v)[:EQ_MUTUAL]:
            mutual.add((s_, l_))
    by_s = collections.defaultdict(list)
    for (s_, l_), d in dice.items():
        by_s[s_].append((-d, l_))
    rows = []
    import build_strongs
    for s_ in sorted(by_s, key=build_strongs.sort_key):
        cand = sorted(by_s[s_])
        top = -cand[0][0]
        keep = [{"ls": l_, "verses": c[(s_, l_)], "dice": round(-d, 3)} for d, l_ in cand[:EQ_MAX]
                if -d >= EQ_MIN_DICE and -d >= EQ_OF_TOP * top and (s_, l_) in mutual]
        if keep:
            rows.append({"strongs": s_, "verses": ns[s_],
                         "evidence": "thin" if ns[s_] < EQ_THIN else "ok", "latin": keep})
    stats = {"verse_pairs": len(pairs), "numbers_seen": len(ns), "numbers_with_latin": len(rows),
             "numbers_with_latin_thin": sum(r["evidence"] == "thin" for r in rows),
             "rule": {"min_verses": EQ_MIN_VERSES, "min_dice": EQ_MIN_DICE, "of_top": EQ_OF_TOP,
                      "max": EQ_MAX, "mutual_top": EQ_MUTUAL, "thin_below": EQ_THIN}}
    return rows, stats


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
    prior = read_committed("manifest.json")
    if not have:
        if prior is None:
            raise SystemExit("missing sources and no committed manifest: run with --fetch, "
                             "build_lemma_spine.py --fetch and fetch_sources.py first")
        print("  sources missing here: the committed manifest is carried forward unchanged")
        return {"manifest.json": prior}, {}
    if sha256_file(LS_FILE) != LS["sha256"]:
        raise SystemExit("HARD STOP: Lewis & Short file differs from the pin")
    import proper_names
    ls_rows = read_ls()
    X = W.Whitaker(house_supplement=True)
    X.names = proper_names.load()
    links, by_head = whitaker_links(X, ls_rows)
    units = vulgate_units()
    form_rows, conc, n_units, token_rows, rule_tokens = build_vulgate(X, links, by_head, units)
    if os.path.exists(KJV_TAGS):
        eq_rows, eq_stats = strongs_latin(units, token_rows)
    else:                       # the KJV tags are local to build_strongs: keep what was recorded
        eq_rows, eq_stats = None, (json.loads(prior)["counts"].get("strongs_latin") if prior else None)
        print("  build/strongs/kjv-tags.jsonl not here: strongs-latin carried forward")
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
            "vulgate_tokens_by_outcome": token_outcomes(token_rows, form_rows),
            "vulgate_tokens_resolved_by_rule": dict(sorted(rule_tokens.items(), key=lambda kv: -kv[1])),
            # a frequency prior is not a reading of the verse: kept apart
            "vulgate_tokens_resolved_by_kind": {
                "a grammar rule took part": sum(n for k, n in rule_tokens.items()
                                                if set(k.split("+")) - PRIORS),
                "priors only (rare-entry, rare-inflection, whole-word)": sum(
                    n for k, n in rule_tokens.items() if set(k.split("+")) <= PRIORS)},
            "vulgate_keys": len(conc),
            "strongs_latin": eq_stats,
        },
        "not_claimed": [
            "A Whitaker lemma is matched to L&S by headword, then by word class; never by meaning.",
            "A context rule (README s.4b) only removes readings; what no rule settles stays null, "
            "and its verse is listed under `possible` for every reading WORDS allows.",
            "A resolved token is tagged with the rule ids that settled it; no rule reads meaning.",
            "Words L&S does not have (Church Latin coinages, many names) keep their Whitaker lemma only.",
            "No uid is proposed or minted.",
        ],
        "files": {},
    }
    local = {"lewis-short.jsonl": jsonl(ls_rows), "whitaker-ls.jsonl": jsonl(wl),
             "vulgate-forms.jsonl": jsonl(form_rows), "vulgate-concordance.jsonl": jsonl(conc)}
    if eq_rows is not None:
        local["strongs-latin.jsonl"] = jsonl(eq_rows)
    for n, text in local.items():
        manifest["files"][n] = {"rows": text.count("\n"),
                                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    if eq_rows is None and prior and "strongs-latin.jsonl" in json.loads(prior)["files"]:
        manifest["files"]["strongs-latin.jsonl"] = json.loads(prior)["files"]["strongs-latin.jsonl"]
    manifest["files_dir"] = "build/latin-key/ (gitignored: built from Perseus's CC BY-SA text)"
    local["vulgate-tokens.jsonl"] = jsonl(token_rows)
    return {"manifest.json": json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"}, local


def token_outcomes(token_rows, form_rows):
    st = {r["form"]: r["status"] for r in form_rows}
    c = collections.Counter()
    for v in token_rows:
        for form, key, rule in v["tokens"]:
            c["sure" if key and not rule else "resolved" if key else
              st[form] if st[form] in ("no-ls", "unread") else "unresolved"] += 1
    return dict(sorted(c.items()))


LOCAL_FILES = ("lewis-short.jsonl", "whitaker-ls.jsonl", "vulgate-forms.jsonl",
               "vulgate-concordance.jsonl", "strongs-latin.jsonl")


def write(out, where=OUT):
    os.makedirs(where, exist_ok=True)
    for n, text in out.items():
        p = os.path.join(where, n)
        with open(p + ".tmp", "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(p + ".tmp", p)                # atomic: a killed run never truncates


def main():
    args = sys.argv[1:]
    if "--fetch" in args:
        fetch()
        return
    committed, local = build()
    if "--check" in args:
        bad = [n for n, t in committed.items() if read_committed(n) != t]
        m = json.loads(committed["manifest.json"])
        for n in committed:
            print(f"  {'DIFFERS' if n in bad else 'same':8} {n}")
        for n in LOCAL_FILES:
            if n in local:
                same = hashlib.sha256(local[n].encode("utf-8")).hexdigest() == m["files"][n]["sha256"]
                bad += [] if same else [n]
                print(f"  {'same' if same else 'DIFFERS':8} build/latin-key/{n} (sha256 in the manifest)")
            else:
                print(f"  {'skip':8} build/latin-key/{n} (not built here)")
        if bad:
            raise SystemExit(1)
        return
    write(committed)
    write(local, LOCAL)
    m = json.loads(committed["manifest.json"])
    for k, v in m["counts"].items():
        print(f"  {k:28} {v}")


if __name__ == "__main__":
    main()
