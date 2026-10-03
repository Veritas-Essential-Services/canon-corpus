#!/usr/bin/env python3
"""press_proof.py -- proof a Press book word by word against the scan of its edition.

    python3 pipeline/press_proof.py owen-mortification          # collate, re-read disputed pages, report
    python3 pipeline/press_proof.py owen-mortification --no-tess # collate only (no page re-OCR)

"Word-perfect against the scans" made mechanical. Three witnesses:

  A  the text the Press set (a CCEL or Gutenberg transcription, or our own
     cleaned OCR)
  B  the Internet Archive's OCR of a scan of the SAME edition (ABBYY, from
     archive.org's hocr search text, which also says which page each word is on)
  C  only where A and B disagree on a real word: a fresh Tesseract read of that
     page's image, fetched from archive.org

A and B are aligned word by word (unique 5-gram anchors, then difflib between
anchors), so every word of the book is checked against the printed page. Most
disagreements are OCR noise in B (a word the dictionary does not know where A
has one it does); those are discarded. What is left is classified:

  confirmed   C agrees with B against A, and B's reading is a known word: the
              transcription (A) is wrong. Written as a correction rule to
              pipeline/press_rules/<slug>.json with its evidence (archive.org
              id, leaf, printed page) -- the build applies it and lists it in the
              book's Note on the Text.
  upheld      C agrees with A: B's OCR misread. Nothing to do.
  review      the witnesses split three ways, or C could not find the spot, or
              a word is present in one text and absent from the other: listed
              for a person in docs/press/proof/<slug>.md with page and leaf.

Nothing is "fixed" on two-witness evidence alone, and nothing is fixed when the
scan's reading is not a word the dictionary (or press_words.txt) knows.
"""
import bisect, difflib, gzip, json, os, re, subprocess, sys, time, unicodedata, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import press_build, press_render

IA_DIR = os.path.join(ROOT, "data", "corpus", "press", "ia")

