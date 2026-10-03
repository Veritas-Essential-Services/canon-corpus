#!/usr/bin/env python3
"""
af_scripture.py -- the scripture references in Lake's notes to the Apostolic
Fathers, read and resolved to KJV unit ids. Used by build_apostolic_fathers.py.

Each note's reference comes twice: as Lake printed it (the label, "Ps. 54, 23;
1 Pet. 5,7") and as First1KGreek encoded it (CTS URNs). Neither is clean.
The labels are OCR ("Prov. 3, 84" for 3, 34; "Dent." for Deut.), and the URNs
were keyed by hand: some are malformed (`cts:urn:...`, `tlg0011`), some name
the wrong book (Lake's "Jon. 3" encoded as John 3; "Ps. 33, 9" as the NT's
27th book), and 177 notes have no URN at all. So:

1. The LABEL is read first, because it is Lake's own words: every book
   abbreviation in it (OCR variants included), then chapter, verse(s), ranges
   and "; ch, v" continuations in the same book.
2. Each URN is a cross-check. A URN that agrees with a label reference marks
   it `urn: true`. A URN naming a book the note does not mention, or numbers
   the note does not print, is kept as its own link, unresolved, with the
   disagreement as `why`. That is the flag; nothing is silently dropped.
3. A note whose label has no reference (a URN alone) is resolved from the URN.

RESOLUTION. Lake mostly cites the Old Testament as the Septuagint numbers it
(his "Ps. 54, 23" is the KJV's Ps 55:22), and First1KGreek keyed every OT
reference to the Septuagint, so OT references go through Brenton's LXX -> KJV
map (data/versification/brenton-kjv.json, PR #9, versification.resolve_brenton).
But not always: "Ps. 37, 9. 38" at 1 Clem. 14.4 is the English Ps 37. So where
the English numbering names a different KJV verse it is kept as `alt_target`,
and where Brenton has no such verse but the English numbering does, that is
the reading (`numbering: "english"`). NT references are the KJV's numbering already
and resolve when the verse exists. References to 1 or 2 Clement resolve to
this build's own unit ids. A whole chapter, a book outside the KJV (Tobit,
Wisdom, Sirach), a verse that does not exist (an OCR digit) and anything not
scripture (Zenobius, Enoch) stay `resolved: false`, each with its reason.
"""
import re

import versification as V

NT = ["Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil",
      "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet",
      "2Pet", "1John", "2John", "3John", "Jude", "Rev"]
# TLG 0527 (Septuaginta) work numbers, as far as this build relies on them. A
# URN's book is only ever trusted when the note's label names the same book.
LXX_TLG = {1: "Gen", 2: "Exod", 3: "Lev", 4: "Num", 5: "Deut", 6: "Josh", 8: "Judg",
           11: "1Sam", 12: "2Sam", 13: "1Kgs", 14: "2Kgs", 15: "1Chr", 16: "2Chr",
           20: "Jdt", 21: "Tob", 23: "1Macc", 24: "2Macc", 27: "Ps", 29: "Prov", 30: "Eccl",
           31: "Song", 32: "Job", 33: "Wis", 34: "Sir", 36: "Hos", 37: "Amos", 38: "Mic",
           39: "Joel", 40: "Obad", 41: "Jonah", 42: "Nah", 43: "Hab", 44: "Zeph", 45: "Hag",
           46: "Zech", 47: "Mal", 48: "Isa", 49: "Jer", 50: "Bar", 51: "Lam", 53: "Ezek", 56: "Dan"}
SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude"}

