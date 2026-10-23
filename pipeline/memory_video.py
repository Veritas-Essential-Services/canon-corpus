"""A memory-work video: one poem learned by heart over one great painting.

The painting fills the screen and drifts slowly the whole way through. The
poem is set beside it on a dark veil, stanza by stanza, in four rounds that
take the words away a little at a time:

  I    Read it through   - every word
  II   Fill the gaps     - every other word cut back to its first letter
  III  First letters     - only the first letter of every word
  IV   Say it alone      - the lines are blank; the viewer recites

then the whole poem once more to check yourself, and a closing card naming
the poem, the painting and where both come from.

The poem comes from data/poetry/texts.jsonl (cut from a pinned public-domain
book, never typed) and the painting from data/art/wall/collection.json. Only
US public-domain poems and paintings are allowed: the script refuses anything
else, because the video is meant for YouTube.

Needs Pillow and ffmpeg. Fonts: EB Garamond and Cinzel (both SIL Open Font
Licence, from github.com/google/fonts) in --fonts, or it falls back to DejaVu.

    python pipeline/memory_video.py --poem "Crossing the Bar" --painting Q257580 --out crossing-the-bar.mp4
    python pipeline/memory_video.py --poem wh-E56K57SPTD --painting Q257580 --size 3840x2160 --out ctb-4k.mp4
    python pipeline/memory_video.py ... --still 40     # write the frame at 40 s as a PNG instead of a video
"""
import argparse
import io
import json
import math
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
POEMS = os.path.join(ROOT, "data", "poetry", "texts.jsonl")
ART = os.path.join(ROOT, "data", "art", "wall", "collection.json")
UA = "WordHoard-memory-video/1.0 (personal memory-work videos)"
FPS = 30
FADE = 0.6  # seconds for the old card to leave, and again for the new one to come
INK = (241, 233, 219)
DIM = (196, 184, 164)
GILT = (214, 178, 106)
ROUNDS = [("I", "Read it through"), ("II", "Fill the gaps"), ("III", "First letters"), ("IV", "Say it alone")]


# --- sources -------------------------------------------------------------

def load_poem(key):
    for line in open(POEMS, encoding="utf-8"):
        r = json.loads(line)
        if key in (r.get("uid"), r.get("citation")) or key.lower() == r.get("title", "").lower():
            return r
    sys.exit(f"no poem {key!r} in {POEMS}")


def load_painting(qid):
    for w in json.load(open(ART, encoding="utf-8"))["works"]:
        if w["qid"] == qid:
            if not w.get("pd_us"):
                sys.exit(f"{qid} is not marked US public domain; refusing to put it in a public video")
            return w
    sys.exit(f"no painting {qid} in {ART}")


def fetch_painting(work, long_edge, cache):
    """Commons' copy at the screen's size (never upscaled past the original), cached on disk."""
    path = os.path.join(cache, f"{work['qid']}-{long_edge}.jpg")
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + work["image"]["file"], "prop": "imageinfo",
                                "iiprop": "url", "iiurlwidth": long_edge, "format": "json", "formatversion": 2})
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": UA})
    ii = json.load(urllib.request.urlopen(req, timeout=60))["query"]["pages"][0]["imageinfo"][0]
    req = urllib.request.Request(ii.get("thumburl") or ii["url"], headers={"User-Agent": UA})
    blob = urllib.request.urlopen(req, timeout=180).read()
    os.makedirs(cache, exist_ok=True)
    with open(path + ".part", "wb") as f:
        f.write(blob)
    os.replace(path + ".part", path)
    return Image.open(io.BytesIO(blob)).convert("RGB")


# --- the poem as stanzas of lines of words --------------------------------

def stanzas(text):
    out = []
    for block in re.split(r"\n\s*\n", text.strip("\n")):
        lines = []
        for raw in block.split("\n"):
            indent = len(raw) - len(raw.lstrip(" "))
            lines.append((indent, raw.strip().split()))
        out.append(lines)
    return out


def cue(word, keep):
    """A word cut back to its first letter, keeping the punctuation round it."""
    if keep:
        return word, None
    m = re.match(r"^([^\w]*)(\w)([\w'’-]*)([^\w]*)$", word)
    if not m:
        return word, None
    lead, first, rest, tail = m.groups()
    return lead + first, (rest, tail)


# --- drawing ---------------------------------------------------------------

