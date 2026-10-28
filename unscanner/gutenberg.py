"""Gutenberg's proofread text laid onto the scan's word boxes.

Adam, 2026-10-28: *"Diff the Gutenberg proofread text against the OCR,"* settle what has an obviously
right answer, and bring him only the real ties.

The OCR knows WHERE every word is printed and is sometimes wrong about WHAT it says. A Project
Gutenberg transcription was proofread by people, page by page, and knows what it says but not where.
Aligned word by word, the two make a text layer that is both in the right place and right.

Both texts are cut into the same pieces: words split at spaces, hyphens and dashes, compared in lower
case with punctuation dropped. Unique four-word runs found once in each text anchor the alignment; the
longest chain of anchors in order (a longest increasing subsequence) fixes it; the stretches between
anchors are aligned by difflib. Each difference is then sorted:

| class | what it looks like | rule |
|---|---|---|
| `equal` | the same word | keep, with Gutenberg's spelling and punctuation |
| `spacing` | the same letters, cut differently: `run- ning` / `running`, `adrought` / `a drought` | Gutenberg's word, spread over the OCR boxes |
| `misread` | the same length of text, mostly the same letters: `saword` / `sword`, `kav` / `kay` | Gutenberg (it was proofread) |
| `furniture` | OCR words Gutenberg leaves out: folios, running heads, plate lettering | keep the OCR; they are on the page |
| `gutenberg_omits` | three or more real words, read with confidence, that Gutenberg does not have | keep the OCR: it is printed. In Pyle's King Arthur these were whole lines Gutenberg dropped at page breaks |
| `sidenote` / `caption` | OCR words that Gutenberg prints elsewhere, as `[Sidenote: ...]` or `[Illustration: ...]` | matched in a second pass against those, near the page |
| `unread` | Gutenberg words with no OCR box (a decorated initial, a line the OCR lost) | counted; no box to put them in |
| `noise` | OCR pieces that match nothing and are not good text (ink in a picture, a sidenote read badly) | keep the OCR's reading unless under 30% confident |
| `print_typo` | the OCR sure of itself, and its word is Gutenberg's with two letters swapped or one dropped or added | perhaps the PRINT is wrong and Gutenberg corrected it silently: a person looks. In King Arthur, two were: *Kinght* and *decended* |
| `dispute` | two different real words (both in the book's vocabulary, the OCR sure of itself) | neither text wins by rule: a person looks at the scan |

A dispute is decided by looking at the scan, never by preferring one source; the decision and who made
it go into the decisions file, and only those still undecided go to Adam.
"""
import bisect
import difflib
import glob
import json
import os
import re

from . import scan as S

SPLIT = re.compile(r"[\s—–-]+")


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower().replace("ſ", "s"))


def pg_body(path):
    """Gutenberg .txt -> (body, notes). body = [original token]; notes = [(kind, token, body position)]
    for the sidenotes and illustration captions, which Gutenberg moves off the printed line."""
    s = open(path, encoding="utf-8").read()
    a = s.find("*** START OF")
    b = s.find("*** END OF")
    s = s[s.find("\n", a) + 1:b] if a >= 0 else s
    body, notes, pos = [], [], 0
    clean = lambda txt: [t.replace("_", "").replace("=", "") for t in SPLIT.split(txt) if norm(t)]
    for m in re.finditer(r"\[(Sidenote|Illustration)(?::\s*(.*?))?\]", s, re.S):
        body += clean(s[pos:m.start()])
        kind = "sidenote" if m.group(1) == "Sidenote" else "caption"
        notes += [(kind, t, len(body)) for t in clean(m.group(2) or "")]
        pos = m.end()
    body += clean(s[pos:])
    return body, notes


ROMAN = re.compile(r"^[ivxlc]+$")
LOOK = str.maketrans({"1": "i", "|": "i", "0": "o", "5": "s", "8": "b"})


