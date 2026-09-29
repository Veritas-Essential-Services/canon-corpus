#!/usr/bin/env python3
"""versification.py -- every Septuagint verse traced to its KJV equivalent.

The standard is STEPBible's TVTMS (Translators Versification Traditions with
Methodology for Standardisation, Tyndale House, CC BY 4.0): one row per verse
where the English, Hebrew, Latin and Greek traditions part company, each row
saying which verse it is in "Standard" (English) numbering, and each carrying
TESTS ("Gen.5:31=Last", "Gen.6:1>Gen.6:2") that tell which pattern a
PARTICULAR Bible follows. This module does what TVTMS is designed for: it
runs those tests against a real Bible -- Swete's Cambridge Septuagint
(1887-1894, the edition LSJ cites; First1KGreek TEI, CC BY-SA 4.0) -- to put
each Swete verse on the Standard number, then runs them against the KJV
(data/greppable/kjv.tsv) to turn Standard numbers into KJV ones.

    python3 pipeline/versification.py --fetch   # TVTMS + First1KGreek's Swete, pinned (gitignored)
    python3 pipeline/versification.py           # write data/versification/lxx-kjv.tsv (COMMITTED)
    python3 pipeline/versification.py --check   # the committed map is what the pinned sources give

The committed map is all that consumers need (lxx_to_kjv() reads it; the
sources are only needed to rebuild it). One row per Swete verse:

    lxx       Swete's own number, book names as lexica.LXX_WORK uses them (Ps.22.1)
    kjv       the KJV verse(s) holding that text, space-separated (Ps.23.1), or empty
    relation  same | renumbered | several (one Greek verse = several KJV verses) |
              part (the Greek verse is part of a KJV verse) | title (a Psalm title,
              which the KJV prints unnumbered) | not-in-kjv (a book or addition the
              KJV's 66 books do not have) | unmatched (TVTMS rows exist for the
              verse but none of their tests fit Swete: numbering assumed unchanged,
              and said so)
    tvtms     the TVTMS action(s) that applied, or "" where no row concerns the verse
"""
import collections, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
SRC = os.path.join(ROOT, "data", "corpus", "versification")
SWETE = os.path.join(ROOT, "data", "corpus", "first1k-lxx")
OUT = os.path.join(ROOT, "data", "versification")
MAP = os.path.join(OUT, "lxx-kjv.tsv")
KJV = os.path.join(ROOT, "data", "greppable", "kjv.tsv")
TVTMS_URL = ("https://raw.githubusercontent.com/STEPBible/STEPBible-Data/{commit}/Versification/"
             "TVTMS%20-%20Translators%20Versification%20Traditions%20with%20Methodology%20for%20"
             "Standardisation%20for%20Eng%2BHeb%2BLat%2BGrk%2BOthers%20-%20STEPBible.org%20CC%20BY.txt")
PINS = {"tvtms": "master", "first1kgreek": "8ee111eb44ecef4120c844e10749178d95d1f30c"}

# TVTMS book codes -> the OSIS names the corpus uses (kjv:Gen.1.1)
OSIS = {"Gen": "Gen", "Exo": "Exod", "Lev": "Lev", "Num": "Num", "Deu": "Deut", "Jos": "Josh",
        "Jdg": "Judg", "Rut": "Ruth", "1Sa": "1Sam", "2Sa": "2Sam", "1Ki": "1Kgs", "2Ki": "2Kgs",
        "1Ch": "1Chr", "2Ch": "2Chr", "Ezr": "Ezra", "Neh": "Neh", "Est": "Esth", "Job": "Job",
        "Psa": "Ps", "Pro": "Prov", "Ecc": "Eccl", "Sng": "Song", "Isa": "Isa", "Jer": "Jer",
        "Lam": "Lam", "Ezk": "Ezek", "Dan": "Dan", "Hos": "Hos", "Jol": "Joel", "Amo": "Amos",
        "Oba": "Obad", "Jon": "Jonah", "Mic": "Mic", "Nam": "Nah", "Hab": "Hab", "Zep": "Zeph",
        "Hag": "Hag", "Zec": "Zech", "Mal": "Mal",
        "Mat": "Matt", "Mrk": "Mark", "Luk": "Luke", "Jhn": "John", "Act": "Acts", "Rom": "Rom",
        "1Co": "1Cor", "2Co": "2Cor", "Gal": "Gal", "Eph": "Eph", "Php": "Phil", "Col": "Col",
        "1Th": "1Thess", "2Th": "2Thess", "1Ti": "1Tim", "2Ti": "2Tim", "Tit": "Titus",
        "Phm": "Phlm", "Heb": "Heb", "Jas": "Jas", "1Pe": "1Pet", "2Pe": "2Pet", "1Jn": "1John",
        "2Jn": "2John", "3Jn": "3John", "Jud": "Jude", "Rev": "Rev"}

