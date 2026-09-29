#!/usr/bin/env python3
"""betacode.py -- Beta Code (the TLG/Perseus ASCII Greek) to Unicode, and a
headword key for matching one lexicon's entries against another's.

Perseus's LSJ writes every Greek word in Beta Code: `lo/gos` is λόγος,
`*)ihsou=s` is Ἰησοῦς, `a)1` is the first homograph of ἀ-. Diacritics follow
their letter (after `*` for a capital, they sit between the `*` and the
letter); they are emitted as combining marks in the order written and
composed by NFC, which is the order Unicode's precomposed letters expect
(breathing, then accent, then iota subscript).

    to_unicode("lo/gos")     -> "λόγος"
    headword_key("λόγος")    -> "λογοσ"   (no marks, lower case, one sigma)
"""
import re, unicodedata

LETTERS = {
    "a": "α", "b": "β", "g": "γ", "d": "δ", "e": "ε", "z": "ζ", "h": "η", "q": "θ",
    "i": "ι", "k": "κ", "l": "λ", "m": "μ", "n": "ν", "c": "ξ", "o": "ο", "p": "π",
    "r": "ρ", "s": "σ", "t": "τ", "u": "υ", "f": "φ", "x": "χ", "y": "ψ", "w": "ω",
    "v": "ϝ",
}
MARKS = {")": "̓", "(": "̔", "/": "́", "\\": "̀", "=": "͂",
         "|": "ͅ", "+": "̈", "_": "̄", "^": "̆"}
PUNCT = {":": "·", ";": ";", "'": "’", "-": "-"}
# a capital's marks sit between * and the letter; a few Perseus keys put them
# after it instead (*)a/ploun), so both are read
RE_TOKEN = re.compile(r"(\*)([)(/\\=|+_^]*)([a-zA-Z])([)(/\\=|+_^]*)|([a-zA-Z])([)(/\\=|+_^]*)(\d?)|(.)", re.S)


def to_unicode(beta):
    """Beta Code -> NFC Unicode Greek. Unknown characters pass through."""
    out = []
    for star, pre, cap, cpost, let, post, sig, other in RE_TOKEN.findall(beta):
        if star:
            base = LETTERS.get(cap.lower(), cap).upper()
            out.append(base + "".join(MARKS[m] for m in pre + cpost))
        elif let:
            l = let.lower()
            if l == "s":
                base = {"1": "σ", "2": "ς", "3": "ϲ"}.get(sig, "σ")
            else:
                base = LETTERS.get(l, let)
            out.append(base + "".join(MARKS[m] for m in post))
            if sig and l != "s":
                out.append(sig)  # a homograph number on a key (a)1): keep it visible
        else:
            out.append(PUNCT.get(other, other))
    s = unicodedata.normalize("NFC", "".join(out))
    # medial sigma at a word's end is final sigma
    return re.sub(r"σ(?=$|[^\ẁ-ͯ])", "ς", s)


def headword_key(word):
    """A matching key: no diacritics, no digits or quantity marks, lower case,
    every sigma the same. Two lexicons agree on a word when their keys agree."""
    s = unicodedata.normalize("NFD", word)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().replace("ς", "σ").replace("ϲ", "σ")
    return re.sub(r"[^\w]|[\d_]", "", s)
