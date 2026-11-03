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

RESOLUTION. NT references are the KJV's numbering already and resolve when
the verse exists. References to 1 or 2 Clement resolve to this build's own
unit ids. An OT reference is read in two numberings: the Septuagint's,
through Brenton's LXX -> KJV map (data/versification/brenton-kjv.json, PR #9,
versification.resolve_brenton), and the English (KJV) numbering as printed.
Where only one of them has such a verse, that one is the reading ("Ps. 54,
23" exists only in the Greek count: the KJV's Ps 55:22). Where both exist
and name different KJV verses, Lake is NOT consistent: read side by side
with the Greek of the section (2026-10-03, all 77 such links), about 50 cite
the English numbering ("Pa 110, 1", "sit thou at my right hand", at 1 Clem.
36.5), 13 the Septuagint's (the prayer at 1 Clem. 59, Hermas's Visions 1-2,
Did. 3.7's "the meek shall inherit the earth"), and the rest neither (an OCR
digit: "Exod. 8, 11" for 3, 11 at 1 Clem. 17.5). That reading is the table
LAKE_OT below, one row per link with its reason. An unread link takes the
English numbering, the majority, as `numbering: "english"` with Brenton's
verse kept as `alt_target`; a link read as neither stays `resolved: false`
with both candidates. A whole chapter, a book outside the KJV (Tobit, Wisdom,
Sirach), a verse that does not exist (an OCR digit) and anything not
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

_I = r"(?:I|1|l|i)\.?\s?"      # "I", "I.", "1", OCR "l" and "i" ("*i Jo. 4, 9")
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
    (r"(?:E(?:ph|pb)|Rph)", "nt", "Eph"), (r"Ph(?:ilipp|il|ll)", "nt", "Phil"), (r"Col", "nt", "Col"),
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


# A capitalised word that is no book ends a book's run of numbers: "Jer 17. 24.
# 25, cf. RL 91, 13-17" (Barn. 15.2) cites Jeremiah 17:24-25 and something else.
_STOP = re.compile(r"(?<![A-Za-z])(?!Cf\b)[A-Z][A-Za-z]+")


def _missing_semicolons(part):
    """Lake's "14, 31 15, 10" (Herm. Sim. 5.6.3) is "14, 31; 15, 10" with the
    semicolon lost: once a chapter has been marked with a comma, a number
    after bare whitespace that takes a comma itself starts a new chapter. A
    bare "32 8-9" (no comma yet) is still chapter and verse."""
    first = part.find(",")
    if first < 0:
        return [part]
    head, tail = part[:first + 1], part[first + 1:]
    return (head + re.sub(r"(\d)\s+(?=\d+\s*,)", r"\1;", tail)).split(";")