def ocr_words(hocr_dir):
    """All pages in leaf order -> [{page, line, word, t, n, bbox, conf, furniture}], one entry per PIECE
    of a word (a word split at hyphens has several pieces; `word` ties them back). `furniture` marks
    running heads (a line's words recurring on 3+ pages) and folios (a line of numbers only)."""
    out, pages = [], []
    for p in sorted(glob.glob(os.path.join(hocr_dir, "*.hocr"))):
        h = S.parse_hocr(p)
        pages.append((os.path.splitext(os.path.basename(p))[0], h["lines"], h["h"]))
    key = lambda line: " ".join(norm(w["t"]) for w in line["words"] if not norm(w["t"]).isdigit())
    seen = {}
    for page, lines, _ in pages:
        for k in {key(l) for l in lines if key(l)}:
            seen[k] = seen.get(k, 0) + 1
    for page, lines, ph in pages:
        top = min((l["bbox"][1] for l in lines), default=0)
        for li, line in enumerate(lines):
            ns = [norm(w["t"]) for w in line["words"]]
            # a running head: the page's top line, short, with a folio at one end (Pyle's right-hand
            # heads name the chapter's topic, so they do not recur)
            alpha = [w["t"] for w in line["words"] if re.search("[A-Za-z]{2}", w["t"])]
            caps = sum(t.isupper() for t in alpha) >= 0.6 * len(alpha) if alpha else False
            head = line["bbox"][1] < 0.1 * ph and 0 < len(ns) <= 10 and (
                (line["bbox"][1] == top and (ns[0].isdigit() or ns[-1].isdigit())) or caps)
            furn = head or seen.get(key(line), 0) >= 3 or all(n.isdigit() or ROMAN.match(n) or not n for n in ns)
            for wi, w in enumerate(line["words"]):
                parts = [x for x in SPLIT.split(w["t"]) if norm(x)]
                for k, x in enumerate(parts):
                    out.append({"page": page, "line": li, "word": wi, "part": k, "parts": len(parts),
                                "t": x, "n": norm(x), "bbox": w["bbox"], "conf": w["conf"], "full": w["t"],
                                "furniture": bool(furn)})
    return out


def _anchors(a, b, k=4):
    """Pairs (i, j) where the k-gram starting there occurs exactly once in each sequence, in order."""
    def grams(seq):
        d = {}
        for i in range(len(seq) - k + 1):
            d.setdefault(tuple(seq[i:i + k]), []).append(i)
        return {g: v[0] for g, v in d.items() if len(v) == 1}
    ga, gb = grams(a), grams(b)
    pairs = sorted((i, gb[g]) for g, i in ga.items() if g in gb)
    # longest chain increasing in both (patience sort on j)
    tails, tails_idx, prev = [], [], [None] * len(pairs)
    for n, (i, j) in enumerate(pairs):
        x = bisect.bisect_left(tails, j)
        if x == len(tails):
            tails.append(j); tails_idx.append(n)
        else:
            tails[x] = j; tails_idx[x] = n
        prev[n] = tails_idx[x - 1] if x else None
    chain, n = [], tails_idx[-1] if tails_idx else None
    while n is not None:
        chain.append(pairs[n]); n = prev[n]
    return chain[::-1]


def align(a, b):
    """-> list of opcodes (tag, i1, i2, j1, j2) over the whole of a and b."""
    ops, pi, pj = [], 0, 0
    for i, j in _anchors(a, b) + [(len(a), len(b))]:
        if i < pi or j < pj:
            continue
        sm = difflib.SequenceMatcher(None, a[pi:i], b[pj:j], autojunk=False)
        ops += [(t, pi + i1, pi + i2, pj + j1, pj + j2) for t, i1, i2, j1, j2 in sm.get_opcodes()]
        pi, pj = i, j
    return ops


def _sim(x, y):
    return difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()


def _typo(a, b):
    """'swap', 'drop', 'extra' when the OCR word is the Gutenberg word with two neighbouring letters
    swapped or one letter missing or added: the shape of a compositor's slip, not of a misread."""
    if len(a) == len(b) and sorted(a) == sorted(b) and a != b:
        d = [k for k in range(len(a)) if a[k] != b[k]]
        if len(d) == 2 and d[1] == d[0] + 1:
            return "swap"
    if len(a) + 1 == len(b) and any(b[:k] + b[k + 1:] == a for k in range(len(b))):
        return "drop"
    if len(a) == len(b) + 1 and any(a[:k] + a[k + 1:] == b for k in range(len(a))):
        return "extra"
    return None