_I = r"(?:I|1|l)\s?"           # "I", "1", OCR "l"
_II = r"(?:II|2|11)\s?"        # "II", "2", OCR "11"
# (pattern, corpus, book). Corpus: nt (KJV numbering), lxx (Brenton), af (this build).
ABBREVS = [
    (_I + r"Clem(?:ent)?\.?", "af", "1clement-lake"), (_II + r"Clem(?:ent)?\.?", "af", "2clement-lake"),
    (_II + r"Cor", "nt", "2Cor"), (_I + r"Cor", "nt", "1Cor"),
    (_II + r"Th(?:ess|ses)", "nt", "2Thess"), (_I + r"Thess", "nt", "1Thess"),
    (_II + r"Tim", "nt", "2Tim"), (_I + r"Tim", "nt", "1Tim"),
    (_II + r"Pet", "nt", "2Pet"), (r"\*?" + _I + r"Pet", "nt", "1Pet"),
    (r"(?:III|3)\s?Jo(?:h)?", "nt", "3John"), (_II + r"Jo(?:h)?", "nt", "2John"), (_I + r"Jo(?:h)?", "nt", "1John"),
    (_II + r"Sam", "lxx", "2Sam"), (_I + r"Sam", "lxx", "1Sam"),
    (_II + r"Kings", "lxx", "2Kgs"), (_I + r"Kings", "lxx", "1Kgs"),
    (_II + r"Chron", "lxx", "2Chr"), (_I + r"Chron", "lxx", "1Chr"),
    (_II + r"Macc", "lxx", "2Macc"), (_I + r"Macc", "lxx", "1Macc"),
    (r"M(?:t|att|atth)", "nt", "Matt"), (r"M(?:k|c|ark)", "nt", "Mark"),
    (r"L(?:uke|uk|k|c)", "nt", "Luke"), (r"J(?:oh|o|uh|ohn)", "nt", "John"),
    (r"Acts", "nt", "Acts"), (r"Rom", "nt", "Rom"), (r"Gal", "nt", "Gal"),
    (r"E(?:ph|pb)", "nt", "Eph"), (r"Ph(?:ilipp|il|ll)", "nt", "Phil"), (r"Col", "nt", "Col"),
    (r"Tit", "nt", "Titus"), (r"Philem", "nt", "Phlm"), (r"H(?:eb|cb|ev)", "nt", "Heb"),
    (r"Ja(?:m|mes|c)", "nt", "Jas"), (r"Jude", "nt", "Jude"), (r"(?:Rev|Apoc)", "nt", "Rev"),
    (r"Gen", "lxx", "Gen"), (r"(?:Exod|Erod|Ex)", "lxx", "Exod"), (r"(?:Lev|Lv)", "lxx", "Lev"),
    (r"Num", "lxx", "Num"), (r"D(?:eut|ent|out|eunt)", "lxx", "Deut"), (r"Jos(?:h)?", "lxx", "Josh"),
    (r"Judg", "lxx", "Judg"), (r"Ruth", "lxx", "Ruth"), (r"Job", "lxx", "Job"),
    (r"(?:Pss|Ps|Pa)", "lxx", "Ps"), (r"Prov", "lxx", "Prov"), (r"Eccles", "lxx", "Eccl"),
    (r"(?:Is|Isaiah)", "lxx", "Isa"), (r"Jer", "lxx", "Jer"), (r"Lam", "lxx", "Lam"),
    (r"Ez(?:ek|ck)", "lxx", "Ezek"), (r"Dan", "lxx", "Dan"), (r"Hos", "lxx", "Hos"),
    (r"Joel", "lxx", "Joel"), (r"Am", "lxx", "Amos"), (r"Jon", "lxx", "Jonah"),
    (r"Mic", "lxx", "Mic"), (r"Hab", "lxx", "Hab"), (r"Z(?:ech|ach)", "lxx", "Zech"),
    (r"Mal(?:ach)?", "lxx", "Mal"), (r"Esther", "lxx", "Esth"),
    (r"Tob", "lxx", "Tob"), (r"Judith", "lxx", "Jdt"), (r"Wisd", "lxx", "Wis"),
    (r"(?:Ecclus|Sirach)", "lxx", "Sir"),
]
# Longest-first alternation, each as a whole word followed by a dot, space or digit.
_ORDER = sorted(range(len(ABBREVS)), key=lambda i: -len(ABBREVS[i][0]))
BOOK_RE = re.compile("|".join(rf"(?P<b{i}>(?<![A-Za-z]){ABBREVS[i][0]})(?![a-z])\.?" for i in _ORDER))


def label_books(label):
    """[(corpus, book, start, end)] for every book abbreviation in the label."""
    out = []
    for m in BOOK_RE.finditer(label):
        i = int(next(k for k, v in m.groupdict().items() if v)[1:])
        out.append((ABBREVS[i][1], ABBREVS[i][2], m.start(), m.end()))
    return out


def parse_label(label):
    """[(corpus, book, chapter, verse or None, end verse or None)] in label order.
    After a book: `ch, v`, `ch, v. v2`, `ch, v, v2`, `ch, v-v2`, `ch` alone, and
    `; ch, v` again in the same book. For a one-chapter book, `n` is the verse."""
    books = label_books(label)
    refs = []
    for k, (corpus, book, _, end) in enumerate(books):
        seg = label[end: books[k + 1][2] if k + 1 < len(books) else len(label)]
        # "(11, 12; 49, 22)" adds chapter, verse pairs of the same book;
        # "(*wulg. 35.9)" is another numbering, and is dropped.
        seg = re.sub(r"\(\s*[^\d\s(][^)]*\)?", " ", seg).replace("(", ";").replace(")", " ")
        seg = re.sub(r"^(\W*)[Il](?=\s*,)", r"\g<1>1", seg)   # OCR: "Is. I, 16" is chapter 1
        for part in seg.split(";"):
            toks = re.findall(r"\d+|-", part)
            while toks and toks[0] == "-":
                toks.pop(0)
            if not toks:
                continue
            if book in SINGLE_CHAPTER:
                refs.append((corpus, book, 1, int(toks[0]), None))
                continue
            ch, rest = int(toks[0]), toks[1:]
            if not [t for t in rest if t != "-"]:
                refs.append((corpus, book, ch, None, None))
                continue
            i = 0
            while i < len(rest):
                if rest[i] == "-":
                    i += 1
                    continue
                v = int(rest[i])
                if i + 2 < len(rest) and rest[i + 1] == "-" and rest[i + 2] != "-":
                    refs.append((corpus, book, ch, v, int(rest[i + 2])))
                    i += 3
                else:
                    refs.append((corpus, book, ch, v, None))
                    i += 1
    return refs


