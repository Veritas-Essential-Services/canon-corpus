#!/usr/bin/env python3
"""The edges out of the three dictionaries of names -> data/dictionaries/ (COMMITTED).

    python3 pipeline/build_dictionary_links.py --fetch   # the Character Sketches scans (IA djvu.xml)
    python3 pipeline/build_dictionary_links.py           # build every edge file
    python3 pipeline/build_dictionary_links.py --check   # rebuild in memory; files must be byte-identical

Reads the built books (data/books/{smith-dgrbm,brewer-character-sketches,
brewer,kjv,shakespeare}.json, gitignored; build them with
structure_texts.py first) and writes one JSONL file per kind of edge:

  names.jsonl        a headword that two or more of the dictionaries share.
                     A shared spelling is a LEAD, not an identity, and every
                     row says `same: "headword"`. Where two of its entries
                     also name two or more of the same other people or places
                     (three, when either entry is long), the pair is listed
                     under `corroborated` with the names they share.
  scripture.jsonl    Brewer's Bible references (`Prov. xxx. 8`, `1 _Sam._
                     xvii.`) -> KJV unit ids, kept only when the verse (or the
                     chapter) exists in data/books/kjv.json. Character Sketches
                     is parsed here; Phrase and Fable's own links are carried
                     over (`how: in-book`).
  shakespeare.jsonl  Brewer's Shakespeare references (`Shakespeare: Titus
                     Andronicus, v. 3`) -> the play, act and scene, kept only
                     when that scene exists in data/books/shakespeare.json.
  classical.jsonl    Smith's ancient-author citations, as Perseus normalised
                     them (`Hdt. 8.33`), -> a CTS URN with the passage, for the
                     works in cts-works.json (each read from Perseus's own
                     catalogue). The rest are counted, not guessed.
  pages-brewer-cs.jsonl  each Character Sketches entry -> the printed page and
                     scan leaf of the 1892 Hess edition at archive.org (eight
                     volumes, charactersketche0Nbrewuoft), found by aligning
                     headwords with the scans' own text layer. The leaf opens
                     at https://archive.org/details/<scan>/page/n<leaf>.
  plates-brewer-cs.jsonl  each plate of that edition (data/art/brewer-sketches/
                     plates.jsonl) -> the entry it illustrates, by its caption
                     and its place in the volume.

Nothing here is resolved by a guess the file does not own up to: every row
carries how it was found.
"""
import argparse, bisect, collections, html, io, json, os, re, sys, unicodedata, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "data", "books")
OUT = os.path.join(ROOT, "data", "dictionaries")
SCANS = os.path.join(ROOT, "data", "corpus", "lexicons", "brewer-cs-scans")
CS_SCAN_IDS = [f"charactersketche0{i}brewuoft" for i in range(1, 9)]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from structure_texts import _brewer_key  # noqa: E402

DICTS = ("smith-dgrbm", "brewer-character-sketches", "brewer")


def load(slug):
    p = os.path.join(BOOKS, slug + ".json")
    if not os.path.exists(p):
        sys.exit(f"missing {p}: run pipeline/structure_texts.py first")
    return json.load(open(p, encoding="utf-8"))


def headword(slug, u):
    return u["lex"].get("lemma") if slug == "smith-dgrbm" else u["lex"].get("headword")


# ------------------------------------------------------------------ names

