#!/usr/bin/env python3
# prov: 2026-10-19 claude-opus-5-5 drafted
# fable_review: pending
"""brewer_plates.py -- the plates of Brewer's *Character Sketches of Romance,
Fiction and the Drama* (Selmar Hess, New York, 1892; 8 vols, ed. Marion
Harland), catalogued for the Pinacotheca and for a later publishing project.

    python3 pipeline/brewer_plates.py --fetch    # manifests, OCR, PDFs -> data/corpus/art/ (gitignored)
    python3 pipeline/brewer_plates.py            # -> data/art/brewer-sketches/plates.jsonl, mints uids
    python3 pipeline/brewer_plates.py --check    # rebuild: mint 0, byte-identical

Adam, 2026-10-19: save the books' pictures into the picture library, by LINK,
"if we give them all unique UIDs for when we want to build out these books for
a later publishing project". So, as for the rest of data/art: facts and links
only, nothing full-size stored here. Each plate links to its page image on the
holder's own IIIF server (archive.org, University of Toronto scans, marked
NOT_IN_COPYRIGHT; published 1892, so US public domain whoever the artist).

HOW A PLATE IS FOUND. Every plate in this edition is bound with a printed tissue
guard in front of it: caption, "X, Artist", often "Y, Engraver", and a short
passage. Measured on vol 6 (2026-10-19): tissue at leaf n, its back at n+1, the
plate at n+2, a blank at n+3. So the script finds the tissues by their OCR (an
artist or engraver credit near the top of a short page) and takes as the plate
the most heavily inked leaf of the next three, rendered small from the scan
PDF. The caption, artist and engraver are read from the tissue's OCR and are
marked as OCR: misreadings stand until a review pass.

THE ADDRESS IS THE LEAF, NOT A RUNNING NUMBER. `brewer-sketches:v6.leaf114` is
a fact about this scan that no later fix can move; "plate 12" would renumber
every plate after one that a better rule finds. The uid is minted once from
that address and never changes (pipeline/wh_uid.py).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402

UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
CACHE = os.path.join(ROOT, "data", "corpus", "art", "brewer-sketches")
OUT_DIR = os.path.join(ROOT, "data", "art", "brewer-sketches")
OUT = os.path.join(OUT_DIR, "plates.jsonl")
MISSING = os.path.join(OUT_DIR, "listed-not-found.jsonl")
SLUG = "brewer-sketches"
VOLUMES = {v: f"charactersketche0{v}brewuoft" for v in range(1, 9)}
UA = "WordHoard-Pinacotheca/1.0 (https://thewordhoard.com; picture study)"

# An artist or engraver credit as this OCR actually prints it: "Artist",
# "ylrtist", "/Irtist", "Artisi", "/irlht", "Engravtr", "Engra'ser", "EngravH".
CREDIT = re.compile(r"(?:\b[A-Za-z/]{0,2}r[tl][il1!][s5h][tl1i]\b|\bEngra\S{0,4})")
CONTRAST_MIN = 30.0
LISTPAGE = re.compile(r"LIST\s+OF\s+ILLUSTRATIONS|face\s+page|^Illustration\b", re.I | re.M)


def get(url, dest, tries=5):
    if os.path.exists(dest):
        return "present"
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r, open(dest + ".tmp", "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            os.replace(dest + ".tmp", dest)
            return f"{os.path.getsize(dest):,} bytes"
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                raise
            time.sleep(5 * 2 ** i)


def fetch():
    os.makedirs(CACHE, exist_ok=True)
    for v, ident in VOLUMES.items():
        base = f"https://archive.org/download/{ident}/{ident}"
        for url, fn in ((f"https://iiif.archive.org/iiif/3/{ident}/manifest.json", f"{ident}.manifest.json"),
                        (base + "_djvu.xml", f"{ident}_djvu.xml"),
                        (base + ".pdf", f"{ident}.pdf")):
            print(f"  v{v} {fn}: {get(url, os.path.join(CACHE, fn))}")


def pages_ocr(path):
    """Each leaf as its OCR lines (the scan's own djvu text layer)."""
    x = open(path, encoding="utf-8", errors="replace").read()
    ent = lambda w: w.replace("&quot;", '"').replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
    out = []
    for o in re.findall(r"<OBJECT.*?</OBJECT>", x, re.S):
        lines = [" ".join(ent(w) for w in re.findall(r"<WORD[^>]*>([^<]*)</WORD>", l))
                 for l in re.findall(r"<LINE>.*?</LINE>", o, re.S)]
        out.append([re.sub(r"\s+", " ", l).strip() for l in lines if l.strip()])
    return out


def ink(pdf, page1):
    """Contrast (grey-level standard deviation) of a 1-based PDF page,
    rendered tiny. A plate is an engraving: strong blacks on paper. Measured
    2026-10-19 over every plate found without a readable title: real plates
    51-90, the pale tissues and blanks that slipped in 9-15. Mean darkness did
    not separate them (a tan tissue is as dark as a light photogravure)."""
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-f", str(page1), "-l", str(page1), "-r", "12", "-gray",
                        pdf, os.path.join(td, "p")], check=True, capture_output=True)
        fn = [f for f in os.listdir(td)][0]
        from PIL import ImageStat
        im = Image.open(os.path.join(td, fn)).convert("L")
        return ImageStat.Stat(im).stddev[0]


