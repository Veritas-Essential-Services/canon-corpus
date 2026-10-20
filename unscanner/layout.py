"""Layout: from OCR'd words to a printed book's structure.

The OCR gives words in boxes. A printed page gives much more than that, and it is all in the geometry:
a paragraph begins where a line is INDENTED; a heading is set LARGER or CENTRED; a page number and a
running head sit in the margin at the top or foot; a plate is a page of picture with a caption. The
Internet Archive's plain OCR text throws the geometry away, which is why the djvu-text ingest of the
Church books had to GUESS paragraph breaks from short last lines. This module reads them off the page.

Rules, in the order they are applied (each one is measured, never assumed; the numbers are reported):

  1. Body size. B = the median line height (tesseract's x_size) over lines of five words or more.
     An em is taken as B. Thresholds below are in ems so a book at any size works.
  2. Measure. Per page, the body's left edge L = the median left of its full lines and the right edge
     R = the 90th percentile of their rights. A page with too few full lines borrows the book's
     median for its side (recto/verso, by page parity).
  3. Furniture, recorded and removed from the text:
     - folio: a top or bottom line that is only a number (arabic or roman) -> the printed page label;
       a top line that STARTS or ENDS with a number and is otherwise in capitals carries both;
     - running head: a top line in capitals, in the top 12% of the page, whose text recurs as a top
       line on two or more pages and is not a CHAPTER line.
  4. Page kind: `blank` (no word read with confidence >= 50), `plate` (a picture covers more than 8%
     of the page outside the words and fewer than 40 words were read), else `text`. A text page may
     still carry `figures` (ornaments, cuts): ink regions over 1.5% of the page that no word covers.
  5. Blocks on a text page, line by line:
     - heading: set at 1.25 B or more, or centred (left and right gaps within 1 em of each other and
       both over 2 em) and in capitals. Consecutive heading lines are one heading block;
     - quote/verse: a line whose left is more than 3 em in from L and is not centred caps. Consecutive
       such lines are one block, line breaks kept;
     - paragraph start: a line indented 0.4 to 3 em from L, or the first body line after a heading;
     - otherwise the line continues the block before it. The first line of a page that is NOT
       indented continues the last paragraph of the previous text page (`cont`); this is the page
       break that the plain OCR text cannot see.
  6. Words broken at the margin: a line ending in "-" before a lower-case word is rejoined. The
     hyphen is KEPT when the book itself prints that compound with a hyphen mid-line; with no
     evidence either way it is kept for a compound of two words the book prints on their own
     ("sea-shore") and dropped for a syllable break ("hid-ing"). Every rejoin is counted and the
     doubtful ones are listed for the review sheet.
"""
import difflib
import re
import statistics
from collections import Counter

ROMAN = re.compile(r"^[ivxlcdm]+$", re.I)
NUM = re.compile(r"^\d{1,4}$")
CAPS = re.compile(r"^[^a-z]*[A-Z][^a-z]*$")
CHAPTER = re.compile(r"^CHAPTER\b", re.I)


def line_text(line):
    return " ".join(w["t"] for w in line["words"])


def _is_folio(tok):
    t = tok.strip(".,:;·-—'\"*")
    return bool(NUM.match(t) or (ROMAN.match(t) and len(t) <= 6 and t.lower() == t))


def _quantile(xs, q):
    xs = sorted(xs)
    if not xs:
        return 0
    return xs[min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))]


def body_size(pages):
    xs = [ln["x_size"] for p in pages for ln in p["lines"] if len(ln["words"]) >= 5 and ln["x_size"]]
    return statistics.median(xs) if xs else 40.0


def measures(pages):
    """Per page (L, R): the body column's edges, borrowing the parity median when a page is thin."""
    raw = {}
    for p in pages:
        full = [ln for ln in p["lines"] if len(ln["words"]) >= 5]
        if len(full) >= 3:
            raw[p["n"]] = (statistics.median(l["bbox"][0] for l in full),
                           _quantile([l["bbox"][2] for l in full], 0.9))
    out = {}
    for parity in (0, 1):
        have = [v for k, v in raw.items() if k % 2 == parity] or list(raw.values()) or [(0, 1000)]
        dflt = (statistics.median(v[0] for v in have), statistics.median(v[1] for v in have))
        for p in pages:
            if p["n"] % 2 == parity:
                out[p["n"]] = raw.get(p["n"], dflt)
    return out