def build_names(books):
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for slug in DICTS:
        for u in books[slug]["units"]:
            if "appendix" in u["lex"]:
                continue
            h = headword(slug, u)
            if h:
                by[_brewer_key(h)][slug].append(u["id"])
    text = {u["id"]: u["text"] for s in DICTS for u in books[s]["units"]}
    rows = []
    for k in sorted(by):
        if len(by[k]) < 2:
            continue
        members = {s: by[k][s] for s in DICTS if s in by[k]}
        row = {"key": k, "same": "headword", "members": members,
               "one_each": all(len(v) == 1 for v in by[k].values())}
        pairs = []
        slugs = list(members)
        for n, a in enumerate(slugs):
            for b in slugs[n + 1:]:
                for x in members[a]:
                    for y in members[b]:
                        shared = _names_in(text[x], k) & _names_in(text[y], k)
                        need = 3 if max(len(text[x]), len(text[y])) > 5000 else 2
                        if len(shared) >= need:
                            pairs.append({"a": x, "b": y, "shared": sorted(shared)[:8],
                                          "shared_n": len(shared)})
        if pairs:
            row["corroborated"] = pairs
        rows.append(row)
    return rows


_NAME_STOP = set("""This That These Those There Their They Then When Where Which While With From
Into Upon About After Before Being Also Though Thus Some Other Such What Whom Whose However Hence
Here Most More Many Much Every Each Both Either Neither Book Books Life Lives According Greek Greeks
Roman Romans Latin English French German Italian Spanish Scotch Irish Saint Lord Lady King Queen
Prince Princess Duke Earl Count Emperor Empress Pope Bishop Christ God Gods Jupiter""".split())


def _names_in(t, key):
    """The proper names an entry mentions, minus its own headword's words and
    the words every entry uses (Greek, King, This ...). Two entries with the
    same headword that name the same other people and places -- Smith's and
    Brewer's Admetus both name Alcestis, Apollo, Thessaly -- are very likely
    about the same figure; a shared spelling alone is only a lead."""
    own = set(key.split("-"))
    return {w for w in re.findall(r"\b[A-Z][a-zæœ]{3,}\b", t)
            if w not in _NAME_STOP and w.lower() not in own}


# ------------------------------------------------------------------ scripture

BIBLE = {  # Brewer's spellings -> OSIS, as data/books/kjv.json names the books
    "Gen": "Gen", "Genesis": "Gen", "Ex": "Exod", "Exod": "Exod", "Exodus": "Exod",
    "Lev": "Lev", "Leviticus": "Lev", "Num": "Num", "Numb": "Num", "Numbers": "Num",
    "Deut": "Deut", "Deuteronomy": "Deut", "Josh": "Josh", "Joshua": "Josh",
    "Judg": "Judg", "Judges": "Judg", "Ruth": "Ruth", "Sam": "Sam", "Samuel": "Sam",
    "Kings": "Kgs", "Kgs": "Kgs", "Chron": "Chr", "Chr": "Chr", "Chronicles": "Chr",
    "Ezra": "Ezra", "Neh": "Neh", "Nehemiah": "Neh", "Esth": "Esth", "Esther": "Esth",
    "Job": "Job", "Ps": "Ps", "Psa": "Ps", "Psalm": "Ps", "Psalms": "Ps",
    "Prov": "Prov", "Proverbs": "Prov", "Eccl": "Eccl", "Eccles": "Eccl", "Ecc": "Eccl",
    "Ecl": "Eccl", "Ecclesiastes": "Eccl", "Cant": "Song", "Song": "Song",
    "Isa": "Isa", "Isaiah": "Isa", "Jer": "Jer", "Jeremiah": "Jer", "Lam": "Lam",
    "Lamentations": "Lam", "Ezek": "Ezek", "Ezekiel": "Ezek", "Dan": "Dan", "Daniel": "Dan",
    "Hos": "Hos", "Hosea": "Hos", "Joel": "Joel", "Amos": "Amos", "Obad": "Obad",
    "Jonah": "Jonah", "Mic": "Mic", "Micah": "Mic", "Nah": "Nah", "Hab": "Hab",
    "Zeph": "Zeph", "Hag": "Hag", "Zech": "Zech", "Mal": "Mal", "Malachi": "Mal",
    "Matt": "Matt", "Matthew": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John",
    "Jno": "John", "Acts": "Acts", "Rom": "Rom", "Romans": "Rom",
    "Cor": "Cor", "Corinthians": "Cor", "Gal": "Gal", "Galatians": "Gal",
    "Eph": "Eph", "Ephesians": "Eph", "Phil": "Phil", "Col": "Col", "Thess": "Thess",
    "Tim": "Tim", "Timothy": "Tim", "Tit": "Titus", "Titus": "Titus", "Heb": "Heb",
    "Hebrews": "Heb", "Jas": "Jas", "James": "Jas", "Pet": "Pet", "Peter": "Pet",
    "Jude": "Jude", "Rev": "Rev", "Revelation": "Rev",
}
NUMBERED = {"Sam", "Kgs", "Chr", "Cor", "Thess", "Tim", "Pet"}   # `John` too, for the epistles
RE_BIBLE = re.compile(
    r"(?<![\w,])(?:(?P<n>[123]|I{1,3}) ?)?_?(?P<book>" + "|".join(sorted(BIBLE, key=len, reverse=True))
    + r")\b\.?_?,? (?P<ch>[ivxlc]+)\b\.?(?: ?(?P<v>\d{1,3})(?:[-—–](?P<v2>\d{1,3}))?)?")