def classify(ocr, body, vocab):
    """Walk the opcodes; -> (assign: {ocr index: Gutenberg token}, rows: one per difference)."""
    a = [w["n"] for w in ocr]
    b = [norm(t) for t in body]
    assign, rows = {}, []

    def row(cls, I, J, **kw):
        I, J = list(I), list(J)
        r = {"class": cls, "ocr": [ocr[i]["t"] for i in I], "pg": [body[j] for j in J],
             "i": [I[0], I[-1] + 1] if I else None, "j": [J[0], J[-1] + 1] if J else None,
             "page": ocr[I[0]]["page"] if I else None}
        r.update(kw)
        rows.append(r)

    def ocr_only(I, j_at):
        I = list(I)
        if not I:
            return
        furn = [i for i in I if ocr[i]["furniture"]]
        rest = [i for i in I if not ocr[i]["furniture"]]
        if furn:
            row("furniture", furn, [], at=j_at)
        if rest:
            real = sum(vocab.get(ocr[i]["n"], 0) >= 2 for i in rest)
            conf = sum(ocr[i]["conf"] for i in rest) / len(rest)
            cls = "gutenberg_omits" if len(rest) >= 3 and real >= 0.7 * len(rest) and conf >= 80 else "noise"
            row(cls, rest, [], at=j_at, conf=round(conf))

    for tag, i1, i2, j1, j2 in align(a, b):
        if tag == "equal":
            for d in range(i2 - i1):
                assign[i1 + d] = body[j1 + d]
            continue
        if tag == "delete":
            ocr_only(range(i1, i2), j1)
            continue
        if tag == "insert":
            row("unread", [], range(j1, j2))
            continue
        I = [i for i in range(i1, i2) if not ocr[i]["furniture"]]
        F = [i for i in range(i1, i2) if ocr[i]["furniture"]]
        J = list(range(j1, j2))
        if F:                                           # a running head or folio inside a split word
            row("furniture", F, [], at=j1)
        if not I:
            row("unread", [], J)
            continue
        oa = "".join(a[i] for i in I)
        pb = "".join(b[j] for j in J)
        if oa == pb or oa.translate(LOOK) == pb.translate(LOOK):
            _spread(ocr, body, I, J, assign)
            row("spacing" if oa == pb else "misread", I, J)
            continue
        # a decorated initial the OCR could not read: the printed word minus its first letter(s)
        first = norm(body[J[0]])
        if len(I) == len(J) and 1 <= len(first) - len(a[I[0]]) <= 2 and first.endswith(a[I[0]]) and a[I[0]] \
                and all(a[x] == b[y] for x, y in zip(I[1:], J[1:])):
            _spread(ocr, body, I, J, assign)
            row("initial", I, J)
            continue
        conf = sum(ocr[i]["conf"] for i in I) / len(I)
        sim = _sim(oa, pb)
        if len(I) == 1 and len(J) == 1 and vocab.get(oa, 0) >= 2 and ocr[I[0]]["conf"] >= 80:
            row("dispute", I, J, conf=round(conf), sim=round(sim, 2))   # two real words: look
            continue
        if len(I) == 1 and len(J) == 1 and len(pb) > 3 and conf >= 85 and _typo(oa, pb):
            # the OCR is sure and the difference has a compositor's shape: perhaps the print itself
            # is wrong and Gutenberg silently corrected it. A person looks; until then, the print.
            row("print_typo", I, J, conf=round(conf), shape=_typo(oa, pb))
            continue
        if sim >= 0.6 or (max(len(I), len(J)) <= 2 and sim >= 0.4):
            _spread(ocr, body, I, J, assign)
            row("misread", I, J, conf=round(conf), sim=round(sim, 2))
            continue
        if conf < 50:
            row("noise", I, [], at=j1, conf=round(conf))
            row("unread", [], J)
            continue
        # try: some OCR words at each end make the Gutenberg words, the middle is something else
        best = None
        for p in range(1, len(I) + 1):
            for q in range(p, len(I) + 1):
                cand = "".join(a[i] for i in I[:p] + I[q:])
                sc = _sim(cand, pb)
                if sc >= 0.8 and (best is None or sc > best[0]):
                    best = (sc, p, q)
        if best:
            _, p, q = best
            _spread(ocr, body, I[:p] + I[q:], J, assign)
            row("misread" if best[0] < 1 else "spacing", I[:p] + I[q:], J, sim=round(best[0], 2))
            ocr_only(I[p:q], j1)
            continue
        ocr_only(I, j1)
        row("unread", [], J)
    return assign, rows


