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
times, and read again by tesseract with only capital letters (and ' - .) allowed, as a line
(--psm 7) and as raw text (--psm 13); one word (--psm 8) dropped letters. Four fresh readings from
two different printings. The word is taken when both printings give it and every other fresh reading only drops letters from it, and only when it is close to what the engines first saw (so a plain word
that never was small caps cannot be rewritten into capitals). It is written in capitals, the way
the page prints it; the house's earlier small-caps rule did the same.
"""
import difflib
import os
import re
import subprocess
import tempfile

CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆŒ'’-."


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


def reread(rec, scan_dirs):
    """Fresh capital-only readings of the word, two per scan. [] when no scan image is at hand."""
    from PIL import Image
    got = []
    with tempfile.TemporaryDirectory() as tmp:
        for s, d in scan_dirs.items():
            r = rec["readings"].get(f"{s}.tess") or rec["readings"].get(f"{s}.djvu")
            png = r and os.path.join(d, "gray", f"{r['n']:04d}.png")
            if not png or not os.path.exists(png):
                continue
            im = Image.open(png).convert("L")
            x0, y0, x1, y1 = r["bbox"]
            c = im.crop((max(0, x0 - 6), max(0, y0 - 8), min(im.width, x1 + 6), min(im.height, y1 + 8)))
            c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
            p = os.path.join(tmp, f"{s}.png")
            c.save(p)
            got += [_ocr(p, 7), _ocr(p, 13)]
    return got


def _drops(short, long):
    """True when short is long with letters left out."""
    it = iter(long)
    return len(short) < len(long) and all(ch in it for ch in short)


def letters(t):
    return re.sub(r"[^a-zæœ]", "", (t or "").lower())


def decide(rec, scan_dirs):
    """The word in capitals with its punctuation kept, or None (leave it to the vote / to Adam)."""
    texts = [r["t"] for r in rec["readings"].values()]
    if not looks_smallcaps({k: r["t"] for k, r in rec["readings"].items()}):
        return None
    fresh = [re.sub("'+", "'", f.replace("’", "'")) for f in reread(rec, scan_dirs)]
    if len(fresh) < 4:
        return None
    fresh = [re.sub(r"^[^A-ZÆŒ]+|[^A-ZÆŒ]+$", "", f) for f in fresh]
    # Enlarged small capitals still lose a letter now and then (CAGLITRO for CAGLIOSTRO). A reading
    # that only DROPS letters from the winner is no objection; any other reading is.
    word = max(set(fresh), key=lambda w: (fresh.count(w), len(w)))
    agree = [i for i, f in enumerate(fresh) if f == word]
    if len(word) < 2 or len({i // 2 for i in agree}) < 2:      # both printings must say it
        return None
    if not all(f == word or _drops(f, word) for f in fresh):
        return None
    if "'" in rec["base"] + "".join(texts) and "’" in rec["base"]:
        word = word.replace("'", "’")
    close = max(difflib.SequenceMatcher(None, word.lower(), letters(t)).ratio() for t in texts)
    if close < 0.6:
        return None
    src = rec["base"].strip()
    m = re.match(r"^(\W*)(.*?)(\W*)$", src)
    return m.group(1) + word + m.group(3)
