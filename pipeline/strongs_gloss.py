#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
strongs_gloss.py -- a DICTIONARY gloss for a Greek token, from Strong's 1890
entry for its Strong's number, by a fixed rule. Never a contextual
translation, and never invented: where no rule fires, the gloss is null and
the build counts it.

    entries = load_entries(xml_text)            # {n: Entry}
    gloss, prov = gloss_for(parsing, entries.get(n))

Pure functions: no files, no network (the build reads the pinned XML and
passes its text in). Rules and worked cases: pipeline/README-nt-jsonl.md s.12.

WHAT A STRONG'S ENTRY GIVES
    A short definition (split in the XML, by Petersen's conversion, between
    <strongs_derivation> and <strongs_def> at the first semicolon, so the two
    are read here as the one paragraph Strong printed), and the KJV
    renderings after ":--". The renderings are in ALPHABETICAL order
    (Strong's layout), not by frequency, so "the first rendering" means
    nothing on its own: lambano's first is "accept", logos's "account". The
    rule therefore lets Strong's own definition choose among the renderings.

THE RULE, in order; the first that fires sets the gloss (its id goes on the token)
    kjv-form    Articles and personal, demonstrative and relative pronouns
                (Robinson T, P, D, R): the first KJV rendering, in Strong's
                order, that is an English form agreeing with the token's
                person, number, gender and case (FORMS). None agrees: null.
                No definition fallback: Strong's defines these by their
                grammar ("the reflexive pronoun self"), not by a sense.
    kjv-sole    The entry has exactly one usable KJV rendering.
    kjv-in-def  The usable KJV rendering that occurs earliest, as a whole
                word, in Strong's definition (clauses about derivation or
                grammar set aside; outside parentheses first, then inside).
                Strong's puts the primary sense first, so this is the primary
                sense in a word the AV actually used. A pronoun form never
                glosses a non-pronoun; a one- or two-letter rendering ("of",
                "to") counts only as the first word of a clause.
    def-head    Nouns, adjectives and verbs only: the head of Strong's first
                sense clause (parentheses off, cut at the first comma, "i.e."
                or " or "; a leading "properly," etc., "a"/"an", and for a
                verb "to"/"I" dropped). More than four words: not taken.
    (none)      null, with the reason.

    Usable rendering: Strong's marks renderings that are not the word's own
    sense ("X" an idiom of the Greek, "+" a rendering needing other words);
    those are skipped. Parenthesised parts ("(at the) first") are Strong's
    optional additions; the base without them is the rendering. The one
    part-of-speech adjustment: a noun takes the noun variant Strong's prints
    ("dark(-ness)" -> "darkness").

OVERRIDES (the later contextual layer)
    data/nt/gloss-overrides.jsonl, one row per token address, `layer`
    "adam-reviewed" or "house". It replaces the dictionary gloss the way
    lemma_spine.apply_override replaces a lemma: the dictionary value and its
    rule are kept under provenance `was`.

    A DRAFT row (`draft: true`, layer "house" only) is the house's proposal
    awaiting Adam's review: it carries `drafted_on` instead of `reviewed_on`,
    and its provenance says `draft: true`, so every consumer can mark it.
    Adam accepts a row by dropping `draft`/`drafted_on` and dating it
    `reviewed_on` (layer "adam-reviewed" if it is now his).