def letters(l):
    return sum(c.isalpha() for c in l) / max(1, len(l.replace(" ", "")))


def plate_title(lines):
    """The plate's own OCR is, when it reads at all, its title in capitals."""
    good = [l for l in lines if letters(l) > 0.7 and len(l.split()) >= 1]   # 0.7: "PUSS-IN-BOOTS." is 0.79
    caps = [l for l in good if l.upper() == l and sum(c.isalpha() for c in l) >= 4]
    if any(re.search(r"COPYRIGHT|PHOTOGRAVURES|HESS\s+PRESS|DIGITIZED", l, re.I) for l in lines):
        return None
    return caps[0].rstrip(".") if caps and len(lines) <= 6 else None


def split_credit(line):
    """'Gustave Dore, Artist Pannemaker, Engraver' -> (artist, engraver)."""
    parts = re.split(r"\s*(?:,\s*)?(" + CREDIT.pattern + r")\s*", line)
    artist = engraver = ""
    for k in range(1, len(parts), 2):
        name = parts[k - 1].strip(" ,.;")
        name = re.sub(r"^.*?(?=(?:[A-Z][\w.'-]*\.?\s*){1,4}$)", "", name) if len(name) > 40 else name
        if parts[k].lower().startswith("engra"):
            engraver = engraver or name
        else:
            artist = artist or name
    return artist, engraver


def tissue(lines):
    """(caption, artist, engraver) when this leaf is a plate's tissue guard."""
    if not (2 <= len(lines) <= 60) or LISTPAGE.search("\n".join(lines[:8])):
        return None
    for k, l in enumerate(lines[:6]):
        if CREDIT.search(l) and len(l.split()) <= 14:
            before = [x for x in lines[:k] if letters(x) > 0.7]
            after = [x for x in lines[k + 1:k + 3] if letters(x) > 0.7 and len(x.split()) <= 8]
            cap = before[-2:] if before else after[:1]
            artist, engraver = split_credit(l)
            return {"caption_ocr": " ".join(cap).strip(), "artist_ocr": artist, "engraver_ocr": engraver}
    return None


def make_row(v, ident, c, leaf, tissue_leaf, cr, title, how):
    body = c["items"][0]["items"][0]["body"]
    return {
        "citation": f"{SLUG}:v{v}.leaf{leaf}",
        "kind": "plate",
        "work": "Character Sketches of Romance, Fiction and the Drama",
        "author": "E. Cobham Brewer; revised American edition, ed. Marion Harland",
        "edition": "Selmar Hess, New York, 1892 (8 vols)",
        "volume": v,
        "leaf": leaf,
        "tissue_leaf": tissue_leaf,
        **cr,
        "plate_title_ocr": title,
        "found_by": how,
        "px": [c.get("width"), c.get("height")],
        "holder": "Internet Archive (University of Toronto, Robarts Library scan)",
        "archive_id": ident,
        "page": f"https://archive.org/details/{ident}/page/n{leaf}/mode/1up",
        "iiif_canvas": c["id"],
        "iiif_image": body["service"][0]["id"],
        "rights": {"pd_us": True,
                   "basis": "published 1892 (US public domain: before 1931); "
                            "archive.org marks the scan NOT_IN_COPYRIGHT"},
        "review": "caption, artist and engraver are OCR of the tissue guard; not yet proofread",
    }