class Fonts:
    def __init__(self, folder, h):
        def load(name, size, fallback):
            for p in (os.path.join(folder or "", name), fallback):
                try:
                    f = ImageFont.truetype(p, size)
                    return f
                except OSError:
                    continue
            return ImageFont.load_default()
        u = h / 1080
        self.body = load("EBGaramond.ttf", round(46 * u), "DejaVuSerif.ttf")
        self.italic = load("EBGaramond-Italic.ttf", round(34 * u), "DejaVuSerif.ttf")
        self.small = load("EBGaramond-Italic.ttf", round(28 * u), "DejaVuSerif.ttf")
        self.title = load("Cinzel.ttf", round(78 * u), "DejaVuSerif.ttf")
        self.label = load("Cinzel.ttf", round(26 * u), "DejaVuSerif.ttf")
        for f in (self.title, self.label):
            try:
                f.set_variation_by_axes([600])
            except Exception:  # noqa: BLE001 -- static fallback font has no axes
                pass
        try:
            self.body.set_variation_by_axes([450])
        except Exception:  # noqa: BLE001
            pass


PLACES = ["left-top", "left-middle", "left-bottom", "right-top", "right-middle", "right-bottom", "centre-top", "centre-bottom"]


class Layout:
    """Where the stanzas sit, and at what size, fixed for the whole video so nothing jumps.

    The block of words goes in one of PLACES: by default the calmest patch of
    the painting, judged by how much edge detail lies under the block, so a
    face, a sun or a ship is left clear. The body size shrinks until the
    longest line fits."""

    def __init__(self, W, H, F, st, img, place=None):
        self.W, self.H = W, H
        d = ImageDraw.Draw(Image.new("L", (1, 1)))
        most = max(len(s) for s in st)
        size = F.body.size
        while True:
            f = F.body.font_variant(size=size)
            ind = round(size * 1.1)
            wide = max((ind if i else 0) + d.textlength(" ".join(w), font=f) for s in st for i, w in s)
            if (wide <= W * 0.44 and most * size * 1.42 <= H * 0.55) or size <= 14:
                break
            size -= 1
        self.font, self.ind, self.lh = f, ind, round(size * 1.42)
        self.head = round(F.label.size * 2.2)
        self.bw, self.bh = round(wide), self.head + most * self.lh
        self.place = place or self.calmest(img)
        h, v = self.place.split("-")
        mx, my = round(W * 0.06), round(H * 0.09)
        self.x0 = {"left": mx, "right": W - mx - self.bw, "centre": (W - self.bw) // 2}[h]
        self.y0 = {"top": my, "bottom": H - my - self.bh, "middle": (H - self.bh) // 2}[v]

    def calmest(self, img):
        g = cover(img, 320, 180, 1.0).convert("L").filter(ImageFilter.FIND_EDGES)
        k = 320 / self.W
        best = None
        for p in PLACES:
            self.place = p
            h, v = p.split("-")
            mx, my = self.W * 0.06, self.H * 0.09
            x = {"left": mx, "right": self.W - mx - self.bw, "centre": (self.W - self.bw) / 2}[h]
            y = {"top": my, "bottom": self.H - my - self.bh, "middle": (self.H - self.bh) / 2}[v]
            box = tuple(round(c * k) for c in (x, y, x + self.bw, y + self.bh))
            score = ImageStat.Stat(g.crop(box)).mean[0]
            if best is None or score < best[0]:
                best = (score, p)
        return best[1]

    def veil(self):
        """A soft dark pool behind the block of words, so they read on any painting."""
        pad = round(self.H * 0.06)
        v = Image.new("RGBA", (self.W, self.H), (8, 7, 6, 0))
        ImageDraw.Draw(v).rounded_rectangle((self.x0 - pad, self.y0 - pad, self.x0 + self.bw + pad, self.y0 + self.bh + pad),
                                            radius=pad, fill=(8, 7, 6, 160))
        return v.filter(ImageFilter.GaussianBlur(pad))

    def top(self, n_lines):
        return self.y0 + self.head


def card_stanza(L, F, stanza, mode, label, seed):
    """One stanza drawn in a round's mode: full, gaps, letters or blank."""
    W, H, f = L.W, L.H, L.font
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    space = d.textlength(" ", font=f)
    top = L.top(len(stanza))
    rule = max(1, H // 540)
    d.text((L.x0, L.y0), label, font=F.label, fill=GILT)
    n = seed
    for i, (indent, words) in enumerate(stanza):
        x = L.x0 + (L.ind if indent else 0)
        y = top + i * L.lh
        base = y + f.getmetrics()[0] + rule * 3
        if mode == "blank":
            width = d.textlength(" ".join(words), font=f)
            d.line((x, base, x + width, base), fill=(*DIM, 110), width=rule)
            continue
        for w in words:
            keep = mode == "full" or (mode == "gaps" and n % 2 == 0)
            shown, cut = cue(w, keep)
            n += 1
            d.text((x, y), shown, font=f, fill=INK)
            x += d.textlength(shown, font=f)
            if cut:
                rest, tail = cut
                rw = d.textlength(rest, font=f)
                d.line((x + rule, base, x + rw - rule, base), fill=(*DIM, 200), width=rule)
                x += rw
                if tail:
                    d.text((x, y), tail, font=f, fill=INK)
                    x += d.textlength(tail, font=f)
            x += space
    return im


def card_whole(L, F, st, label):
    """The whole poem at once, centred over a darkened frame, to check yourself."""
    W, H = L.W, L.H
    total = sum(len(s) for s in st) + len(st) - 1
    size = min(L.font.size, int((H * 0.80) / (total * 1.32)))
    f = L.font.font_variant(size=max(12, size))
    im = Image.new("RGBA", (W, H), (8, 7, 6, 150))
    d = ImageDraw.Draw(im)
    ind = round(f.size * 1.1)
    wide = max((ind if i else 0) + d.textlength(" ".join(w), font=f) for s in st for i, w in s)
    x0 = round((W - wide) / 2)
    lh = round(f.size * 1.32)
    y = (H - lh * total) // 2
    d.text(((W - d.textlength(label, font=F.label)) // 2, y - round(F.label.size * 2.2)), label, font=F.label, fill=GILT)
    for s in st:
        for indent, words in s:
            d.text((x0 + (ind if indent else 0), y), " ".join(words), font=f, fill=INK)
            y += lh
        y += lh
    return im


def card_centre(W, H, lines):
    """Title and round cards: centred lines on a soft dark band."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    heights = [f.getbbox(t)[3] + round(f.size * 0.55) for t, f, _ in lines]
    band = Image.new("RGBA", (W, H), (8, 7, 6, 0))
    bd = ImageDraw.Draw(band)
    bh = sum(heights) + H // 6
    bd.rectangle((0, (H - bh) // 2, W, (H + bh) // 2), fill=(8, 7, 6, 175))
    band = band.filter(ImageFilter.GaussianBlur(H // 20))
    im.alpha_composite(band)
    d = ImageDraw.Draw(im)
    y = (H - sum(heights)) // 2
    for (t, f, c), hh in zip(lines, heights):
        d.text(((W - d.textlength(t, font=f)) // 2, y), t, font=f, fill=c)
        y += hh
    return im


def card_caption(W, H, F, text):
    """A small caption low on the frame, for the painting's own moment."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tw = d.textlength(text, font=F.small)
    pad = F.small.size
    y = H - pad * 3
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shade).rectangle((0, y - pad, W, H), fill=(6, 5, 4, 150))
    im.alpha_composite(shade.filter(ImageFilter.GaussianBlur(pad)))
    d.text(((W - tw) // 2, y), text, font=F.small, fill=DIM)
    return im


# --- the plan: a list of (card, seconds, veiled) ------------------------------------

def plan(W, H, F, L, poem, work):
    st = stanzas(poem["text"])
    painter = work["artist"] or "Unknown painter"
    words = lambda s: sum(len(w) for _, w in s)  # noqa: E731
    cards = [
        (card_centre(W, H, [("Memory Work", F.label, GILT), (poem["title"], F.title, INK), (poem["poet"], F.italic, DIM)]), 6.0, False),
        (card_caption(W, H, F, f"{work['title']}  ·  {painter}" + (f", {work['year']}" if work.get("year") else "")
                      + (f"  ·  {work['holding']}" if work.get("holding") else "")), 7.0, False),
    ]
    modes = ["full", "gaps", "letters", "blank"]
    pace = [0.50, 0.60, 0.70, 0.75]  # seconds per word: slower as the words go
    seed = 0
    for (num, name), mode, sec in zip(ROUNDS, modes, pace):
        cards.append((card_centre(W, H, [(f"Round {num}", F.label, GILT), (name, F.title, INK)]), 3.5, False))
        for i, s in enumerate(st):
            label = f"{num}  ·  {name}  ·  {i + 1} of {len(st)}"
            cards.append((card_stanza(L, F, s, mode, label, seed), 3.0 + sec * words(s), True))
            seed += sum(len(w) for _, w in s)
    cards.append((card_whole(L, F, st, "The whole poem"), 6.0 + 0.30 * sum(words(s) for s in st), False))
    credit = [("Memory Work", F.label, GILT), (f"“{poem['title']}”, {poem['poet']}", F.italic, INK),
              (f"{work['title']}, {painter}" + (f", {work['year']}" if work.get("year") else ""), F.italic, INK),
              ("Poem and painting are in the public domain in the United States.", F.small, DIM),
              ("Image: Wikimedia Commons", F.small, DIM)]
    cards.append((card_centre(W, H, credit), 8.0, False))
    return cards


# --- the painting's slow drift ------------------------------------------------

def cover(img, W, H, margin):
    """The painting scaled to cover the frame with a little to spare for the drift."""
    s = max(W / img.width, H / img.height) * margin
    return img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)


def background(big, W, H, t, total):
    """Ease from one corner of the spare area to the other over the whole video."""
    u = 0.5 - 0.5 * math.cos(math.pi * min(1, t / total))
    dx, dy = big.width - W, big.height - H
    x, y = dx * u, dy * (1 - u) * 0.6 + dy * 0.2
    return big.transform((W, H), Image.AFFINE, (1, 0, x, 0, 1, y), resample=Image.BILINEAR)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poem", required=True, help="title, uid or citation from data/poetry/texts.jsonl")
    ap.add_argument("--painting", required=True, help="Wikidata QID from data/art/wall/collection.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--place", choices=PLACES, help="where the words sit (default: the calmest patch of the painting)")
    ap.add_argument("--fonts", default=os.path.join(ROOT, "fonts"))
    ap.add_argument("--image", help="a local copy of the painting instead of fetching it")
    ap.add_argument("--cache", default=os.path.join(ROOT, "build", "memory-video-cache"))
    ap.add_argument("--still", type=float, help="write the frame at this second as a PNG and stop")
    a = ap.parse_args()
    W, H = (int(x) for x in a.size.lower().split("x"))

    poem, work = load_poem(a.poem), load_painting(a.painting)
    if not poem.get("text"):
        sys.exit(f"{poem['title']} has no hosted text (not US public domain, or not cut yet)")
    img = Image.open(a.image).convert("RGB") if a.image else fetch_painting(work, max(W, H) * 2 if W < 3840 else W, a.cache)
    big = cover(img, W, H, 1.12)
    F = Fonts(a.fonts, H)
    L = Layout(W, H, F, stanzas(poem["text"]), img, a.place)
    v = L.veil()
    cards = plan(W, H, F, L, poem, work)
    starts, t = [], 0.0
    for _, sec, _ in cards:
        starts.append(t)
        t += sec
    total = t
    veiled = [c[2] for c in cards]  # the veil sits under the stanza cards only
    clear = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def fade(layer, alpha):
        return layer if alpha >= 1 else Image.blend(clear, layer, alpha)

    def frame(t):
        bg = background(big, W, H, t, total).convert("RGBA")
        i = max(k for k, s in enumerate(starts) if s <= t)
        span = 2 * FADE if i else 1.5
        u = min(1.0, (t - starts[i]) / span)
        prev = i - 1 if i and u < 1 else None
        va = veiled[i] * u + (veiled[prev] * (1 - u) if prev is not None else 0)
        if va > 0:
            bg.alpha_composite(fade(v, va))
        if prev is None:
            bg.alpha_composite(fade(cards[i][0], u))
        elif u < 0.5:  # the old words leave before the new ones come, so they never overlap
            bg.alpha_composite(fade(cards[prev][0], 1 - 2 * u))
        else:
            bg.alpha_composite(fade(cards[i][0], 2 * u - 1))
        end = total - t
        if end < 1.5:  # fade to black at the very end
            bg = Image.blend(bg, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 1 - end / 1.5)
        return bg.convert("RGB")

    if a.still is not None:
        frame(a.still).save(a.out)
        print(f"{a.out}: frame at {a.still}s of {total:.0f}s")
        return
    print(f"{poem['title']} over {work['title']}: {total:.0f}s, {len(cards)} cards, words at {L.place}")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "128k", a.out + ".part.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = math.ceil(total * FPS)
    for k in range(n):
        p.stdin.write(frame(k / FPS).tobytes())
        if k % (FPS * 20) == 0:
            print(f"  {k / FPS:.0f}s / {total:.0f}s", flush=True)
    p.stdin.close()
    if p.wait():
        sys.exit("ffmpeg failed")
    os.replace(a.out + ".part.mp4", a.out)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
