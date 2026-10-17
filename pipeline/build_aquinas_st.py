#!/usr/bin/env python3
"""The Summa Theologiae, Latin and English, keyed together at the ARTICLE and
at each part of the article (objection, sed contra, respondeo, reply).

    python3 pipeline/build_aquinas_st.py           # build both books + the key
    python3 pipeline/build_aquinas_st.py --check   # rebuild the key in memory; must be byte-identical

Inputs (gitignored, fetched):
  English: CCEL's complete Summa, data/corpus/ccel/aquinas-summa-full.xml (the
           file ingest_summa_supplement.py already fetches): the Fathers of the
           English Dominican Province, 2nd revised edition (1920-22), with
           CCEL's article divisions (div4 id="FP_Q2_A3").
  Latin:   Corpus Thomisticum pages, data/corpus/corpus-thomisticum/sth*.html
           (pipeline/fetch_corpus_thomisticum.py): the Leonine text, one <P> per
           part of the article, each titled with its citation ("I q. 2 a. 3 co.").

The KEY is the Thomist citation itself, which both editions print:
    I.q2.a3.co     First Part, question 2, article 3, the body (respondeo)
    I-II.q90.a1.arg2   second objection     .sc  sed contra   .ad2  reply to obj. 2
    II-II.q1.pr    the question's prologue  III.q60.a1   the article (title row)
Parts: I, I-II, II-II, III, Suppl, App1, App2. A second sed contra is .sc2
(and the first then .sc1); a reply to the sed contra is .ad-sc. Because the
key is the citation, "keying" is not a guess: two texts either print the same
part of the same article or they don't, and the key file says which.

Outputs:
  data/books/aquinas-st-en.json, data/books/aquinas-st-la.json   (gitignored)
      units {id, key, ref, text, links}; id = <slug>:<key>
  data/books/aquinas-st.parallel.json                            (gitignored)
      one row per key: {key, ref, en, la}
  data/aquinas/st-key.jsonl                                      (COMMITTED)
      one row per article: its key, the English title, the parts each side
      has, and status (both / en-only / la-only / parts-differ). Facts about
      the two editions; no text but the English article title.
  data/books/manifest.json entries for both books.
"""
import hashlib, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
EN_SRC = os.path.join(ROOT, "data", "corpus", "ccel", "aquinas-summa-full.xml")
LA_DIR = os.path.join(ROOT, "data", "corpus", "corpus-thomisticum")
BOOKS = os.path.join(ROOT, "data", "books")
KEY_OUT = os.path.join(ROOT, "data", "aquinas", "st-key.jsonl")
MANIFEST = os.path.join(BOOKS, "manifest.json")

EN_PART = {"FP": "I", "FS": "I-II", "SS": "II-II", "TP": "III", "XP": "Suppl",
           "AP1": "App1", "AP2": "App2"}
PART_ORDER = ["ST", "I", "I-II", "II-II", "III", "Suppl", "App1", "App2"]
PART_NAME = {"ST": "", "I": "I", "I-II": "I-II", "II-II": "II-II", "III": "III",
             "Suppl": "Suppl.", "App1": "Suppl. App. I", "App2": "Suppl. App. II"}