def roman(s):
    vals = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}
    n = 0
    for a, b in zip(s, s[1:] + " "):
        n += -vals[a] if vals.get(b, 0) > vals[a] else vals[a]
    return n


def build_scripture(books):
    kjv = {u["id"] for u in books["kjv"]["units"]}
    chapters = {i.rsplit(".", 1)[0] for i in kjv}
    rows, missed = [], collections.Counter()
    # Phrase and Fable's converter already parses its own citations into the
    # book's links (structure_texts.brewer_scripture); they are carried over as
    # they are, so one question never gets two answers.
    for u in books["brewer"]["units"]:
        for l in u["links"]:
            if l.get("kind") == "scripture" and l.get("resolved"):
                row = {"from": u["id"], "cite": l["ref"], "target": l["target"], "level": "verse",
                       "how": "in-book"}
                if l.get("end"):
                    row["to"] = "kjv:" + l["end"]
                rows.append(row)
    for slug in ("brewer-character-sketches",):
        for u in books[slug]["units"]:
            for m in RE_BIBLE.finditer(u["text"]):
                book, n = BIBLE[m["book"]], m["n"]
                if m["book"] in ("John", "Mark") and u["text"][max(0, m.start() - 5):m.start()] == "King ":
                    continue                       # Shakespeare's King John, not the gospel
                if n:
                    n = {"I": "1", "II": "2", "III": "3"}.get(n, n)
                if book in NUMBERED:
                    if not n:
                        missed["no book number"] += 1; continue
                    book = n + book
                elif n and book == "John":
                    book = n + book
                elif n:
                    continue                       # `2 Gen.` is not a citation
                ch = roman(m["ch"])
                if m["v"]:
                    target, level = f"kjv:{book}.{ch}.{int(m['v'])}", "verse"
                    ok = target in kjv
                else:
                    target, level = f"kjv:{book}.{ch}", "chapter"
                    ok = target in chapters
                if not ok:
                    missed["no such verse in the KJV"] += 1; continue
                row = {"from": u["id"], "cite": " ".join(m.group(0).split()), "target": target,
                       "level": level}
                if m["v2"] and int(m["v2"]) > int(m["v"]):
                    end = f"kjv:{book}.{ch}.{int(m['v2'])}"
                    if end in kjv:
                        row["to"] = end
                rows.append(row)
    return rows, dict(missed)


# ------------------------------------------------------------------ shakespeare