# Swete's books in First1KGreek: (folder, file, TVTMS code or None, the corpus's LXX name).
# By TITLE, never by number: First1K's tlg035 is the Psalms of Solomon, LSJ's is Wisdom.
# Where First1K holds two editions, the Swete one (Isaiah grc1 1905; Sirach grc2 1896).
BOOKS = [("tlg001", "grc1", "Gen", "Gen"), ("tlg002", "grc1", "Exo", "Exod"), ("tlg003", "grc1", "Lev", "Lev"),
         ("tlg004", "grc1", "Num", "Num"), ("tlg005", "grc1", "Deu", "Deut"), ("tlg006", "grc1", "Jos", "Josh"),
         ("tlg008", "grc1", "Jdg", "Judg"), ("tlg010", "grc1", "Rut", "Ruth"), ("tlg011", "grc1", "1Sa", "1Sam"),
         ("tlg012", "grc1", "2Sa", "2Sam"), ("tlg013", "grc1", "1Ki", "1Kgs"), ("tlg014", "grc1", "2Ki", "2Kgs"),
         ("tlg015", "grc1", "1Ch", "1Chr"), ("tlg016", "grc1", "2Ch", "2Chr"), ("tlg017", "grc1", None, "1Esd"),
         ("tlg018", "grc1", "EZRNEH", "2Esd"), ("tlg019", "grc1", "Est", "Esth"), ("tlg020", "grc1", None, "Jdt"),
         ("tlg021", "grc1", None, "Tob"), ("tlg023", "grc1", None, "1Macc"), ("tlg024", "grc1", None, "2Macc"),
         ("tlg025", "grc1", None, "3Macc"), ("tlg026", "grc1", None, "4Macc"), ("tlg027", "grc1", "Psa", "Ps"),
         ("tlg028", "grc1", None, "Odes"), ("tlg029", "grc1", "Pro", "Prov"), ("tlg031", "grc1", "Sng", "Song"),
         ("tlg032", "grc1", "Job", "Job"), ("tlg033", "grc1", None, "Wis"), ("tlg034", "grc2", None, "Sir"),
         ("tlg035", "grc1", None, "PsSol"), ("tlg036", "grc1", "Hos", "Hos"), ("tlg037", "grc1", "Amo", "Amos"),
         ("tlg038", "grc1", "Mic", "Mic"), ("tlg039", "grc1", "Jol", "Joel"), ("tlg040", "grc1", "Oba", "Obad"),
         ("tlg041", "grc1", "Jon", "Jonah"), ("tlg042", "grc1", "Nam", "Nah"), ("tlg043", "grc1", "Hab", "Hab"),
         ("tlg044", "grc1", "Zep", "Zeph"), ("tlg045", "grc1", "Hag", "Hag"), ("tlg046", "grc1", "Zec", "Zech"),
         ("tlg047", "grc1", "Mal", "Mal"), ("tlg048", "grc1", "Isa", "Isa"), ("tlg049", "grc1", "Jer", "Jer"),
         ("tlg050", "grc1", None, "Bar"), ("tlg051", "grc1", "Lam", "Lam"), ("tlg052", "grc1", None, "EpJer"),
         ("tlg053", "grc1", "Ezk", "Ezek"), ("tlg054", "grc1", None, "SusOG"), ("tlg055", "grc1", None, "Sus"),
         ("tlg056", "grc1", "Dan", "DanOG"), ("tlg057", "grc1", "Dan", "Dan"), ("tlg058", "grc1", None, "BelOG"),
         ("tlg059", "grc1", None, "Bel")]