def find_plates(v, ident):
    man = json.load(open(os.path.join(CACHE, f"{ident}.manifest.json"), encoding="utf-8"))
    canvases = man["items"]
    ocr = pages_ocr(os.path.join(CACHE, f"{ident}_djvu.xml"))
    pdf = os.path.join(CACHE, f"{ident}.pdf")
    n = min(len(canvases), len(ocr))
    ink_cache, taken, rows = {}, set(), []

    def leaf_ink(i):
        if i not in ink_cache:
            ink_cache[i] = ink(pdf, i + 1)
        return ink_cache[i]

    for i in range(n):
        cr = tissue(ocr[i])
        if not cr:
            continue
        near = [j for j in (i + 2, i + 1, i + 3, i - 2, i - 1, i - 3) if 0 <= j < n and j not in taken]
        capw = norm_words(cr["caption_ocr"])
        titled = [j for j in near if plate_title(ocr[j])
                  and (not capw or norm_words(plate_title(ocr[j])) & capw)]
        if titled:
            best, how = titled[0], "title"
        else:
            quiet = [j for j in near if sum(len(l.split()) for l in ocr[j]) <= 40
                     and not any(re.search(r"COPYRIGHT|PHOTOGRAVURES|DIGITIZED", l, re.I) for l in ocr[j])]
            best = max(quiet, key=leaf_ink, default=None)
            how = "ink"
            if best is None or leaf_ink(best) < CONTRAST_MIN:
                continue
        taken.add(best)
        rows.append(make_row(v, ident, canvases[best], best, i, cr, plate_title(ocr[best]) or "", how))
    # Match to the volume's own List of Illustrations; look for what is missing.
    listed = parse_list(ocr)
    used, pairs = set(), []
    for ri, r in enumerate(rows):
        key = norm_words(r["plate_title_ocr"]) | norm_words(r["caption_ocr"])
        for k, e in enumerate(listed):
            ew = norm_words(e["title"])
            sc = len(ew & key) / max(1, len(ew | key))
            if sc >= 0.3:
                pairs.append((sc, ri, k))
    done = set()
    for sc, ri, k in sorted(pairs, key=lambda x: (-x[0], x[1], x[2])):   # best first, whole volume
        if ri in done or k in used:
            continue
        done.add(ri); used.add(k)
        rows[ri]["list"] = {"n": k + 1, **listed[k]}
    missing = []
    for k, e in enumerate(listed):
        if k in used:
            continue
        found = None
        if isinstance(e["faces"], int):
            pl = printed_leaf(ocr, e["faces"])
            if pl is not None:
                for j in range(max(0, pl - 4), min(n, pl + 4)):
                    if j in taken:
                        continue
                    t = plate_title(ocr[j])
                    if t and len(norm_words(t) & norm_words(e["title"])) >= 1:
                        found = j
                        break
                if found is None:   # the plate's title did not OCR: the inkiest quiet leaf
                    quiet = [j for j in range(max(0, pl - 4), min(n, pl + 4))
                             if j not in taken and sum(len(l.split()) for l in ocr[j]) <= 12]
                    best = max(quiet, key=leaf_ink, default=None)
                    if best is not None and leaf_ink(best) >= CONTRAST_MIN:
                        found = best
        if found is None:
            missing.append({"volume": v, "n": k + 1, **e})
            continue
        taken.add(found)
        r = make_row(v, ident, canvases[found], found, None,
                     {"caption_ocr": "", "artist_ocr": "", "engraver_ocr": ""},
                     plate_title(ocr[found]) or "", "list" if plate_title(ocr[found]) else "list+ink")
        r["list"] = {"n": k + 1, **e}
        rows.append(r)
    rows.sort(key=lambda r: r["leaf"])
    return rows, missing, len(listed)


def norm_words(t):
    t = re.sub(r"[^A-Za-z ]", " ", (t or "").upper().replace("-", " "))
    return {w for w in t.split() if len(w) > 2 and w not in {"THE", "AND", "HIS", "HER", "MR", "MRS"}}