def _spread(ocr, body, I, J, assign):
    """Gutenberg's words over the OCR pieces: one to one when the counts agree, else its letters spread
    in proportion to the pieces' lengths (a word broken over a line keeps both halves findable)."""
    I, J = list(I), list(J)
    if len(I) == len(J):
        for i, j in zip(I, J):
            assign[i] = body[j]
        return
    if len(I) == 1:
        assign[I[0]] = " ".join(body[j] for j in J)
        return
    letters = "".join(body[j] for j in J) if len(J) == 1 else " ".join(body[j] for j in J)
    lens = [max(1, len(ocr[i]["t"])) for i in I]
    tot, pos = sum(lens), 0
    for k, i in enumerate(I):
        end = len(letters) if k == len(I) - 1 else round(len(letters) * sum(lens[:k + 1]) / tot)
        assign[i] = letters[pos:end].strip()
        pos = end


def second_pass(ocr, notes, rows, assign, window=400):
    """Sidenotes and captions. Gutenberg moves them off the printed line; the OCR reads them in small
    pieces between the body lines, often badly (they are set in small italic). So per page, every OCR
    piece still unplaced is gathered in reading order and aligned against the notes Gutenberg prints
    near that page's text."""
    used = set()
    by_page = {}
    for r in rows:
        if r["class"] in ("gutenberg_omits", "noise") and r["i"]:
            by_page.setdefault(r["page"], []).append(r)
    for page, rs in by_page.items():
        I = [i for r in rs for i in range(r["i"][0], r["i"][1])
             if not ocr[i]["furniture"] and i not in assign and ocr[i]["t"] in r["ocr"]]
        if len(I) < 2:
            continue
        at = sum(r["at"] for r in rs) / len(rs)
        cand = [k for k, (_, _, pos) in enumerate(notes) if abs(pos - at) <= window and k not in used]
        if not cand:
            continue
        a = [ocr[i]["n"] for i in I]
        b = [norm(notes[k][1]) for k in cand]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        placed = set()
        for t, a1, a2, b1, b2 in sm.get_opcodes():
            if t == "equal" or (t == "replace" and a2 - a1 == b2 - b1):
                for d in range(a2 - a1):
                    if t == "equal" or _sim(a[a1 + d], b[b1 + d]) >= 0.5:
                        assign[I[a1 + d]] = notes[cand[b1 + d]][1]
                        used.add(cand[b1 + d]); placed.add(I[a1 + d])
            elif t == "replace" and _sim("".join(a[a1:a2]), "".join(b[b1:b2])) >= 0.6:
                _spread(ocr, [notes[k][1] for k in cand], I[a1:a2], range(b1, b2), assign)
                used.update(cand[b1:b2]); placed.update(I[a1:a2])
        for r in rs:
            n = sum(i in placed for i in range(r["i"][0], r["i"][1]))
            if n:
                r["class"] = notes[cand[0]][0] if n >= len(r["ocr"]) / 2 else r["class"]
                r["matched"] = n
    return used


def moved_pass(ocr, body, rows, assign, window=1500):
    """A stretch the OCR read in another order (a chapter's first line beside its drop initial, a
    caption read before the text above it) shows up as an OCR-only run AND a Gutenberg-only run close
    by. Pair them and align the two."""
    pending = [r for r in rows if r["class"] == "unread" and r["j"]]
    for r in rows:
        if r["class"] not in ("gutenberg_omits", "noise") or len(r["ocr"]) < 3:
            continue
        I = [i for i in range(r["i"][0], r["i"][1]) if not ocr[i]["furniture"]]
        a = [ocr[i]["n"] for i in I]
        best = None
        for u in pending:
            if abs(u["j"][0] - r["at"]) > window:
                continue
            J = list(range(u["j"][0], u["j"][1]))
            sm = difflib.SequenceMatcher(None, a, [norm(body[j]) for j in J], autojunk=False)
            hit = sum(m.size for m in sm.get_matching_blocks())
            if hit >= max(3, 0.5 * len(a)) and (best is None or hit > best[0]):
                best = (hit, u, J, sm)
        if not best:
            continue
        hit, u, J, sm = best
        for t, a1, a2, b1, b2 in sm.get_opcodes():
            if t == "equal":
                for d in range(a2 - a1):
                    assign[I[a1 + d]] = body[J[b1 + d]]
            elif t == "replace":
                _spread(ocr, body, I[a1:a2], J[b1:b2], assign)
        r["class"] = "moved"
        r["matched"] = hit
        u["class"] = "moved"


