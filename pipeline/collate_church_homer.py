#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted (Church's Homers: second-scan collation, Adam's request)
# fable_review: pending
"""collate_church_homer.py -- Church's Iliad and Odyssey for Boys and Girls, collated.

The two books have been in the corpus since 2026-10-16 as the Unscanner's reading of ONE scan each
(data/unscanned/<slug>.unscanned.json.gz, SHIPPED_WORKING_TEXT in fetch_sources.py): unproofread
tesseract. This script reads that text against the Archive's OCR of the same scan AND of other
printings from the same plates, word by word, and writes a collated text. Nothing is typed into the
source text: every change is a rule here, a vote of the witnesses, or a reading of the page image
recorded in data/unscanned/<slug>.collation-reads.json (what was seen, on which leaf).

    python3 pipeline/collate_church_homer.py --fetch   # the witnesses' OCR, pinned by sha256 (gitignored)
    python3 pipeline/collate_church_homer.py           # -> data/unscanned/<slug>.collated.json, .collation.json, .md
    python3 pipeline/collate_church_homer.py --check   # the committed outputs are what the rules make

THE WITNESSES (all printings from the 1906/1907 Macmillan plates, "Set up and electrotyped"; every
printing used is dated before 1931, the US public-domain line):
  base  the Unscanner's re-OCR (tesseract, with layout) of the base scan
  A     the Archive's own OCR of that same scan (a second engine on the same paper)
  B     the Archive's OCR of a Google scan of the FIRST printing (Harvard copy)
  C     (Iliad only) the Archive's tesseract OCR of a 1927 printing (Better World Books copy)
Left out on purpose: iliadforboysgirl0000reva (1932 printing, "New Edition October, 1930") and
bwb_Y0-BOC-827 (Odyssey, copyright 1934, reprinted to 1942): both after 1930.

THE RULES, in order (counts go into each book's collation.json):
  1. Witness furniture: Google's notice and "Digitized by Google" lines; any line three-quarters
     capitals (running heads, chapter heads, captions, small-capital lines); folios; printer's
     signature marks ("B 17"); a line-end hyphen (- or the Archive's soft hyphen) rejoins the word,
     the hyphen kept only when the book prints the word hyphened elsewhere.
  2. Base dirt: "_" (underline specks) removed; doubled single quotes made double quotes, and
     tesseract's “‘ / ‘“‘ / ”’ for the book's wide double marks made “ and ”; a stray
     mark standing alone between words (- | © ' , .) removed; the book's spaced ; : ? ! closed up
     (the base already closes most). A word read on the page image ("tokens" in the reads file)
     replaces the base's before anything else.
  3. Names in their PRINTED form (NAMES): Church marks quantities and diaereses (Telemăchus,
     Menelaüs, Ænēas, Briseïs) and no OCR engine keeps them. Every form was read on the page image,
     every occurrence of the marked names looked at (the reads file lists where the print differs).
     Applied to capitalised words only, in every witness, before the vote.
  4. Alignment: each witness against the base, word by word on letters only (case, accents and
     punctuation ignored), difflib over the whole book.
  5. The vote, place by place (a place is a run where any witness's letters differ). A witness
     abstains where it is missing or garbled for 8+ words running. The base reading stands when at
     least one witness has it and no other reading has as many votes; a reading two witnesses
     share, with more votes than any other, replaces it
     (with the base's punctuation kept round a single word). No majority: the place is OPEN, and
     its reading comes from the page image (reads file); an open place with no read keeps the base
     and is counted.
  6. Words two witnesses have and the base lacks are put in (lines the base dropped).
  7. Structure: units left empty are dropped; the printer's colophon goes; a chapter's first word
     (printed in small capitals) is set in capitals, with the next word after a one-letter word
     ("A GREAT") or where the reads say so ("KING PRIAM"); the List of Illustrations is read
     from the page image (reads file); a unit that begins in
     lower case continues the paragraph before it (the base split paragraphs round plates);
     footnotes are taken out of the running text and attached to their paragraph. The corpus
     units keep their ids (the Armarium's plates point at them); the reading text joins them.

Punctuation is voted for quotation marks only (rule 5c): the Archive's OCR of the Google scans prints
quotation marks as '3, /1, **, so it never votes for a mark. Stops and commas are the base's, except
by rule 2 and by reads.
"""
import argparse, collections, difflib, gzip, hashlib, html, json, os, re, sys, unicodedata, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
WITDIR = os.path.join(REPO, "data", "corpus", "archive", "witness")
OUTDIR = os.path.join(REPO, "data", "unscanned")
DL = "https://archive.org/download/{id}/{fn}"

# ------------------------------------------------------------------ the books