GREEK_FAMILY = {"Greek", "Greek2", "Greek3", "GreekUndivided", "GreekIntegrated", "GrkTitleSeparate",
                "GrkTitleMerged", "Greek2Undivided", "GreekIntegrated2", "GreekUndivided2",
                "GrkTitleSeparate2", "Greek2-NETS", "Greek+NRSV", "AllBibles"}
_RE_REF = re.compile(r"^([1-4]?[A-Za-z]{2,3})\.(\w+):(\w+)(?:[.!](\w+))?$")


class _Ref:
    """RE_REF.match with the book code normalised (TVTMS writes PSA.118:176 once)."""
    @staticmethod
    def match(s):
        m = _RE_REF.match(s)
        return None if m is None else _Norm(m)


class _Norm:
    def __init__(self, m):
        b = m.group(1)
        self._g = (b[0] + b[1:].lower() if b[1:].isupper() and b.isalpha() else b,) + m.groups()[1:]

    def groups(self):
        return self._g


RE_REF = _Ref


# ---------------------------------------------------------------- a Bible, as TVTMS's tests see it
class Bible:
    """verse -> word count, and each chapter's last verse. Keys are TVTMS
    refs ('Psa.3:1'); a book's chapters and verses as the edition numbers them."""
    def __init__(self, verses, text_before_v1=False):
        self.words = verses                                # {(code, ch, v): words}
        # Swete numbers a Psalm's title as verse 1, so no text ever stands before v.1
        self.text_before_v1 = text_before_v1
        self.last = {}
        for (b, c, v) in verses:
            if v.isdigit() and (b, c) not in self.last or v.isdigit() and int(v) > int(self.last[(b, c)]):
                self.last[(b, c)] = v

    def exists(self, b, c, v, sub=None):
        if (b, c, v) not in self.words:
            return False
        return sub in (None, "0", "")     # no edition here carries subverses

    def test(self, t):
        """True / False, or None when the test is of a kind this cannot judge."""
        t = t.strip()
        if not t:
            return True
        m = re.fullmatch(r"([1-4]?[A-Za-z]{2,3})\.(\w+):TextBeforeV1=(Exist|NotExist)", t, re.I)
        if m:
            if self.text_before_v1 is None:
                return None
            return self.text_before_v1 if m.group(3).lower() == "exist" else not self.text_before_v1
        m = re.fullmatch(r"(\S+?)=(Exist|NotExist|Last)", t)
        if m:
            r = RE_REF.match(m.group(1))
            if not r:
                return None
            b, c, v, sub = r.groups()
            if m.group(2) == "Last":
                return self.last.get((b, c)) == v
            e = self.exists(b, c, v, sub)
            return e if m.group(2) == "Exist" else not e
        m = re.fullmatch(r"(\S+?)(\*2)?([<>])(\S+?)(\*2)?", t)
        if m:
            a, b = RE_REF.match(m.group(1)), RE_REF.match(m.group(4))
            if not a or not b:
                return None
            wa, wb = self.words.get(a.groups()[:3]), self.words.get(b.groups()[:3])
            if wa is None or wb is None:
                return False
            wa, wb = wa * (2 if m.group(2) else 1), wb * (2 if m.group(5) else 1)
            return wa < wb if m.group(3) == "<" else wa > wb
        return None