def _play_key(title):
    k = _brewer_key(title.replace("Cæsar", "Caesar"))
    k = re.sub(r"^(the|a)-", "", k)
    k = re.sub(r"^(\d)-henry-(iv|vi)$", r"henry-\2-\1", k)
    k = re.sub(r"^henry-(iv|vi)-(?:part-)?(\d|i{1,3})$",
               lambda m: f"henry-{m[1]}-{ {'i': 1, 'ii': 2, 'iii': 3}.get(m[2], m[2])}", k)
    return {"midsummer-nights-dream": "a-midsummer-nights-dream", "lucrece": "rape-of-lucrece",
            "loves-labour-s-lost": "loves-labours-lost", "loves-labour-lost": "loves-labours-lost",
            "merry-wives": "merry-wives-of-windsor", "all-s-well-that-ends-well": "alls-well-that-ends-well",
            "the-tempest": "tempest", "two-gentlemen": "two-gentlemen-of-verona",
            "shrew": "taming-of-the-shrew", "pericles-prince-of-tyre": "pericles"}.get(k, k)


RE_SHAK = re.compile(r"Shakespeare[:,]? +_?(?P<t>[A-Z0-9][A-Za-z0-9'’.æ ]{2,40}?)_?\s*[.,]?\s*"
                     r"(?:\((?:\d{4})\))?[.,]?\s*(?:act +)?(?P<a>[ivx]{1,4})\b\.?(?:,? *(?:sc\. *)?(?P<s>\d{1,2}))?")


def build_shakespeare(books):
    ids = [u["id"] for u in books["shakespeare"]["units"]]
    plays = {i.split(":")[1].split(".")[0] for i in ids}
    scenes = {".".join(i.split(".")[:3]) for i in ids}
    rows, missed = [], collections.Counter()
    for slug in ("brewer-character-sketches", "brewer"):
        for u in books[slug]["units"]:
            for m in RE_SHAK.finditer(u["text"].replace("_", "")):
                play = _play_key(m["t"].strip(" .,"))
                if play not in plays:
                    missed["play not recognised"] += 1; continue
                act = roman(m["a"])
                target = f"shakespeare:{play}.{act}" + (f".{int(m['s'])}" if m["s"] else "")
                if m["s"] and target not in scenes:
                    missed["no such scene"] += 1; continue
                if not m["s"] and not any(s.startswith(target + ".") for s in scenes):
                    missed["no such act"] += 1; continue
                rows.append({"from": u["id"], "cite": " ".join(m.group(0).split()), "target": target,
                             "level": "scene" if m["s"] else "act"})
    return rows, dict(missed)


# ------------------------------------------------------------------ classical (Smith -> CTS)

def build_classical(books):
    works = json.load(open(os.path.join(OUT, "cts-works.json"), encoding="utf-8"))["works"]
    abbrevs = sorted(works, key=len, reverse=True)
    rows, missed = [], collections.Counter()
    for u in books["smith-dgrbm"]["units"]:
        for l in u["links"]:
            if l["kind"] != "classical":
                continue
            cite = l["cite"].strip()
            ab = next((a for a in abbrevs if cite.startswith(a + " ") or cite == a), None)
            if not ab:
                missed[cite.split(" ")[0]] += 1; continue
            passage = cite[len(ab):].strip()
            if passage and not re.fullmatch(r"[\d.]+[a-z]?", passage):
                missed["passage not a number"] += 1; continue
            rows.append({"from": u["id"], "cite": cite,
                         "urn": works[ab]["urn"] + (f":{passage.rstrip('.')}" if passage else "")})
    top = dict(collections.Counter(missed).most_common(25))
    return rows, {"unresolved": sum(missed.values()), "top_unresolved_abbreviations": top}


# ------------------------------------------------------------------ Character Sketches scan pages

def fetch_scans():
    os.makedirs(SCANS, exist_ok=True)
    for ia in CS_SCAN_IDS:
        dest = os.path.join(SCANS, f"{ia}_djvu.xml")
        if os.path.exists(dest):
            continue
        url = f"https://archive.org/download/{ia}/{ia}_djvu.xml"
        print("fetch", url)
        with urllib.request.urlopen(url, timeout=120) as r:
            data = r.read()
        open(dest + ".tmp", "wb").write(data)
        os.replace(dest + ".tmp", dest)