def norm(w):
    w = unicodedata.normalize("NFKD", w)
    w = w.replace("æ", "ae").replace("Æ", "ae").replace("œ", "oe").replace("ſ", "s")
    w = "".join(ch for ch in w if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", w.lower())

TOKEN = re.compile(r"[A-Za-zÀ-ɏͰ-Ͽἀ-῿0-9][A-Za-zÀ-ɏͰ-Ͽἀ-῿0-9'’]*")

# ------------------------------------------------------------- witness A
def book_tokens(doc, with_notes=False):
    """Witness A as (norm, original, block index). Footnotes are left out of
    the running text (the page prints them at its foot, not inline);
    note_tokens() gives them separately."""
    toks = []
    for bi, b in enumerate(doc["blocks"]):
        if b.get("k") not in ("para", "argument", "quote", "heading", "display", "tp", "list"):
            continue
        md = b.get("md") or " ".join(b.get("items", []))
        text = press_render.plain(md)
        for m in TOKEN.finditer(text):
            n = norm(m.group(0))
            if n:
                toks.append((n, m.group(0), bi))
    return toks

def note_tokens(doc):
    """{label: [(norm, original)]} and {label: block index of its call}."""
    out, home = {}, {}
    for bi, b in enumerate(doc["blocks"]):
        for lab in re.findall(r"\[\^([^\]]+)\]", b.get("md", "")):
            home.setdefault(lab, bi)
    for lab, md in doc["notes"].items():
        out[lab] = [(norm(m.group(0)), m.group(0)) for m in TOKEN.finditer(press_render.plain(md)) if norm(m.group(0))]
    return out, home

# ------------------------------------------------------------- witness B
def ia_get(ident, name):
    os.makedirs(IA_DIR, exist_ok=True)
    dest = os.path.join(IA_DIR, name)
    if not os.path.exists(dest):
        press_build.fetch(f"https://archive.org/download/{ident}/{name}", dest)
    return dest

def ocr_witness(ident):
    st = gzip.open(ia_get(ident, f"{ident}_hocr_searchtext.txt.gz"), "rt", encoding="utf-8").read()
    pidx = json.load(gzip.open(ia_get(ident, f"{ident}_hocr_pageindex.json.gz"), "rt"))
    try:
        pn = json.load(open(ia_get(ident, f"{ident}_page_numbers.json"), encoding="utf-8"))["pages"]
        printed = {i: p.get("pageNumber") or "" for i, p in enumerate(pn)}
    except Exception:
        printed = {}
    # pageindex rows are [text_start, text_end, hocr_start, hocr_end]; row L
    # is the page archive.org serves as image n{L-1} and lists as
    # page_numbers[L-1] (checked by eye on Goold vol. 6: row 21 = image n20 = p. 7)
    starts = [p[0] for p in pidx]
    # join words broken across lines: "seduc-\ntions"
    joined = []
    toks = []
    for m in re.finditer(r"([A-Za-zÀ-ɏ]+)-\s*\n\s*([a-zÀ-ɏ]+)|" + TOKEN.pattern, st):
        if m.group(1):
            w, off = m.group(1) + m.group(2), m.start()
        else:
            w, off = m.group(0), m.start()
        n = norm(w)
        if n:
            leaf = bisect.bisect_right(starts, off) - 2
            toks.append((n, w, leaf))
    return toks, printed

# ------------------------------------------------------------- alignment
def align(a, b, k=5):
    """Pairs of matching index ranges, via unique k-gram anchors and difflib
    between them. Returns difflib-style opcodes over the whole of a."""
    def grams(seq):
        d = {}
        for i in range(len(seq) - k + 1):
            g = tuple(seq[i:i + k])
            d[g] = -1 if g in d else i
        return {g: i for g, i in d.items() if i >= 0}
    an = [t[0] for t in a]
    bn = [t[0] for t in b]
    ga, gb = grams(an), grams(bn)
    pairs = sorted((i, gb[g]) for g, i in ga.items() if g in gb)
    # longest increasing chain in b-position (patience-style)
    tails, prev, idx = [], [None] * len(pairs), []
    for n, (i, j) in enumerate(pairs):
        p = bisect.bisect_left(tails, j)
        if p == len(tails):
            tails.append(j); idx.append(n)
        else:
            tails[p] = j; idx[p] = n
        prev[n] = idx[p - 1] if p else None
    chain = []
    n = idx[-1] if idx else None
    while n is not None:
        chain.append(pairs[n]); n = prev[n]
    chain.reverse()
    ops = []
    ai = bi = None
    if chain:
        # the book's first words, before the first anchor: diffed against as
        # many of the witness's words (plus slack) before its first anchor;
        # the witness's extra lead-in is context, not a finding
        i0, j0 = chain[0]
        if i0:
            w0 = max(0, j0 - int(i0 * 1.2) - 10)
            sm = difflib.SequenceMatcher(None, an[:i0], bn[w0:j0], autojunk=False)
            head = [(t, i1, i2, w0 + j1, w0 + j2) for t, i1, i2, j1, j2 in sm.get_opcodes()]
            while head and head[0][0] == "insert":
                head.pop(0)
            ops += head
    for i, j in chain:
        if ai is not None and (i < ai or j < bj):
            continue
        if ai is None:
            ai, bj = i, j
        if i > ai or j > bj:
            sm = difflib.SequenceMatcher(None, an[ai:i], bn[bj:j], autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                ops.append((tag, ai + i1, ai + i2, bj + j1, bj + j2))
        ops.append(("equal", i, i + k, j, j + k))
        ai, bj = i + k, j + k
    if chain and ai < len(an):
        # and the last words, after the last anchor, the same way
        w1 = min(len(bn), bj + int((len(an) - ai) * 1.2) + 10)
        sm = difflib.SequenceMatcher(None, an[ai:], bn[bj:w1], autojunk=False)
        tail = [(t, ai + i1, ai + i2, bj + j1, bj + j2) for t, i1, i2, j1, j2 in sm.get_opcodes()]
        while tail and tail[-1][0] == "insert":
            tail.pop()
        ops += tail
    return ops, (chain[0] if chain else None), (chain[-1] if chain else None)

# ------------------------------------------------------------- witness C
def tess_page(ident, leaf):
    d = os.path.join(IA_DIR, "tess", ident)
    os.makedirs(d, exist_ok=True)
    txt = os.path.join(d, f"{leaf}.txt")
    if os.path.exists(txt):
        return open(txt, encoding="utf-8").read()
    img = os.path.join(d, f"{leaf}.jpg")
    if not os.path.exists(img):
        press_build.fetch(f"https://archive.org/download/{ident}/page/n{leaf}.jpg", img)
    r = subprocess.run(["tesseract", img, "stdout", "-l", "eng", "--psm", "3"], capture_output=True,
                       text=True, env={**os.environ, "OMP_THREAD_LIMIT": "1"})
    out = r.stdout
    press_build.atomic_write(txt, out)
    os.remove(img)
    return out

def third_reading(ident, leaves, before, after, width):
    """Find the disputed spot on the re-read page(s) by the words around it;
    return the tokens the page has between them (normalised), or None."""
    for leaf in leaves:
        t = [norm(m.group(0)) for m in TOKEN.finditer(re.sub(r"-\s*\n\s*", "", tess_page(ident, leaf)))]
        t = [x for x in t if x]
        for i in range(len(t) - len(before) + 1):
            if t[i:i + len(before)] == before:
                j = i + len(before)
                for w in range(0, width + 3):
                    if t[j + w: j + w + len(after)] == after:
                        return t[j: j + w], leaf
        # fuzzy: 2 of the 3 words either side, the nearer word required
        nb, na = len(before), len(after)
        for i in range(len(t) - nb + 1):
            hb = sum(x == y for x, y in zip(t[i:i + nb], before))
            if hb < nb - 1 or t[i + nb - 1] != before[-1]:
                continue
            j = i + nb
            for w in range(0, width + 2):
                seg = t[j + w: j + w + na]
                if len(seg) == na and seg[0] == after[0] and sum(x == y for x, y in zip(seg, after)) >= na - 1:
                    return t[j: j + w], leaf
    return None, None

def prefetch(ident, leaves, workers=4):
    """Re-read many pages at once (Tesseract is single-threaded per page)."""
    from concurrent.futures import ThreadPoolExecutor
    todo = [l for l in sorted(set(leaves))
            if not os.path.exists(os.path.join(IA_DIR, "tess", ident, f"{l}.txt"))]
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda l: _safe_tess(ident, l), todo))