BOOKS = {
    "church-iliad-boys": {
        "title": "The Iliad for Boys and Girls",
        "author": "Alfred J. Church",
        "subtitle": "Told from Homer in Simple Language",
        "first_published": "New York: The Macmillan Company, September 1907",
        "base": {"file": "data/unscanned/church-iliad-boys.unscanned.json.gz",
                 "scan": "iliadforboysgirl00chur_0",
                 "printing": "1923 printing (Library of Congress copy); title page dated 1923, "
                             "'Set up and electrotyped. Published September, 1907.'"},
        "witnesses": [
            ("A", "iliadforboysgirl00chur_0", "iliadforboysgirl00chur_0_djvu.xml",
             "249a06995024c7f5ee3380c13a8854e7ce5453e5ac997c7edb1bb25f0db89d51",
             "the base scan (1923 printing), the Archive's own OCR"),
            ("B", "iliadforboysand00homegoog", "iliadforboysand00homegoog_djvu.xml",
             "023fa2a936d62199d64dff2576345e29055ea359dcab365ebf50eb677f531d89",
             "FIRST PRINTING, 1907 (Harvard copy, scanned by Google), ABBYY FineReader 8.0"),
            ("C", "bwb_Y0-BOA-876", "bwb_Y0-BOA-876_djvu.xml",
             "67179c567c0869e776bc348462556c1476cb3bbcbbb8168324c64192c1bbbce9",
             "1927 printing (title page dated 1927; copyright 1907), tesseract 5.3"),
        ],
    },
    "church-odyssey-boys": {
        "title": "The Odyssey for Boys and Girls",
        "author": "Alfred J. Church",
        "subtitle": "Told from Homer",
        "first_published": "New York: The Macmillan Company, September 1906",
        "base": {"file": "data/unscanned/church-odyssey-boys.unscanned.json.gz",
                 "scan": "odysseyforboysgi00chur",
                 "printing": "1906, the first printing (New York Public Library copy)"},
        "witnesses": [
            ("A", "odysseyforboysgi00chur", "odysseyforboysgi00chur_djvu.xml",
             "15155b6ef7cbb1b8d69bbcbda9d34ad333ae4b7a89b15a265357f6126daad642",
             "the base scan (1906), the Archive's own OCR"),
            ("B", "odysseyforboysa00unkngoog", "odysseyforboysa00unkngoog_djvu.xml",
             "9146cb7cd96ff47e00137f10249ec6764a00b4d2a08d48f3c18feb1c6af83284",
             "1906 (Harvard copy, scanned by Google), ABBYY FineReader 8.0"),
        ],
    },
}

# Rule 3. printed form -> the letter keys (see key()) the OCRs make of it. Each printed form was read
# on the base scan's page images (2026-11-03), every occurrence for the marked names.
BREVE_Y = "y̆"
NAMES = {
    "church-iliad-boys": {
        "Menelaüs": "menelaus menelaiis menelatis menelats menelais menelairs menelaitis menelaias",
        "Ænēas": "aeneas aneas aineas eneas afneas atneas neas ineas 7eneas zneas ieneas jeneas",
        "Æneus": "aeneus aneus aineus ieneus",
        "Œneus": "oeneus ceneus",
        "Ætolians": "aetolians atolians attolians etolians aftolians hitolians altolians ietolians jetolians",
        "Sarpēdon": "sarpedon",
        # the plates' own misprints, in the 1907 first printing as in the 1923 (leaves n206, n242 of
        # iliadforboysand00homegoog): kept as printed, marks and all
        "Sarēpdon": "sarepdon",
        "Sarpdoēn": "sarpdoen",
        "Pandărus": "pandarus pandrus pandjtrus",
        "Machāon": "machaon",
        "Briseïs": "briseis brisris",
        "Chryseïs": "chryseis",
        "Andromaché": "andromache",
        "Antilŏchus": "antilochus antilechus antilschus",
        "Deïphobus": "deiphobus detphobus",
        "Helĕnus": "helenus helsnus",
        "Bellerŏphon": "bellerophon bellerephon bellerbphon",
        "Hephæstus": "haephaestus hephaestus hephestus hephzstus hepheastus",
        "Aphrodité": "aphrodite",
        "Phœnix": "phoenix phcenix phceenix pheenix phcnix",
        "Agēnor": "agenor",
        "Artĕmis": "artemis artsmis",
        "Polydămas": "polydamas polydsmas",
        "Meriŏnes": "meriones",
        "Mycenæ": "mycenae mycenz mycens",
        "Chrysé": "chryse",
        "Latōna": "latona lat5na",
        "Chimæra": "chimaera chimera",
        "Sol" + BREVE_Y + "mi": "solymi",
        "Astyănax": "astyanax astysnax astynax",
        "Sthenĕlus": "sthenelus",
        "Thebé": "thebe",
        "Arisbé": "arisbe",
        "Pæonia": "paeonia pzonia",
        "Scæan": "scaean scaan scean scsan",
        "Athené": "athene athenee",
    },
    "church-odyssey-boys": {
        "Telemăchus": "telemachus telemadchus telemschus telemchus teiemschus teiemachus",
        "Menelaüs": "menelaus menelaiis menelatis menelaitis menelaias",
        "Antinoüs": "antinous antinoiis antinotis antinols antinows",
        "Eur" + BREVE_Y + "lŏchus": "eurylochus euryl5chus",
        "Alcinoüs": "alcinous alcinoiis",
        "Amphinŏmus": "amphinomus amphindmus",
        "Agelaüs": "agelaus agelaiis",
        "Ismărus": "ismarus",
        "Athené": "athene",
        "Circé": "circe",
        "Penelopé": "penelope",
        "Hermioné": "hermione",
        "Areté": "arete",
        "Samé": "same",        # capitalised only: the island (Ithaca's neighbour), not "the same"
    },
}