def find_columns(p):
    """Two columns of type side by side (Brewer's Character Sketches, 2026-10-20) -> marks each line
    with "col" (0 left, 1 right) and returns 2; a page in one column -> 1, lines untouched.
    Two columns: at least 8 lines wholly left of the page's middle and 8 wholly right of it, and
    at most a sixth of the lines across it (a heading over both columns is allowed). p["lines"]
    keeps its order (the word positions there are what review answers are keyed by); the reading
    order across the columns is carried by the blocks build_blocks makes for each column."""
    W = p.get("w") or max((ln["bbox"][2] for ln in p["lines"]), default=0)
    mid, slack = W / 2, 0.02 * W
    left = [ln for ln in p["lines"] if ln["bbox"][2] < mid + slack]
    right = [ln for ln in p["lines"] if ln["bbox"][0] > mid - slack]
    span = len(p["lines"]) - len(left) - len(right)
    if len(left) < 8 or len(right) < 8 or span > len(p["lines"]) / 6:
        return 1
    for ln in p["lines"]:
        x0, _, x1, _ = ln["bbox"]
        ln["col"] = 0 if (x0 + x1) / 2 < mid else 1
    return 2


def column_measure(lines):
    """(L, R) of one column from its own full lines, as measures() does for a page."""
    full = [ln for ln in lines if len(ln["words"]) >= 5] or lines
    return (statistics.median(l["bbox"][0] for l in full), _quantile([l["bbox"][2] for l in full], 0.9))


def _strip_folio(line):
    """Split a top line into (folio label or None, remaining words)."""
    ws = line["words"]
    if ws and _is_folio(ws[0]["t"]) and len(ws) > 1:
        return ws[0]["t"].strip(".,"), ws[1:]
    if ws and _is_folio(ws[-1]["t"]) and len(ws) > 1:
        return ws[-1]["t"].strip(".,"), ws[:-1]
    if len(ws) == 1 and _is_folio(ws[0]["t"]):
        return ws[0]["t"].strip(".,"), []
    return None, ws


def _norm(ws):
    return re.sub(r"[^A-Z ]", "", " ".join(w["t"] for w in ws).upper()).strip()


def _top_lines(p):
    """The line(s) where a running head sits: the first line, or on a two-column page the top line of
    each column. Two-column pages are allowed a deeper band (Character Sketches' heads sit at 13%)."""
    if p.get("columns") == 2:
        out = []
        for c in (0, 1):
            col = [i for i, ln in enumerate(p["lines"]) if ln.get("col") == c]
            if col:
                out.append(min(col, key=lambda i: p["lines"][i]["bbox"][1]))
        return out, 0.16
    return ([0] if p["lines"] else []), 0.12