def tvtms_rows(path):
    """[(types, source, standard, action, tests)] from the Expanded section."""
    lines = open(path, encoding="utf-8-sig").read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("#DataStart(Expanded)"))
    end = next(i for i, l in enumerate(lines) if l.startswith("#DataEnd(Expanded)"))
    out = []
    for l in lines[start + 1:end]:
        c = l.split("\t")
        if len(c) < 4 or not c[0].strip() or c[0].startswith(("SourceType", "'=", "#")):
            continue
        types = {t.strip() for t in c[0].split("+")}
        tests = [t for t in (c[8].split("&") if len(c) > 8 else []) if t.strip()]
        out.append((types, c[1].strip(), c[2].strip(), c[3].strip(), tests))
    return out


def standard_refs(s, book):
    """'Gen.5:32; 6:1' / 'Gen.2:25-3:1' / 'Psa.3:Title' -> [(code, ch, v, part)],
    part True for a subverse. A range is expanded verse by verse later (needs counts)."""
    out = []
    cur_b = book
    for piece in re.split(r";\s*", s):
        piece = piece.strip()
        if not piece or piece.startswith("Absent"):
            continue
        m = re.match(r"^(?:([1-4]?[A-Za-z]{2,3})\.)?(\w+):(\w+)(?:[.!](\w+))?(?:-(?:(\w+):)?(\w+)(?:[.!]\w+)?)?$", piece)
        if not m:
            continue
        b, c, v, sub, c2, v2 = m.groups()
        cur_b = b or cur_b
        out.append((cur_b, c, v, bool(sub and sub != "0"), c2 or (c if v2 else None), v2))
    return out


def swete_bible():
    """(Bible over TVTMS codes, [(lxx_name, ch, v, code_or_None, words)]) in Swete's order."""
    import cts
    words, order = {}, []
    base = os.path.join(SWETE, "data", "tlg0527")
    for folder, ed, code, name in BOOKS:
        path = os.path.join(base, folder, f"tlg0527.{folder}.1st1K-{ed}.xml")
        if not os.path.exists(path):
            raise SystemExit(f"Swete is not fetched: {path} (versification.py --fetch)")
        _, leaves = cts.walk(path)
        for refs, text in leaves:
            if len(refs) != 2 or not text:
                continue
            c, v = refs
            w = len(text.split())
            tcode, tc = code, c
            if code == "EZRNEH":           # Esdras B = Ezra 1-10 + Nehemiah 1-13
                if c.isdigit():
                    tcode, tc = ("Ezr", c) if int(c) <= 10 else ("Neh", str(int(c) - 10))
                else:
                    tcode = None
            if tcode:
                words[(tcode, tc, v)] = w
            order.append((name, c, v, tcode, tc))
    return Bible(words), order


def kjv_bible():
    words = {}
    inv = {o: t for t, o in OSIS.items()}
    with open(KJV, encoding="utf-8") as f:
        next(f)
        for line in f:
            vid, text = line.rstrip("\n").split("\t", 1)
            _, b, c, v = vid.split(".") if vid.count(".") == 3 else (None, *vid.split(":")[1].split("."))
            words[(inv[b], c, v)] = len(re.sub(r"[\[\]]", "", text).split())
    return Bible(words)


SUBVERSE_TEST = re.compile(r"^\S+:\w+[.!]\w+=(Exist|NotExist)$")
SOFT_TEST = re.compile(r"[<>]")
FAMILY_RANK = ["Greek", "GreekUndivided", "Greek2", "Greek2Undivided", "GreekIntegrated", "GrkTitleSeparate"]


