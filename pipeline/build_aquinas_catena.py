#!/usr/bin/env python3
"""The Catena Aurea, Latin and English, keyed by GOSPEL, CHAPTER and LECTIO.

    python3 pipeline/build_aquinas_catena.py           # books + parallel file + key
    python3 pipeline/build_aquinas_catena.py --check   # key byte-identical

The key is the Latin's own division: CA.Mt.5.3 = Catena in Matthaeum, cap. 5,
lectio 3. Each lectio is one stretch of the gospel (a few verses) and the
Fathers' comments on it, quoted one after another. Witnesses:
  la   Corpus Thomisticum (local only, as for the Summa: docs/AQUINAS.md).
  en   The Oxford translation (J. H. Newman, ed., 1841-45), US public domain:
       Matthew and Mark clean from CCEL (ThML); Luke and John raw Internet
       Archive OCR (pipeline/aquinas_shelf.json).
The English prints no lectio numbers. Its sections (each opens with the
verses it comments on) are placed on the lectiones by the SEQUENCE OF FATHERS
quoted in them: Jerome, Chrysostom, Gloss, Rabanus ... is a fingerprint that
survives translation. The fit is recorded per row. The committed key holds
no text: per lectio, the verses, the Fathers in order, and the fit.
"""
import difflib, hashlib, html, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CT = os.path.join(ROOT, "data", "corpus", "corpus-thomisticum")
SHELF = os.path.join(ROOT, "data", "corpus", "aquinas")
BOOKS = os.path.join(ROOT, "data", "books")
KEY_OUT = os.path.join(ROOT, "data", "aquinas", "catena-key.jsonl")
MANIFEST = os.path.join(BOOKS, "manifest.json")
GOSPELS = [  # key, CT file prefix, CT abbreviation, English files (first chapter of each)
    ("Mt", "cmt", "Mt.", [("aquinas-catena-matthew.xml", 1)]),
    ("Mc", "cmc", "Mc.", [("aquinas-catena-mark.xml", 1)]),
    ("Lc", "clc", "Lc.", [("aquinas-catena-luke-p1.txt", 1), ("aquinas-catena-luke-p2.txt", 11)]),
    ("Io", "cjo", "Io.", [("aquinas-catena-john-p1.txt", 1), ("aquinas-catena-john-p2.txt", 11)]),
]
NAMES = {"Mt": "Matthew", "Mc": "Mark", "Lc": "Luke", "Io": "John"}

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

# The Fathers, as each witness names them, to one short form. First letters
# are enough to tell them apart; the aliases cover the Latin and the
# English spellings (Hieronymus = Jerome, Beda = Bede, Pseudo-Chrys. = the
# Opus imperfectum, cited in the Latin as "Chrysostomus super Matth.").
ALIAS = {"aug": "augu", "hier": "jero", "beda": "bede", "isid": "isid", "dama": "damn", "joan": "damn",
         "orig": "orig", "theo": "theo", "aug.": "augu", "chrys": "chry", "greg": "greg", "grego": "greg",
         "nyss": "nyss", "glos": "glos", "raba": "raba", "rabn": "raba", "remi": "remi", "hila": "hila",
         "ambr": "ambr", "basi": "basi", "cyri": "cyri", "dion": "dion", "alcu": "alcu", "seve": "seve",
         "euse": "euse", "titu": "titu", "atha": "atha", "leo": "leo", "cass": "cass", "maxi": "maxi",
         "gela": "gela", "phot": "phot", "fulg": "fulg", "prud": "prud", "apol": "apol", "inno": "inno",
         "barl": "barl", "pros": "pros", "seve": "seve", "vict": "vict", "eust": "eust", "anas": "anas",
         "nest": "nest", "ammo": "ammo", "athe": "athe", "chro": "chro", "anti": "anti", "aste": "aste",
         "bern": "bern", "gemm": "gemm", "isaa": "isaa", "jose": "jose", "lact": "lact", "mart": "mart",
         "paul": "paul", "pela": "pela", "phil": "phil", "pier": "pier", "proc": "proc", "seve": "seve",
         "symm": "symm", "tert": "tert", "anse": "anse", "arnu": "arnu"}
