#!/usr/bin/env python3
"""A second, fully public-domain Latin witness of the Summa: the editio altera
Romana (Rome: Forzani, 1894, 6 vols.), from the Internet Archive's OCR text
layer, cut into the same key as pipeline/build_aquinas_st.py.

    python3 pipeline/aquinas_st_1894.py --fetch   # the five text volumes' djvu.txt
    python3 pipeline/aquinas_st_1894.py           # parse; report coverage against the key

Used by build_aquinas_st.py (parse_1894). The text is UNPROOFREAD OCR and the
book's honesty field says so. Its cut is checked part by part against the
Leonine (Corpus Thomisticum) where both exist: a part whose words do not
overlap the Leonine's is flagged, never silently kept as aligned.

Volumes (archive.org ids): 1 = I, 2 = I-II, 3 = II-II, 4 = III,
5 = Supplement; vol. 6 is the index and is not used.
"""
import os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "data", "corpus", "aquinas-1894")
VOLS = {"I": "summatheologicae0001thom", "I-II": "summatheologicae0002thom",
        "II-II": "summatheologicae0003thom", "III": "summatheologicae0004thom",
        "Suppl": "summatheologicae0005thom"}
REPAIRS = []
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}

ORDW = ("primum secundum tertium quartum quintum sextum septimum octavum nonum decimum "
        "undecimum duodecimum decimumtertium decimumquartum decimumquintum decimumsextum").split()
ORD = {w: i + 1 for i, w in enumerate(ORDW)}

def roman(s):
    s = s.upper().replace("L", "L")
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    if not s or any(c not in vals for c in s):
        return None
    n = 0
    for i, c in enumerate(s):
        v = vals[c]
        n += -v if i + 1 < len(s) and vals[s[i + 1]] > v else v
    return n

def fetch():
    os.makedirs(DIR, exist_ok=True)
    for part, ident in VOLS.items():
        dest = os.path.join(DIR, ident + ".txt")
        if os.path.exists(dest) and os.path.getsize(dest) > 100000:
            continue
        url = f"https://archive.org/download/{ident}/{ident}_djvu.txt"
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600).read()
        with open(dest + ".tmp", "wb") as f:
            f.write(data)
        os.replace(dest + ".tmp", dest)
        print(f"{part}: {len(data):,} bytes")

RE_HEAD = re.compile(r"^(\d+\s+)?QUAESTIO\s+\S+\s+ARTICULUS\s+\S+(\s+\S{1,4})?$")
RE_Q = re.compile(r"^QUAESTIO\s+([IVXLCl1]+)\.?$")
RE_A = re.compile(r"^ARTICULUS\s+([IVXLCl1]+|UNICUS)\b")
RE_PRAET = re.compile(r"^\W{0,3}\d{0,2}\W{0,3}\s*Praeterea\b")
RE_SC = re.compile(r"^\W{0,3}(Sed\s+contra|In\s+contrarium)\b")
RE_CO = re.compile(r"^\W{0,3}Respondeo\b")
RE_AD = re.compile(r"^\W{0,3}Ad\s+(\w+)(?:\s*,\s*et\s+\w+)?\s+(?:ergo\s+)?(?:dicendum|patet|sufficit|dicendum)", re.I)
RE_PROC = re.compile(r"^\W{0,3}Ad\s+(\w+(?:\s+\w+)?)\s+sic\s+proceditur", re.I)
RE_PATET = re.compile(r"^\W{0,3}(?:Et\s+)?(?:per\s+hoc\s+|sic\s+|ex\s+hoc\s+)?patet\s+(?:etiam\s+)?(?:responsio|solutio)\s+ad\s+(\w+)", re.I)