def find_furniture(pages):
    """Mark folios and running heads. Returns {page n: {"label", "head", "drop": set(line idx)}}."""
    tops = {}
    for p in pages:
        if not p["lines"]:
            continue
        idx, band = _top_lines(p)
        ln = p["lines"][idx[0]]
        if ln["bbox"][1] > band * p["h"]:
            continue
        folio, ws = _strip_folio(ln)
        text = " ".join(w["t"] for w in ws)
        if ws and CAPS.match(text) and not CHAPTER.match(text) and len(ws) <= 10:
            tops[p["n"]] = (folio, _norm(ws), text)
        elif folio and not ws:
            tops[p["n"]] = (folio, None, "")
    counts = Counter(v[1] for v in tops.values() if v[1])
    heads = [k for k, c in counts.items() if c >= 2]
    out = {}
    for p in pages:
        info = {"label": None, "head": None, "drop": set(), "inferred": False}
        idx, band = _top_lines(p) if p["lines"] else ([], 0.12)
        # a running head can be set as two lines of one row ("217" and "PLAIDS" read apart): every
        # line beside a column's top line (its top within half a line of it) is examined too
        for top in list(idx):
            y = p["lines"][top]["bbox"][1]
            h = p["lines"][top]["bbox"][3] - y
            idx += [i for i, ln in enumerate(p["lines"]) if i not in idx and abs(ln["bbox"][1] - y) < 0.5 * h
                    and ln.get("col") == p["lines"][top].get("col")]
        for li in idx:
            if p["lines"][li]["bbox"][1] > band * p["h"]:
                continue
            folio, ws = _strip_folio(p["lines"][li])
            key = _norm(ws)
            # a running head the OCR mangled ("THe «CYC@hOPS") still sits where running heads sit
            # and still reads most of the way like one: similarity 0.6 or better counts
            near = max((difflib.SequenceMatcher(None, key, h).ratio() for h in heads), default=0) if key else 0
            two = p.get("columns") == 2
            # a two-column page's head is one capitalised word or two over each column ("PIPCHIN",
            # "214 PIPPA"): every entry's headword differs, so it recurs only as a shape, not a text
            short_caps = two and key and len(ws) <= 3 and CAPS.match(" ".join(w["t"] for w in ws))
            if key and (counts.get(key, 0) >= 2 or near >= 0.6 or short_caps) and not CHAPTER.match(key):
                info["head"] = info["head"] or " ".join(w["t"] for w in ws)
                info["label"] = info["label"] or folio
                info["drop"].add(li)
            elif folio and not ws:
                info["label"] = info["label"] or folio
                info["drop"].add(li)
        # the foot: a short line, centred on the page, in the bottom 15%, is the folio's place. Old-style
        # figures defeat the OCR ("29" read "=o"), so the place decides, and the number is inferred
        # from the neighbours below if it cannot be read.
        for i in range(len(p["lines"]) - 1, max(-1, len(p["lines"]) - 3), -1):
            ln = p["lines"][i]
            x0, y0, x1, y1 = ln["bbox"]
            txt = line_text(ln)
            if i in info["drop"] or y0 < 0.85 * p["h"] or len(txt) > 6 or len(ln["words"]) > 2:
                continue
            if abs((x0 + x1) / 2 - p["w"] / 2) > 0.2 * p["w"]:     # a signature mark ("c") may sit beside it
                continue
            info["drop"].add(i)
            num = [w["t"] for w in ln["words"] if _is_folio(w["t"])]
            if num and not info["label"]:
                info["label"] = num[-1].strip(".,")
            info["foot"] = True
            break
        # a printer's signature mark: a scrap of one or two short words ("III", "ni", "B 2") at the foot
        # of a column, set small and off to the side, telling the binder which sheet this is. It is
        # not text (Character Sketches vol. 6, 2026-10-20: twenty "III"s had reached the review sheet).
        cols = [c for c in (0, 1) if any(ln.get("col") == c for ln in p["lines"])] or [None]
        for c in cols:
            mine = [i for i, ln in enumerate(p["lines"]) if c is None or ln.get("col") == c]
            if not mine:
                continue
            last = max(mine, key=lambda i: p["lines"][i]["bbox"][1])
            ln = p["lines"][last]
            x0, y0, x1, y1 = ln["bbox"]
            txt = line_text(ln)
            body_h = statistics.median(l["bbox"][3] - l["bbox"][1] for l in (p["lines"][i] for i in mine))
            if last not in info["drop"] and y0 > 0.75 * p["h"] and len(ln["words"]) <= 2 \
                    and len(re.sub(r"\W", "", txt)) <= 4 and (y1 - y0) < 0.7 * body_h:
                info["drop"].add(last)
                info["signature"] = txt
        out[p["n"]] = info
    _infer_labels(pages, out)
    return out


def _infer_labels(pages, out):
    """Fill an unreadable folio from its neighbours: label = scan page + offset, where the nearest
    readable folio on EACH side gives the same offset (plates are unnumbered inserts, so the offset
    changes across them; where the two sides disagree nothing is guessed)."""
    known = {}
    for p in pages:
        lab = out[p["n"]]["label"]
        if lab and lab.isdigit():
            known[p["n"]] = int(lab) - p["n"]
    ks = sorted(known)
    # a folio READ wrongly (old-style "36" read "30") is caught the same way: if the nearest readable
    # folios on both sides agree with each other and not with it, the sequence wins and it is flagged
    for k in ks:
        before = [x for x in ks if x < k]
        after = [x for x in ks if x > k]
        if before and after and known[before[-1]] == known[after[0]] != known[k] \
                and after[0] - before[-1] <= 6:
            out[k]["label"] = str(k + known[before[-1]])
            out[k]["inferred"] = "corrected"
    for k in ks:
        if out[k].get("inferred") == "corrected":
            known[k] = int(out[k]["label"]) - k
    for p in pages:
        info = out[p["n"]]
        if info["label"] or not (info.get("foot") or info["head"]):
            continue
        before = [k for k in ks if k < p["n"]]
        after = [k for k in ks if k > p["n"]]
        if before and after and known[before[-1]] == known[after[0]]:
            info["label"] = str(p["n"] + known[before[-1]])
            info["inferred"] = True