def _safe_tess(ident, leaf):
    try:
        tess_page(ident, leaf)
    except Exception as e:
        print(f"leaf {leaf}: {e}", file=sys.stderr)

# ------------------------------------------------------------- driver
def proof(slug, use_tess=True):
    cat = json.load(open(press_build.CATALOG, encoding="utf-8"))
    e = cat["titles"][slug]
    scan = e.get("scan")
    if not scan:
        raise SystemExit(f"{slug}: the catalog names no scan of its edition (\"scan\")")
    if "ia" in scan:
        ident = scan["ia"]
    else:
        shelf = json.load(open(os.path.join(HERE, f"{scan['shelf']}_shelf.json"), encoding="utf-8"))
        ident = shelf["internet_archive"][scan["volume"]][0]
    doc = press_build.convert(slug, e, press_build.source_file(slug, e))
    a = book_tokens(doc)
    b, printed = ocr_witness(ident)
    ops, first, last = align(a, b)
    words = press_build.wordlist()
    ok = lambda w: press_build.known(w, words)
    matched = sum(i2 - i1 for t, i1, i2, _, _ in ops if t == "equal")
    findings = []
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        A = [x[0] for x in a[i1:i2]]
        B = [x[0] for x in b[j1:j2]]
        if "".join(A) == "".join(B):
            continue  # the same letters, split or joined differently (line-end hyphens)
        if tag == "replace" and len("".join(A)) <= 3 and re.fullmatch(r"[0-9ivxlc]+", "".join(A)):
            continue  # a numeral the OCR misread (5 -> o, iii -> hi)
        if tag == "replace" and re.fullmatch(r"[ivxlc]+", "".join(A)) and re.fullmatch(r"[ivxlc1]+|via|hi", "".join(B)):
            continue  # a chapter numeral: KJV-checked already, and OCR reads numerals worst of all
        # OCR noise: B has garbage where A has good words
        if tag == "replace" and all(ok(x) or x.isdigit() for x in A) and not all(ok(x) for x in B):
            continue
        if tag == "insert":
            # B-only words: running heads, page numbers, line noise, garbled Greek
            origs = [x[1] for x in b[j1:j2]]
            if len(B) > 6 or all(x.isdigit() or not ok(x) for x in B) \
                    or all(o.isupper() or o.isdigit() for o in origs) \
                    or sum(ok(x) and len(x) > 2 for x in B) < 0.6 * len(B):
                continue
        if tag == "delete" and (len(A) > 12 or all(x.isdigit() for x in A)):
            # A-only long runs: matter the scan volume prints elsewhere (or not at all)
            findings.append({"kind": "absent-from-scan", "a": " ".join(x[1] for x in a[i1:i2])[:80],
                             "block": a[i1][2], "n": i2 - i1})
            continue
        if any(re.search(r"[Ͱ-Ͽἀ-῿]", x[1]) for x in a[i1:i2]):
            continue  # Greek: the English OCR cannot witness it
        if tag == "replace" and len(A) == len(B) and all(x.isdigit() for x in A + B):
            continue
        ctx_b = [x[0] for x in a[max(0, i1 - 3): i1]]
        ctx_a = [x[0] for x in a[i2: i2 + 3]]
        leaves = sorted({x[2] for x in b[max(0, j1 - 1): j2 + 1]})
        f = {"kind": tag, "a": " ".join(x[1] for x in a[i1:i2]), "b": " ".join(x[1] for x in b[j1:j2]),
             "before": " ".join(x[1] for x in a[max(0, i1 - 4): i1]),
             "after": " ".join(x[1] for x in a[i2: i2 + 4]), "block": a[min(i1, len(a) - 1)][2],
             "leaf": leaves, "page": [printed.get(l, "") for l in leaves]}
        f["_ctx"] = (ctx_b, ctx_a, max(len(A), len(B)), A, B)
        findings.append(f)
    # witness C: re-read the disputed pages (in parallel), then vote
    pending = [f for f in findings if "_ctx" in f]
    if use_tess:
        prefetch(ident, [l + d for f in pending for l in f["leaf"] for d in (0, 1, -1) if l + d >= 0])
    for f in pending:
        ctx_b, ctx_a, width, A, B = f.pop("_ctx")
        f["verdict"] = "review"
        if not use_tess or len(ctx_b) < 3 or len(ctx_a) < 3:
            continue
        near = sorted({l + d for l in f["leaf"] for d in (0, 1, -1) if l + d >= 0})
        c, leaf = third_reading(ident, near, ctx_b, ctx_a, width)
        if leaf is not None:
            f["leaf"], f["page"] = [leaf], [printed.get(leaf, "")]
        if c is None:
            continue
        f["c"] = " ".join(c)
        if c == A:
            f["verdict"] = "upheld"
        elif c == B and all(ok(x) for x in B):
            f["verdict"] = "confirmed"

    # footnotes: each is looked for in the scan near where its call was aligned
    nt, home = note_tokens(doc)
    a_to_b = {}
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            for d in range(i2 - i1):
                a_to_b[i1 + d] = j1 + d
    block_first = {}
    for i, t in enumerate(a):
        block_first.setdefault(t[2], i)
    bn = [x[0] for x in b]
    notes_checked = notes_missing = 0
    for lab, toks in nt.items():
        if not toks or lab not in home:
            continue
        ai = block_first.get(home[lab])
        bj = next((a_to_b[k] for k in range(ai, ai + 400) if k in a_to_b), None) if ai is not None else None
        if bj is None:
            continue
        lo, hi = max(0, bj - 200), min(len(b), bj + 1500)
        A = [t[0] for t in toks]
        sm = difflib.SequenceMatcher(None, A, bn[lo:hi], autojunk=False)
        best = max(sm.get_matching_blocks(), key=lambda m: m.size)
        if best.size < min(3, len(A)):
            if all(re.fullmatch(r"[0-9ivxlc]+|[a-z]{2,6}", x) for x in A) and len(A) <= 8:
                continue  # a bare scripture reference (KJV-checked already); OCR mangles these
            notes_missing += 1
            findings.append({"kind": "note-not-found", "a": " ".join(t[1] for t in toks)[:80], "b": "",
                             "before": "", "after": "", "block": home[lab], "leaf": [b[bj][2]],
                             "page": [printed.get(b[bj][2], "")], "verdict": "review", "note": lab})
            continue
        notes_checked += 1
        start = lo + best.b - best.a
        win = bn[max(0, start): start + len(A) + 8]
        sm2 = difflib.SequenceMatcher(None, A, win, autojunk=False)
        for tag, i1, i2, j1, j2 in sm2.get_opcodes():
            if tag == "equal" or tag == "insert" and j1 >= len(A):
                continue
            AA, BB = A[i1:i2], win[j1:j2]
            if "".join(AA) == "".join(BB) or (AA and all(ok(x) or x.isdigit() for x in AA) and BB
                                                 and not all(ok(x) for x in BB)):
                continue
            if any(re.search(r"[\u0370-\u03FF\u1F00-\u1FFF]", t[1]) for t in toks[i1:i2]) or not AA and not BB:
                continue
            if tag == "insert" and (all(not ok(x) for x in BB) or i1 == len(A)):
                continue
            findings.append({"kind": "note-" + tag, "a": " ".join(t[1] for t in toks[i1:i2]),
                             "b": " ".join(BB), "before": " ".join(t[1] for t in toks[max(0, i1 - 3):i1]),
                             "after": " ".join(t[1] for t in toks[i2:i2 + 3]), "block": home[lab],
                             "leaf": [b[min(len(b) - 1, max(0, start))][2]], "page": [printed.get(b[max(0, start)][2], "")],
                             "verdict": "review", "note": lab})
    # rules first: writing them can send a confirmed finding back to review,
    # and the counts below must agree with the rows
    write_rules(slug, ident, doc, findings)
    res = {"slug": slug, "scan": ident, "notes_checked": notes_checked, "notes_not_found": notes_missing, "book_words": len(a), "scan_words": len(b),
           "aligned_words": matched, "coverage": round(matched / max(1, len(a)), 4),
           "findings": findings,
           "counts": {v: sum(1 for f in findings if (f.get("verdict") if f["kind"] != "absent-from-scan" else f["kind"]) == v)
                      for v in ("confirmed", "upheld", "review", "absent-from-scan")},
           "checked": time.strftime("%Y-%m-%d")}
    press_build.atomic_write(os.path.join(press_build.OUT, slug, "proof.json"),
                             json.dumps(res, indent=1, ensure_ascii=False))
    write_sheet(slug, e, res)
    return res