def _scan_leaves(ia):
    t = open(os.path.join(SCANS, f"{ia}_djvu.xml"), encoding="utf-8").read()
    leaves = []
    for obj in re.findall(r"<OBJECT.*?</OBJECT>", t, re.S):
        lines = [" ".join(html.unescape(w) for w in re.findall(r"<WORD[^>]*>([^<]*)</WORD>", ln))
                 for ln in re.findall(r"<LINE>(.*?)</LINE>", obj, re.S)]
        leaves.append([re.sub(r"\s+", " ", x).strip() for x in lines])
    return leaves


def _norm(s):
    s = s.replace("Æ", "AE").replace("æ", "ae").replace("Œ", "OE").replace("œ", "oe")
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def _page_map(leaves):
    """{leaf: printed page}. Candidate folios are numbers in a leaf's first two
    lines; the folios are the longest chain in which the page number rises,
    the leaf rises, and the gap between them never shrinks (plates add leaves,
    never pages). A leaf between two read folios is filled in only when the
    leaves and the pages between them agree one for one."""
    pts = sorted({(li, int(t)) for li, L in enumerate(leaves) for line in L[:2]
                  for t in re.findall(r"(?<![\w])(\d{1,3})(?![\w])", line)})
    best, prv = [1] * len(pts), [-1] * len(pts)
    for j, (lj, nj) in enumerate(pts):
        for i in range(max(0, j - 40), j):
            li, ni = pts[i]
            if li < lj and ni < nj and lj - nj >= li - ni and nj - ni <= lj - li and best[i] + 1 > best[j]:
                best[j], prv[j] = best[i] + 1, i
    if not pts:
        return {}, set()
    j, chain = max(range(len(pts)), key=lambda k: best[k]), []
    while j != -1:
        chain.append(pts[j]); j = prv[j]
    chain.reverse()
    m = dict(chain)
    read = set(m)
    for (a, na), (b, nb) in zip(chain, chain[1:]):
        if b - a == nb - na:
            for k in range(a + 1, b):
                m[k] = na + (k - a)
    return m, read


def build_pages(books):
    if not all(os.path.exists(os.path.join(SCANS, f"{ia}_djvu.xml")) for ia in CS_SCAN_IDS):
        return None
    seq, maps = [], {}
    for v, ia in enumerate(CS_SCAN_IDS, 1):
        leaves = _scan_leaves(ia)
        maps[v] = _page_map(leaves)
        for li, L in enumerate(leaves):
            for line in L:
                seq.append((v, li, _norm(line[:40])))
    idx = collections.defaultdict(list)
    for k, (_, _, s) in enumerate(seq):
        for n in range(4, min(len(s), 24) + 1):
            idx[s[:n]].append(k)
    U = books["brewer-character-sketches"]["units"]
    cands = []
    for i, u in enumerate(U):
        h = _norm(u["lex"]["headword"])[:24]
        ps = idx.get(h, []) if len(h) >= 4 else []
        if 0 < len(ps) <= 60:
            cands.append((i, ps))
    # the headwords' scan lines must rise with the dictionary's own order: the
    # longest such chain (each entry tries its candidate lines last-first, so
    # one entry contributes at most one line)
    tails, tails_id, prev = [], [], {}
    for i, ps in cands:
        for p in sorted(ps, reverse=True):
            j = bisect.bisect_left(tails, p)
            prev[(i, p)] = tails_id[j - 1] if j else None
            if j == len(tails):
                tails.append(p); tails_id.append((i, p))
            else:
                tails[j], tails_id[j] = p, (i, p)
    chain, n = [], (tails_id[-1] if tails_id else None)
    while n:
        chain.append(n); n = prev[n]
    found = {}
    for i, p in sorted(chain):
        v, leaf, _ = seq[p]
        pm, read = maps[v]
        if leaf not in pm:
            continue
        found[i] = {"id": U[i]["id"], "scan": CS_SCAN_IDS[v - 1], "volume": v, "leaf": leaf,
                    "page": pm[leaf], "page_how": "read" if leaf in read else "counted"}
    # An entry whose headword the scan's OCR garbled sits between two found
    # ones: on their page when both are on one page ("between"), else on a
    # page from the first's to the second's ("between, range").
    rows, idx = [], sorted(found)
    for i in range(len(U)):
        if i in found:
            rows.append(found[i]); continue
        k = bisect.bisect_left(idx, i)
        if k == 0 or k == len(idx):
            continue
        a, b = found[idx[k - 1]], found[idx[k]]
        if a["volume"] != b["volume"] or b["page"] < a["page"]:
            continue
        row = {"id": U[i]["id"], "scan": a["scan"], "volume": a["volume"], "leaf": a["leaf"],
               "page": a["page"], "page_how": "between"}
        if b["page"] != a["page"]:
            row.update(leaf_to=b["leaf"], page_to=b["page"], page_how="between, range")
        rows.append(row)
    return rows