def paragraphs(path):
    """OCR text -> paragraphs: spaces collapsed, running heads and folios
    dropped, line-end hyphenation (the ¬ sign, or '-' before a lower-case
    letter) rejoined, and a paragraph broken by a page rejoined to the one
    before when it does not start with a capital."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    paras, cur = [], []
    for line in raw.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            if cur:
                paras.append(cur)
                cur = []
            continue
        if re.fullmatch(r"\d{1,4}|\W{1,3}|\d{1,4}\W?", line) or RE_HEAD.match(line):
            if cur:
                paras.append(cur)
                cur = []
            continue
        cur.append(line)
    if cur:
        paras.append(cur)
    out = []
    for lines in paras:
        text = ""
        for ln in lines:
            if text.endswith("¬"):
                text = text[:-1] + ln
            elif re.search(r"[a-z]-$", text) and re.match(r"[a-z]", ln):
                text = text[:-1] + ln
            else:
                text = (text + " " + ln).strip()
        out.append(text)
    merged = []
    for t in out:
        if merged and (merged[-1].endswith("¬") or (re.match(r"[a-z,;:]", t) and not merged[-1].endswith("."))):
            merged[-1] = merged[-1].rstrip("¬") + ("" if merged[-1].endswith("¬") else " ") + t
        else:
            merged.append(t)
    return merged

def parse_volume(part, path):
    paras = paragraphs(path)
    first = next((i for i, p in enumerate(paras) if "sic proceditur" in p), None)
    if first is None:
        return []
    # the volume opens with its table of questions; the text proper begins at
    # the first question's heading, which the OCR sometimes misses
    art1 = max(i for i in range(first) if RE_A.match(paras[i]))
    qh = [i for i in range(art1) if RE_Q.match(paras[i])]
    units, q, a, seg, nsc, narg = [], None, None, None, 0, 0
    cur, fresh_q = None, True
    if qh and roman(RE_Q.match(paras[qh[-1]]).group(1)) == 1:
        start = qh[-1]
    else:
        start, q = art1, 1
        cur = {"key": f"{part}.q1.pr", "text": ""}
        units.append(cur)

    def emit(key, text):
        nonlocal cur
        cur = {"key": key, "text": text}
        units.append(cur)

    for p in paras[start:]:
        if re.match(r"^(INDEX|TABULA|QUAEST\.\s*&)", p):
            break
        mq = RE_Q.match(p)
        if mq:
            n = roman(mq.group(1).replace("l", "I").replace("1", "I"))
            if n is None or not (q is None or 0 < n - q <= 2):
                n = 1 if q is None else q + 1
            q, a, seg, fresh_q = n, None, "pr", True
            emit(f"{part}.q{q}.pr", "")
            continue
        if q is None:
            continue
        ma = RE_A.match(p)
        if ma and "QUAESTIO" not in p:
            r = ma.group(1)
            n = 1 if r == "UNICUS" else roman(r.replace("l", "I").replace("1", "I"))
            if n is None or not (a is None or 0 < n - a <= 2):
                n = 1 if a is None else a + 1
            a, seg, nsc, narg = n, "title", 0, 0
            emit(f"{part}.q{q}.a{a}", "")
            continue
        # "Ad secundum sic proceditur" opens article 2 and says so in words:
        # it overrules a misread or missing ARTICULUS heading, and an article 1
        # after a later article means a QUAESTIO heading was lost.
        mp = RE_PROC.match(p)
        if mp:
            w = mp.group(1).lower().replace(" ", "")
            n = ORD.get(w) or ORD.get(w.split()[0] if " " in mp.group(1) else w)
            if n is None:
                n = ORD.get(mp.group(1).lower().split()[0])
            if n:
                if n == 1 and a is not None and not fresh_q:
                    q += 1
                    REPAIRS.append(f"{part}.q{q}: question heading not found by OCR; inferred from 'Ad primum sic proceditur'")
                if seg != "title" or n != a:
                    if seg == "title" and units and units[-1]["key"] == f"{part}.q{q if not (n == 1 and a is not None and not fresh_q) else q - 1}.a{a}":
                        title = units.pop()["text"]
                    else:
                        title = ""
                    a = n
                    emit(f"{part}.q{q}.a{a}", title)
                a, nsc, narg, seg, fresh_q = n, 0, 1, "arg1", False
                emit(f"{part}.q{q}.a{a}.arg1", p)
                continue
        akey = f"{part}.q{q}.a{a}" if a else None
        if akey is None:                           # the question's title and prologue
            cur["text"] = (cur["text"] + "\n" + p).strip()
            continue
        if seg == "title":
            # title, then the cross-references in parentheses, until the
            # objection (a single-article question opens "Deinde ... Et videtur")
            if not re.search(r"\bvidetur\b", p, re.I) or (len(p) < 160 and p.upper() == p):
                cur["text"] = (cur["text"] + "\n" + p).strip()
                continue
            narg, fresh_q = 1, False
            seg = "arg1"
            emit(f"{akey}.arg1", p)
            continue
        m = RE_AD.match(p) or RE_PATET.match(p)
        if RE_PRAET.match(p) and seg.startswith("arg"):
            narg += 1
            seg = f"arg{narg}"
            emit(f"{akey}.{seg}", p)
        elif RE_SC.match(p) and not seg.startswith("ad") and seg != "co":
            nsc += 1
            seg = f"sc{nsc}"
            emit(f"{akey}.{seg}", p)
        elif RE_CO.match(p) and seg != "co" and not seg.startswith("ad"):
            seg = "co"
            emit(f"{akey}.co", p)
        elif m and seg != "title" and (seg == "co" or seg.startswith("ad")):
            w = m.group(1).lower()
            if w in ("objecta", "obiecta", "argumenta", "ea", "id", "illud", "illa"):
                seg = "ad-sc"
            elif w in ORD:
                seg = f"ad{ORD[w]}"
            else:
                cur["text"] += "\n" + p
                continue
            emit(f"{akey}.{seg}", p)
        else:
            cur["text"] = (cur["text"] + "\n" + p).strip()
    # one sed contra per article is .sc; drop empty title rows' noise
    keys = {u["key"] for u in units}
    for u in units:
        if u["key"].endswith(".sc1") and u["key"][:-1] + "2" not in keys:
            u["key"] = u["key"][:-1]
    seen, out = {}, []
    for u in units:                      # a key met twice (OCR lost a heading): flag, keep
        k = u["key"]
        if k in seen and re.fullmatch(r"[^.]+\.q\d+\.(a\d+|pr)", k):
            continue                     # a heading read twice: its text is the same title
        if k in seen:
            seen[k] += 1
            u["key"] = f"{k}~{seen[k]}"
        else:
            seen[k] = 1
        out.append(u)
    return out

def parse_1894():
    units = []
    for part, ident in VOLS.items():
        path = os.path.join(DIR, ident + ".txt")
        if not os.path.exists(path):
            raise SystemExit(f"missing {path}: run pipeline/aquinas_st_1894.py --fetch")
        units += parse_volume(part, path)
    # The 1894 edition prints the Supplement's appendix as questions 100-102;
    # the English (and the usual citation) calls them App. I q.1-2 and App. II
    # q.1. Matched by their titles (de existentia purgatorii = App. II q.1).
    ren = {"Suppl.q100": "App2.q1", "Suppl.q101": "App1.q2", "Suppl.q102": "App1.q1"}
    for u in units:
        m = re.match(r"(Suppl\.q10[012])(?=\.)", u["key"])
        if m:
            u["key"] = ren[m.group(1)] + u["key"][m.end():]
    for u in units:
        u["links"] = []
    return units

def words(s):
    return set(w for w in re.findall(r"[a-z]{4,}", (s or "").lower().replace("j", "i").replace("v", "u")))

def overlap(a, b):
    wa, wb = words(a), words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))

if __name__ == "__main__":
    if "--fetch" in sys.argv:
        fetch()
        sys.exit(0)
    from collections import Counter
    u = parse_1894()
    print(len(u), "units;", Counter(x["key"].split(".")[0] for x in u))