def parse_label(label):
    """[(corpus, book, chapter, verse or None, end)] in label order. `end` is a
    verse of the same chapter, a (chapter, verse) pair for a range that crosses
    into the next chapter ("4, 19-5, 6"), or None.
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
        stop = _STOP.search(seg)
        seg = seg[:stop.start()] if stop else seg
        for part in (q for p in seg.split(";") for q in _missing_semicolons(p)):
            # "4, 19-5, 6" (1 Clem. 39.2): a range into the next chapter
            cross = None
            first = part.find(",")
            if first >= 0:
                m = re.search(r"(\d+)\s*-\s*(\d+)\s*,\s*(\d+)", part[first + 1:])
                if m:
                    cross = (int(m.group(1)), (int(m.group(2)), int(m.group(3))))
                    part = part[:first + 1 + m.start()] + m.group(1)
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
                    last = cross is not None and i == len(rest) - 1 and v == cross[0]
                    refs.append((corpus, book, ch, v, cross[1] if last else None))
                    i += 1
    return refs


# Lake's OT references where the Septuagint's and the English numbering both
# have the verse and name different KJV verses, read against the Greek of the
# section and Brenton's English of both candidates (2026-10-03). Key: (unit id,
# the link's printed ref). "lxx": the Septuagint's count is the passage;
# "english": the English count is; "neither": neither verse is the passage.
_LXX, _EN = "lxx", "english"
LAKE_OT = {
    ("1clement-lake:2.8", "Prov 7:8"): ("neither", "the section quotes Prov 7:3 (the tablet of the heart): an OCR digit"),
    ("1clement-lake:13.1", "Jer 9:23-24"): (_EN, "let not the wise man glory in his wisdom"),
    ("1clement-lake:14.4", "Ps 37:9"): (_EN, "the upright shall inhabit the land"),
    ("1clement-lake:14.4", "Ps 87:5-7"): ("neither", "OCR'd 'Ps. 87. B5-B7'; 1 Clem. 14.5 quotes Ps 37:35-37"),
    ("1clement-lake:15.2", "Ps 61:5"): (_LXX, "they bless with their mouth but curse in their heart"),
    ("1clement-lake:15.5", "Ps 12:3-5"): (_EN, "the Lord shall cut off all flattering lips"),
    ("1clement-lake:16.14", "Ps 22:6-8"): (_EN, "I am a worm, and no man"),
    ("1clement-lake:17.5", "Exod 8:11"): ("neither", "'who am I?' from the bush is Exod 3:11: an OCR digit"),
    ("1clement-lake:22.1", "Ps 34:11"): (_EN, "come, ye children, hearken unto me"),
    ("1clement-lake:22.1", "Ps 34:17"): (_EN, "the end of the run Ps 34:11-17 the section quotes"),
    ("1clement-lake:26.2", "Ps 3:5"): (_EN, "I laid me down and slept; I awaked"),
    ("1clement-lake:27.6", "Ps 10:1-3"): ("neither", "1 Clem. 27.7 quotes Ps 19:1-3, the heavens declare: an OCR digit"),
    ("1clement-lake:28.2", "Ps 109:7-8"): ("neither", "whither shall I go from thy spirit is Ps 139:7-8: an OCR digit"),
    ("1clement-lake:35.6", "Ps 50:10"): (_EN, "1 Clem. 35.7 quotes Ps 50:16-23, 'unto the wicked God saith'"),
    ("1clement-lake:36.2", "Ps 104:4"): (_EN, "who maketh his angels spirits"),
    ("1clement-lake:36.5", "Ps 110:1"): (_EN, "sit thou at my right hand"),
    ("1clement-lake:45.5", "Dan 6:16"): (_EN, "Daniel cast into the den of lions"),
    ("1clement-lake:48.2", "Ps 118:19"): (_EN, "open to me the gates of righteousness"),
    ("1clement-lake:48.2", "Ps 118:20"): (_EN, "this gate of the Lord, into which the righteous shall enter"),
    ("1clement-lake:50.6", "Ps 32:1"): (_EN, "blessed is he whose transgression is forgiven"),
    ("1clement-lake:50.6", "Ps 32:2"): (_EN, "blessed is the man unto whom the Lord imputeth not iniquity"),
    ("1clement-lake:51.3", "Ps 49:14"): (_LXX, "offer unto God the sacrifice of praise (1 Clem. 52.3)"),
    ("1clement-lake:52.2", "Ps 50:14"): (_EN, "offer unto God thanksgiving (1 Clem. 52.3)"),
    ("1clement-lake:52.2", "Ps 50:15"): (_EN, "call upon me in the day of trouble (1 Clem. 52.3)"),
    ("1clement-lake:54.3", "Ps 24:1"): (_EN, "the earth is the Lord's, and the fulness thereof"),
    ("1clement-lake:56.4", "Ps 141:5"): (_EN, "let the righteous smite me; it shall be a kindness"),
    ("1clement-lake:59.3", "Ps 32:10"): (_LXX, "the Lord bringeth the counsel of the heathen to nought"),
    ("1clement-lake:59.4", "Ps 78:13"): (_LXX, "we thy people and sheep of thy pasture"),
    ("1clement-lake:59.4", "Ps 94:7"): (_LXX, "we are the people of his pasture, and the sheep of his hand"),
    ("1clement-lake:60.2", "Ps 40:2"): (_EN, "he set my feet upon a rock, and established my goings"),
    ("1clement-lake:60.3", "Ps 80:3"): (_EN, "cause thy face to shine"),
    ("1clement-lake:60.3", "Ps 80:7"): (_EN, "cause thy face to shine"),
    ("1clement-lake:60.4", "Jer 32:21"): (_EN, "with a strong hand, and with a stretched out arm"),
    ("1clement-lake:61.2", "Deut 13:18"): (_EN, "to do that which is good and pleasing before the Lord"),
    ("barnabas-lake:6.5", "Ps 18:12"): ("neither", "OCR'd 'I 18, 12': Barn. 6.6 quotes Ps 118:12, they compassed me about like bees"),
    ("barnabas-lake:12.10", "Ps 110:1"): (_EN, "the Lord said unto my Lord, sit thou at my right hand"),
    ("barnabas-lake:15.1", "Ps 23:4"): (_LXX, "clean hands and a pure heart"),
    ("barnabas-lake:19.9", "Ps 17:8"): (_EN, "the apple of the eye"),
    ("barnabas-lake:20.2", "Ps 4:2"): (_EN, "ye love vanity, and seek after leasing"),
    ("didache-lake:3.8", "Ps 36:11"): (_LXX, "the meek shall inherit the earth"),
    ("didache-lake:5.2", "Ps 4:2"): (_EN, "ye love vanity, and seek after leasing"),
    ("diognetus-lake:3.3", "Ps 146:6"): (_EN, "which made heaven, and earth, the sea"),
    ("hermas-lake:Vis.1.1.6", "Ps 123:1"): (_EN, "thou that dwellest in the heavens"),
    ("hermas-lake:Vis.1.3.3", "Ps 58:6"): (_LXX, "the God of hosts (ὁ θεὸς τῶν δυνάμεων)"),
    ("hermas-lake:Vis.1.3.4", "Ps 135:6"): (_LXX, "that stretched out the earth above the waters"),
    ("hermas-lake:Vis.2.1.2", "Ps 85:9"): (_LXX, "and shall glorify thy name"),
    ("hermas-lake:Vis.2.1.2", "Ps 85:12"): (_LXX, "I will glorify thy name for evermore"),
    ("hermas-lake:Vis.2.2.6", "Ps 15:2"): (_EN, "he that worketh righteousness"),
    ("hermas-lake:Vis.2.3.2", "Ps 106:3"): (_EN, "he that doeth righteousness at all times"),
    ("hermas-lake:Vis.2.3.2", "Ps 15:2"): (_EN, "he that walketh uprightly, and worketh righteousness"),
    ("hermas-lake:Vis.3.9.8", "Ps 47:2"): (_EN, "a great King"),
    ("hermas-lake:Vis.4.1.3", "Ps 99:3"): (_EN, "thy great and terrible name"),
    ("hermas-lake:Vis.4.2.1", "Ps 19:5"): (_EN, "as a bridegroom coming out of his chamber"),
    ("hermas-lake:Vis.4.2.4", "Ps 62:7"): (_EN, "in God is my salvation"),
    ("hermas-lake:Vis.4.2.4", "Dan 6:22"): (_EN, "my God hath sent his angel"),
    ("hermas-lake:Mand.10.1.6", "Ps 111:10"): (_EN, "the fear of the Lord is the beginning of wisdom"),
    ("hermas-lake:Mand.12.3.1", "Ps 15:2"): (_EN, "worketh righteousness, and speaketh the truth"),
    ("hermas-lake:Mand.12.4.2", "Ps 8:7"): (_LXX, "thou hast put all things under his feet"),
    ("hermas-lake:Mand.12.6.2", "Ps 15:2"): (_EN, "worketh righteousness"),
    ("hermas-lake:Sim.1.1.7", "Ps 103:18"): (_EN, "to those that remember his commandments to do them"),
    ("hermas-lake:Sim.6.1.1", "Ps 119:1"): (_EN, "blessed are the undefiled, who walk in the law"),
    ("hermas-lake:Sim.6.3.6", "Ps 51:10"): (_EN, "create in me a clean heart"),
    ("hermas-lake:Sim.6.3.6", "Ps 62:12"): (_EN, "thou renderest to every man according to his work"),
    ("hermas-lake:Sim.9.18.5", "Ps 99:3"): (_EN, "thy great and terrible name"),
    ("ignatius-lake:Eph.15.1", "Ps 33:9"): (_EN, "he spake, and it was done"),
    ("ignatius-lake:Eph.15.1", "Ps 143:5"): ("neither", "probably Ps 148:5, he commanded and they were created: an OCR digit"),
    ("martyrdom-polycarp-lake:2.3", "Isa 64:4"): (_EN, "neither hath the eye seen"),
    ("polycarp-phil-lake:12.1", "Ps 4:5"): (_LXX, "be ye angry, and sin not"),
}

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
    if isinstance(end, tuple):
        return f"{book} {ch}:{v}-{end[0]}:{end[1]}"
    return f"{book} {ch}" + (f":{v}" if v else "") + (f"-{end}" if end else "")


def resolve(ref, ctx, uid=None):
    """The link fields for one reference, in unit `uid`."""
    corpus, book, ch, v, end = ref
    out = {"ref": printed(ref), "corpus": corpus}
    if v is None:
        return {**out, "resolved": False, "why": "cites a whole chapter, not a verse"}

    def one(verse, ch=ch):
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
            if r["target"] == direct:
                return r
            # Both numberings have the verse and name different ones: LAKE_OT
            # says which Lake meant where it has been read; else the English.
            reading, why = LAKE_OT.get((uid, printed(ref)), (None, None))
            if reading == "lxx":
                return {**r, "alt_target": direct, "numbering": "lxx", "why_numbering": f"read: {why}"}
            if reading == "neither":
                return {"resolved": False, "candidates": [r["target"], direct],
                        "why": f"neither numbering's verse is the passage: {why}"}
            return {"resolved": True, "target": direct, "alt_target": r["target"], "numbering": "english",
                    "why_numbering": f"read: {why}" if reading else
                    "unread: both numberings have the verse; the English is Lake's usual one"}
        if r.get("why", "").startswith("no such verse"):
            return {"resolved": True, "target": direct, "numbering": "english",
                    "why_numbering": "Brenton's Septuagint has no such verse; the English numbering fits"}
        return r

    r = one(v)
    out.update({k: r[k] for k in ("resolved", "target", "spans", "alt_target", "candidates", "numbering",
                                  "why_numbering", "why") if k in r})
    if r.get("resolved") and isinstance(end, tuple):
        last = one(end[1], end[0])
        if last.get("resolved"):
            out["through"] = last["target"]
    elif r.get("resolved") and end and end > v:
        last = one(end)
        if last.get("resolved"):
            out["through"] = last["target"]
    if corpus == "lxx" and out.get("numbering") != "english" and "candidates" not in out:
        out["via"] = "brenton-kjv"
    return out


def resolve_note(label, urns, ctx, uid=None):
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
        links.append({"label": label, "cts": hit, **resolve(ref, ctx, uid),
                      "source": "label+urn" if hit else "label"})
    for u, p, err in parsed:
        if u in used:
            continue
        if p is None:
            if u and lrefs:
                continue              # a broken URN where the label already says it
            links.append({"label": label, "cts": u, "resolved": False, "why": err, "source": "urn"})
        elif not lrefs:
            links.append({"label": label, "cts": u, **resolve(p, ctx, uid), "source": "urn"})
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