# ------------------------------------------------------------------ text helpers

def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def key(t):
    """Letters only, for alignment and voting: case, accents, ligatures and punctuation ignored."""
    s = fold(t).casefold().replace("æ", "ae").replace("œ", "oe").replace("0", "o")
    return re.sub(r"[^0-9a-z]", "", s)

CORE = re.compile(r"^(\W*?)([\wÀ-ɏ̀-ͯ](?:.*[\wÀ-ɏ̀-ͯ])?)(\W*)$", re.S)

def split_tok(t):
    m = CORE.match(t)
    return (m.group(1), m.group(2), m.group(3)) if m else (t, "", "")

def name_map(slug):
    m = {}
    for printed, keys in NAMES[slug].items():
        for k in keys.split():
            m[k] = printed
    return m

def canon(tok, nmap, stats=None):
    """Rule 3: a capitalised word whose letters are a known OCR form of a name -> the printed form."""
    pre, core, suf = split_tok(tok)
    if not core or not any(c.isupper() for c in core[:2]):
        return tok
    poss = ""
    m = re.match(r"^(.*?)([’']s)$", core)
    stem = m.group(1) if m else core
    if m:
        poss = m.group(2)
    p = nmap.get(key(stem))
    if not p:
        return tok
    if stem.isupper() and len(stem) > 1:
        p = p.upper()
    new = pre + p + poss + suf
    if stats is not None and new != tok:
        stats[p] += 1
    return new

def base_rules(tok, stats):
    """Rule 2."""
    t = tok
    if re.search(r"[\[\]]", t) and re.search(r"[A-Za-z]", t):
        t = re.sub(r"[\[\]]", "", t)            # "[I", "I[", "[then": a bracket the base read beside a letter
        stats["brackets beside a letter removed"] += 1
    if re.match(r"^\.[a-z]", t):
        t = t[1:]                                  # ".man", ".escape": a speck read as a stop
        stats["speck before a word removed"] += 1
    if "_" in t:
        t = t.replace("_", "")
        stats["underline specks removed"] += 1
    if re.match(r"^/[A-ZÆŒ]", t):
        t = t[1:]
        stats["slash before a capital removed"] += 1
    for a, b in (("‘‘", "“"), ("’’", "”"), ("““", "“"), ("””", "”")):
        if a in t:
            t = t.replace(a, b)
            stats["doubled quotes made double"] += 1
    # tesseract reads the book's wide opening double mark as “‘ or ‘“‘, and its closing as ”’ or ’”’
    t2 = re.sub(r"^(?:‘“‘|“‘|‘“)(?=\w)", "“", t)
    t2 = re.sub(r"(?<=[\w.,;:!?])(?:’”’)$", "’”", t2)
    t2 = re.sub(r"(?<=[\w.,;:!?])(?:”’)$", "”", t2)
    if t2 != t:
        t = t2
        stats["tesseract's double marks (“‘, ”’) made single double marks"] += 1
    return t

# ------------------------------------------------------------------ witnesses (rule 1)

GOOGLE = re.compile(r"Digitized by|^/?Google|VjOOQ|OOQIC|^Google$", re.I)
SIGNATURE = re.compile(r"^[A-Za-z°^]{1,2}\s*\d{1,3}\s*\+?$|^[\divxlcIVXLC.,'’ ]{1,6}$")

def xml_pages(path):
    x = open(path, encoding="utf-8").read()
    out = []
    for o in x.split("<OBJECT ")[1:]:
        lines = []
        for l in re.findall(r"<LINE>(.*?)</LINE>", o, re.S):
            ws = [(html.unescape(w).strip(), c) for c, w in
                  re.findall(r'<WORD coords="([^"]*)"[^>]*>([^<]*)</WORD>', l)]
            ws = [w for w in ws if w[0]]
            if ws:
                lines.append(ws)
        out.append(lines)
    return out

def mostly_caps(words):
    letters = [c for c in "".join(words) if c.isalpha()]
    return len(letters) >= 3 and sum(c.isupper() for c in letters) / len(letters) >= 0.75