def drop_specks(p):
    """Lines that are scanner dirt: no word of two letters or digits read with confidence 40+."""
    keep, n = [], 0
    for ln in p["lines"]:
        if any(w["conf"] >= 40 and len(re.sub(r"[^A-Za-z0-9]", "", w["t"])) >= 2 for w in ln["words"]) \
                or any(w["conf"] >= 80 and re.match(r"^[A-Za-z0-9]$", w["t"]) for w in ln["words"]):
            keep.append(ln)
        else:
            n += 1
    p["lines"] = keep
    return n


def page_kind(p, ink=None):
    """blank / plate / text. `ink` = picture coverage outside words (fraction), from images.ink_regions."""
    good = [w for ln in p["lines"] for w in ln["words"] if w["conf"] >= 50 and len(w["t"]) > 1]
    if ink is not None and ink > 0.08 and len(good) < 40:
        return "plate"
    if not good:
        return "blank"
    return "text"


def build_blocks(p, B, L, R, drop):
    """One text page -> blocks. Each block: {"type", "lines", "cont"} (lines keep their words)."""
    blocks, cur = [], None
    em = B
    body_seen = False
    after_heading = False
    for i, ln in enumerate(p["lines"]):
        if i in drop:
            continue
        x0, y0, x1, y1 = ln["bbox"]
        text = line_text(ln)
        lgap, rgap = x0 - L, R - x1
        centred = abs(lgap - rgap) < em and lgap > 2 * em and rgap > 2 * em
        big = ln["x_size"] >= 1.25 * B
        # a line in capitals, balanced in the measure (gaps within 1.5 em of each other), of eight words
        # or fewer, is a heading even when it fills most of the line ("THE ODYSSEY FOR BOYS")
        caps_line = bool(CAPS.match(text)) and len(re.sub(r"[^A-Za-z]", "", text)) >= 4 \
            and len(ln["words"]) <= 8 and abs(lgap - rgap) < 1.5 * em
        if big or caps_line or (centred and CAPS.match(text)) or (CHAPTER.match(text) and len(ln["words"]) <= 3):
            if cur and cur["type"] == "heading":
                cur["lines"].append(ln)
            else:
                cur = {"type": "heading", "lines": [ln], "cont": False}
                blocks.append(cur)
            after_heading = True
            continue
        if lgap > 3 * em:
            if cur and cur["type"] == "quote":
                cur["lines"].append(ln)
            else:
                cur = {"type": "quote", "lines": [ln], "cont": False}
                blocks.append(cur)
            body_seen = True
            continue
        indented = 0.4 * em < lgap <= 3 * em
        if indented or after_heading or cur is None or cur["type"] != "para":
            cont = not indented and not after_heading and not body_seen and cur is None
            cur = {"type": "para", "lines": [ln], "cont": cont}
            blocks.append(cur)
        else:
            cur["lines"].append(ln)
        body_seen = True
        after_heading = False
    return blocks


def hyphen_evidence(pages):
    """Words the book prints WITH a hyphen mid-line, and words it prints whole: the evidence for
    deciding whether a margin hyphen is the compound's or the compositor's."""
    hyph, whole = Counter(), Counter()
    for p in pages:
        for ln in p["lines"]:
            ws = ln["words"]
            for j, w in enumerate(ws):
                t = re.sub(r"[^\w-]", "", w["t"]).lower()
                if j == len(ws) - 1 and t.endswith("-"):
                    continue
                if "-" in t.strip("-"):
                    hyph[t] += 1
                elif t:
                    whole[t] += 1
    return hyph, whole


SUFFIXES = {"ship", "ness", "ment", "ful", "less", "hood", "dom", "men", "man", "ward", "wards", "some",
            "self", "selves", "ing", "ed", "er", "est", "ly", "tion", "sion"}


def _compound(head, a, b, whole):
    """With no evidence either way, a break is kept as a hyphen when the word was already hyphened
    before the margin ("brother-in-" + "law"), or when both halves are words this book prints on
    their own, three letters or more, and the second is not a suffix ("sea-" + "shore", not
    "friend-" + "ship"). Every such choice is listed on the review sheet."""
    if "-" in head.rstrip("-"):
        return True
    return len(a) >= 3 and len(b) >= 3 and whole.get(a, 0) > 0 and whole.get(b, 0) > 0 and b not in SUFFIXES