def apply_decisions(ocr, rows, assign, decisions):
    """A person's rulings, made by looking at the scan: for a dispute, `choice` "pg" or "ocr"; for any
    single printed word the alignment could not mend, `text`. -> number applied."""
    n = 0
    for d in decisions:
        for r in rows:
            if r["class"] in ("dispute", "print_typo") and r["page"] == d["page"] and r["ocr"] == d["ocr"] \
                    and r["pg"] == d.get("pg") and d.get("choice"):
                if d["choice"] == "pg":
                    _spread(ocr, r["pg"], range(r["i"][0], r["i"][1]), range(len(r["pg"])), assign)
                r["decided"] = d["choice"]
                n += 1
        if d.get("text"):
            for i, w in enumerate(ocr):
                if w["page"] == d["page"] and w["full"] == d["ocr"][0]:
                    assign[i] = d["text"]
                    n += 1
    return n


def page_words(ocr, assign, min_conf=30):
    """-> {page: [(text, bbox)]}, one entry per printed word: Gutenberg's spelling where it was placed,
    the OCR's reading elsewhere; unplaced pieces under `min_conf` (ink in pictures) are left out."""
    out, cur = {}, None
    for i, w in enumerate(ocr):
        k = (w["page"], w["line"], w["word"])
        if k != cur:
            cur = k
            out.setdefault(w["page"], []).append([w["full"], w["bbox"], [], True])
        ent = out[w["page"]][-1]
        if i in assign:
            ent[2].append((w["t"], assign[i]))
        elif w["conf"] < min_conf and not w["furniture"]:
            ent[3] = False
    res = {}
    for page, ents in out.items():
        lst = []
        for full, bbox, subs, keep in ents:
            if subs:
                t = full
                for old, new in subs:
                    t = t.replace(old, new, 1) if old in t else t
                lst.append((t, bbox))
            elif keep:
                lst.append((full, bbox))
        res[page] = lst
    return res


def run(hocr_dir, pg_path, out_dir, decisions_path=None):
    ocr = ocr_words(hocr_dir)
    body, notes = pg_body(pg_path)
    vocab = {}
    for t in body + [t for _, t, _ in notes]:
        vocab[norm(t)] = vocab.get(norm(t), 0) + 1
    assign, rows = classify(ocr, body, vocab)
    moved_pass(ocr, body, rows, assign)
    used = second_pass(ocr, notes, rows, assign)
    decided = 0
    if decisions_path and os.path.exists(decisions_path):
        decided = apply_decisions(ocr, rows, assign, json.load(open(decisions_path)))
    for r in rows:                                  # what the second pass placed is not noise any more
        if r["class"] == "noise" and r["i"] and all(i in assign for i in range(r["i"][0], r["i"][1])
                                                    if not ocr[i]["furniture"]):
            r["class"] = "sidenote"
    os.makedirs(out_dir, exist_ok=True)
    counts = {}
    for r in rows:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    with open(os.path.join(out_dir, "differences.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = {"ocr_pieces": len(ocr), "pg_body_words": len(body), "pg_note_words": len(notes),
               "ocr_pieces_given_pg_text": len(assign), "notes_placed": len(used), "decisions_applied": decided,
               "differences": dict(sorted(counts.items()))}
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w"), indent=1)
    return ocr, body, assign, rows, summary


if __name__ == "__main__":
    import sys
    print(json.dumps(run(*sys.argv[1:5])[-1], indent=1))
