# prov: 2026-10-20 claude-opus-5-5 drafted
# fable_review: pending
"""Rules learned from Adam's own picks on the Proof Desk (vol 6, 117 answers, 2026-10-20).

Each rule clears a review item ONLY when it reproduces what Adam chose on items of the same kind;
tests/learned_test is the check (python3 -m unscanner.learned --check <review.json> <picks dir>).
Every cleared item records which rule cleared it, and stays changeable on the page.

  roman      a garbled roman numeral ("Ill", "lU", "HI", "m", "NI", "IL.", "1.", "11.") -> the
             roman reading (III, II., i., ii.); digits never win over a roman reading.
  ligature   one engine reads "e" where the other reads "se"/"ce"/"ae"/"ee" -> æ (Æ when capital):
             Phsedrus/Phedrus -> Phædrus.
  smallcaps  a word in small capitals (case jumbled inside it: CaGLiostTRo) -> the dictionary word
             among the readings, in full capitals.
  abbrev     one reading is a stock abbreviation of the book (etc., &c., viz., i.e., e.g., cf.,
             ib., ibid., sc., q.v.) -> that one. Adam, 2026-10-20: "etc. is more likely to show up in
             this book than ctc." Runs before c-for-e, which alone would pick ctc over etc.
  c-for-e    two readings differ only by c/e -> the one with c, unless only the e-form is a word.
  ll-for-U   two readings differ only by ll/U (the Archive's engine) -> ll.
  ll-in-word a capital U inside a lowercase word (RoUa, DurtaiUe, baU,) is ll, or li/il: Adam,
             2026-10-20: "ll is more likely to show up in the middle of a lowercase word than the
             uppercase letter U." Taken when another reading spells exactly that. Any number of readings.
  R-E-B-h    readings differ only by R~E/B/P or b~h -> our engine's reading (the Archive's misreads).
  same-scan  both engines on one scan agree, the other scan's two engines disagree with each
             other -> the agreeing pair, unless a rival is a word and the pair is not.
"""
import re
from .editions import key

GARBLE_CH = set("IlL1|iUHmnNWTuZ!")
VALID_ROMAN = re.compile(r"^(?=[MDCLXVI])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")


def is_roman(t):
    """A well-formed roman numeral, all capitals or all small letters, with its own punctuation:
    'III', 'II.', '(XI.)', 'iii.'. Not 'll' (letters), not 'IL' (not a numeral)."""
    core = re.sub(r"^[\(\[{]+|[\.\),;:\]]+$", "", t.strip())
    if not core or not (core.isupper() or core.islower()):
        return False
    if core.islower() and not re.search(r"[ivx]", core):
        return False
    return bool(VALID_ROMAN.match(core.upper()))


def roman_rule(rd, ctx):
    romans = [r for r in rd if is_roman(r)]
    others = [r for r in rd if not is_roman(r)]
    letters = lambda t: re.sub(r"[^A-Za-z0-9|!]", "", t)
    if not romans:
        # a bare heading numeral every engine garbled: "Ill", "lU", "m", "ul", "NI" -> III
        if all(0 < len(letters(r)) <= 3 and set(letters(r)) <= GARBLE_CH | {"m"} for r in rd) and len(ctx.split()) == 1:
            return "III"
        return None
    if all(set(letters(r)) <= GARBLE_CH | set("IVXLivxl") | set("0123456789") for r in others):
        # prefer the longest well-formed roman reading (II. over I., iii. over i.)
        romans.sort(key=lambda r: (-len(letters(r)), r))
        best = romans[0]
        if best.strip().upper() == best.strip() or best.strip().lower() == best.strip():
            return best.strip()
    return None


LIG = re.compile(r"(se|ce|ae|ee)")


def ligature_rule(rd):
    """'Phsedrus' + 'Phedrus' -> 'Phædrus'; 'Fcemina' + 'Femina' -> 'Fæmina'."""
    plain = [r for r in rd if "æ" not in r.lower()]
    for a in plain:
        for b in plain:
            if a == b:
                continue
            ka, kb = a.strip(), b.strip()
            for m in LIG.finditer(kb):
                cand = kb[:m.start()] + "e" + kb[m.end():]
                if key(cand) == key(ka) and len(ka) >= 3:
                    i = m.start()
                    # position of that e in a: same prefix length
                    if ka[:i].lower() == kb[:i].lower():
                        out = ka[:i] + ("Æ" if ka[i:i + 1].isupper() or (i == 0 and ka[:1].isupper()) else "æ") + ka[i + 1:]
                        return out
            # capital: '-iEthiopes'/'Aathiopes' -> Æthiopes
            if re.match(r"^(Aa|Ae|-iE|AE)", kb) and ka[:1] == "A" and key(ka[2:]) == key(re.sub(r"^(Aa|Ae|-iE|AE)", "", kb)):
                return "Æ" + ka[2:]
    return None