def new_log():
    return {"kept": 0, "joined": 0, "joined_unattested": 0, "doubtful": []}


def _join_more(prev, t, log):
    """Rule 6b (2026-10-20, from Character Sketches vol. 6), for breaks the lower-case test does not
    see. Returns the joined token, or None to leave the break alone.
      - a date or number range: "1630-" + "1706" -> "1630-1706";
      - a word in SMALL CAPITALS broken at the margin: "Dia-" + "MONDS.)" -> "DIAMONDS.)" (the first
        half's short capitals were read as lower case; the whole word is capitals);
      - a compound whose second half is a name: "Fitz-" + "James", "Anglo-" + "Saxon", "Cross-" +
        "Bun" -> the hyphen kept.
    Only inside one paragraph: the caller never offers a break across a paragraph start, which is
    where a capital after a hyphen is a new entry ("Pari-" / "Schamir (The)")."""
    a = re.sub(r"[^\w]", "", prev)
    b = re.sub(r"[^\w]", "", t)
    if a.isdigit() and t[:1].isdigit():
        log["kept"] += 1
        return prev + t
    smallcaps = len(b) >= 2 and b.isalpha() and (b.isupper() or sum(c.isupper() for c in b) >= 2)
    if smallcaps and a[:1].isupper():
        log["joined_unattested"] += 1
        log["doubtful"].append(f"{a}-{b} (small caps)")
        return (prev[:-1] + t).upper()
    if b[:1].isupper() and b[1:].islower() and a[:1].isalpha():
        log["kept_unattested"] = log.get("kept_unattested", 0) + 1
        log["doubtful"].append(f"{a}-{b} (name, kept)")
        return prev + t
    return None


PREFIXES = {"con", "com", "per", "pro", "pre", "sub", "sur", "dis", "des", "mis", "ser", "ver", "inter",
            "trans", "over", "under", "re", "de", "in", "un", "ex"}
NUMBER_WORDS = {"twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"}
ENDINGS = ("s", "es", "d", "ed", "ing", "ings", "ly", "er", "ers", "est", "ness", "ment", "ments", "eth", "ren",
           "ies", "ied", "ion", "ions", "or", "ors", "ous", "ity", "ances", "ance", "ations")


def in_dictionary(word, dictionary):
    """A headword, or a headword with one of the common endings ("conditions", "perverted")."""
    if word in dictionary:
        return True
    for e in ENDINGS:
        if word.endswith(e) and len(word) - len(e) >= 3:
            st = word[:-len(e)]
            if st in dictionary or st + "e" in dictionary or (e in ("ies", "ied") and st + "y" in dictionary) \
                    or (len(st) > 3 and st[-1] == st[-2] and st[:-1] in dictionary):
                return True
    return False


def _webster(prev, t, dictionary):
    """Rule 6c for a margin break the book gives no evidence on. True = keep the hyphen, False = join,
    None = no opinion (the old guess decides).
      - a name broken mid-word: a capital first half and a lower-case second ("Ben-" + "tham",
        "Mont-" + "gomery", "Copper-" + "field"): join (a name's real hyphen has a capital after it,
        "Fitz-James", which rule 6b keeps);
      - Webster prints it hyphened ("first-rate", "knight-errant", "to-day"): keep;
      - Webster prints it solid, or a solid headword with an ending ("pasture", "conditions",
        "perverted", "dwellings"): join;
      - the first half a prefix ("con-", "per-", "sub-"): join;
      - "fifty-seven", "thirty-eight": keep."""
    # the half before the margin is the last segment of an already-hyphened word: "fellow-trav-" +
    # "eller" is fellow-traveller, "go-be-" + "tween" is go-between
    a = re.sub(r"[^\w]", "", prev[:-1].split("-")[-1]).lower()
    m = re.match(r"[\w]+", t)
    b = m.group(0).lower() if m else ""
    if not a or not b:
        return None
    if "-" in prev[:-1] and in_dictionary(a + b, dictionary):
        return False
    if prev.lstrip("“‘(\"'[")[:1].isupper() and t[:1].islower() and "-" not in prev[:-1] \
            and f"{a}-{b}" not in dictionary:
        return False
    if f"{a}-{b}" in dictionary and (a + b) not in dictionary:
        return True
    if in_dictionary(a + b, dictionary):
        return False
    if a in PREFIXES and "-" not in prev[:-1]:           # "con-" + "gress"; but "father-in-" + "law" stays
        return False
    if a in NUMBER_WORDS:
        return True
    if len(a) >= 3 and len(b) >= 3 and b not in SUFFIXES and in_dictionary(a, dictionary) \
            and in_dictionary(b, dictionary):
        return True                                       # "knife-" + "grinder", "subtle-" + "witted"
    return None