LISTHEAD = re.compile(r"LIST\s+OF\s+ILLUSTRATIONS|\b\w{0,3}ustration\s+Artist", re.I)
SECTION = re.compile(r"PHOTOGRAVURES|ENGRAVINGS|TYPOGRAVURES|ETCHINGS", re.I)


def parse_list(ocr):
    """The volume's List of Illustrations: [{title, artist, faces}] in order.
    Its pages are the early leaves whose head says so; the page-number column
    is often lost by the OCR, so `faces` may be None."""
    entries, carry = [], ""
    for lines in ocr[:40]:
        if not LISTHEAD.search("\n".join(lines[:5])):
            continue
        for l in lines:
            l = re.sub(r"(?:\s*[.\-•■,^*]\s*){3,}", " ", l).strip()   # dot leaders
            if (LISTHEAD.search(l) or SECTION.search(l) or re.search(r"^VOLUME|VOL\.|^page$|^To face", l)
                    or re.fullmatch(r"[IVXivx]+\.?", l) or letters(l) < 0.5):
                continue
            if carry.endswith("-"):
                l, carry = carry[:-1] + l, ""
            if l.endswith("-") and not re.search(r"\d\s*$", l):
                carry = l
                continue
            m = re.match(r"^(.*?)\s*(\d{1,3}|Frontispiece)?\s*$", l)
            body, faces = m.group(1), m.group(2)
            caps = re.match(r"^([A-Z0-9 ().,'&^{}\-]+?)(?=\s+[A-Z][a-z]|\s+[A-Z]\.|[\s.\-•■,]*$)", body)
            if not caps or sum(c.isupper() for c in caps.group(1)) < 3:
                continue
            title = re.sub(r"[\s.\-•■,^]+$", "", caps.group(1)).strip()
            artist = re.sub(r"^[\s.\-•■,^*]+", "", body[caps.end():]).strip()
            entries.append({"title": re.sub(r"\s+", " ", title), "artist": artist,
                            "faces": "frontispiece" if faces == "Frontispiece" else (int(faces) if faces else None)})
    # A title that wrapped without a hyphen reads as an entry with neither
    # artist nor page; it belongs to the line after it.
    merged = []
    for e in entries:
        if merged and not merged[-1]["artist"] and merged[-1]["faces"] is None:
            prev = merged.pop()
            e = {**e, "title": prev["title"] + " " + e["title"]}
        merged.append(e)
    return merged


def printed_leaf(ocr, page):
    """The leaf whose running head carries printed page number `page`."""
    for i, lines in enumerate(ocr):
        if any(l.strip() == str(page) for l in lines[:4]):
            return i
    return None


def build(reg, vols=None):
    out, gaps = [], []
    for v, ident in VOLUMES.items():
        if vols and v not in vols:
            continue
        rows, missing, listed = find_plates(v, ident)
        for r in rows:
            out.append({"uid": reg.uid_for(r["citation"]), **r})
        gaps += missing
        unmatched = sum(1 for r in rows if "list" not in r)
        print(f"  vol {v}: {len(rows)} plates of {listed} listed; {len(missing)} listed but not found; "
              f"{unmatched} found but not matched to the list")
    return out, gaps


def render(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n" for r in rows).encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    reg = U.WhUidRegistry(UIDS)
    rows, gaps = build(reg)
    blob = render(rows)
    s = reg.stats()
    print(f"  {len(rows)} plates; uids minted {s['minted']} / reused {s['reused']} / registry {s['total']:,}")
    if a.check:
        reg.assert_no_mint()
        same = (os.path.exists(OUT) and open(OUT, "rb").read() == blob
                and os.path.exists(MISSING) and open(MISSING, "rb").read() == render(gaps))
        print("  CHECK " + ("ok: mint 0, byte-identical" if same else "FAILED: plates.jsonl differs"))
        sys.exit(0 if same else 1)
    os.makedirs(OUT_DIR, exist_ok=True)
    for path, data in ((OUT, blob), (MISSING, render(gaps))):
        with open(path + ".tmp", "wb") as f:
            f.write(data)
        os.replace(path + ".tmp", path)
    reg.save()
    print(f"  -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
