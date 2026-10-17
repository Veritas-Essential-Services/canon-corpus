"""A second witness: the Internet Archive's own OCR, consulted where ours is unsure.

The Archive ran a different OCR engine over the same scan years ago; its plain text (`_djvu.txt`) is
a second, independent reading. Two readers rarely make the same mistake, so where they disagree the
book itself can usually say which is right. The rule is narrow on purpose:

  a word of ours is replaced by the Archive's reading only when ALL of these hold --
    - the two texts align there one word for one word (difflib over the whole book, letters only);
    - our OCR read that word with confidence under 80;
    - our reading occurs at most once in the whole book (it is unattested);
    - the Archive's reading occurs at least twice in OUR text among words read with confidence 90+
      (the book itself attests it, by our own clean readings, not the Archive's).

Letters are compared without case, punctuation or accents, so the Archive's habit of dropping accents
(it prints "Athene" for the book's "Athené") never counts as a disagreement and never overwrites ours.
Only the letters are taken from the Archive; our punctuation and capitalisation stay. Every replacement
is recorded on the word (`was`) and listed on the review sheet.
"""
import difflib
import re
import unicodedata
from collections import Counter


def norm(t):
    t = unicodedata.normalize("NFKD", t)
    return re.sub(r"[^a-z]", "", "".join(c for c in t if not unicodedata.combining(c)).lower())


def _core_span(t):
    m = re.search(r"[A-Za-zÀ-ÿ].*[A-Za-zÀ-ÿ]|[A-Za-zÀ-ÿ]", t)
    return (m.start(), m.end()) if m else (0, len(t))


def _recase(src, model):
    if model.isupper() and len(model) > 1:
        return src.upper()
    if model[:1].isupper():
        return src[:1].upper() + src[1:].lower()
    return src.lower()


def collate(pages, witness_text, low=80, clean=90):
    """Mend our words in place from the witness. Returns a report dict."""
    ours = [w for p in pages if p["kind"] == "text" for ln in p["lines"] for w in ln["words"]]
    ours = [w for w in ours if norm(w["t"])]
    theirs = [t for t in re.findall(r"\S+", witness_text) if norm(t)]
    a = [norm(w["t"]) for w in ours]
    b = [norm(t) for t in theirs]
    attested = Counter(norm(w["t"]) for w in ours if w["conf"] >= clean)
    count = Counter(a)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    made, agree, considered = [], 0, 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            agree += i2 - i1
            continue
        if tag != "replace" or (i2 - i1) != (j2 - j1):
            continue
        for k in range(i2 - i1):
            w, theirs_t = ours[i1 + k], theirs[j1 + k]
            considered += 1
            mine, alt = a[i1 + k], b[j1 + k]
            if w["conf"] >= low or count[mine] > 1 or attested[alt] < 2:
                continue
            s, e = _core_span(w["t"])
            ts, te = _core_span(theirs_t)
            letters = re.sub(r"[^A-Za-zÀ-ÿ'’-]", "", theirs_t[ts:te]) or alt
            keep = lambda x: re.sub(r"[^.,;:!?'\"“”‘’()\[\]—-]", "", x)    # real punctuation only, not specks
            new = keep(w["t"][:s]) + _recase(letters, w["t"][s:e]) + keep(w["t"][e:])
            made.append({"was": w["t"], "now": new, "conf": w["conf"]})
            w["was"], w["t"] = w["t"], new
    return {"aligned_words": agree, "ours": len(a), "witness": len(b),
            "agreement": round(agree / max(1, len(a)), 4), "disagreements_considered": considered,
            "mended": len(made), "mends": made}