URN_RE = re.compile(r"urn:cts:greekLit:tlg(\d{4})\.tlg(\d{3}):(\d+)(?:\.(\d+))?(?:-(\d+)(?:\.(\d+))?)?")


def parse_urn(urn):
    """(corpus, book, chapter, verse, end verse) or (None, reason)."""
    if not urn:
        return None, "no URN"
    s = urn.replace("cts:urn:", "urn:cts:").rstrip(").,;")
    m = URN_RE.fullmatch(s)
    if not m:
        return None, f"malformed URN {urn!r}"
    grp, work, ch, v, a, b = m.groups()
    grp, work = int(grp), int(work)
    end = int(b) if b else (int(a) if a and v else None)
    if grp == 31 and 1 <= work <= 27:
        corpus, book = "nt", NT[work - 1]
    elif grp == 527 and work in LXX_TLG:
        corpus, book = "lxx", LXX_TLG[work]
    elif grp == 1271 and work in (1, 2):
        corpus, book = "af", f"{work}clement-lake"
    else:
        return None, f"URN names a work that is not scripture or not known here ({urn})"
    return (corpus, book, int(ch), int(v) if v else None, end), None


def printed(ref):
    corpus, book, ch, v, end = ref
    return f"{book} {ch}" + (f":{v}" if v else "") + (f"-{end}" if end else "")


def resolve(ref, ctx):
    """The link fields for one reference."""
    corpus, book, ch, v, end = ref
    out = {"ref": printed(ref), "corpus": corpus}
    if v is None:
        return {**out, "resolved": False, "why": "cites a whole chapter, not a verse"}

    def one(verse):
        if corpus == "nt":
            t = f"kjv:{book}.{ch}.{verse}"
            return ({"resolved": True, "target": t} if t in ctx["kjv_ids"]
                    else {"resolved": False, "why": "no such verse in the KJV (an OCR digit?)"})
        if corpus == "af":
            t = f"{book}:{ch}.{verse}"
            return ({"resolved": True, "target": t} if t in ctx["af_ids"]
                    else {"resolved": False, "why": f"no section {ch}.{verse} in {book}"})
        r = V.resolve_brenton(f"{book}.{ch}.{verse}", ctx["bmap"], ctx["kjv_ids"])
        direct = f"kjv:{book}.{ch}.{verse}"
        if direct not in ctx["kjv_ids"]:
            return r
        if r.get("resolved"):
            # Lake mostly numbers as the LXX does, but not always (his "Ps. 37,
            # 9. 38" at 1 Clem. 14.4 is the English Ps 37): where the two
            # numberings name different verses, both are kept.
            return r if r["target"] == direct else {**r, "alt_target": direct}
        if r.get("why", "").startswith("no such verse"):
            return {"resolved": True, "target": direct, "numbering": "english",
                    "why_numbering": "Brenton's Septuagint has no such verse; the English numbering fits"}
        return r

    r = one(v)
    out.update({k: r[k] for k in ("resolved", "target", "spans", "alt_target", "numbering",
                                  "why_numbering", "why") if k in r})
    if r.get("resolved") and end and end > v:
        last = one(end)
        if last.get("resolved"):
            out["through"] = last["target"]
    if corpus == "lxx" and out.get("numbering") != "english":
        out["via"] = "brenton-kjv"
    return out


def resolve_note(label, urns, ctx):
    """Every link for one note: the label's references first, each confirmed
    by a URN where one agrees, then every URN that agrees with none, flagged."""
    lrefs = parse_label(label)
    books = {(c, b) for c, b, _, _ in label_books(label)}
    parsed = [(u, *parse_urn(u)) for u in urns]
    used = set()
    links = []
    for ref in lrefs:
        hit = next((u for u, p, _ in parsed if p and p[:4] == ref[:4]), None)
        if hit:
            used.add(hit)
        links.append({"label": label, "cts": hit, **resolve(ref, ctx),
                      "source": "label+urn" if hit else "label"})
    for u, p, err in parsed:
        if u in used:
            continue
        if p is None:
            if u and lrefs:
                continue              # a broken URN where the label already says it
            links.append({"label": label, "cts": u, "resolved": False, "why": err, "source": "urn"})
        elif not lrefs:
            links.append({"label": label, "cts": u, **resolve(p, ctx), "source": "urn"})
        elif (p[0], p[1]) not in books:
            links.append({"label": label, "cts": u, "ref": printed(p), "resolved": False, "source": "urn",
                          "why": f"the URN names {p[1]}, which the note does not cite: a keying error"})
        else:
            links.append({"label": label, "cts": u, "ref": printed(p), "resolved": False, "source": "urn",
                          "why": "the URN's numbers are not the note's: one of the two has a slip"})
    if not links:
        links.append({"label": label, "cts": None, "resolved": False, "source": "label",
                      "why": "no scripture reference in the note"})
    return links