KNOWN = set(ALIAS.values()) | {"augu"}

def father(name):
    name = re.sub(r"^pseudo-?\s*", "", name.lower())        # Pseudo-Chrys. is cited in the Latin as Chrysostomus
    k = name.replace("st.", "").strip(" .,;:")[:4]
    k = ALIAS.get(k, k)
    return k if k in KNOWN else None

# ------------------------------------------------------------ Latin (CT)
def parse_la(prefix, abbr):
    lec = {}
    rx = re.compile(r'<P TITLE="Catena in ' + re.escape(abbr) + r', cap\. (\d+) l\. (\d+)"[^>]*>(.*?)</P>', re.S)
    for f in sorted(x for x in os.listdir(CT) if x.startswith(prefix) and x.endswith(".html")):
        s = open(os.path.join(CT, f), "rb").read().decode("latin-1")
        for m in rx.finditer(s):
            c, l, inner = int(m.group(1)), int(m.group(2)), m.group(3)
            inner = re.sub(r'^\s*<A NAME="\d+">\s*<SPAN CLASS="ref">.*?</SPAN>\s*</A>', "", inner, flags=re.S)
            # the attribution is the roman between the italic quotations
            fathers = [father(w) for w in re.findall(r"(?:^|</I>\s*\.?\s*)([A-Z][a-z]+)", inner)]
            d = lec.setdefault((c, l), {"text": "", "fathers": []})
            d["text"] = (d["text"] + " " + clean(inner)).strip()
            d["fathers"] += [x for x in fathers if x]
    return lec

# ----------------------------------------------------- English (CCEL ThML)
def parse_en_thml(path):
    """[(chapter, {verses, paras, fathers})]: a section opens at each run of
    class="scripture" paragraphs (the verses commented on)."""
    s = open(path, encoding="utf-8").read()
    divs = list(re.finditer(r'<div2[^>]*title="Chapter (\d+)"[^>]*>', s))
    out = []
    for i, m in enumerate(divs):
        c = int(m.group(1))
        seg = s[m.end(): divs[i + 1].start() if i + 1 < len(divs) else len(s)]
        cur, prev = None, None
        for pm in re.finditer(r'<p\b[^>]*class="(\w+)"[^>]*>(.*?)</p>', seg, re.S):
            cls, t = pm.group(1), clean(pm.group(2))
            if not t:
                continue
            if cls == "scripture":
                if prev != "scripture":
                    cur = {"verses": [], "paras": [], "fathers": []}
                    out.append((c, cur))
                vm = re.match(r"(?:Ver\.\s*)?(\d+)", t)
                if vm:
                    cur["verses"].append(int(vm.group(1)))
                cur["paras"].append(t)
            elif cur is not None:
                fm = re.match(r"([A-Z][\w\-]+)\.?[^:]{0,80}:", t)
                if fm and father(fm.group(1)):
                    cur["fathers"].append(father(fm.group(1)))
                cur["paras"].append(t)
            prev = cls
    return out

# --------------------------------------------------- English (IA OCR text)
RE_CHAP = re.compile(r"^CHAP\.\s+\S+")
RE_RUN = re.compile(r"GOSPEL\s+ACCORDING|\bST\.\s+(LUKE|LUKK|JOHN|J0HN|JOHX)\b")
RE_VERSE = re.compile(r"^(?:Ver\.\s*)?(\d{1,2})\s*\.\s+[\"'(]?\s*[A-Z]")
RE_FATHER_OCR = re.compile(r"\b([A-Z][A-Z]{2,})\s?[;:.,]")
RE_FATHER_SC = re.compile(r"(?<![\w.])(B\s?ede|[A-Z][a-z]{2,10})\.\s+(?=[A-Z(])")   # small capitals read as "Aug."