def jumbled(t):
    s = re.sub(r"[^A-Za-z]", "", t)
    return len(s) >= 4 and s != s.upper() and sum(c.isupper() for c in s[1:]) >= 2


def smallcaps_rule(groups, lexicon, word):
    """Only OUR engine's jumble counts: the Archive's engine garbles plain words into capitals
    ('lAHle' for Little), so its capitals are no sign of small capitals."""
    rd = list(groups)
    if not any(jumbled(t) for t, ws in groups.items() if any(w.endswith(".tess") for w in ws)):
        return None
    words = sorted({key(r) for r in rd if word(key(r))})
    if len(words) == 1:
        src = next(r for r in rd if key(r) == words[0]).strip()
        core = re.match(r"^(\W*)(.*?)(\W*)$", src)
        return core.group(1) + core.group(2).upper() + core.group(3)
    return None


ABBREV = {"etc.", "&c.", "viz.", "i.e.", "e.g.", "cf.", "ib.", "ibid.", "sc.", "q.v."}


def abbrev_rule(rd):
    """The reading that is a stock abbreviation, kept with its own trailing punctuation."""
    hits = {t.strip() for t in rd if re.sub(r"[,;:)]+$", "", t.strip()).lower() in ABBREV}
    return hits.pop() if len(hits) == 1 else None


IN_WORD_U = re.compile(r"(?<=[a-z])U(?=[a-z]|[^A-Za-z]*$)")


def ll_rule(rd):
    """Readings with a U inside a lowercase word, read as ll/li/il, matched against the others."""
    bad = [t.strip() for t in rd if IN_WORD_U.search(t)]
    q = lambda t: re.sub(r"[“”\"]", '"', re.sub(r"[‘’']", "'", t))     # quote marks are not the question
    good = {q(t.strip()): t.strip() for t in rd if not IN_WORD_U.search(t) and "U" not in t[1:]}
    if not bad or not good:
        return None
    hits = set()
    for t in bad:
        for rep in ("ll", "li", "il"):
            c = q(IN_WORD_U.sub(rep, t))
            if c in good:
                hits.add(good[c])
                break
    return hits.pop() if len(hits) == 1 else None


def only_swaps(a, b, pairs):
    """True when a and b differ only by the given (x, y) substitutions; returns the direction map."""
    import difflib
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    seen = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        x, y = a[i1:i2], b[j1:j2]
        if (x, y) in pairs or (y, x) in pairs:
            seen.append((x, y))
        else:
            return None
    return seen or None


def swap_rules(groups, word):
    """groups: {text: [witnesses]} with exactly two readings. -> (rule, pick) or None."""
    if len(groups) != 2:
        return None
    (a, wa), (b, wb) = groups.items()
    A, B = a.strip(), b.strip()
    s = only_swaps(A, B, {("c", "e")})
    if s:
        withc = A if A.count("c") > B.count("c") else B
        other = B if withc == A else A
        if word(key(other)) and not word(key(withc)):
            return "c-for-e", other
        return "c-for-e", withc
    s = only_swaps(A, B, {("ll", "U"), ("lI", "U"), ("li", "U"), ("ll", "Ll")})
    if s:
        return "ll-for-U", A if "ll" in A else B
    s = only_swaps(A, B, {("R", "E"), ("R", "B"), ("R", "P"), ("b", "h"), ("R", "Ii"), ("F", "P")})
    if s:
        ours = [t for t, ws in groups.items() if all(w.endswith(".tess") for w in ws)]
        if ours:
            return "R-E-B-h", ours[0].strip()
    return None


def decide(item, word, lexicon=frozenset()):
    """A review item -> (pick, rule) or (None, None)."""
    groups = {r["text"]: r["by"] for r in item["readings"]}
    rd = list(groups)
    ctx = re.sub(r"[⟦⟧]", "", item["context"])
    p = roman_rule(rd, ctx)
    if p:
        return p, "roman"
    p = ligature_rule(rd)
    if p:
        return p, "ligature"
    p = abbrev_rule(rd)
    if p:
        return p, "abbrev"
    p = ll_rule(rd)
    if p:
        return p, "ll-in-word"
    p = smallcaps_rule(groups, lexicon, word)
    if p:
        return p, "smallcaps"
    s = swap_rules(groups, word)
    if s:
        return s[1], s[0]
    # same-scan: both engines on one scan agree; the other scan's engines disagree
    for t, ws in groups.items():
        scans = {w.split(".")[0] for w in ws}
        if len(ws) == 2 and len(scans) == 1:
            other = [x for x, v in groups.items() if x != t]
            if len(other) >= 2 and all(len(groups[x]) == 1 for x in other):
                exact = lambda k: len(k) >= 3 and k in lexicon       # no suffix guessing here: "cating" is not "cat"
                if not exact(key(t)) and any(exact(key(x)) for x in other):
                    return None, None
                return t.strip(), "same-scan"
    return None, None