"""

import json
import os
import re

SOURCE = "strongs-1890"
OVERRIDES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "nt", "gloss-overrides.jsonl")
OVERRIDE_LAYERS = ("adam-reviewed", "house")
RULES = {
    "kjv-form": ("article or pronoun: the first KJV rendering, in Strong's order, that is an "
                 "English form agreeing in person, number, gender and case"),
    "kjv-sole": "the entry has exactly one usable KJV rendering",
    "kjv-in-def": ("the usable KJV rendering that occurs earliest, as a whole word, in Strong's "
                   "definition (derivation and grammar clauses set aside; outside parentheses "
                   "first)"),
    "def-head": ("noun, adjective or verb: the head of Strong's first sense clause (parentheses "
                 "off, cut at the first comma, 'i.e.' or ' or '; at most four words)"),
}
RULE_ORDER = ("kjv-form", "kjv-sole", "kjv-in-def", "def-head")

# ---------------------------------------------------------------------------
# Reading an entry
# ---------------------------------------------------------------------------


class Entry:
    __slots__ = ("n", "definition", "kjv")

    def __init__(self, n, definition, kjv):
        self.n, self.definition, self.kjv = n, definition, kjv


def _text(xml):
    """Inline XML -> plain text: a Strong's reference becomes G<n>, a Greek
    word its Unicode, a pronunciation nothing."""
    s = re.sub(r'<strongsref[^>]*strongs="0*(\d+)"[^>]*/>', r"G\1", xml)
    s = re.sub(r'<greek[^>]*unicode="([^"]*)"[^>]*/>', r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def load_entries(xml):
    out = {}
    for n, body in re.findall(r'<entry strongs="0*(\d+)">(.*?)</entry>', xml, re.S):
        d = re.search(r"<strongs_derivation>(.*?)</strongs_derivation>", body, re.S)
        f = re.search(r"<strongs_def>(.*?)</strongs_def>", body, re.S)
        k = re.search(r"<kjv_def>(.*?)</kjv_def>", body, re.S)
        # Petersen split Strong's one paragraph at its first semicolon; put it back.
        parts = [_text(x.group(1)) for x in (d, f) if x]
        definition = "; ".join(p for p in parts if p)
        out[int(n)] = Entry(int(n), definition, _text(k.group(1)) if k else "")
    return out


def _unparen(s):
    """Drop every parenthesised part, nested or not; stray brackets go too."""
    prev = None
    while prev != s:
        prev, s = s, re.sub(r"\([^()]*\)", " ", s)
    return re.sub(r"\s+", " ", s.replace("(", " ").replace(")", " ")).strip()


def _split_top(text, sep):
    """Split at `sep` outside parentheses (Strong's parentheses often hold
    commas and semicolons of their own). An unbalanced ')' is ignored."""
    out, depth, cur = [], 0, ""
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def kjv_renderings(entry):
    """[(base, marker, variants)] in Strong's order. marker is 'X', '+' or ''.
    The base is the rendering without its parenthesised optional parts;
    `variants` are the base with each attached suffix ("dark(-ness)" ->
    ["darkness"]), which fit() may prefer."""
    s = (entry.kjv if entry else "").strip()
    if not s.startswith(":--"):
        return []
    s = s[3:].strip().rstrip(".").replace("((", "(")    # "((him-, my-" is a typo in the XML
    out = []
    for it in _split_top(s, ","):
        it = it.strip()
        marker = it[0] if it[:1] in ("X", "+") and (len(it) == 1 or it[1] == " ") else ""
        body = it[1:].strip() if marker else it
        base = re.sub(r"\s+", " ", _unparen(body).replace("…", " ")).strip(" -")
        if " -" in base or "- " in base:
            continue
        if not re.fullmatch(r"[A-Za-z](?:[A-Za-z' -]*[A-Za-z])?", base):
            continue
        variants = []
        m = re.fullmatch(r"([A-Za-z]+)\(([^()]*)\)", body.replace(" ", ""))
        if m:
            variants = [m.group(1) + v.strip("-") for v in m.group(2).split(",")
                        if v.startswith("-") and v.strip("-").isalpha()]
        out.append((base, marker, variants))
    return out


def usable(entry):
    """The renderings that are the word's own sense: [(base, variants)]."""
    seen, out = set(), []
    for base, marker, variants in kjv_renderings(entry):
        if not marker and base.lower() not in seen:
            seen.add(base.lower())
            out.append((base, variants))
    return out


NOUN_SUFFIXES = ("ness", "ment", "tion", "ity", "ship", "hood", "dom")


def fit(rendering, code):
    """The form of a rendering that fits the token's part of speech. One case
    only: a noun takes the noun variant Strong's prints ("dark(-ness)" glosses
    a noun as "darkness"). Everything else is the base as printed."""
    base, variants = rendering
    if (code or "").startswith("N-"):
        for v in variants:
            if v.lower().endswith(NOUN_SUFFIXES):
                return v
    return base