def parse_en_ocr(path, first_chapter):
    """Raw OCR of the 1841-45 printing: chapters by their CHAP. headings in
    sequence, a section at each run of numbered verse paragraphs (the verse
    number counting up within the chapter), Fathers by their names in
    capitals with a semicolon (CHRYSOSTOM;). Running heads dropped; margin
    notes stay in the text, which is unproofread."""
    raw = open(path, encoding="utf-8", errors="replace").read().split("\n")
    paras, cur = [], []
    for line in raw:
        line = re.sub(r"\s+", " ", line).strip()
        if not line or RE_RUN.search(line) and len(line) < 70 or re.fullmatch(r"[\dIl]{1,4}|\W{1,3}", line):
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if RE_CHAP.match(line) and len(line) < 20:        # a heading on its own line, text straight after
            if cur:
                paras.append(" ".join(cur))
            paras.append(line)
            cur = []
            continue
        cur.append(line)
    if cur:
        paras.append(" ".join(cur))
    # the Fathers' names are set in capitals (CHRYSOSTOM;) in some volumes and
    # in small capitals, which the OCR reads as "Aug.", in others
    caps = sum(1 for p in paras for n in RE_FATHER_OCR.findall(p) if father(n))
    rx = RE_FATHER_OCR if caps > len(paras) / 10 else RE_FATHER_SC
    out, c, sec, last_v, in_verses = [], None, None, 0, False
    for p in paras:
        p = re.sub(r"(\w)- (\w)", r"\1\2", p)
        if RE_CHAP.match(p) and len(p) < 20:
            c = first_chapter if c is None else c + 1
            last_v, in_verses = 0, False
            continue
        if c is None:
            continue
        vm = RE_VERSE.match(p)
        if vm and last_v < int(vm.group(1)) <= last_v + 6 and not RE_FATHER_OCR.match(p):
            if not in_verses:
                sec = {"verses": [], "paras": [], "fathers": []}
                out.append((c, sec))
            sec["verses"].append(int(vm.group(1)))
            sec["paras"].append(p)
            last_v, in_verses = int(vm.group(1)), True
            continue
        if len(p) > 30:                 # a margin note between two verses does not end the run
            in_verses = False
        if sec is None:
            continue
        sec["fathers"] += [f for f in (father(n.replace(" ", "")) for n in rx.findall(p)) if f]
        sec["paras"].append(p)
    return out

# -------------------------------------------------------------- alignment
def runs(xs):
    """A Father named twice running counts once: the Latin says Idem, the OCR
    keeps the margin note that repeats the name."""
    return [x for i, x in enumerate(xs) if i == 0 or xs[i - 1] != x]

