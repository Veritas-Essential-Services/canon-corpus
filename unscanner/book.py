"""The Unscanner's driver: a scanned PDF in, a structured book out.

    work/<slug>/source.pdf          the scan (archive.org, or a local file copied in)
    work/<slug>/gray/0001.png       each page at 300 dpi, grey, for OCR and measurement
    work/<slug>/hocr/0001.hocr      tesseract's words, boxes and confidences
    work/<slug>/book.json           the structure this module builds (rebuilt every run; cheap)

Pages are rasterised and OCR'd once and reused; everything after that is measurement and is rerun.
"""
import difflib
import json
import os
import re
import statistics

import numpy as np
from PIL import Image

from . import fonts as F
from . import images as I
from . import layout as L
from . import scan as S
from . import style as ST

RE_CHAPTER = re.compile(r"^CHAPTER[.,:]?\s+([IVXLC1l]+|\d+)\b\.?\s*(.*)$", re.I)


def roman(s):
    if s.isdigit():
        return int(s)
    s = s.replace("1", "I").replace("l", "I").upper()     # OCR: a roman one read as digit one or ell
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    tot = 0
    for i, ch in enumerate(s):
        v = vals.get(ch, 0)
        tot += -v if i + 1 < len(s) and vals.get(s[i + 1], 0) > v else v
    return tot


def to_roman(n):
    out = ""
    for v, r in ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += r; n -= v
    return out


def title_case(s):
    small = {"a", "an", "and", "at", "by", "for", "in", "of", "on", "or", "the", "to", "with", "from"}
    ws = s.lower().split()
    return " ".join(w if (i and w in small) else w[:1].upper() + w[1:] for i, w in enumerate(ws))


class Work:
    def __init__(self, root, slug):
        self.root, self.slug = root, slug
        self.dir = os.path.join(root, slug)
        os.makedirs(self.dir, exist_ok=True)

    def p(self, *parts):
        return os.path.join(self.dir, *parts)


def _ocr_one(args):
    pdf, n, png, hocr, dpi = args
    S.rasterize(pdf, n, png, dpi=dpi)
    S.ocr_page(png, hocr)
    return n


def ocr_pages(work, pdf, pages, log=print, dpi=300, jobs=1):
    """Rasterise + OCR each page not already done. Resumable; returns {n: (png, hocr)}.

    `jobs` pages run at once, each tesseract on ONE thread (OMP_THREAD_LIMIT=1): on a small box, two
    single-threaded pages at a time beat one page with two threads fighting."""
    out, todo = {}, []
    for n in pages:
        png = work.p("gray", f"{n:04d}.png")
        hocr = work.p("hocr", f"{n:04d}.hocr")
        if not os.path.exists(hocr):
            todo.append((pdf, n, png, hocr, dpi))
        out[n] = (png, hocr)
    if jobs > 1 and len(todo) > 1:
        from multiprocessing import Pool
        with Pool(jobs) as pool:
            for n in pool.imap_unordered(_ocr_one, todo):
                log(f"  ocr p{n}")
    else:
        for t in todo:
            log(f"  ocr p{_ocr_one(t)}")
    return out


def analyse(work, done, font_cache, dpi=300, log=print, match_fonts=True):
    """OCR'd pages -> the book structure (dict, also written to book.json)."""
    pages = []
    for n in sorted(done):
        png, hocr = done[n]
        p = S.parse_hocr(hocr)
        p["n"] = n
        p["specks"] = L.drop_specks(p)
        pages.append(p)
    B = L.body_size(pages)
    meas = L.measures(pages)
    furn = L.find_furniture(pages)
    style_counts = {"italic": 0, "smallcaps": 0}
    for p in pages:
        png = done[p["n"]][0]
        if not os.path.exists(png):
            S.rasterize(work.p("source.pdf"), p["n"], png, dpi=dpi)
        words = [w["bbox"] for ln in p["lines"] for w in ln["words"]]
        cover, regions = I.ink_regions(png, words)
        p["ink"] = round(cover, 4)
        p["kind"] = L.page_kind(p, cover)
        p["figures"] = regions if p["kind"] != "blank" else []
        p["label"] = furn[p["n"]]["label"]
        p["head"] = furn[p["n"]]["head"]
        p["label_inferred"] = furn[p["n"]]["inferred"]
        p["drop"] = sorted(furn[p["n"]]["drop"])
        if p["kind"] == "text":
            a = np.asarray(Image.open(png).convert("L"))
            c = ST.mark_page(a, p["lines"])
            style_counts["italic"] += c["italic"]
            style_counts["smallcaps"] += c["smallcaps"]
            Lm, Rm = meas[p["n"]]
            p["blocks"] = L.build_blocks(p, B, Lm, Rm, set(p["drop"]))
            p["measure"] = [Lm, Rm]
        else:
            p["blocks"] = []
    font_rank = []
    if match_fonts:
        fonts = F.fetch_fonts(font_cache)
        sample = F.sample_words(pages, {n: done[n][0] for n in done}, limit=80)
        font_rank = F.match(sample, fonts, dpi=dpi)
    return pages, {"body_px": B, "style": style_counts, "fonts": font_rank}