def resolve(bible, rows_by_src, code, c, v, families=None):
    """-> (standard refs, actions, state) for one verse of `bible`.
    state: "row" (a row's tests all passed), "soft" (every STRUCTURAL test of
    a row passed -- exists / last verse of the chapter -- while its subverse
    tests, which an edition printing whole verses cannot show, were set aside
    and its word-count comparisons, which are heuristics, decided between
    rows), "none" (no row concerns the verse: its number is Standard's), or
    "unmatched" (rows exist and none fits: the number is assumed unchanged)."""
    rows = rows_by_src.get(f"{code}.{c}:{v}", [])
    if not rows:
        return [(code, c, v, False, None, None)], [], "none"
    strict, soft = [], []
    for types, src, std, action, tests in rows:
        if families is not None and not (types & families):
            continue
        hard_ok, soft_score, strict_ok = True, 0, True
        for t in tests:
            r = bible.test(t)
            is_sub, is_soft = bool(SUBVERSE_TEST.match(t.strip())), bool(SOFT_TEST.search(t))
            if r is not True:
                strict_ok = False
            if is_sub:
                continue
            if is_soft:
                soft_score += 1 if r is True else -1 if r is False else 0
            elif r is not True:
                hard_ok = False
        if strict_ok:
            strict.append((std, action))
        elif hard_ok:
            rank = min((FAMILY_RANK.index(t) for t in types if t in FAMILY_RANK), default=len(FAMILY_RANK))
            soft.append((-soft_score, rank, std, action))
    if strict:
        chosen, state = strict, "row"
    elif soft:
        soft.sort(key=lambda x: (x[0], x[1]))
        chosen, state = [(soft[0][2], soft[0][3])], "soft"
    else:
        return [(code, c, v, False, None, None)], [], "unmatched"
    std, actions = [], []
    for s_, a in chosen:
        for r in standard_refs(s_, code):
            if r not in std:
                std.append(r)
        if a not in actions:
            actions.append(a + (" (soft)" if state == "soft" else ""))
    return std, actions, state


def expand(refs, verses_in):
    """[(code, ch, v, part, c2, v2)] -> [(code, ch, v, part)], ranges expanded
    over the chapters' verse counts (verses_in: {(code, ch): last verse})."""
    out = []
    for code, c, v, part, c2, v2 in refs:
        if not v2 or not (c.isdigit() and v.isdigit() and v2.isdigit()):
            out.append((code, c, v, part))
            continue
        ch, vv = int(c), int(v)
        end_c, end_v = int(c2), int(v2)
        while (ch, vv) <= (end_c, end_v):
            out.append((code, str(ch), str(vv), part))
            last = verses_in.get((code, str(ch)))
            if last and vv >= int(last):
                ch, vv = ch + 1, 1
            else:
                vv += 1
            if len(out) > 400:
                break
    return out


def build():
    rows = tvtms_rows(os.path.join(SRC, "tvtms.txt"))
    by_src = collections.defaultdict(list)
    for r in rows:
        by_src[r[1]].append(r)
    swete, order = swete_bible()
    kjv = kjv_bible()
    # Standard -> KJV: the KJV's own rows, tested against the KJV, inverted
    std_to_kjv = collections.defaultdict(list)
    for (b, c, v) in kjv.words:
        if b == "Psa":
            continue
        std, _, state = resolve(kjv, by_src, b, c, v)
        if state in ("row", "soft"):
            for (sb, sc, sv, part) in expand(std, kjv.last):
                std_to_kjv[(sb, sc, sv)].append((b, c, v))
    out, stats = [], collections.Counter()
    for name, c, v, code, tc in order:
        lxx = f"{name}.{c}.{v}"
        if code is None:
            out.append((lxx, "", "not-in-kjv", "")); stats["not-in-kjv"] += 1
            continue
        std, actions, state = resolve(swete, by_src, code, tc, v, GREEK_FAMILY)
        if state in ("unmatched", "soft"):
            # The tests identify the pattern whatever its label: Swete's Daniel 3
            # runs to v.100, which TVTMS files under Latin (3:98-100 = KJV 4:1-3).
            # A strict pass in any tradition beats a Greek row taken on soft evidence.
            any_std, any_actions, any_state = resolve(swete, by_src, code, tc, v, None)
            if any_state == "row" or (any_state == "soft" and state == "unmatched"):
                std, actions, state = any_std, [a + " (another tradition's pattern)" for a in any_actions], any_state
        if any(r[2].lower() == "title" for r in std):
            out.append((lxx, "", "title", "; ".join(actions))); stats["title"] += 1
            continue
        kjv_refs, part = [], False
        for (sb, sc, sv, p) in expand(std, kjv.last):
            part = part or p
            for kb, kc, kv in (std_to_kjv.get((sb, sc, sv)) or [(sb, sc, sv)]):
                osis = f"{OSIS[kb]}.{kc}.{kv}" if kb in OSIS else None
                if osis and (kb, kc, kv) in kjv.words and osis not in kjv_refs:
                    kjv_refs.append(osis)
        if not kjv_refs:
            rel = "not-in-kjv"
        elif state == "unmatched":
            rel = "unmatched"
        elif part:
            rel = "part"
        elif len(kjv_refs) > 1:
            rel = "several"
        elif kjv_refs[0] == f"{OSIS.get(code, name)}.{tc}.{v}":
            rel = "same"
        else:
            rel = "renumbered"
        stats[rel] += 1
        out.append((lxx, " ".join(kjv_refs), rel, "; ".join(actions)))
    return out, stats