def witness_tokens(path, vocab, stats):
    toks = []
    for p, lines in enumerate(xml_pages(path)):
        coords = [[c for _, c in l] for l in lines]
        lines = [[w for w, _ in l] for l in lines]
        txt = " ".join(w for l in lines for w in l)
        if "This is a digital copy of a book" in txt or "Usage guidelines" in txt:
            stats["Google notice pages"] += 1
            continue
        if lines and re.match(r"^[A-Za-z°^]{1,2}\s+\S{1,3}$", " ".join(lines[-1])):
            lines, coords = lines[:-1], coords[:-1]          # a printer's signature mark at the foot ("F 81")
            stats["folios and signature marks"] += 1
        for l, cl in zip(lines, coords):
            s = " ".join(l)
            if GOOGLE.search(s):
                stats["Google lines"] += 1
                continue
            if mostly_caps(l):
                stats["capital lines (heads, captions)"] += 1
                continue
            if SIGNATURE.match(s):
                stats["folios and signature marks"] += 1
                continue
            for k, w in enumerate(l):
                toks.append({"t": w, "p": p, "c": cl[k], "eol": k == len(l) - 1})
    out = []
    for t in toks:
        if out and out[-1].get("hy"):
            prev = out.pop()
            head = prev["t"][:-1]
            joined_plain, joined_hy = head + t["t"], head + "-" + t["t"]
            # keep the hyphen only if the book prints the word hyphened (the base's own spelling)
            kh = re.sub(r"[^\w\-]", "", joined_hy).lower()
            t = dict(t, t=joined_hy if kh in vocab else joined_plain, p=prev["p"], c=prev["c"])
            stats["line-end hyphens rejoined"] += 1
        if t["eol"] and re.search(r"[A-Za-z][-¬]$", t["t"]):
            t = dict(t, hy=True)
        out.append(t)
    return out

# ------------------------------------------------------------------ collation (rules 4-6)

ABSTAIN_RUN = 8
CLEAN_PUNCT = re.compile(r"[“”‘’\"'(.,;:!?—-]*")
DEBUG = {}       # place -> word boxes on the base scan (for the review montages; not written out)

def align(bk, wk):
    """Per base token: ("eq"|"sub"|"blk", [witness idx]) or None; insertions by gap."""
    n = len(bk)
    tok, ins = [None] * n, collections.defaultdict(list)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, bk, wk, autojunk=False).get_opcodes():
        if op == "equal":
            for d in range(i2 - i1):
                tok[i1 + d] = ("eq", [j1 + d])
        elif op == "insert":
            ins[i1].extend(range(j1, j2))
        elif op == "replace":
            if "".join(bk[i1:i2]) == "".join(wk[j1:j2]):
                for d in range(i1, i2):     # the same letters, spaced differently
                    tok[d] = ("eq", list(range(j1, j2)) if d == i1 else [])
            elif i2 - i1 == j2 - j1:
                for d in range(i2 - i1):
                    tok[i1 + d] = ("sub", [j1 + d])
            else:
                for d in range(i1, i2):
                    tok[d] = ("blk", list(range(j1, j2)) if d == i1 else [])
    return tok, ins

def abstentions(tok):
    """A witness abstains over runs of 8+ base words it does not match (missing page, garble)."""
    n, out, i = len(tok), [False] * len(tok), 0
    while i < n:
        if tok[i] is None or tok[i][0] != "eq":
            j = i
            while j < n and (tok[j] is None or tok[j][0] != "eq"):
                j += 1
            if j - i >= ABSTAIN_RUN:
                for k in range(i, j):
                    out[k] = True
            i = j
        else:
            i += 1
    return out