# ------------------------------------------------------------------ Character Sketches plates

PLATES = os.path.join(ROOT, "data", "art", "brewer-sketches", "plates.jsonl")
_PLATE_STOP = {"the", "and", "his", "her", "with", "from", "their", "there", "before", "after", "death", "sister", "daughter",
               "lady", "king", "queen", "engraver", "artist", "painting"}


def _plate_tokens(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return [t for t in re.findall(r"[a-z]+", s)
            if (len(t) >= 3 or re.fullmatch(r"[ivx]+", t)) and t not in _PLATE_STOP]


def build_plates(books, pages):
    """Each plate of the 1892 Hess edition (data/art/brewer-sketches, from the
    plates thread) -> the Character Sketches entry it illustrates. A plate is
    bound near its entry, so only entries within ten scan leaves of the plate
    in the same volume are candidates (an entry with no read page takes the
    leaf of the entry before it). Every word of the entry's headword must be
    in the plate's caption as OCR read it. When the headword carries a
    qualifier (`Deans (Douce Davie)`) and none of its words is in the caption,
    the plate may show another bearer of the name, so the row keeps its
    candidates, unresolved. Captions are unproofread OCR: a misread name finds
    nothing, and nothing is guessed in its place."""
    if not os.path.exists(PLATES):
        return None
    U = {u["id"]: u for u in books["brewer-character-sketches"]["units"]}
    known = {r["id"]: r for r in pages}
    order = [i for i in U if "appendix" not in U[i]["lex"]]
    byvol, last = collections.defaultdict(list), None
    for n, i in enumerate(order):
        if i in known:
            last = known[i]; byvol[last["volume"]].append((i, last["leaf"])); continue
        nxt = next((known[j] for j in order[n + 1:n + 40] if j in known), None)
        if last and nxt and last["volume"] == nxt["volume"]:
            byvol[last["volume"]].append((i, last["leaf"]))
    rows = []
    for line in open(PLATES, encoding="utf-8"):
        p = json.loads(line)
        ct = set(_plate_tokens(p.get("caption_ocr")) + _plate_tokens(p.get("plate_title_ocr")))
        if not ct:
            continue
        cands = []
        for i, leaf in byvol.get(p["volume"], []):
            d = abs(leaf - p["leaf"])
            ht = _plate_tokens(U[i]["lex"]["headword"])
            if d > 10 or not ht or not all(a in ct for a in ht):
                continue
            qt = _plate_tokens(U[i]["lex"].get("qualifier", "")) if not re.match(
                r"\d+ syl", U[i]["lex"].get("qualifier", "")) else []
            qm = sum(1 for a in qt if a in ct)
            cands.append((len(ht), qm, -d, i, bool(qt)))
        if not cands:
            continue
        cands.sort(reverse=True)
        top = [c for c in cands if c[:2] == cands[0][:2]]
        row = {"plate": p["citation"], "uid": p["uid"], "caption_ocr": p.get("caption_ocr", "")}
        if len(top) == 1 and not (top[0][4] and top[0][1] == 0):
            row.update(target=top[0][3], resolved=True,
                       how="headword in caption" + (" + qualifier" if top[0][1] else ""))
        else:
            row.update(candidates=[c[3] for c in top], resolved=False,
                       how="headword in caption; qualifier not" if len(top) == 1 else "several entries fit")
        rows.append(row)
    return rows


# ------------------------------------------------------------------ main

def dump_jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n" for r in rows)


def build_all():
    books = {s: load(s) for s in DICTS + ("kjv", "shakespeare")}
    files, summary = {}, {}
    names = build_names(books)
    files["names.jsonl"] = dump_jsonl(names)
    summary["names"] = {"rows": len(names), "one_each": sum(r["one_each"] for r in names),
                        "in_all_three": sum(len(r["members"]) == 3 for r in names),
                        "corroborated_rows": sum("corroborated" in r for r in names),
                        "corroborated_pairs": sum(len(r.get("corroborated", [])) for r in names)}
    scr, miss = build_scripture(books)
    files["scripture.jsonl"] = dump_jsonl(scr)
    summary["scripture"] = {"rows": len(scr), "dropped": miss}
    sh, miss = build_shakespeare(books)
    files["shakespeare.jsonl"] = dump_jsonl(sh)
    summary["shakespeare"] = {"rows": len(sh), "dropped": miss}
    cl, miss = build_classical(books)
    files["classical.jsonl"] = dump_jsonl(cl)
    summary["classical"] = dict(rows=len(cl), **miss)
    pages = build_pages(books)
    if pages is None:                    # scans not fetched: the committed rows stand
        print("note: Character Sketches scans not fetched (--fetch); pages-brewer-cs.jsonl read as committed")
        pages = [json.loads(l) for l in open(os.path.join(OUT, "pages-brewer-cs.jsonl"), encoding="utf-8")]
    files["pages-brewer-cs.jsonl"] = dump_jsonl(pages)
    summary["pages-brewer-cs"] = {"rows": len(pages),
                                  "of_entries": len(books["brewer-character-sketches"]["units"]),
                                  "read": sum(r["page_how"] == "read" for r in pages),
                                  "between": sum(r["page_how"] == "between" for r in pages),
                                  "range": sum(r["page_how"] == "between, range" for r in pages)}
    plates = build_plates(books, pages)
    if plates is not None:
        files["plates-brewer-cs.jsonl"] = dump_jsonl(plates)
        summary["plates-brewer-cs"] = {"rows": len(plates), "resolved": sum(r["resolved"] for r in plates)}
    summary["sources"] = {s: books[s]["source"].get("sha256") for s in DICTS + ("kjv", "shakespeare")}
    files["summary.json"] = json.dumps(summary, ensure_ascii=False, indent=1) + "\n"
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fetch", action="store_true", help="download the Character Sketches scans' text layer")
    ap.add_argument("--check", action="store_true", help="rebuild in memory and compare with the committed files")
    a = ap.parse_args()
    if a.fetch:
        fetch_scans()
    files = build_all()
    if a.check:
        bad = [fn for fn, s in files.items()
               if not os.path.exists(os.path.join(OUT, fn))
               or open(os.path.join(OUT, fn), encoding="utf-8").read() != s]
        print("check:", "OK, byte-identical" if not bad else f"DIFFERS: {bad}")
        sys.exit(1 if bad else 0)
    os.makedirs(OUT, exist_ok=True)
    for fn, s in files.items():
        p = os.path.join(OUT, fn)
        with open(p + ".tmp", "w", encoding="utf-8") as f:
            f.write(s)
        os.replace(p + ".tmp", p)
    print(files["summary.json"])


if __name__ == "__main__":
    main()