def validate(rows):
    """An independent check of the map: PROPER NAMES. A Swete verse naming
    Abraham or Israel should land on a KJV verse naming them too. Greek names
    (capitalised words, a few titles of God left out) are reduced to their
    first two consonants, as are the KJV verse's capitalised words; for every
    verse the map MOVES, does the verse it names share more names than the
    KJV verse of the same number? A measurement, not an input."""
    import cts
    from betacode import headword_key
    kjvt = {}
    with open(KJV, encoding="utf-8") as f:
        next(f)
        for line in f:
            k, t = line.rstrip("\n").split("\t", 1)
            kjvt[k[4:]] = t
    greek = {}
    base = os.path.join(SWETE, "data", "tlg0527")
    for folder, ed, code, name in BOOKS:
        if code is None:
            continue
        _, leaves = cts.walk(os.path.join(base, folder, f"tlg0527.{folder}.1st1K-{ed}.xml"))
        for refs, t in leaves:
            if len(refs) == 2:
                greek[f"{name}.{refs[0]}.{refs[1]}"] = t
    TR = str.maketrans("αβγδεζηθικλμνξοπρστυφχψω", "abgdezetiklmnxoprstufksw")
    skip = {"κυριοσ", "θεοσ", "κυριε", "θεε", "κυριου", "θεου", "κυριω", "θεω", "κυριον", "θεον"}
    def gkeys(t):
        out = set()
        for w in re.findall(r"[\u0391-\u03a9\u1f08-\u1f0f\u1f18-\u1f1d\u1f28-\u1f2f\u1f38-\u1f3f"
                            r"\u1f48-\u1f4d\u1f59-\u1f5f\u1f68-\u1f6f\u1fb8-\u1fbc\u1fc8-\u1fcc"
                            r"\u1fd8-\u1fdb\u1fe8-\u1fec\u1ff8-\u1ffc][\w\u0300-\u036f]+", t):
            k = headword_key(w)
            if k in skip or len(k) < 3:
                continue
            c = re.sub(r"[aeiouhw]", "", k.translate(TR))
            if len(c) >= 2:
                out.add(c[:2])
        return out
    def ekeys(t):
        stop = {"And", "The", "For", "But", "Then", "Now", "LORD", "God", "Lord", "Thou", "Thy", "Thee",
                "Behold", "When", "Wherefore", "Therefore", "Let", "Who", "What", "Why", "How", "Yea", "Also"}
        out = set()
        for w in re.findall(r"\b[A-Z][a-z]+", t):
            if w in stop:
                continue
            e = w.lower().replace("ph", "f").replace("ch", "k").replace("th", "t").replace("c", "k").replace("j", "i")
            c = re.sub(r"[aeiouhyw]", "", e)
            if len(c) >= 2:
                out.add(c[:2])
        return out
    moved = better = worse = tie = 0
    against = []
    for lxx, kjv, rel, _ in rows:
        if rel not in ("renumbered", "several") or lxx not in greek:
            continue
        g = gkeys(greek[lxx])
        if not g:
            continue
        got = max((len(g & ekeys(kjvt.get(k, ""))) for k in kjv.split()), default=0)
        base_ = len(g & ekeys(kjvt.get(lxx, "")))
        moved += 1
        better += got > base_
        worse += got < base_
        tie += got == base_
        if got < base_:
            against.append(f"{lxx} -> {kjv}")
    return {"moved verses with a proper name": moved, "the map's verse shares more names": better,
            "the same-number verse shares more names": worse, "no difference": tie,
            "the verses where names favour the same number (read these)": against}