def write_rules(slug, ident, doc, findings):
    """Confirmed readings become correction rules (merged, never duplicated)."""
    p = os.path.join(press_build.RULES, f"{slug}.json")
    rules = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    have = {(r["find"], r["replace"]) for r in rules.get("corrections", [])}
    for f in findings:
        if f.get("verdict") == "confirmed" and f["kind"] != "replace":
            # no rule is written for an insertion or deletion: a person places it
            f["verdict"] = "review"; f["why"] = "confirmed, but an insertion or deletion is left to a person"
        if f.get("verdict") != "confirmed" or f["kind"] != "replace":
            continue
        md = doc["blocks"][f["block"]].get("md", "")
        # the smallest unique stretch of markdown holding the bad word(s), unique
        # as a whole word too (a rule must never land inside a longer word)
        def once(t):
            rx = re.compile(r"(?<![A-Za-z])" + re.escape(t) + r"(?![A-Za-z])")
            return (sum(b.get("md", "").count(t) for b in doc["blocks"]) == 1 and
                    sum(len(rx.findall(b.get("md", ""))) for b in doc["blocks"]) == 1)
        bad = f["a"]
        if not (md.count(bad) == 1 and once(bad)):
            ctx = f["before"].split()[-1:] + [bad]
            bad2 = " ".join(ctx)
            if not once(bad2):
                f["verdict"] = "review"; f["why"] = "confirmed, but no unique place to apply it"
                continue
            find, repl = bad2, bad2.replace(bad, f["b"])
        else:
            find, repl = bad, f["b"]
        if (find, repl) in have:
            continue
        rules.setdefault("corrections", []).append({
            "find": find, "replace": repl, "count": 1,
            "why": f"the scan reads “{f['b']}” (archive.org {ident}, leaf {','.join(map(str, f['leaf']))}, "
                   f"printed p. {','.join(x for x in f['page'] if x) or '?'}): its OCR and a fresh Tesseract "
                   f"read agree against the transcription",
            "evidence": {"ia": ident, "leaf": f["leaf"], "page": f["page"], "ocr": f["b"], "tesseract": f.get("c")},
            "by": "press_proof"})
        have.add((find, repl))
    if rules:
        press_build.atomic_write(p, json.dumps(rules, indent=1, ensure_ascii=False) + "\n")