# A clause of Strong's paragraph that says where the word comes from, not
# what it means ...
_DERIV = re.compile(
    r"^(?:from|of (?:uncertain|foreign|Hebrew|Chaldee|Latin|Aramaic)|a primary|primary|probably|"
    r"perhaps|apparently|compare|see|(?:a |an )?(?:prolonged|strengthened|reduplicated|contracted|"
    r"collateral|obsolete|derivative|root|form)\b|akin|middle voice|(?:the )?(?:same as|base of)|"
    r"neuter|feminine|masculine|used (?:only )?(?:in|as)|including)", re.I)
# ... or that describes its grammar, not its sense.
_META = re.compile(r"\b(?:person|singular|plural|indicative|imperative|infinitive|participle|"
                   r"tense|voice|preposition|particle|conjunction|adverb|pronoun|article|"
                   r"genitive|dative|accusative|nominative)\b", re.I)


def _after_comma(c):
    parts = _split_top(c, ",")
    return ",".join(parts[1:]).strip() if len(parts) > 1 else ""


def sense_clauses(entry, remainders=False):
    """Strong's definition split at semicolons, the clauses about derivation
    or grammar dropped. A clause citing another entry (G<n>) outside
    parentheses is derivational. With `remainders`, a dropped clause shaped
    "a primary preposition denoting origin, from, out" gives back what
    follows its first comma, where Strong's sense often begins."""
    out = []
    for c in (x.strip() for x in _split_top(entry.definition if entry else "", ";")):
        bare = _unparen(c).strip(" ,.:")
        if not bare:
            continue
        if not (_DERIV.match(bare) or _META.search(bare) or re.search(r"\bG\d+", bare)):
            out.append(c)
        elif remainders and not re.search(r"\bG\d+", bare):
            rest = _after_comma(c)
            if rest:
                out.append(rest)
    return out


# ---------------------------------------------------------------------------
# Closed classes: English forms and what they agree with
# ---------------------------------------------------------------------------

# form -> (classes it may gloss, person, numbers, genders, case slots).
# Slots: nom (nominative, vocative), obl (dative, accusative), gen. A genitive
# takes a possessive or an oblique form ("my", or "me" as in "of me"),
# whichever Strong's lists first.
_ANY_G = "MFN"
FORMS = {
    "i": ("P", "1", "S", _ANY_G, "nom"), "me": ("P", "1", "S", _ANY_G, "obl"),
    "my": ("P", "1", "S", _ANY_G, "gen"), "mine": ("P", "1", "S", _ANY_G, "gen"),
    "we": ("P", "1", "P", _ANY_G, "nom"), "us": ("P", "1", "P", _ANY_G, "obl"),
    "our": ("P", "1", "P", _ANY_G, "gen"),
    "thou": ("P", "2", "S", _ANY_G, "nom"), "thee": ("P", "2", "S", _ANY_G, "obl"),
    "thy": ("P", "2", "S", _ANY_G, "gen"), "thine": ("P", "2", "S", _ANY_G, "gen"),
    "ye": ("P", "2", "P", _ANY_G, "nom"), "you": ("P", "2", "P", _ANY_G, "obl"),
    "your": ("P", "2", "P", _ANY_G, "gen"),
    "he": ("PD", "3", "S", "M", "nom"), "him": ("PD", "3", "S", "M", "obl"),
    "his": ("PD", "3", "S", "M", "gen"),
    "she": ("PD", "3", "S", "F", "nom"), "her": ("PD", "3", "S", "F", "obl gen"),
    "it": ("PD", "3", "S", "N", "nom obl"), "its": ("PD", "3", "S", "N", "gen"),
    "they": ("PD", "3", "P", _ANY_G, "nom"), "them": ("PD", "3", "P", _ANY_G, "obl"),
    "their": ("PD", "3", "P", _ANY_G, "gen"),
    "this": ("D", "3", "S", _ANY_G, "nom obl gen"), "that": ("DR", "3", "SP", _ANY_G, "nom obl gen"),
    "these": ("D", "3", "P", _ANY_G, "nom obl gen"), "those": ("D", "3", "P", _ANY_G, "nom obl gen"),
    "the": ("T", "3", "SP", _ANY_G, "nom obl gen"),
    "who": ("R", "3", "SP", "MF", "nom"), "whom": ("R", "3", "SP", "MF", "obl"),
    "whose": ("R", "3", "SP", _ANY_G, "gen"),
    "which": ("R", "3", "SP", _ANY_G, "nom obl gen"), "what": ("R", "3", "SP", "N", "nom obl"),
}
CLOSED = set("TPDR")
_SLOT = {"N": "nom", "V": "nom", "G": "gen", "D": "obl", "A": "obl"}