def clean(s):
    s = re.sub(r"<note\b.*?</note>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("---", "—")
    return re.sub(r"\s+", " ", s).strip()

def ref_of(key):
    """I-II.q90.a1.ad2 -> 'ST I-II q.90 a.1 ad 2' (the way Thomists cite)."""
    bits = key.split(".")
    out = ["ST", PART_NAME.get(bits[0], bits[0])]
    for b in bits[1:]:
        if b == "pr":
            out.append("pr.")
        elif re.fullmatch(r"q\d+", b):
            out.append(f"q.{b[1:]}")
        elif re.fullmatch(r"a\d+", b):
            out.append(f"a.{b[1:]}")
        elif b.startswith("arg"):
            out.append(f"arg.{b[3:]}")
        elif b.startswith("sc"):
            out.append("s.c." + (f" {b[2:]}" if b[2:] else ""))
        elif b == "co":
            out.append("co.")
        elif b == "ad-sc":
            out.append("ad s.c.")
        elif b.startswith("ad"):
            out.append(f"ad {b[2:]}")
        else:
            out.append(b)
    return " ".join(out)

def seg_sort(seg):
    """Order inside an article: title, arg1.., sc.., co, ad1.., ad-sc."""
    if seg == "":
        return (0, 0)
    if seg == "body":
        return (3, -1)
    m = re.fullmatch(r"(arg|sc|co|ad)(\d*)|ad-sc", seg)
    if seg == "ad-sc":
        return (5, 0)
    kind, n = m.group(1), int(m.group(2) or 0)
    return ({"arg": 1, "sc": 2, "co": 3, "ad": 4}[kind], n)

# ----------------------------------------------------------------- English
RE_DIV = re.compile(r"<div([234])\b([^>]*)>")
RE_P = re.compile(r"<p\b[^>]*?(?:/>|>(.*?)</p>)", re.S)
RE_LABEL = re.compile(r"^\s*<b>\s*(Objection \d+[:.]|On the contrary[,.:]?|I answer that[,.:]?|"
                      r"Reply to Objection \d+[:.]|Reply Obj\. \d+[:.])\s*</b>\s*", re.S)
# The same labels printed without bold (a handful of articles): the paragraph
# still opens that part, and its words are kept whole ("I answer with Augustine").
RE_PLAIN_LABEL = re.compile(r"^\s*(Objection \d+[:.]|On the contrary\b|I answer\b|Reply to Objection \d+[:.])")

def en_label(lab):
    lab = lab.strip()
    if lab.startswith("Objection"):
        return "arg" + re.search(r"\d+", lab).group(0)
    if lab.startswith("On the contrary"):
        return "sc"
    if lab.startswith("I answer"):
        return "co"
    return "ad" + re.search(r"\d+", lab).group(0)

SPECIAL_PR = {"FS.i.i": "I-II.pr", "TP.i": "III.pr"}

def parse_parts(seg):
    """The labelled parts of one article; unlabelled paragraphs continue the
    part above them. Returns (paragraphs before the first label, parts)."""
    pre, parts, cur = [], [], None
    for p in RE_P.finditer(seg):
        inner = p.group(1) or ""
        if re.match(r"\s*<h\d", inner):
            continue
        lm = RE_LABEL.match(inner)
        text = clean(inner[lm.end():] if lm else inner)
        pm = None if lm else RE_PLAIN_LABEL.match(text)
        if pm and en_label(pm.group(1)) in {q["seg"] for q in parts}:
            pm = None              # "I answer, then, with Dionysius": the body going on
        if lm or pm:
            cur = {"seg": en_label((lm or pm).group(1)), "text": [text] if text else [], "src": [inner]}
            parts.append(cur)
        elif text and cur is not None:
            cur["text"].append(text)
            cur["src"].append(inner)
        elif text:
            pre.append((text, inner))
    return pre, parts

REPAIRS = []   # every repair the English needed, written into the key file

def renumber(akey, parts):
    """CCEL occasionally prints a label twice ("Reply to Objection 1" for the
    second reply). When a repeated label's neighbour number is missing, the
    occurrence standing where that number belongs takes it: the first one if
    the missing number is lower, the second if higher. Anything else stays
    repeated and is flagged ~2 downstream."""
    for i, p in enumerate(parts):
        m = re.fullmatch(r"(arg|ad)(\d+)", p["seg"])
        if not m:
            continue
        j = next((j for j in range(i + 1, len(parts)) if parts[j]["seg"] == p["seg"]), None)
        if j is None:
            continue
        kind, n = m.group(1), int(m.group(2))
        labels = {q["seg"] for q in parts}
        for cand, who in ((n - 1, i), (n + 1, j)):
            c = f"{kind}{cand}"
            if cand > 0 and c not in labels:
                REPAIRS.append({"key": akey, "repair": f"{'first' if who == i else 'second'} of two '{p['seg']}' labels read as {c}"})
                parts[who]["seg"] = c
                break

def number_sc(parts):
    nsc = sum(1 for p in parts if p["seg"] == "sc")
    k = 0
    for p in parts:                 # two or more sed contras are numbered, as the Latin numbers them
        if p["seg"] == "sc" and nsc > 1:
            k += 1
            p["seg"] = f"sc{k}"

def emit_article(units, akey, title, parts):
    number_sc(parts)
    renumber(akey, parts)
    units.append({"key": akey, "text": title, "links": []})
    seen = set()
    for p in parts:
        key = f"{akey}.{p['seg']}"
        n = 2
        while key in seen:              # a label printed twice: keep both, flag it with ~n
            key = f"{akey}.{p['seg']}~{n}"
            n += 1
        seen.add(key)
        units.append({"key": key, "text": "\n".join(p["text"]), "links": links_of("".join(p["src"]))})

def parse_en(path):
    raw = open(path, encoding="utf-8").read()
    body = raw[raw.find("<ThML.body>"):]
    marks = [(m.start(), m.end(), m.group(1), dict(re.findall(r'(\w+)="([^"]*)"', m.group(2))))
             for m in RE_DIV.finditer(body)]
    units, titles = [], {}
    for i, (st, en, lvl, at) in enumerate(marks):
        did = at.get("id", "")
        nxt = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        seg = body[en:nxt]
        if did in SPECIAL_PR:
            paras = [clean(p.group(1) or "") for p in RE_P.finditer(seg) if not re.match(r"\s*<h", p.group(1) or "")]
            units.append({"key": SPECIAL_PR[did], "text": "\n".join(x for x in paras if x), "links": links_of(seg)})
            continue
        if lvl == "2":
            continue
        if lvl == "3":
            m = re.fullmatch(r"([A-Z]+\d?)_Q(\d+)", did)
            if not m:
                continue          # a treatise prologue the Latin does not print separately
            base = f"{EN_PART[m.group(1)]}.q{int(m.group(2))}"
            titles[base] = clean(at.get("title", ""))
            pre, parts = parse_parts(seg)
            if pre:
                units.append({"key": base + ".pr", "text": "\n".join(t for t, _ in pre),
                              "links": links_of("".join(x for _, x in pre))})
            if parts:            # a question of one article, printed without an article heading
                titles[base + ".a1"] = titles[base]
                emit_article(units, base + ".a1", titles[base], parts)
            continue
        m = re.fullmatch(r"([A-Z]+\d?)_Q(\d+)_A(\d+)", did)
        if not m:
            continue
        akey = f"{EN_PART[m.group(1)]}.q{int(m.group(2))}.a{int(m.group(3))}"
        h = re.search(r"<h4[^>]*>(.*?)</h4>", seg, re.S)
        titles[akey] = clean(h.group(1)) if h else clean(at.get("title", ""))
        pre, parts = parse_parts(seg)
        if pre:                   # text before the first label: kept, keyed .body, never dropped
            parts.insert(0, {"seg": "body", "text": [t for t, _ in pre], "src": [x for _, x in pre]})
        # Two articles under one heading: a second "Objection 1" after the
        # body starts the next article, when CCEL has no division for it.
        nxt_key = f"{EN_PART[m.group(1)]}_Q{int(m.group(2))}_A{int(m.group(3)) + 1}"
        cut = next((i for i, p in enumerate(parts) if i and p["seg"] == "arg1"
                    and any(q["seg"] == "co" for q in parts[:i])), None)
        if cut is not None and f'id="{nxt_key}"' not in body:
            k2 = f"{EN_PART[m.group(1)]}.q{int(m.group(2))}.a{int(m.group(3)) + 1}"
            REPAIRS.append({"key": k2, "repair": f"printed inside {akey} with no heading of its own; split at its first objection"})
            titles[k2] = ""
            emit_article(units, akey, titles[akey], parts[:cut])
            emit_article(units, k2, "", parts[cut:])
            continue
        emit_article(units, akey, titles[akey], parts)
    return units, titles

def links_of(s):
    out = []
    for o in re.findall(r'osisRef="Bible\.(\w+):([^"]+)"', s):
        out.append({"osis": o[1], "versification": o[0], "resolved": False})
    return out

# ------------------------------------------------------------------- Latin
RE_LP = re.compile(r'<P TITLE="([^"]*)"[^>]*>(.*?)</P>', re.S)

def la_key(title):
    t = title.replace("ª", "").strip()
    t = re.sub(r"\s+", " ", t)
    if t == "Summa theologiae, pr.":
        return "ST.pr"
    m = re.fullmatch(r"(I|I-II|II-II|III) pr\.", t)
    if m:
        return m.group(1) + ".pr"
    m = re.fullmatch(r"(I|I-II|II-II|III|Supplementum|Suppl\.?) q\. (\d+) (.*)", t)
    if not m:
        return None
    part = {"Supplementum": "Suppl", "Suppl.": "Suppl", "Suppl": "Suppl"}.get(m.group(1), m.group(1))
    rest = m.group(3)
    base = f"{part}.q{int(m.group(2))}"
    if rest in ("pr.", "pr"):
        return base + ".pr"
    m2 = re.fullmatch(r"a\. (\d+) (.*)", rest)
    if m2:
        a, s = f"{base}.a{int(m2.group(1))}", m2.group(2).strip()
    else:                        # a question of one article: "I q. 71 arg. 1"
        a, s = f"{base}.a1", rest
    if s == "co.":
        return a + ".co"
    if s == "s. c.":
        return a + ".sc"
    mm = re.fullmatch(r"s\. c\. (\d+)", s)
    if mm:
        return a + f".sc{int(mm.group(1))}"
    mm = re.fullmatch(r"arg\. (\d+)", s)
    if mm:
        return a + f".arg{int(mm.group(1))}"
    mm = re.fullmatch(r"ad (\d+)", s)
    if mm:
        return a + f".ad{int(mm.group(1))}"
    if s in ("ad arg.", "ad s. c."):
        return a + ".ad-sc"
    return None

def parse_la(d):
    units, unknown = [], []
    files = sorted(f for f in os.listdir(d) if re.fullmatch(r"sth\d+\.html", f))
    for f in files:
        s = open(os.path.join(d, f), "rb").read().decode("latin-1")
        for m in RE_LP.finditer(s):
            title, inner = html.unescape(m.group(1)), m.group(2)
            inner = re.sub(r'^\s*<A NAME="\d+">\s*<SPAN CLASS="ref">.*?</SPAN>\s*</A>', "", inner, flags=re.S)
            key = la_key(title)
            if key is None:
                unknown.append((f, title))
                continue
            units.append({"key": key, "text": clean(inner), "links": []})
    return units, unknown

# ------------------------------------------- the existing Gutenberg English
# The Adler-shelf books aquinas-summa, -1-2, -2-2, -3 (the same Dominican
# translation, Gutenberg's own digitization) keep their paragraph ids. This
# maps each of their units to the key, so the Latin can be read beside them
# too. Built exactly as pipeline/ingest_adler.py builds them, ids included.
PG_PART = {"aquinas-summa": "I", "aquinas-summa-1-2": "I-II", "aquinas-summa-2-2": "II-II", "aquinas-summa-3": "III"}
RE_PG_ART = re.compile(r"^([A-Z]+) ARTICLE\b\s*(?:\[([^\]]*)\])?\s*$")
ORD = {w: i + 1 for i, w in enumerate(
    "FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHTH NINTH TENTH ELEVENTH TWELFTH "
    "THIRTEENTH FOURTEENTH FIFTEENTH SIXTEENTH".split())}
RE_PG_Q = re.compile(r"^QUESTION (\d+)\s*$")
RE_PG_LAB = re.compile(r"^(?:Objection (\d+)|Obj\. (\d+))\s*:\s*(_On the contrary)?|^(_On the contrary,?_)|^(_I answer that,?_)|^Reply Obj\. (\d+)")

def gutenberg_map():
    sys.path.insert(0, HERE)
    import structure_texts as st
    shelf = json.load(open(os.path.join(HERE, "adler_shelf.json"), encoding="utf-8"))
    out = {}
    for slug, part in PG_PART.items():
        src = os.path.join(ROOT, "data", "corpus", "adler", slug + ".txt")
        if not os.path.exists(src):
            raise SystemExit(f"missing {src}: run pipeline/ingest_adler.py (or fetch Gutenberg {shelf[slug]['gutenberg_id']}) first")
        b = shelf[slug]
        book = st.convert_gutenberg_prose(src, slug, b["title"], b["author"], b["chapre"])
        seen = {}
        for u in book["units"]:          # ingest_adler.py's de-duplication, verbatim
            if u["id"] in seen:
                seen[u["id"]] += 1
                u["id"] = f"{u['id']}~{seen[u['id']]}"
            else:
                seen[u["id"]] = 1
        cur, seg, nsc = None, None, 0
        for u in book["units"]:
            t = u["text"].strip()
            if t.startswith(">"):
                continue                   # the transcriber's quoted sample, not the text
            m = RE_PG_ART.match(t)
            if m and m.group(1) in ORD:
                # the bracket is usually "[I-II, Q. 6, Art. 3]" but the file has typos
                # ("[I. Q. 9, Art. 2]", "[II-II, Q., 40, Art. 3]", "[Q. 98, Art. 1]") or none
                nums = re.findall(r"\d+", re.sub(r"^\s*[IV-]+[.,]", "", m.group(2) or ""))
                q = int(nums[0]) if nums else int(cur.split(".")[1][1:]) if cur else None
                if q is None:
                    continue
                cur, seg, nsc = f"{part}.q{q}.a{ORD[m.group(1)]}", "", 0
                out.setdefault(cur, []).append(u["id"])
                continue
            mq = RE_PG_Q.match(t)
            if mq:
                cur, seg, nsc = f"{part}.q{int(mq.group(1))}", "pr", 0
                out.setdefault(cur + ".pr", []).append(u["id"])
                continue
            if cur is None:
                continue
            ml = RE_PG_LAB.match(t)
            if ml:
                if seg == "pr":            # a question of one article
                    cur, nsc = cur + ".a1", 0
                if ml.group(1) or ml.group(2):
                    seg = "arg" + (ml.group(1) or ml.group(2))
                elif ml.group(4):
                    nsc += 1
                    seg = f"sc{nsc}"
                elif ml.group(5):
                    seg = "co"
                else:
                    seg = "ad" + ml.group(6)
            key = cur if seg in ("", "pr") and not cur.endswith(".pr") and seg == "" else (
                f"{cur}.{seg}" if seg != "pr" else cur + ".pr")
            out.setdefault(key, []).append(u["id"])
    # one sed contra is .sc, as everywhere else
    for k in [k for k in out if k.endswith(".sc1")]:
        if k[:-1] + "2" not in out:
            out[k[:-1]] = out.pop(k)
    return out

# ------------------------------------------------------------------ the key
def akey_of(key):
    m = re.match(r"([^.]+\.q\d+\.a\d+|[^.]+\.q\d+\.pr|[^.]+\.pr)", key)
    return m.group(1) if m else key

def build_key(en_units, la_units, titles, pg=None):
    en_by, la_by = {}, {}
    for u in en_units:
        en_by.setdefault(akey_of(u["key"]), []).append(u["key"][len(akey_of(u["key"])) + 1:])
    for u in la_units:
        la_by.setdefault(akey_of(u["key"]), []).append(u["key"][len(akey_of(u["key"])) + 1:])
    def order(k):
        b = k.split(".")
        if b[1] == "pr":
            return (PART_ORDER.index(b[0]), 0, 0)
        q = int(b[1][1:])
        a = 0 if b[2] == "pr" else int(b[2][1:])
        return (PART_ORDER.index(b[0]), q, a)
    pg_ids = {}
    for k, v in (pg or {}).items():
        pg_ids.setdefault(akey_of(k), []).extend(v)
    rows = []
    for ak in sorted(set(en_by) | set(la_by), key=order):
        e = sorted({s for s in en_by.get(ak, []) if s}, key=lambda s: (seg_sort(s.split("~")[0]), s))
        l = sorted({s for s in la_by.get(ak, []) if s}, key=seg_sort)
        if ak not in la_by:
            status = "en-only"
        elif ak not in en_by:
            status = "la-only"
        elif ak.endswith(".pr"):
            status = "both"
        else:
            status = "both" if e == l else "parts-differ"
        row = {"key": ak, "ref": ref_of(ak), "status": status}
        if pg is not None:
            ids = pg_ids.get(ak, [])
            if ids:
                row["pg"] = [ids[0], ids[-1]] if len(ids) > 1 else ids
        rep = [r["repair"] for r in REPAIRS if r["key"] == ak]
        if rep:
            row["en_repairs"] = rep
        if not ak.endswith(".pr"):
            row["title_en"] = titles.get(ak, "")
            row["en"] = e
            row["la"] = l
        rows.append(row)
    return rows

def dump_key(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)

def write_atomic(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(path + ".tmp", path)

def book(slug, title, author, units, lang):
    for u in units:
        u["id"] = f"{slug}:{u['key']}"
        u["ref"] = ref_of(u["key"].split("~")[0])
    return {"slug": slug, "title": title, "author": author, "lang": lang,
            "units": [{k: u[k] for k in ("id", "key", "ref", "text", "links")} for u in units]}

def main(argv):
    check = "--check" in argv
    en_units, titles = parse_en(EN_SRC)
    la_units, unknown = parse_la(LA_DIR)
    if unknown:
        print(f"WARNING: {len(unknown)} Latin paragraphs with a title the key cannot read, e.g. {unknown[:5]}")
    pg = gutenberg_map()
    rows = build_key(en_units, la_units, titles, pg)
    text = dump_key(rows)
    if check:
        old = open(KEY_OUT, encoding="utf-8").read()
        if old != text:
            print("CHECK FAILED: data/aquinas/st-key.jsonl differs from a rebuild")
            return 1
        print(f"check ok: {len(rows)} rows byte-identical")
        return 0
    write_atomic(KEY_OUT, text)
    en_b = book("aquinas-st-en", "Summa Theologiae (English, Fathers of the English Dominican Province, 2nd ed. 1920-22), keyed by article",
                "Thomas Aquinas (tr. Fathers of the English Dominican Province)", en_units, "en")
    la_b = book("aquinas-st-la", "Summa Theologiae (Latin, Leonine text via Corpus Thomisticum), keyed by article",
                "Thomas Aquinas", la_units, "la")
    la_by = {u["key"]: u for u in la_b["units"]}
    en_by = {u["key"]: u for u in en_b["units"]}
    par = []
    for r in rows:
        ak = r["key"]
        segs = [""] if ak.endswith(".pr") else [""] + sorted(set(r.get("en", [])) | set(r.get("la", [])),
                                                             key=lambda s: (seg_sort(s.split("~")[0]), s))
        for s in segs:
            k = ak if s == "" else f"{ak}.{s}"
            e, l = en_by.get(k), la_by.get(k)
            if not e and not l:
                continue
            par.append({"key": k, "ref": ref_of(k.split("~")[0]),
                        "en": e["text"] if e else None, "la": l["text"] if l else None,
                        "pg_en": pg.get(k, [])})
    for b in (en_b, la_b):
        write_atomic(os.path.join(BOOKS, b["slug"] + ".json"), json.dumps(b, ensure_ascii=False))
    write_atomic(os.path.join(BOOKS, "aquinas-st.parallel.json"), json.dumps(par, ensure_ascii=False))
    update_manifest(en_b, la_b, rows)
    from collections import Counter
    c = Counter(r["status"] for r in rows)
    print(f"en units {len(en_b['units'])}, la units {len(la_b['units'])}, key rows {len(rows)}: {dict(c)}")
    return 0

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def update_manifest(en_b, la_b, rows):
    m = json.load(open(MANIFEST, encoding="utf-8"))
    arts = [r for r in rows if not r["key"].endswith(".pr")]
    both = sum(1 for r in arts if r["status"] in ("both", "parts-differ"))
    scheme = {"citation": "Thomist citation: part, question, article, part of the article (I.q2.a3.co = ST I q.2 a.3 co.)",
              "resolution": "part of the article (objection, sed contra, respondeo, reply)",
              "honesty": "exact: both editions print these divisions; where the two editions divide an article differently, data/aquinas/st-key.jsonl says so (status parts-differ) and nothing is forced to line up",
              "key_file": "data/aquinas/st-key.jsonl",
              "parallel_with": None}
    m["aquinas-st-en"] = {
        "title": en_b["title"], "author": en_b["author"], "format": "thml",
        "sha256": sha(EN_SRC), "units": len(en_b["units"]),
        "scheme": {**scheme, "parallel_with": "aquinas-st-la"},
        "source": "https://ccel.org/ccel/a/aquinas/summa.xml (DC.Rights: Public Domain)",
        "rights": {"license": "public-domain", "basis": "the translation was published 1911-1925 (2nd revised ed. 1920-22), before 1931: US public domain. The digital text (Sandra K. Perry's, as on Gutenberg) was keyed from the Benziger Brothers 1947 printing; only the translation is used, none of that printing's added matter",
                   "redistribute_whole": True},
        "builder": "pipeline/build_aquinas_st.py",
        "note": f"The same translation as the Gutenberg books aquinas-summa, -1-2, -2-2, -3 and aquinas-summa-supp, which keep their own ids; this book re-cuts CCEL's text at the article part so it can stand beside the Latin. {both} of {len(arts)} articles have a Latin witness. Scripture references are recorded as the source tagged them (Vulgate versification, resolved: false)."}
    m["aquinas-st-la"] = {
        "title": la_b["title"], "author": la_b["author"], "format": "corpus-thomisticum-html",
        "sha256": hashlib.sha256("".join(sha(os.path.join(LA_DIR, f)) for f in sorted(os.listdir(LA_DIR)) if f.startswith("sth")).encode()).hexdigest(),
        "units": len(la_b["units"]),
        "scheme": {**scheme, "parallel_with": "aquinas-st-en"},
        "source": "https://www.corpusthomisticum.org/iopera.html (Textum Leoninum Romae 1888-1906 editum, ed. E. Alarcon)",
        "rights": {"license": "underlying text public domain (Leonine edition, Rome 1888-1906); electronic edition claimed by the publisher",
                   "attribution": "Corpus Thomisticum, ed. Enrique Alarcon, Fundacion Tomas de Aquino / Universidad de Navarra",
                   "source_url": "https://www.corpusthomisticum.org/",
                   "publisher_notice": "(c) Fundacion Tomas de Aquino quoad hanc editionem. Iura omnia asservantur",
                   "redistribute_whole": False,
                   "pending": "Adam's ruling: docs/AQUINAS.md, The Latin question"},
        "builder": "pipeline/build_aquinas_st.py",
        "note": "No Supplement: Corpus Thomisticum prints the Supplement's source (Scriptum super Sententiis IV), not the Supplement itself."}
    write_atomic(MANIFEST, json.dumps(m, ensure_ascii=False, indent=1) + "\n")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