def load_dictionary(repo):
    """Webster 1913's headwords, lower case, hyphens kept ("first-rate", "outspoken"): the third
    witness for a margin hyphen, after the book's own spellings (rule 6c). Empty when not built."""
    import gzip
    import json
    import os
    path = os.path.join(repo, "data", "lexicons", "webster1913.json.gz")
    if not os.path.exists(path):
        return frozenset()
    return frozenset(k.lower() for k in json.load(gzip.open(path)))


def join_tokens(lines, hyph, whole, log, show=lambda w: w["t"], more=False, dictionary=frozenset()):
    """Lines (each a list of words) -> tokens [{"t", "it"}], rejoining margin-broken words by the
    book's own evidence (rule 6). `show` renders a word (small capitals in their real case).
    more=True adds rule 6b (_join_more): ranges, small capitals and names; and 6d, the OCR dirt round
    a break (a lone "-" or "," after it, "--" for "-", a continuation opening with "-" or a quote
    mark). Pass it only lines of ONE paragraph.
    dictionary (load_dictionary) adds rule 6c: when the book itself never prints the word mid-line,
    Webster's headword decides, solid ("pas-ture" -> "pasture", "con-gress" -> "congress") or hyphened
    ("first-rate", "knight-errant"); the old guess (_compound) only when Webster has neither.
    Both off by default, so the books already built from it rebuild byte-identical."""
    toks = []
    for ws in lines:
        first = True
        for w in ws:
            t = show(w)
            if more:
                # OCR dirt around a margin break (6d): a lone "-" "," or "_" after a word already
                # broken ("be- -", "be- , trothed"), a leading underscore ("_tention"), "--" for "-"
                # ("con-- temptibly"), and a continuation that opens with "-" or a quote mark
                # ("ex- -ploits", "Decem- ‘ber")
                if toks and toks[-1]["t"].endswith("-"):
                    if t in ("-", "—", "_", ",", "."):
                        continue
                    if toks[-1]["t"].endswith("--") and t[:1].islower():
                        toks[-1]["t"] = toks[-1]["t"][:-1]
                    if len(t) > 1 and t[0] in "-‘'_" and t[1:2].islower():
                        t = t[1:]
                t = t.lstrip("_") or t
            if not t:
                continue
            if more and first and toks and toks[-1]["t"].endswith("-") and not toks[-1]["t"].endswith("--") \
                    and not t[:1].islower():
                j = _join_more(toks[-1]["t"], t, log)
                if j is not None:
                    toks[-1]["t"] = j
                    first = False
                    continue
            if first and toks and toks[-1]["t"].endswith("-") and not toks[-1]["t"].endswith("--") \
                    and t[:1].islower():
                prev = toks[-1]
                a = re.sub(r"[^\w]", "", prev["t"]).lower()
                b = re.sub(r"[^\w]", "", t).lower()
                if f"{a}-{b}" in hyph and hyph[f"{a}-{b}"] >= whole.get(a + b, 0):
                    prev["t"] = prev["t"] + t          # the book's own compound: keep the hyphen
                    log["kept"] += 1
                elif dictionary and re.sub(r"[^\w]", "", t).lower() in ("the", "a", "an", "of", "and", "to", "in",
                                                                        "she", "he", "it", "is", "was"):
                    prev["t"] = prev["t"][:-1]          # "called-" + "the": a stray hyphen, two words (6c)
                    toks.append({"t": t, "it": bool(w.get("it"))})
                    log["stray"] = log.get("stray", 0) + 1
                elif dictionary and (a + b) not in whole and _webster(prev["t"], t, dictionary) is not None:
                    keep = _webster(prev["t"], t, dictionary)
                    prev["t"] = prev["t"] + t if keep else prev["t"][:-1] + t
                    k = "kept_webster" if keep else "joined_webster"
                    log[k] = log.get(k, 0) + 1
                elif (a + b) not in whole and _compound(prev["t"], a, b, whole):
                    prev["t"] = prev["t"] + t          # no evidence, but it reads as a compound: keep, list it
                    log["kept_unattested"] = log.get("kept_unattested", 0) + 1
                    log["doubtful"].append(f"{a}-{b} (kept)")
                else:
                    prev["t"] = prev["t"][:-1] + t
                    if (a + b) in whole:
                        log["joined"] += 1
                    else:
                        log["joined_unattested"] += 1
                        log["doubtful"].append(f"{a}-{b}")
            else:
                toks.append({"t": t, "it": bool(w.get("it"))})
            first = False
    return toks