def fit(a, b):
    a, b = runs(a), runs(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()

def align(lat, eng):
    """Sections onto lectiones, one gospel at a time, in order: 1:1, or two
    English sections in one lectio, or one English section over two lectiones.
    A section in another chapter costs more. Returns [(lectio keys, section indexes, fit)]."""
    L, E = len(lat), len(eng)
    NEG = -1e9
    best = [[NEG] * (E + 1) for _ in range(L + 1)]
    back = [[None] * (E + 1) for _ in range(L + 1)]
    best[0][0] = 0.0
    def chap_ok(li, ej):
        return all(lat[i][0][0] == eng[j][0] for i in li for j in ej)
    for i in range(L + 1):
        for j in range(E + 1):
            if best[i][j] <= NEG / 2:
                continue
            for di, dj, cost in ((1, 1, 0.0), (1, 2, 0.2), (1, 3, 0.4), (2, 1, 0.3), (3, 1, 0.5), (1, 0, 0.6), (0, 1, 0.6)):
                ni, nj = i + di, j + dj
                if ni > L or nj > E:
                    continue
                li, ej = list(range(i, ni)), list(range(j, nj))
                if li and ej and not chap_ok(li, ej):
                    # the Latin keeps the medieval chapter breaks in places
                    # (its Mt 5, lectiones 22-23 are Mt 6:1-4): allowed, at a cost
                    cost += 0.25
                f = fit(sum((lat[x][1]["fathers"] for x in li), []), sum((eng[x][1]["fathers"] for x in ej), [])) if li and ej else 0.0
                v = best[i][j] + f - cost
                if v > best[ni][nj]:
                    best[ni][nj], back[ni][nj] = v, (i, j, f)
    out, i, j = [], L, E
    while (i, j) != (0, 0):
        pi, pj, f = back[i][j]
        out.append((list(range(pi, i)), list(range(pj, j)), f))
        i, j = pi, pj
    return out[::-1]

# ------------------------------------------------------------------ build
def build(check=False):
    rows, la_all, en_all, report = [], {}, {}, {}
    for g, prefix, abbr, files in GOSPELS:
        lec = parse_la(prefix, abbr)
        lat = sorted(lec.items())
        eng = []
        for fn, first in files:
            path = os.path.join(SHELF, fn)
            eng += parse_en_thml(path) if fn.endswith(".xml") else parse_en_ocr(path, first)
        steps = align(lat, eng)
        n1 = sum(1 for li, ej, f in steps if len(li) == 1 and len(ej) == 1)
        report[g] = {"lectiones": len(lat), "sections": len(eng), "one_to_one": n1,
                     "median_fit": sorted(f for li, ej, f in steps if li and ej)[len(steps) // 2] if steps else 0}
        for li, ej, f in steps:
            for x in li:
                (c, l), d = lat[x]
                key = f"CA.{g}.{c}.{l}"
                la_all[key] = d
                r = {"key": key, "ref": f"Catena in {abbr} cap. {c} l. {l}", "fathers_la": d["fathers"]}
                if ej:
                    secs = [eng[y][1] for y in ej]
                    vs = sorted({v for s in secs for v in s["verses"]})
                    r.update({"verses": [vs[0], vs[-1]] if vs else None, "fathers_en": sum((s["fathers"] for s in secs), []),
                              "fit": round(f, 2), "en_sections": len(ej)})
                    chs = sorted({eng[y][0] for y in ej})
                    if chs != [c]:                   # the verses are in another chapter of the English (and the Bible)
                        r["en_chapter"] = chs[0] if len(chs) == 1 else chs
                    if len(li) > 1:
                        r["en_shared_with"] = [f"CA.{g}.{lat[y][0][0]}.{lat[y][0][1]}" for y in li if y != x]
                    if x == li[0]:
                        en_all[key] = {"verses": vs, "paras": sum((s["paras"] for s in secs), [])}
                    else:
                        r["en_in"] = f"CA.{g}.{lat[li[0]][0][0]}.{lat[li[0]][0][1]}"
                r["witnesses"] = ["la"] + (["en"] if ej else [])
                rows.append(r)
            if not li:
                for y in ej:
                    c, s = eng[y]
                    key = f"CA.{g}.{c}.en{y}"
                    en_all[key] = {"verses": s["verses"], "paras": s["paras"]}
                    rows.append({"key": key, "ref": f"Catena in {abbr} cap. {c} (English section with no lectio)",
                                 "verses": [min(s["verses"]), max(s["verses"])] if s["verses"] else None,
                                 "fathers_en": s["fathers"], "witnesses": ["en"]})
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    if check:
        ok = open(KEY_OUT, encoding="utf-8").read() == text
        print("check ok" if ok else "CHECK FAILED: data/aquinas/catena-key.jsonl differs from a rebuild")
        return 0 if ok else 1
    os.makedirs(os.path.dirname(KEY_OUT), exist_ok=True)
    with open(KEY_OUT + ".tmp", "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(KEY_OUT + ".tmp", KEY_OUT)
    write_books(rows, la_all, en_all, report)
    for g, r in report.items():
        print(g, r)
    low = [r for r in rows if r.get("fit", 1) < 0.5 and "en" in r["witnesses"] and "la" in r["witnesses"]]
    print(f"{len(rows)} rows; {len(low)} with a Fathers fit under 0.5")
    return 0

def ref(key):
    _, g, c, l = key.split(".")
    return f"Catena Aurea, {NAMES[g]} {c}, lectio {l}" if not l.startswith("en") else f"Catena Aurea, {NAMES[g]} {c}"

def write_books(rows, la_all, en_all, report):
    def book(slug, title, author, ch, text_of):
        units = []
        for k, d in ch.items():
            for j, p in enumerate(text_of(d), 1):
                units.append({"id": f"{slug}:{k[3:]}.{j}", "key": k, "ref": f"{ref(k)}, par. {j}", "text": p, "links": []})
        b = {"slug": slug, "title": title, "author": author, "units": units}
        tmp = os.path.join(BOOKS, slug + ".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False)
        os.replace(tmp, os.path.join(BOOKS, slug + ".json"))
        return b
    bl = book("aquinas-catena-la", "Catena Aurea (Latin, via Corpus Thomisticum)", "Thomas Aquinas", la_all, lambda d: [d["text"]])
    be = book("aquinas-catena-en", "Catena Aurea (English, Oxford 1841-45)", "Thomas Aquinas (tr. J. H. Newman, ed.)", en_all, lambda d: d["paras"])
    par = [{"key": r["key"], "ref": r["ref"], "la": la_all.get(r["key"]), "en": en_all.get(r.get("en_in", r["key"]))} for r in rows]
    tmp = os.path.join(BOOKS, "aquinas-catena.parallel.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(par, f, ensure_ascii=False)
    os.replace(tmp, os.path.join(BOOKS, "aquinas-catena.parallel.json"))
    m = json.load(open(MANIFEST, encoding="utf-8"))
    sch = {"citation": "gospel, chapter, lectio (CA.Mt.5.3 = Catena in Mt. cap. 5 l. 3)", "key_file": "data/aquinas/catena-key.jsonl"}
    sha = lambda paths: hashlib.sha256(b"".join(open(p, "rb").read() for p in paths)).hexdigest()
    m["aquinas-catena-la"] = {"title": bl["title"], "author": bl["author"], "format": "corpus-thomisticum-html",
        "sha256": sha([os.path.join(CT, f) for f in sorted(os.listdir(CT)) if f[:3] in ("cmt", "cmc", "clc", "cjo")]),
        "units": len(bl["units"]),
        "scheme": {**sch, "resolution": "lectio", "honesty": "exact: Corpus Thomisticum's own chapter and lectio"},
        "source": "https://www.corpusthomisticum.org/iopera.html",
        "rights": {"license": "underlying text public domain; electronic edition claimed by the publisher",
                   "publisher_notice": "(c) Fundacion Tomas de Aquino quoad hanc editionem. Iura omnia asservantur",
                   "redistribute_whole": False, "pending": "Adam's ruling: docs/AQUINAS.md, The Latin question"},
        "builder": "pipeline/build_aquinas_catena.py", "note": f"{len(la_all)} lectiones."}
    m["aquinas-catena-en"] = {"title": be["title"], "author": be["author"], "format": "thml + ia-djvu-ocr",
        "sha256": sha([os.path.join(SHELF, fn) for _, _, _, fs in GOSPELS for fn, _ in fs]),
        "units": len(be["units"]),
        "scheme": {**sch, "resolution": "lectio (the English prints none; its sections are placed by the Fathers they quote, fit per row in the key)",
                   "honesty": "Matthew and Mark clean (CCEL); Luke and John raw OCR, unproofread, with margin notes left in the text. A section is placed on a lectio by the sequence of Fathers quoted, which survives translation; the fit is recorded and low fits are listed in docs/AQUINAS.md"},
        "source": "pipeline/aquinas_shelf.json (CCEL catena1, catena2; Internet Archive, Luke and John)",
        "rights": {"license": "public-domain", "basis": "Oxford: J. H. Parker, 1841-1845; US public domain", "redistribute_whole": True,
                   "ccel_terms": "CCEL asks non-commercial use of some prepared editions: check before republishing"},
        "builder": "pipeline/build_aquinas_catena.py",
        "note": "; ".join(f"{g}: {r['sections']} sections on {r['lectiones']} lectiones, {r['one_to_one']} one to one" for g, r in report.items())}
    with open(MANIFEST + ".tmp", "w", encoding="utf-8") as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + "\n")
    os.replace(MANIFEST + ".tmp", MANIFEST)

if __name__ == "__main__":
    sys.exit(build("--check" in sys.argv))