def features(code):
    """Robinson code -> (class, person, case, number, gender) for T/P/D/R,
    else None. `P-GSM` has no person digit: it is autos, third person."""
    m = re.match(r"^([TPDR])-([123])?([NVGDA])([SP])([MFN])?", code or "")
    if not m:
        return None
    cls, per, case, num, gen = m.groups()
    return cls, per or "3", case, num, gen


def form_fits(form, feats):
    spec = FORMS.get(form.lower())
    if not spec or feats is None:
        return False
    classes, per, nums, gens, slots = spec
    cls, p, case, num, gen = feats
    slot, slots = _SLOT[case], slots.split()
    ok_slot = slot in slots or (slot == "gen" and "obl" in slots)
    return cls in classes and p == per and num in nums and (gen is None or gen in gens) and ok_slot


# ---------------------------------------------------------------------------
# The rule
# ---------------------------------------------------------------------------

_LEAD = re.compile(r"^(?:properly|literally|figuratively|especially|specially|generally|"
                   r"by (?:implication|extension|analogy|Hebraism)|i\.e\.|also|hence|"
                   r"(?:used )?adverbially|abstractly|concretely)\b[ ,]*", re.I)


def _strip_lead(s):
    prev = None
    while prev != s:
        prev, s = s, _LEAD.sub("", s.lstrip(' "(,.:')).strip()
    return s


def _pos(code):
    return (code or "").split("-")[0]


def def_head(entry, code):
    """The head of the first sense clause, or None."""
    for c in sense_clauses(entry)[:1]:
        h = _strip_lead(_unparen(c).strip(" ,.:"))
        h = re.split(r",|;|:|\bi\.e\.|\bor\b|\bthat is\b", h, 1)[0].strip(" ,.:")
        h = re.sub(r"^(?:a|an)\s+", "", h, flags=re.I)
        if _pos(code) == "V":
            h = re.sub(r"^(?:to|I)\s+", "", h)
        h = h.replace('"', "").strip()
        if h and len(h.split()) <= 4 and re.fullmatch(r"[A-Za-z][A-Za-z' -]*", h):
            return h
    return None


def _find(r, text, verb=False):
    """Where rendering `r` first occurs in `text` as a whole word, or None.
    One or two letters ("of", "to", "be") count only as the first word of a
    comma- or semicolon-clause, or for a verb right after "to": elsewhere
    they are part of a phrase ("in front of")."""
    pos = 0
    for clause in re.split(r"(?<=[;,])", text):
        if len(r) <= 2:
            head = _strip_lead(clause)
            if re.match(re.escape(r) + r"(?![A-Za-z])", head, re.I):
                return pos + clause.find(head[:len(r)])
            m = re.search(r"(?<![A-Za-z])to " + re.escape(r) + r"(?![A-Za-z])", clause, re.I) if verb else None
            if m:
                return pos + m.start() + 3
        else:
            m = re.search(r"(?<![A-Za-z])" + re.escape(r) + r"(?![A-Za-z])", clause, re.I)
            if m:
                return pos + m.start()
        pos += len(clause)
    return None