def collate(slug, cfg, base_units, wit_paths, reads):
    nmap = name_map(slug)
    stats = collections.Counter()
    names = collections.Counter()
    # base tokens, rules 2-3
    B = []
    token_reads = reads.get("tokens", {})
    used_reads = set()
    for ui, u in enumerate(base_units):
        for ti, t in enumerate(u["text"].split()):
            here = u["id"].split(":", 1)[1] + "#" + str(ti)
            if here in token_reads:                   # a word read on the page image
                t2 = token_reads[here]["out"]
                used_reads.add("tokens/" + here)
                if not t2:
                    continue
            else:
                t2 = base_rules(t, stats)
            if t2 in ("", "-", "|", "©", "'", ",", ".", "_"):
                stats["stray marks standing alone removed"] += 1   # "King of - Troy", "into © the"
                continue
            if t2 in (";", ":", "?", "!") and B and B[-1]["u"] == ui:
                B[-1]["t"] += t2                       # the book's spaced ; : ? ! closed up
                stats["spaced ; : ? ! closed up"] += 1
                continue
            B.append({"raw": t, "t": canon(t2, nmap, names), "u": ui, "i": ti})
    vocab = set()
    for b in B:
        for w in re.findall(r"[\w\-’']+", b["t"].lower()):
            vocab.add(re.sub(r"[^\w\-]", "", w))
    bk = [key(b["t"]) for b in B]
    N = len(B)
    W = []
    for sig, ident, fn, sha, note in cfg["witnesses"]:
        wst = collections.Counter()
        toks = witness_tokens(wit_paths[sig], vocab, wst)
        for t in toks:
            t["t"] = canon(t["t"], nmap)
        wk = [key(t["t"]) for t in toks]
        tok, ins = align(bk, wk)
        ab = abstentions(tok)
        W.append({"sig": sig, "toks": toks, "tok": tok, "ins": ins, "ab": ab, "stats": wst})
    # rule 5b, case: where the letters agree, every witness (two or more) prints the word's first
    # letter in the other case, and the base's own word is not in capitals throughout ("[then" /
    # Then, "How I can" / how), the witnesses' case is taken
    for i in range(N):
        pre, core, suf = split_tok(B[i]["t"])
        if not core or core.isupper() and len(core) > 1:
            continue
        cores = []
        for w in W:
            x = w["tok"][i]
            if w["ab"][i] or not x or x[0] != "eq" or len(x[1]) != 1:
                cores = None
                break
            cores.append(split_tok(w["toks"][x[1][0]]["t"])[1])
        if not cores or len(cores) < 2:
            continue
        firsts = {c[:1] for c in cores}
        if len(firsts) == 1 and core[:1] != cores[0][:1] and core[:1].lower() == cores[0][:1].lower():
            B[i]["t"] = pre + cores[0][:1] + core[1:] + suf
            stats["first letter's case from the witnesses"] += 1
    # rule 5c, quotation marks only: where every witness has the word alone (no punctuation set apart
    # before or after it), the base's opening and closing quotation marks give way when all the
    # witnesses agree. Only quotation marks change: never a stop or a comma. The Google scans' OCR
    # (B) does not vote, its marks being '3, /1, ** ; it may only confirm that a mark is absent.
    QT = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})
    def quotes(x):
        return "".join(ch for ch in x.translate(QT) if ch in "\"'")
    for i in range(N):
        pre, core, suf = split_tok(B[i]["t"])
        if not core:
            continue
        got = {}
        for w in W:
            x = w["tok"][i]
            if w["ab"][i] or not x or x[0] != "eq" or len(x[1]) != 1:
                got = None
                break
            j = x[1][0]
            nxt = w["toks"][j + 1]["t"] if j + 1 < len(w["toks"]) else "x"
            prv = w["toks"][j - 1]["t"] if j > 0 else "x"
            if not key(nxt) or not key(prv) or re.search(r"[“‘\"'*]$", prv):
                got = None
                break
            got[w["sig"]] = split_tok(w["toks"][j]["t"])
        if not got:
            continue
        voters = [v for k, v in got.items() if k != "B"]
        if len(voters) < 2 and not (len(voters) == 1 and "B" in got):
            continue
        # opening marks
        wp = {quotes(v[0]) for v in voters}
        bpq = quotes(pre)
        if len(wp) == 1:
            q = wp.pop()
            if "B" in got and len(voters) < 2 and (q or quotes(got["B"][0]) or re.search(r"[*\"']", got["B"][0])):
                q = None                       # with one voter, only a mark both lack can go
            if q is not None and q != bpq and re.fullmatch(r"[“”‘’\"']*", pre):
                B[i]["t"] = {"": "", '"': "“", "'": "‘", "\"'": "“‘", "'\"": "‘“"}.get(q, pre) + core + suf
                stats["opening quotation marks from the witnesses"] += 1
                pre = split_tok(B[i]["t"])[0]
        if len(voters) >= 2:
            ws = {v[2] for v in voters}
            if len(ws) == 1:
                wsuf = ws.pop()
                plain = lambda x: re.sub(r"[“”‘’\"']", "", x)
                if plain(wsuf) == plain(suf) and quotes(wsuf) != quotes(suf):
                    new = wsuf.translate(str.maketrans({'"': "”", "'": "’", "“": "”", "‘": "’"}))
                    B[i]["t"] = pre + core + new
                    stats["closing quotation marks from the witnesses"] += 1
    # slots: 2i = gap before token i, 2i+1 = token i, 2N = gap at the end
    def gap_diff(g):
        # punctuation alone, set apart by one engine ("me ?"), is not a variant: punctuation is not voted
        lens = [len(w["ins"].get(g, [])) if any(key(w["toks"][j]["t"]) for j in w["ins"].get(g, [])) else 0
                for w in W]
        live = [x for x in lens if x]
        return bool(live) and (len(live) >= 2 or min(live) < ABSTAIN_RUN)
    diff = [False] * (2 * N + 1)
    for i in range(N):
        diff[2 * i + 1] = any(not w["ab"][i] and (w["tok"][i] is None or w["tok"][i][0] != "eq") for w in W)
    for g in range(N + 1):
        diff[2 * g] = gap_diff(g)
    places, s = [], 0
    while s < len(diff):
        if diff[s]:
            e = s
            while e < len(diff) and diff[e]:
                e += 1
            places.append((s, e))
            s = e
        else:
            s += 1
    addr = lambda i: base_units[B[i]["u"]]["id"].split(":", 1)[1] + "#" + str(B[i]["i"])
    out_tokens = {i: [B[i]["t"]] for i in range(N)}   # replaced per place below
    gap_out = collections.defaultdict(list)
    records = []
    counts = collections.Counter()
    for s, e in places:
        toks_i = [(x - 1) // 2 for x in range(s, e) if x % 2 == 1]
        gaps = [x // 2 for x in range(s, e) if x % 2 == 0]
        base_s = " ".join(B[i]["t"] for i in toks_i)
        rd = {}
        for w in W:
            if toks_i and all(w["ab"][i] for i in toks_i):
                continue
            idx = []
            for x in range(s, e):
                if x % 2 == 0:
                    g = x // 2
                    if len(w["ins"].get(g, [])) < ABSTAIN_RUN or sum(1 for v in W if v["ins"].get(g)) >= 2:
                        idx += w["ins"].get(g, [])
                else:
                    i = (x - 1) // 2
                    if w["tok"][i] and not w["ab"][i]:
                        idx += w["tok"][i][1]
            rd[w["sig"]] = " ".join(w["toks"][j]["t"] for j in idx)
        bkey = "".join(bk[i] for i in toks_i)
        votes = collections.Counter(key(v) for v in rd.values())
        votes[bkey] += 1
        top, topn = votes.most_common(1)[0]
        tie = sum(1 for v in votes.values() if v == topn) > 1
        if toks_i:
            at = addr(toks_i[0])
        else:
            g = gaps[0]
            at = "^" + (addr(g) if g < N else "end")
        maxo = max([v for k, v in votes.items() if k != bkey] or [0])
        if not toks_i:
            # rule 6: words the base lacks go in only when two witnesses have them (never before the
            # first word or after the last: front and back matter)
            wv = collections.Counter(key(v) for v in rd.values() if key(v))
            k2, n2 = (wv.most_common(1)[0] if wv else ("", 0))
            g = gaps[0]
            if n2 >= 2 and 0 < g < N:
                by = "witnesses"
                out = next(rd[sig] for sig in ("A", "C", "B") if sig in rd and key(rd[sig]) == k2)
            else:
                by, out = "base", None
        elif votes[bkey] > maxo and (votes[bkey] >= 2 or not rd):
            by, out = "base", None
        elif not tie and topn >= 2 and top != bkey:
            by = "witnesses"
            src = next(sig for sig in ("A", "C", "B") if sig in rd and key(rd[sig]) == top)
            ws = rd[src].split()
            while ws and not key(ws[0]):        # the witness's stray punctuation at the edges
                ws.pop(0)
            while ws and not key(ws[-1]):
                ws.pop()
            if ws:
                # the base's punctuation round the place is kept when it is clean punctuation;
                # otherwise (OCR dirt like "©") the witness's own
                pre0 = split_tok(B[toks_i[0]]["t"])[0]
                suf0 = split_tok(B[toks_i[-1]]["t"])[2]
                p1, c1, s1 = split_tok(ws[0])
                ws[0] = (pre0 if CLEAN_PUNCT.fullmatch(pre0) else p1) + c1 + (s1 if len(ws) > 1 else "")
                p2, c2, s2 = split_tok(ws[-1])
                if len(ws) == 1:
                    p2, c2 = "", ws[0]
                ws[-1] = p2 + c2 + (suf0 if CLEAN_PUNCT.fullmatch(suf0) else s2)
            out = " ".join(ws)
        else:
            by, out = "open", None
        if at in reads:
            by, out = "read", reads[at]["out"]
            used_reads.add(at)
        counts[by] += 1
        rec = {"at": at, "base": base_s, **{k: rd[k] for k in sorted(rd)}, "by": by}
        wa = W[0]
        near = [wa["tok"][i][1][0] for i in toks_i if wa["tok"][i] and wa["tok"][i][1]] or \
               [wa["tok"][i][1][0] for i in range(max(0, (toks_i or gaps)[0] - 3), min(N, (toks_i or gaps)[0] + 3))
                if wa["tok"][i] and wa["tok"][i][1]]
        if near:
            rec["leaf"] = wa["toks"][near[0]]["p"]
            DEBUG.setdefault(slug, {})[at] = [wa["toks"][j]["c"] for j in range(max(0, near[0] - 2), min(len(wa["toks"]), near[0] + 3))
                                              if wa["toks"][j]["p"] == rec["leaf"]]
        if out is not None:
            rec["out"] = out
            if at in reads and reads[at].get("seen"):
                rec["seen"] = reads[at]["seen"]
        if any(B[i]["u"] != B[toks_i[0]]["u"] for i in toks_i) if toks_i else False:
            rec["spans_units"] = True
        records.append(rec)
        if out is not None:
            if toks_i:
                out_tokens[toks_i[0]] = out.split()
                for i in toks_i[1:]:
                    out_tokens[i] = []
            else:
                g = gaps[0]
                gap_out[g] = out.split()
    # assemble unit texts (a gap's words go to the end of the unit before it)
    unit_toks = [[] for _ in base_units]
    for i in range(N + 1):
        if gap_out.get(i):
            unit_toks[B[i - 1]["u"] if i > 0 else 0].extend(gap_out[i])
        if i < N:
            unit_toks[B[i]["u"]].extend(out_tokens[i])
    unit_texts = [" ".join(t for t in ts if t) for ts in unit_toks]
    unused = sorted((set(k for k in reads if not k.startswith("_") and k not in ("structure", "tokens", "illustrations",
                                                                       "illustrations_first_printing"))
                     | set("tokens/" + k for k in token_reads)) - used_reads)
    wstats = {w["sig"]: dict(w["stats"]) for w in W}
    return unit_texts, records, {"places": dict(counts), "base_rules": dict(stats), "names": dict(names),
                                 "witness_rules": wstats, "unused_reads": unused,
                                 "words_base": N}

# ------------------------------------------------------------------ structure (rule 7)

TERMINAL = re.compile(r"[.!?:;”’\"')—]$")

def structure(slug, base_units, unit_texts, reads, nmap):
    st = reads.get("structure", {})
    joins_read = set(st.get("join", []))
    nojoin_read = set(st.get("no_join", []))
    drop_read = set(st.get("drop", []))
    chapters, stats = [], collections.Counter()
    corpus_units = []
    cur = None
    texts = {u["id"].split(":", 1)[1]: t.strip() for u, t in zip(base_units, unit_texts)}
    notes = collections.defaultdict(list)
    # footnotes: the base ran each into the text at its page's foot. A read names the pieces to
    # take out (as the collated text has them), the reference mark's place, and the note as printed.
    for fn in st.get("footnotes", []):
        for piece in fn["pieces"]:
            # a piece runs from its first words to its last, with the marks the base put before it
            # (the note's number read as "1", "''" or a quotation mark)
            t = texts[piece["unit"]]
            a = t.find(piece["from"])
            b = t.find(piece["to"], a)
            if a < 0 or b < 0:
                sys.exit(f"footnote piece not found in {piece['unit']}: {piece['from']}")
            b += len(piece["to"])
            while a > 0 and not t[a - 1].isspace():
                a -= 1
            m = re.search(r"(?:^|\s)(?:1|''|‘|“)\s*$", t[:a])
            if m:
                a = m.start()
            texts[piece["unit"]] = " ".join((t[:a] + " " + t[b:]).split())
        a = fn["anchor"]
        if a["find"] not in texts[a["unit"]]:
            sys.exit(f"footnote anchor not found in {a['unit']}: {a['find']}")
        texts[a["unit"]] = texts[a["unit"]].replace(a["find"], a["replace"], 1)
        notes[a["unit"]].append(fn["mark"] + " " + fn["text"])
        stats["footnotes taken out of the text"] += 1
    for uid in texts:
        # stray marks the base left at a paragraph's end ("Greeks.” -", "them.” |")
        t2 = re.sub(r"(?<=[.!?:;”’])(\s+[-|,©'])+$", "", texts[uid])
        if t2 != texts[uid]:
            texts[uid] = t2
            stats["stray marks at a paragraph's end"] += 1
    for u in base_units:
        uid = u["id"].split(":", 1)[1]
        text = texts[uid]
        if uid in drop_read:
            stats["units dropped (read)"] += 1
            continue
        if not re.search(r"[^\W\d_]", text):
            stats["units left with no letters, dropped"] += 1
            continue
        if re.fullmatch(r"Printed in the United States of America\.?", text):
            stats["colophon dropped"] += 1
            continue
        ch = uid.rsplit(".", 1)[0]
        title = u["ref"].rsplit(", par.", 1)[0]
        title = " ".join(canon(w, nmap) for w in title.split())
        if cur is None or cur["key"] != ch:
            cur = {"key": ch, "title": title, "paragraphs": []}
            chapters.append(cur)
            # a chapter opens on a word in small capitals (THE, ONCE, WHEN): set in capitals.
            # After a one-letter word the next goes too ("A GREAT"); a read can widen it ("KING PRIAM").
            ws = text.split()
            n = st.get("opening_caps", {}).get(uid) or (2 if len(split_tok(ws[0])[1]) == 1 else 1)
            for i in range(min(n, len(ws))):
                pre, core, suf = split_tok(ws[i])
                if core and not core.isupper():
                    ws[i] = pre + core.upper() + suf
                    stats["chapter-opening word set in capitals"] += 1
            text = " ".join(ws)
        unit = {"id": u["id"], "ref": u["ref"], "text": text, "links": u.get("links", []),
                "pages": u.get("pages", []), "printed": u.get("printed", [])}
        if notes.get(uid):
            unit["notes"] = notes[uid]
        corpus_units.append(unit)
        prev = cur["paragraphs"][-1] if cur["paragraphs"] else None
        first = re.sub(r"^\W+", "", text)[:1]
        join = False
        if prev and uid not in nojoin_read:
            if uid in joins_read:
                join, why = True, "read"
            elif first.islower():
                join, why = True, "lower case"
        if join:
            sep = "" if prev["text"].endswith("-") and first.islower() else " "
            if sep == "":
                prev["text"] = prev["text"][:-1]
            prev["text"] += sep + text
            prev["units"].append(u["id"])
            prev["pages"] = sorted(set(prev["pages"]) | set(unit["pages"]))
            prev["printed"] = list(dict.fromkeys(prev["printed"] + unit["printed"]))
            if notes.get(uid):
                prev.setdefault("footnotes", []).extend(notes[uid])
            stats["paragraph joins (" + why + ")"] += 1
        else:
            cur["paragraphs"].append({"text": text, "units": [u["id"]], "pages": list(unit["pages"]),
                                      "printed": list(unit["printed"])})
            if notes.get(uid):
                cur["paragraphs"][-1]["footnotes"] = list(notes[uid])
    return chapters, corpus_units, dict(stats)

# ------------------------------------------------------------------ illustrations

def illustrations(reads):
    return reads.get("illustrations", [])

# ------------------------------------------------------------------ io

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def fetch():
    os.makedirs(WITDIR, exist_ok=True)
    for slug, cfg in BOOKS.items():
        for sig, ident, fn, sha, note in cfg["witnesses"]:
            p = os.path.join(WITDIR, fn)
            if not os.path.exists(p):
                print("fetch", ident, fn)
                tmp = p + ".part"
                urllib.request.urlretrieve(DL.format(id=ident, fn=fn), tmp)
                os.replace(tmp, p)
            got = sha256(p)
            if got != sha:
                sys.exit(f"{fn}: sha256 {got} is not the pinned {sha}; refusing")
    print("witnesses present and pinned")

def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"

def to_md(book):
    L = [f"# {book['title']}", "", f"*{book['subtitle']}* — {book['author']}", "",
         f"First published {book['first_published']}. Collated text: see "
         f"`{book['slug']}.collation.json` and `README.md` beside this file.", ""]
    if book["illustrations"]:
        L += ["## List of Illustrations", ""]
        for il in book["illustrations"]:
            L.append(f"- {il['title']} — {il['facing']}")
        L.append("")
    if book.get("illustrations_first_printing"):
        fp = book["illustrations_first_printing"]
        L += [f"### The first printing's list ({fp['printing']})", "", fp["note"], ""]
        for il in fp["list"]:
            L.append(f"- {il['title']} — {il['facing']}")
        L.append("")
    for n, ch in enumerate(book["chapters"], 1):
        L += [f"## {ch['title']}", ""]
        for p in ch["paragraphs"]:
            L += [p["text"], ""]
            for fnote in p.get("footnotes", []):
                L += [f"> {fnote}", ""]
    return "\n".join(L)

def build(slug, check=False):
    cfg = BOOKS[slug]
    raw = gzip.open(os.path.join(REPO, cfg["base"]["file"]), "rb").read()
    base = json.loads(raw.decode("utf-8"))
    base_units = base["units"]
    wit_paths = {}
    for sig, ident, fn, sha, note in cfg["witnesses"]:
        p = os.path.join(WITDIR, fn)
        if not os.path.exists(p):
            sys.exit(f"missing witness {fn}: run --fetch first")
        if sha256(p) != sha:
            sys.exit(f"{fn}: not the pinned file")
        wit_paths[sig] = p
    rpath = os.path.join(OUTDIR, slug + ".collation-reads.json")
    reads = json.load(open(rpath, encoding="utf-8")) if os.path.exists(rpath) else {}
    unit_texts, records, stats = collate(slug, cfg, base_units, wit_paths, reads)
    nmap = name_map(slug)
    chapters, corpus_units, sstats = structure(slug, base_units, unit_texts, reads, nmap)
    stats["structure"] = sstats
    words = sum(len(p["text"].split()) for c in chapters for p in c["paragraphs"])
    book = {
        "slug": slug, "title": cfg["title"], "subtitle": cfg["subtitle"], "author": cfg["author"],
        "first_published": cfg["first_published"],
        "source": {
            "base": {"file": cfg["base"]["file"], "sha256": sha256(os.path.join(REPO, cfg["base"]["file"])),
                     "unpacked_sha256": hashlib.sha256(raw).hexdigest(),
                     "what": "the Unscanner's re-OCR (tesseract, with layout) of archive.org " + cfg["base"]["scan"],
                     "printing": cfg["base"]["printing"]},
            "witnesses": [{"siglum": s, "archive_id": i, "file": f, "sha256": h, "what": n}
                          for s, i, f, h, n in cfg["witnesses"]],
            "reads": os.path.relpath(rpath, REPO) if reads else None,
            "rights": "US public domain: first published 1906/1907, and every printing used is dated before 1931.",
        },
        "stats": {"chapters": len(chapters),
                  "paragraphs": sum(len(c["paragraphs"]) for c in chapters),
                  "words": words, **stats},
        "illustrations": illustrations(reads),
        **({"illustrations_first_printing": reads["illustrations_first_printing"]}
           if reads.get("illustrations_first_printing") else {}),
        "chapters": [{"n": n, "title": c["title"],
                      "paragraphs": c["paragraphs"]} for n, c in enumerate(chapters, 1)],
        "units": corpus_units,
    }
    outs = {
        slug + ".collated.json": dumps(book),
        slug + ".collation.json": dumps({"slug": slug, "stats": book["stats"], "source": book["source"],
                                         "places": records}),
        slug + ".md": to_md(book),
    }
    bad = []
    for fn, text in outs.items():
        p = os.path.join(OUTDIR, fn)
        if len(text.encode("utf-8")) > 5_000_000:
            sys.exit(f"{fn} is over 5 MB")
        if check:
            if not os.path.exists(p) or open(p, encoding="utf-8").read() != text:
                bad.append(fn)
        else:
            tmp = p + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp, p)
    return book, bad

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("slugs", nargs="*")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    bad_all = []
    for slug in a.slugs or BOOKS:
        book, bad = build(slug, check=a.check)
        s = book["stats"]
        print(f"{slug}: {s['chapters']} chapters, {s['paragraphs']} paragraphs, {s['words']} words; "
              f"places {s['places']}; unused reads {len(s['unused_reads'])}")
        bad_all += bad
    if a.check:
        if bad_all:
            sys.exit("differs from the committed output: " + ", ".join(bad_all))
        print("check: byte-identical")

if __name__ == "__main__":
    main()