def write_sheet(slug, e, res):
    c = res["counts"]
    L = [f"# Proof sheet: {e['title']}", "",
         f"`{slug}` collated word by word against archive.org `{res['scan']}` "
         f"({res['checked']}; `python3 pipeline/press_proof.py {slug}`).", "",
         f"- Words in the book: {res['book_words']:,}; aligned to the scan: {res['aligned_words']:,} "
         f"({res['coverage']:.1%})",
         f"- Transcription errors confirmed by the scan and corrected: **{c['confirmed']}** "
         f"(rules in `pipeline/press_rules/{slug}.json`)",
         f"- Scan OCR misreads, transcription upheld: {c['upheld']}",
         f"- For a person to look at: **{c['review']}**",
         f"- Passages the scan volume does not carry: {c['absent-from-scan']}",
         f"- Footnotes checked against the page: {res['notes_checked']} (not found on the page: {res['notes_not_found']})", ""]
    rev = [f for f in res["findings"] if f.get("verdict") == "review"]
    if rev:
        L += ["## To look at", "",
              "Each row: what the book prints, what the scan's OCR reads, a fresh re-read of the page "
              "(blank: the spot could not be found on it), and where to look. Answer by adding a "
              "correction to the rules file, or leave the book as it is.", "",
              "| # | Book | Scan OCR | Re-read | Leaf (printed p.) | Around |", "|---:|---|---|---|---|---|"]
        for n, f in enumerate(rev, 1):
            loc = ", ".join(f"{l} ({p})" if p else str(l) for l, p in zip(f["leaf"], f["page"]))
            L.append(f"| {n} | {f['a'] or '∅'} | {f['b'] or '∅'} | {f.get('c', '')} | {loc} | "
                     f"…{f['before'][-25:]} ⟨⟩ {f['after'][:25]}… |")
    press_build.atomic_write(os.path.join(ROOT, "docs", "press", "proof", f"{slug}.md"), "\n".join(L) + "\n")