def assemble(pages, slug, extra_heads=(), heading_fixes=None):
    """Text pages' blocks -> a reading stream, then divisions. Returns (front, divisions, log).

    The work starts at the first CHAPTER heading; what comes before is front matter (title page,
    Contents, preface), kept for the faithful edition and left out of the citable units. A CHAPTER
    number seen a second time (a half-title, a plate's heading) is not a new chapter.
    """
    hyph, whole = L.hyphen_evidence(pages)
    extras = {L._norm([{"t": h}]): h for h in extra_heads}
    log = L.new_log()
    stream = []                       # {"type", "lines": [(page n, [words])], ...}
    first_text = next((p["n"] for p in pages if p["kind"] == "text"), None)
    for p in pages:
        if p["kind"] != "text":
            if first_text is None or p["n"] < first_text:
                continue              # the binding: covers, end-papers, a library's bookplate
            if p["kind"] == "plate":
                stream.append({"type": "plate", "page": p["n"], "figures": p["figures"],
                               "caption": [ln["words"] for ln in p["lines"]]})
            continue
        for b in p["blocks"]:
            if b["type"] == "heading":
                # a heading block may stack the book's title, "CHAPTER I" and the chapter's title:
                # split it at every CHAPTER line, so each part is judged on its own
                run = []
                for ln in b["lines"] + [None]:
                    is_ch = ln is not None and RE_CHAPTER.match(L.line_text(ln))
                    if (ln is None or is_ch) and run:
                        stream.append({"type": "heading", "lines": [(p["n"], x["words"]) for x in run],
                                       "pages": [p["n"]]})
                        run = []
                    if ln is not None:
                        if is_ch:
                            stream.append({"type": "heading", "lines": [(p["n"], ln["words"])], "pages": [p["n"]]})
                        else:
                            run.append(ln)
                continue
            lines = [(p["n"], ln["words"]) for ln in b["lines"]]
            if b["cont"] and stream:
                prev = next((s for s in reversed(stream) if s["type"] != "plate"), None)
                if prev is not None and prev["type"] == "para":
                    prev["lines"].extend(lines)
                    prev["pages"].append(p["n"])
                    continue
            stream.append({"type": b["type"], "lines": lines, "pages": [p["n"]]})
        for fig in p["figures"]:
            stream.append({"type": "figure", "page": p["n"], "bbox": fig})
    for s in stream:
        if s["type"] in ("para", "quote", "heading"):
            s["toks"] = L.join_tokens([ws for _, ws in s["lines"]], hyph, whole, log, ST.display)
            s["text"] = L.tokens_text(s["toks"])
    # a heading that reads like the running heads (the book's title over its first page) is furniture
    heads = {L._norm([{"t": p["head"]}]) for p in pages if p.get("head")}

    def is_head(text):
        k = L._norm([{"t": text}])
        return any(difflib.SequenceMatcher(None, k, h).ratio() >= 0.75 for h in heads)

    # (but a chapter's own title, right after its CHAPTER line, is the recto running head too: keep it)
    stream = [s for k, s in enumerate(stream)
              if not (s["type"] == "heading" and is_head(s["text"]) and not RE_CHAPTER.match(s["text"])
                      and not (k and stream[k - 1]["type"] == "heading" and RE_CHAPTER.match(stream[k - 1]["text"])))]
    front, divisions, seen, by_tag, renumbered = [], [], set(), {}, []
    cur = None
    i = 0
    while i < len(stream):
        s = stream[i]
        if s["type"] == "heading":
            m = RE_CHAPTER.match(s["text"])
            if m:
                num = roman(m.group(1))
                tag = f"ch{num}"
                title = m.group(2).strip()
                j = i + 1
                while not title and j < len(stream) and stream[j]["type"] == "heading" \
                        and not RE_CHAPTER.match(stream[j]["text"]):
                    title = stream[j]["text"]; j += 1
                title = re.sub(r"[^A-Za-z]+$", "", title)
                for bad, good in (heading_fixes or {}).items():
                    title = re.sub(rf"(?<![A-Za-z]){re.escape(bad)}(?![A-Za-z])", good.upper() if title.isupper() else good, title)
                tconf = _conf(stream[i + 1:j]) if j > i + 1 else _conf([s])
                # Chapters are numbered in order, and a misread numeral ("XXXI" for XXI, "XVII" for XVIII)
                # must not make a chapter vanish as a "repeat" or jump the count. The number read is kept
                # when it is the next one, or a repeat of a chapter whose title it also repeats, or -- if read
                # cleanly (capitals only, confidence 85+; "XXiIi" is not clean) -- at most two ahead (a
                # chapter heading this run failed to see). Anything else takes the next number
                # in sequence, and the renumbering is reported.
                last = max((int(t[2:]) for t in seen if t.startswith("ch") and t[2:].isdigit()), default=0)
                clean = m.group(1).isdigit() or (m.group(1).isupper() and min(
                    (w["conf"] for _, ws in s["lines"] for w in ws), default=0) >= 85)
                if last and num != last + 1 and not (clean and last + 1 < num <= last + 3):   # (the first stands)
                    d = by_tag.get(tag)
                    repeat = d is not None and (not title or not d["title"] or difflib.SequenceMatcher(
                        None, title.upper(), d["title"].upper()).ratio() >= 0.75)
                    cur_same = cur is not None and title and difflib.SequenceMatcher(
                        None, title.upper(), (cur.get("title") or "").upper()).ratio() >= 0.75
                    if not repeat and not cur_same and title:
                        renumbered.append(f"read {m.group(1)} ({num}), sequence gives {last + 1}: {title}")
                        num, tag = last + 1, f"ch{last + 1}"
                    elif cur_same and tag not in seen:
                        i = j; continue           # this chapter's heading again, with its numeral misread
                label = f"Chapter {to_roman(num)}" + (f": {title_case(title)}" if title else "")
                if tag in seen:
                    # the same heading printed again (half-title, plate page): not a new chapter, but if
                    # this printing was read more surely, its reading of the title wins
                    d = by_tag[tag]
                    same = difflib.SequenceMatcher(None, title.upper(), (d["title"] or "").upper()).ratio()
                    if title and tconf > d["title_conf"] and (not d["title"] or same >= 0.5):
                        d.update(label=label, title=title, title_conf=tconf)
                    i = j; continue
                seen.add(tag)
                cur = {"label": label, "key": tag, "items": [], "heading": s["text"], "title": title,
                       "title_conf": tconf if title else -1}
                by_tag[tag] = cur
                divisions.append(cur)
                i = j; continue
            if cur is not None:
                # an unnumbered section opens a division only when the run DECLARES it (extra_heads):
                # a guessed one would turn every caption in capitals into a chapter
                key = L._norm([{"t": s["text"]}])
                hit = next((h for h in extras if difflib.SequenceMatcher(None, key, h).ratio() >= 0.85), None)
                if hit:
                    tag = re.sub(r"[^a-z]+", "-", extras[hit].lower()).strip("-")
                    if tag not in seen:
                        seen.add(tag)
                        cur = {"label": title_case(extras[hit]), "key": tag, "items": [], "heading": s["text"],
                               "title": extras[hit], "title_conf": _conf([s])}
                        by_tag[tag] = cur
                        divisions.append(cur)
                    i += 1; continue
                # the chapter's title printed again (over a plate, on a half-title): not a heading
                if difflib.SequenceMatcher(None, s["text"].upper(), (cur.get("title") or "").upper()).ratio() >= 0.6:
                    i += 1; continue
        if cur is not None and s["type"] in ("para", "quote") and len(s["text"].split()) <= 6 \
                and difflib.SequenceMatcher(None, s["text"].upper(), (cur.get("title") or "").upper()).ratio() >= 0.5:
            i += 1; continue          # the chapter title reprinted on a half-title, misread as body
        (cur["items"] if cur is not None else front).append(s)
        i += 1
    log["renumbered"] = renumbered
    return front, divisions, log


def _conf(items):
    cs = [w["conf"] for it in items for _, ws in it.get("lines", []) for w in ws]
    return sum(cs) / len(cs) if cs else 0


def units(divisions, slug):
    out = []
    for d in divisions:
        n = 0
        for s in d["items"]:
            if s["type"] not in ("para", "quote"):
                continue
            n += 1
            out.append({"id": f"{slug}:{d['key']}.{n}", "ref": f"{d['label']}, par. {n}", "text": s["text"],
                        "links": [], "pages": s["pages"]})
    return out


def confidence(pages):
    cs = [w["conf"] for p in pages if p["kind"] == "text" for ln in p["lines"] for w in ln["words"]]
    if not cs:
        return {}
    return {"words": len(cs), "mean_conf": round(statistics.mean(cs), 2),
            "below_80": sum(1 for c in cs if c < 80), "below_60": sum(1 for c in cs if c < 60)}
