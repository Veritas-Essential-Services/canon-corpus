# prov: 2026-10-20 claude-opus-5-5 drafted
# fable_review: pending
"""Small capitals: a shape of the type, read as one.

Adam, 2026-10-20, on KATERFELTO in Character Sketches vol. 6: "Do you see how it gets confused
when the first letter of a word is a capital letter larger than the rest of the word in smaller
capital letters? Can you make it recognize this as a shape of some of the typography in this book?"

Why the engines fail. A small-capital word prints a full capital and then capitals cut to the
height of a lowercase x. Tesseract and the Archive's engine judge case partly by height, so the
short capitals come out as lowercase (Katerfelto) or as a jumble of the two (KateErFELTo, where the
small R was read as "Er"). Four readings, four different words: the vote can only send it to Adam.

What this does. A word whose readings look like small capitals (a capital after a lowercase
letter inside the word, or a reading in all capitals) is cut out of EACH scan, enlarged three
and read again by tesseract with only capital letters (and ' - .) allowed, as a line (--psm 7), at
four crop sizes. One word (--psm 8) and raw text (--psm 13) dropped letters. Within a scan the
fullest read is kept when the others only drop letters from it. The word is taken when both
printings give the same word, and only when it is close to what the engines first saw (so a plain word
that never was small caps cannot be rewritten into capitals). It is written in capitals, the way
the page prints it; the house's earlier small-caps rule did the same.
"""
import difflib
import os
import re
import subprocess
import tempfile

CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆŒ'’-."


def heads_entry(rec):
    """The book's headwords are small capitals, and a headword is followed by its bracket:
    LONG (St. John), MORISON (Dr.). The engines read those as plain words (Lone, Mortson), with
    nothing jumbled to give them away, so position is the sign."""
    line = (rec.get("line") or "").strip()
    base = rec["base"].strip()
    return bool(base) and base[0].isupper() and line.startswith(base) and line[len(base):].lstrip().startswith("(")


def looks_smallcaps(readings):
    """readings: {engine: text} for one word. Only tesseract's jumble counts as a sign: the
    Archive's engine turns a plain 'll' into 'U' (RoUa for Rolla) and that is another rule."""
    for eng, t in readings.items():
        if not eng.endswith(".tess"):
            continue
        s = re.sub(r"[^A-Za-zÆŒæœ]", "", t or "")
        if len(s) < 3:
            continue
        if re.search(r"[a-zæœ][A-ZÆŒ]", s):          # KateErFELTo: a capital after a lowercase letter
            return True
        if s.isupper() and len(s) >= 4:              # KATERFELTO read right by one engine
            return True
    return False


def _ocr(png, psm):
    out = subprocess.run(
        ["tesseract", png, "-", "--psm", str(psm), "-c", f"tessedit_char_whitelist={CAPS}"],
        capture_output=True, text=True, env={**os.environ, "OMP_THREAD_LIMIT": "1"}).stdout
    return re.sub(r"\s+", "", out)


VARIANTS = ((6, 3), (20, 3), (20, 2), (20, 4))       # (padding px, enlargement)


def reread(rec, scan_dirs):
    """{scan: [fresh capital-only line readings at several crop sizes]}; a scan with no image is absent."""
    from PIL import Image, ImageOps
    got = {}
    with tempfile.TemporaryDirectory() as tmp:
        for s, d in scan_dirs.items():
            r = rec["readings"].get(f"{s}.tess") or rec["readings"].get(f"{s}.djvu")
            png = r and os.path.join(d, "gray", f"{r['n']:04d}.png")
            if not png or not os.path.exists(png):
                continue
            im = Image.open(png).convert("L")
            x0, y0, x1, y1 = r["bbox"]
            for pad, k in VARIANTS:
                c = im.crop((max(0, x0 - pad), max(0, y0 - 10), min(im.width, x1 + pad), min(im.height, y1 + 10)))
                c = ImageOps.expand(c.resize((c.width * k, c.height * k), Image.LANCZOS), 30, fill=255)
                p = os.path.join(tmp, f"{s}-{pad}-{k}.png")
                c.save(p)
                got.setdefault(s, []).append(_ocr(p, 7))
    return got


def _fullest(reads):
    """The reading every other one only drops letters from; None when two reads contradict."""
    reads = [re.sub(r"^[^A-ZÆŒ]+|[^A-ZÆŒ]+$", "", re.sub("'+", "'", f.replace("’", "'"))) for f in reads]
    reads = [f for f in reads if f]
    if not reads:
        return None
    top = max(reads, key=lambda w: (len(w), reads.count(w)))
    return top if all(f == top or _drops(f, top) for f in reads) else None


def _drops(short, long):
    """True when short is long with letters left out."""
    it = iter(long)
    return len(short) < len(long) and all(ch in it for ch in short)


def letters(t):
    return re.sub(r"[^a-zæœ]", "", (t or "").lower())


def decide(rec, scan_dirs):
    """The word in capitals with its punctuation kept, or None (leave it to the vote / to Adam)."""
    texts = [r["t"] for r in rec["readings"].values()]
    if not (looks_smallcaps({k: r["t"] for k, r in rec["readings"].items()}) or heads_entry(rec)):
        return None
    per_scan = {sc: _fullest(reads) for sc, reads in reread(rec, scan_dirs).items()}
    # Both printings must give the same word. Enlarged small capitals still lose a letter now and
    # then (LN, LON for LONG), so within one scan a read that only DROPS letters is no objection.
    words = set(per_scan.values())
    if len(per_scan) < 2 or None in words or len(words) != 1:
        return None
    word = words.pop()
    if len(word) < 2:
        return None
    if "'" in rec["base"] + "".join(texts) and "’" in rec["base"]:
        word = word.replace("'", "’")
    close = max(difflib.SequenceMatcher(None, word.lower(), letters(t)).ratio() for t in texts)
    if close < 0.6:
        return None
    src = rec["base"].strip()
    m = re.match(r"^(\W*)(.*?)(\W*)$", src)
    return m.group(1) + word + m.group(3)