def dump(rows):
    return "lxx\tkjv\trelation\ttvtms\n" + "".join("\t".join(r) + "\n" for r in rows)


_MAP = None


def lxx_to_kjv(ref):
    """'Ps.22.1' -> (['Ps.23.1'], 'renumbered'); unknown -> ([], None). Reads the committed map."""
    global _MAP
    if _MAP is None:
        _MAP = {}
        if os.path.exists(MAP):
            with open(MAP, encoding="utf-8") as f:
                next(f)
                for line in f:
                    lxx, kjv, rel, _ = line.rstrip("\n").split("\t")
                    _MAP[lxx] = (kjv.split() if kjv else [], rel)
    return _MAP.get(ref, ([], None))


def fetch():
    os.makedirs(SRC, exist_ok=True)
    p = os.path.join(SRC, "tvtms.txt")
    if not os.path.exists(p):
        import urllib.request
        with urllib.request.urlopen(TVTMS_URL.format(commit=PINS["tvtms"]), timeout=120) as r, open(p + ".tmp", "wb") as f:
            f.write(r.read())
        os.replace(p + ".tmp", p)
    if not os.path.isdir(os.path.join(SWETE, ".git")):
        subprocess.run(["git", "clone", "--filter=blob:none", "--sparse", "--depth", "1",
                        "https://github.com/OpenGreekAndLatin/First1KGreek", SWETE], check=True)
        subprocess.run(["git", "-C", SWETE, "sparse-checkout", "set", "data/tlg0527"], check=True)


def main():
    if "--fetch" in sys.argv:
        fetch()
    rows, stats = build()
    text = dump(rows)
    if "--check" in sys.argv:
        same = os.path.exists(MAP) and open(MAP, encoding="utf-8", newline="").read() == text
        print("CHECK PASSED: lxx-kjv.tsv byte-identical." if same else "CHECK FAILED: the map differs.")
        sys.exit(0 if same else 1)
    os.makedirs(OUT, exist_ok=True)
    with open(MAP + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(MAP + ".tmp", MAP)
    v = validate(rows)
    meta = {"rows": len(rows), "relations": dict(sorted(stats.items())), "check_against_brenton": v,
            "sources": {"tvtms": {"what": "STEPBible TVTMS versification traditions", "license": "CC BY 4.0",
                                  "attribution": "Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)",
                                  "source_url": "https://github.com/STEPBible/STEPBible-Data"},
                        "swete": {"what": "Swete, The Old Testament in Greek (1887-1894), First1KGreek TEI",
                                  "license": "CC BY-SA 4.0 (markup); text public domain",
                                  "source_url": "https://github.com/OpenGreekAndLatin/First1KGreek",
                                  "commit": PINS["first1kgreek"]},
                        "kjv": "data/greppable/kjv.tsv (this repo)"},
            "license": "CC BY-SA 4.0 (built from CC BY and CC BY-SA sources); facts about verse numbering"}
    with open(os.path.join(OUT, "lxx-kjv.meta.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{len(rows):,} Swete verses -> {MAP}")
    for k, n in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k:<12} {n:>6,}")
    print("  check:", v)


if __name__ == "__main__":
    main()