def gloss_for(code, entry):
    """(gloss or None, provenance). `code` is Robinson's parsing, `entry` the
    Strong's Entry for the token's number (None if Strong's has none)."""
    def got(g, rule):
        return g, {"source": SOURCE, "by": "lemma_key", "rule": rule, "kind": "dictionary"}

    def none(why):
        return None, {"source": None, "by": None, "rule": None, "kind": None, "why": why}

    if entry is None:
        return none("Strong's has no entry for this number")
    renderings = usable(entry)
    pos = _pos(code)
    if pos in CLOSED:
        feats = features(code)
        for r in renderings:
            if form_fits(r[0], feats):
                return got(r[0], "kjv-form")
        return none("no KJV rendering agrees in person, number, gender and case")
    # A pronoun form never glosses a non-pronoun ("that" is a conjunction too).
    content = [r for r in renderings if r[0].lower() not in FORMS or r[0].lower() == "that"]
    if len(renderings) == 1 and content:
        return got(fit(content[0], code), "kjv-sole")
    clauses = sense_clauses(entry, remainders=True)
    # Outside parentheses first: Strong's parentheses qualify ("literally or
    # figuratively") more often than they define. Then inside them.
    # A parenthesis about grammar ("with the genitive case, ...") is never searched.
    inside = [re.sub(r"\((?:[^()]|\([^()]*\))*\)",
                     lambda m: " " if _META.search(m.group(0)) else m.group(0), c) for c in clauses]
    for text in ("; ".join(_unparen(c) for c in clauses), "; ".join(inside)):
        best = None
        for r in content:
            at = _find(r[0], text, verb=(pos == "V"))
            if at is not None and (best is None or (at, -len(r[0])) < (best[0], -len(best[1][0]))):
                best = (at, r)
        if best:
            return got(fit(best[1], code), "kjv-in-def")
    if pos in ("N", "A", "V"):
        h = def_head(entry, code)
        if h:
            return got(h, "def-head")
    return none("no KJV rendering in the definition; " + (
        "no usable definition head" if pos in ("N", "A", "V")
        else "a function word takes no definition head"))


# ---------------------------------------------------------------------------
# The override layer (the shape of lemma_spine's)
# ---------------------------------------------------------------------------

OVERRIDE_KEYS = {"address", "surface", "gloss", "plain_form", "layer", "reviewed_on", "note",
                 "draft", "drafted_on"}
DRAFT_LAYERS = ("house",)     # a draft is the house's; Adam's own rows are never drafts


def load_overrides(path=None):
    """{token address: row}, from `path` or OVERRIDES. A missing file is no
    overrides. Any malformed row is a hard stop: an answer that cannot be
    applied must not be dropped."""
    path = path or OVERRIDES
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            where = f"{os.path.basename(path)}:{n}"
            extra = set(row) - OVERRIDE_KEYS
            if extra:
                raise ValueError(f"{where}: unknown fields {sorted(extra)}")
            if "draft" in row and row["draft"] is not True:
                raise ValueError(f"{where}: `draft` is true or absent")
            dated = "drafted_on" if row.get("draft") else "reviewed_on"
            undated = "reviewed_on" if row.get("draft") else "drafted_on"
            for k in ("address", "surface", "layer", dated):
                if not isinstance(row.get(k), str) or not row[k]:
                    raise ValueError(f"{where}: `{k}` is required")
            if undated in row:
                raise ValueError(f"{where}: a {'draft' if row.get('draft') else 'reviewed'} row "
                                 f"carries `{dated}`, not `{undated}`")
            if row["layer"] not in OVERRIDE_LAYERS:
                raise ValueError(f"{where}: layer must be one of {OVERRIDE_LAYERS}")
            if row.get("draft") and row["layer"] not in DRAFT_LAYERS:
                raise ValueError(f"{where}: only {DRAFT_LAYERS} rows may be drafts")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row[dated]):
                raise ValueError(f"{where}: {dated} must be YYYY-MM-DD")
            if not {"gloss", "plain_form"} & set(row):
                raise ValueError(f"{where}: sets neither gloss nor plain_form")
            for k in ("gloss", "plain_form"):
                if k in row and (not isinstance(row[k], str) or not row[k].strip()):
                    raise ValueError(f"{where}: {k} may not be empty")
            if row["address"] in out:
                raise ValueError(f"{where}: {row['address']} is overridden twice")
            out[row["address"]] = row
    return out


def apply_override(gloss, plain_form, prov, surface, ov):
    """One override row onto a token's dictionary gloss. Returns (gloss,
    plain_form, provenance). The dictionary value and its rule are kept
    under `was`; nothing is lost."""
    if ov["surface"] != surface:
        raise ValueError(f"{ov['address']}: override is for {ov['surface']!r}, "
                         f"the token is {surface!r}")
    new = {"source": ov["layer"], "by": "address", "rule": None, "kind": "contextual"}
    if ov.get("draft"):
        new.update(draft=True, drafted_on=ov["drafted_on"])
    else:
        new["reviewed_on"] = ov["reviewed_on"]
    if ov.get("note"):
        new["note"] = ov["note"]
    new["was"] = {"value": gloss, **prov}
    return ov.get("gloss", gloss), ov.get("plain_form", plain_form), new