# ===================================================================== OCR books
# A book set from a scan has no independent transcription to check against:
# its text IS one OCR (ABBYY, archive.org's). The second witness is a fresh
# Tesseract read of every page in the treatise. Two different engines reading
# the same page and agreeing is strong evidence; where they disagree:
#   ABBYY's word unknown, Tesseract's known   -> an OCR fix (applied, listed)
#   ABBYY's word known, Tesseract's unknown   -> ABBYY upheld
#   both known and different, or both unknown -> a person looks at the page
RE_ANCHOR = re.compile(r'\[\]\{#[^}]*leaf="(\d+)"[^}]*\}')

def book_tokens_leaves(doc):
    toks, leaf = [], None
    for bi, b in enumerate(doc["blocks"]):
        if b.get("k") not in ("para", "heading", "argument", "quote"):
            continue
        md = b.get("md", "")
        pos = 0
        for m in list(RE_ANCHOR.finditer(md)) + [None]:
            seg = md[pos: m.start() if m else len(md)]
            for t in TOKEN.finditer(press_render.plain(seg)):
                n = norm(t.group(0))
                if n:
                    toks.append((n, t.group(0), bi, leaf))
            if m:
                leaf = int(m.group(1))
                pos = m.end()
    return toks

def tess_tokens(ident, leaves):
    out = []
    for leaf in leaves:
        txt = re.sub(r"-\s*\n\s*(?=[a-z])", "", tess_page(ident, leaf))
        for t in TOKEN.finditer(txt):
            n = norm(t.group(0))
            if n:
                out.append((n, t.group(0), leaf))
    return out