SENT_END = re.compile(r"[.!?)\]”\"’']$")


def dashes(text, authors=frozenset()):
    """Rule 7 (2026-10-20, Adam: "Look at every hyphen or dash or em dash and make sure they all make
    sense"). After the margin breaks are rejoined:
      - a range of numbers takes an en dash, as the page sets it: "1554-1628" -> "1554–1628", and a
        range broken at the margin "(1276- 1347)" -> "(1276–1347)"; an open one "(1812- )" -> "(1812– )";
      - an em dash is set close, as this book sets it: "stream.” — Spenser" -> "stream.”—Spenser";
      - a lone "-" (the OCR's reading of a dash, or of dirt):
          after a sentence, before a name the book elsewhere prints after ".—" (`authors`, the book's
          own evidence): the attribution dash, "pyramid. - Tennyson" -> "pyramid.—Tennyson";
          otherwise dirt, and dropped: "(1593). - Pinch (Tom)" (a new entry), "wife of - Sir Henry";
      - a hyphen glued to a sentence's end before a new sentence, "(1836)- Saxon" -> "(1836). Saxon"
        is NOT guessed: only "(1836)- " -> "(1836) " and ".- " -> ". ";
      - "St.- Leonard" -> "St. Leonard", and a hyphen after a short function word before a capital
        ("by- Sæmund") is dropped.
    Returns (text, counts)."""
    from collections import Counter as _C
    n = _C()

    def sub(pat, rep, s, key):
        out, k = re.subn(pat, rep, s)
        n[key] += k
        return out
    text = sub(r"(?<=\d)-(?=\d)", "–", text, "range")
    text = sub(r"(?<=\d)- (?=\d{1,4}\b)", "–", text, "range, broken")
    text = sub(r"(?<=\(\d{4})- (?=\))", "– ", text, "open range")
    text = sub(r" — ", "—", text, "em dash closed up")
    text = sub(r"(?<=\S) —(?=\S)", "—", text, "em dash closed up")
    toks = text.split(" ")
    out = []
    i = 0
    while i < len(toks):
        t = toks[i]
        if t == "-" and out and i + 1 < len(toks):
            nxt = re.sub(r"^[^\w]+", "", toks[i + 1])
            if SENT_END.search(out[-1]) and nxt.split(",")[0].rstrip(".") in authors:
                out[-1] = out[-1] + "—" + toks[i + 1]
                n["attribution dash"] += 1
                i += 2
                continue
            n["stray hyphen dropped"] += 1
            i += 1
            continue
        if len(t) > 1 and t.endswith("-") and i + 1 < len(toks):
            nxt = toks[i + 1]
            core = re.sub(r"[^\w.]", "", t[:-1])
            if re.search(r"[.)”’]-$", t) and nxt[:1].isupper():
                t = t[:-1]
                n["stray hyphen dropped"] += 1
            elif core.lower() in ("by", "of", "the", "and", "to", "in", "at", "on", "a", "st.") and nxt[:1].isupper():
                t = t[:-1]
                n["stray hyphen dropped"] += 1
        out.append(t)
        i += 1
    return " ".join(out), dict(n)


def attribution_names(texts):
    """The names a book prints after ".—" (its own attributions): "Tennyson", "Sir", "Byron"."""
    from collections import Counter as _C
    c = _C()
    for t in texts:
        for m in re.finditer(r"[.!?”\")]—([A-Z][\w’'é]+)", t):
            c[m.group(1)] += 1
    return frozenset(k for k, v in c.items() if v >= 2)


def tokens_text(toks):
    return " ".join(t["t"] for t in toks)