def match_case(src, new):
    if src.isupper() and len(src) > 1:
        return new.upper()
    if src[:1].isupper():
        return new[:1].upper() + new[1:]
    return new

PREFIXES = {"co", "re", "pre", "self", "fore", "over", "under", "out", "non", "anti"}

def plausible(an, bn, ao):
    """A fix only when Tesseract's word could be a misread of ABBYY's: close in
    spelling, more than one letter, not '&c.' (which tokenises to 'c'), and not
    a split that may have lost a hyphen ('co partners' for 'co-partners')."""
    if len(bn.replace(" ", "")) < 2 or "&" in ao or re.fullmatch(r"[fS]e?c", ao):
        return False
    if " " in bn and bn.split()[0].lower() in PREFIXES:
        return False
    return difflib.SequenceMatcher(None, an.lower(), bn.replace(" ", "").lower()).ratio() >= 0.6

def proof_ocr(slug):
    cat = json.load(open(press_build.CATALOG, encoding="utf-8"))
    e = cat["titles"][slug]
    src = e["source"]
    ident = src.get("ia") or json.load(open(os.path.join(HERE, f"{src['shelf']}_shelf.json"),
                                            encoding="utf-8"))["internet_archive"][src["volume"]][0]
    lo, hi = src["leaves"]
    leaves = list(range(lo, hi + 1))
    prefetch(ident, leaves)
    doc = press_build.convert(slug, e, press_build.source_file(slug, e))
    a = book_tokens_leaves(doc)
    b = tess_tokens(ident, leaves)
    ops, _, _ = align(a, b, k=4)
    words = press_build.wordlist()
    ok = lambda w: press_build.known(w, words)
    fixes, review, upheld = [], [], 0
    for tag, i1, i2, j1, j2 in ops:
        if tag != "replace":
            continue
        A, B = a[i1:i2], b[j1:j2]
        if "".join(x[0] for x in A) == "".join(x[0] for x in B):
            continue
        if len(A) == len(B):
            pairs = list(zip(A, B))
        elif len(A) == 1 and len(B) == 2 and ok(B[0][0]) and ok(B[1][0]) and not ok(A[0][0]):
            # ABBYY ran two words together ("andone" -> "and one")
            pairs = [(A[0], (B[0][0] + " " + B[1][0], B[0][1] + " " + B[1][1], B[0][2]))]
        elif len(A) == 2 and len(B) == 1 and ok(B[0][0]) and not (ok(A[0][0]) and ok(A[1][0])):
            # ABBYY split one word ("afi ection")
            pairs = [((A[0][0] + A[1][0], A[0][1] + " " + A[1][1], A[0][2], A[0][3]), B[0])]
        elif all(ok(x[0]) or x[0].isdigit() for x in A) and not all(ok(x[0]) for x in B):
            upheld += len(A)        # ABBYY's words are words; Tesseract's run is not
            continue
        else:
            review.append({"a": " ".join(x[1] for x in A), "b": " ".join(x[1] for x in B),
                           "leaf": A[0][3], "before": " ".join(x[1] for x in a[max(0, i1 - 4):i1]),
                           "after": " ".join(x[1] for x in a[i2:i2 + 4])})
            continue
        for (an, ao, abi, aleaf), (bn, bo, bleaf) in pairs:
            if an == bn:
                continue
            aok = ok(an) or an.isdigit()
            bok = all(ok(x) for x in bn.split())
            if aok and (not bok or (len(bn) < len(an) and an.startswith(bn))):
                upheld += 1         # Tesseract misread, or read only the start of the word
            elif bok and not aok and not re.search(r"\d", bo) and plausible(an, bn, ao):
                fixes.append({"leaf": aleaf, "from": ao, "to": match_case(ao.split()[0], bo),
                              "why": "ABBYY and Tesseract disagree; only Tesseract's reading is a word",
                              "by": "press_proof"})
            else:
                review.append({"a": ao, "b": bo, "leaf": aleaf})
    # merge the fixes into the rules file
    p = os.path.join(press_build.RULES, f"{slug}.json")
    rules = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    have = {(f["leaf"], f["from"]) for f in rules.get("ocr_fixes", [])}
    new = []
    for f in fixes:
        if (f["leaf"], f["from"]) not in have and f["leaf"] is not None:
            have.add((f["leaf"], f["from"]))
            new.append(f)
    rules.setdefault("ocr_fixes", []).extend(new)
    press_build.atomic_write(p, json.dumps(rules, indent=1, ensure_ascii=False) + "\n")
    matched = sum(i2 - i1 for t, i1, i2, _, _ in ops if t == "equal")
    res = {"slug": slug, "scan": ident, "mode": "two-engine", "book_words": len(a), "tesseract_words": len(b),
           "agreeing_words": matched, "agreement": round(matched / max(1, len(a)), 4),
           "ocr_fixes_new": len(new), "ocr_fixes_total": len(rules["ocr_fixes"]), "upheld": upheld,
           "review": review, "checked": time.strftime("%Y-%m-%d")}
    press_build.atomic_write(os.path.join(press_build.OUT, slug, "proof.json"),
                             json.dumps(res, indent=1, ensure_ascii=False))
    L = [f"# Proof sheet: {e['title']}", "",
         f"`{slug}` is set from the OCR of archive.org `{ident}` (leaves {lo}-{hi}). Proofed by a second "
         f"engine: every page re-read with Tesseract and collated word by word ({res['checked']}).", "",
         f"- Words: {len(a):,}; the two engines agree on {matched:,} ({res['agreement']:.1%})",
         f"- OCR errors fixed where only one engine's reading is a word: **{res['ocr_fixes_total']}** "
         f"(`pipeline/press_rules/{slug}.json`, `ocr_fixes`)",
         f"- ABBYY upheld against a Tesseract misread: {upheld}",
         f"- For a person to look at: **{len(review)}**", ""]
    if review:
        L += ["| # | ABBYY | Tesseract | Leaf |", "|---:|---|---|---|"]
        for n, r in enumerate(review[:400], 1):
            L.append(f"| {n} | {r['a'] or '∅'} | {r['b'] or '∅'} | {r['leaf']} |")
        if len(review) > 400:
            L.append(f"\n…and {len(review) - 400} more in data/press/{slug}/proof.json.")
    press_build.atomic_write(os.path.join(ROOT, "docs", "press", "proof", f"{slug}.md"), "\n".join(L) + "\n")
    return res

if __name__ == "__main__":
    cat = json.load(open(press_build.CATALOG, encoding="utf-8"))
    slug = sys.argv[1]
    if cat["titles"][slug]["source"]["kind"] == "ia-extract":
        r = proof_ocr(slug)
        print(json.dumps({k: r[k] for k in ("book_words", "agreeing_words", "agreement", "ocr_fixes_new",
                                              "ocr_fixes_total", "upheld")}, ensure_ascii=False), "review", len(r["review"]))
    else:
        r = proof(slug, use_tess="--no-tess" not in sys.argv)
        print(json.dumps({k: r[k] for k in ("book_words", "scan_words", "aligned_words", "coverage", "counts")}))
