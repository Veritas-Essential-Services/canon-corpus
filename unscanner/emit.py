"""Outputs: the book re-set, four ways, plus the sheet a person proofs it against.

  reflow/index.html   the book as a reader reads it: chapters, paragraphs, italics, plates, in the
                      matched typeface (embedded; OFL)
  pages/index.html    the FAITHFUL edition: every page at its printed size, every word at the place it
                      was printed, in the matched face, scaled to the printed word's width; plates and
                      ornaments are cut from the scan, never redrawn
  book.epub           the reflowed book as EPUB 3, font and plates inside
  units.json          the canon-corpus book shape ({id, ref, text, links}) for ingestion, every unit
                      carrying the scan pages and printed page labels it came from
  review.html         scan beside reconstruction, page by page; words the OCR read with low confidence
                      are marked; the numbers that say how far to trust it are at the top
"""
import html
import json
import os
import uuid
import zipfile

from PIL import Image

from . import fonts as F
from . import images as I
from . import scan as S

esc = html.escape


def _toks_html(toks):
    out, in_i = [], False
    for t in toks:
        if t["it"] and not in_i:
            out.append("<i>"); in_i = True
        elif not t["it"] and in_i:
            out[-1] = out[-1].rstrip()
            out.append("</i> "); in_i = False
        out.append(esc(t["t"]) + " ")
    s = "".join(out).rstrip()
    return s + ("</i>" if in_i else "")


def plate_images(work, pdf, pages, dpi_colour=150, dpi_ocr=300):
    """Cut every plate and figure from a colour raster. -> {(page n, idx): relative jpg path}."""
    out = {}
    os.makedirs(work.p("img"), exist_ok=True)
    for p in pages:
        if not p["figures"]:
            continue
        col = work.p("colour", f"{p['n']:04d}.png")
        S.rasterize(pdf, p["n"], col, dpi=dpi_colour, gray=False)
        for k, bb in enumerate(p["figures"]):
            name = f"p{p['n']:04d}-{bb[0]}-{bb[1]}-{bb[2]}-{bb[3]}.jpg"     # named by its box: a re-run never reuses a stale cut
            path = work.p("img", name)
            if not os.path.exists(path):
                I.crop(col, bb, dpi_colour / dpi_ocr, path)
            out[(p["n"], k)] = name
    return out


def _fig_html(item, imgs, prefix):
    if item["type"] == "plate":
        ims = [imgs.get((item["page"], k)) for k in range(len(item["figures"]))]
        cap = " ".join(" ".join(w["t"] for w in ws) for ws in item["caption"])
        body = "".join(f'<img src="{prefix}{esc(i)}" alt="">' for i in ims if i)
        return f'<figure class="plate">{body}' + (f"<figcaption>{esc(cap)}</figcaption>" if cap else "") + "</figure>"
    return ""


def _items_html(items, imgs, prefix, figure_index):
    out = []
    for s in items:
        if s["type"] == "para":
            out.append(f'<p>{_toks_html(s["toks"])}</p>')
        elif s["type"] == "quote":
            out.append(f'<blockquote>{_toks_html(s["toks"])}</blockquote>')
        elif s["type"] == "heading":
            out.append(f'<h3>{_toks_html(s["toks"])}</h3>')
        elif s["type"] == "plate":
            out.append(_fig_html(s, imgs, prefix))
        elif s["type"] == "figure":
            k = figure_index.get((s["page"], tuple(s["bbox"])))
            name = imgs.get((s["page"], k)) if k is not None else None
            if name:
                out.append(f'<figure class="cut"><img src="{prefix}{esc(name)}" alt=""></figure>')
    return "\n".join(out)


def _figure_index(pages):
    return {(p["n"], tuple(bb)): k for p in pages for k, bb in enumerate(p["figures"])}


BOOK_CSS = """
body{font-family:'%(fam)s',Georgia,serif;font-size:%(pt)spt;line-height:1.45;max-width:34em;margin:2em auto;
padding:0 16px;color:#222;background:#fbf8f1}
h1,h2{font-weight:400;text-align:center;letter-spacing:.06em}
h2{margin-top:3em;font-size:1.15em;text-transform:uppercase}
p{margin:0;text-indent:1.5em;text-align:justify;hyphens:auto}
h2+p,figure+p,blockquote+p{text-indent:0}
blockquote{margin:.6em 2em;white-space:normal}
figure{margin:1.5em 0;text-align:center}figure img{max-width:100%%}
figcaption{font-size:.85em;letter-spacing:.05em;margin-top:.4em}
.front{color:#555;font-size:.9em}
@media (prefers-color-scheme:dark){body{background:#1d1b18;color:#e8e2d6}}
"""


def reflow_html(work, meta, front, divisions, imgs, fam, font_info, pages):
    d = work.p("out", "reflow")
    os.makedirs(d, exist_ok=True)
    faces = F.css_face(font_info, fam, embed_dir=d) if font_info else ""
    for name in set(imgs.values()):
        open(os.path.join(d, name), "wb").write(open(work.p("img", name), "rb").read())
    fi = _figure_index(pages)
    css = faces + BOOK_CSS % {"fam": fam, "pt": min(13, max(10, round(meta.get("pt", 12))))}
    parts = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
             f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>{esc(meta['title'])}</title><style>{css}</style></head><body>",
             f"<h1>{esc(meta['title'])}</h1><p style='text-align:center;text-indent:0'>{esc(meta['author'])}</p>"]
    if front:
        parts.append(f"<div class='front'>{_items_html(front, imgs, '', fi)}</div>")
    for dv in divisions:
        parts.append(f"<h2 id='{esc(dv['key'])}'>{esc(dv['label'])}</h2>")
        parts.append(_items_html(dv["items"], imgs, "", fi))
    parts.append(f"<hr><p class='front'>{esc(meta['colophon'])}</p></body></html>")
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(parts))
    return os.path.join(d, "index.html")


FIT_JS = """
document.querySelectorAll('.w').forEach(function(s){var w=+s.dataset.w;var r=s.getBoundingClientRect().width;
if(r>0)s.style.transform='scaleX('+(w/r).toFixed(3)+')';});
"""


def pages_html(work, meta, pages, imgs, fam, font_info, px_em):
    """The faithful edition: absolutely positioned words over a page the size of the original."""
    d = work.p("out", "pages")
    os.makedirs(d, exist_ok=True)
    faces = F.css_face(font_info, fam, embed_dir=d) if font_info else ""
    for name in set(imgs.values()):
        open(os.path.join(d, name), "wb").write(open(work.p("img", name), "rb").read())
    css = faces + (f".pg{{position:relative;margin:24px auto;background:#fffdf8;box-shadow:0 1px 4px #0003;"
                   f"font-family:'{fam}',Georgia,serif;color:#1a1a1a}}"
                   ".w{position:absolute;white-space:pre;transform-origin:0 0;line-height:1}"
                   ".fig{position:absolute}.lbl{text-align:center;font:12px sans-serif;color:#888}"
                   "body{background:#ddd;margin:0}")
    out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{esc(meta['title'])} (pages)</title>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'><style>{css}</style></head><body>"]
    scale = 0.5        # 300 dpi raster -> 150 css px per inch: a page close to print size on screen
    for p in pages:
        w, h = p["w"] * scale, p["h"] * scale
        out.append(f"<div class='lbl'>scan p.{p['n']}" + (f" · printed {esc(p['label'])}" if p.get("label") else "")
                   + f" · {p['kind']}</div><div class='pg' id='p{p['n']}' style='width:{w:.0f}px;height:{h:.0f}px'>")
        for k, bb in enumerate(p["figures"]):
            name = imgs.get((p["n"], k))
            if name:
                x0, y0, x1, y1 = [v * scale for v in bb]
                out.append(f"<img class='fig' src='{esc(name)}' style='left:{x0:.0f}px;top:{y0:.0f}px;"
                           f"width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px' alt=''>")
        if p["kind"] != "plate":
            for ln in p["lines"]:
                for wd in ln["words"]:
                    x0, y0, x1, y1 = [v * scale for v in wd["bbox"]]
                    # the em box: baseline sits ~0.8 em below the top of the ascenders
                    fs = px_em * scale
                    top = (ln["bbox"][3] + ln["baseline"][1]) * scale - 0.8 * fs if ln["baseline"] else y0
                    st = "font-style:italic;" if wd.get("it") else ""
                    t = wd["t"]
                    if wd.get("sc"):
                        st += "font-variant:small-caps;"
                        t = t[:1] + t[1:].lower() if wd["sc"] == "cap" else t.lower()
                    out.append(f"<span class='w' data-w='{x1 - x0:.1f}' style='left:{x0:.1f}px;top:{top:.1f}px;"
                               f"font-size:{fs:.1f}px;{st}'>{esc(t)}</span>")
        out.append("</div>")
    out.append(f"<script>{FIT_JS}</script></body></html>")
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(out))
    return os.path.join(d, "index.html")


def epub(work, meta, front, divisions, imgs, fam, font_info, pages):
    path = work.p("out", "book.epub")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fi = _figure_index(pages)
    bid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "unscanner:" + meta["slug"]))
    css = (F.css_face(font_info, fam, rel="fonts/") if font_info else "") + BOOK_CSS % {"fam": fam, "pt": 11}
    css = css.split("@media")[0]
    chapters = []
    if front:
        chapters.append(("front", "Front matter", front))
    for dv in divisions:
        chapters.append((dv["key"], dv["label"], dv["items"]))

    def xhtml(title, body):
        return ("<?xml version='1.0' encoding='utf-8'?>\n<html xmlns='http://www.w3.org/1999/xhtml' "
                "xmlns:epub='http://www.idpf.org/2007/ops' xml:lang='en'><head><meta charset='utf-8'/>"
                f"<title>{esc(title)}</title><link rel='stylesheet' href='book.css'/></head><body>{body}</body></html>")

    def x(s):   # html void tags -> xhtml
        return s.replace("<hr>", "<hr/>").replace("alt=\"\">", "alt=\"\"/>")

    files = []
    with zipfile.ZipFile(path + ".part", "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   "<?xml version='1.0'?><container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:container'>"
                   "<rootfiles><rootfile full-path='OEBPS/content.opf' media-type='application/oebps-package+xml'/>"
                   "</rootfiles></container>", compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/book.css", css, compress_type=zipfile.ZIP_DEFLATED)
        manifest = ["<item id='css' href='book.css' media-type='text/css'/>",
                    "<item id='nav' href='nav.xhtml' media-type='application/xhtml+xml' properties='nav'/>"]
        if font_info:
            for fn in sorted(os.listdir(font_info["dir"])):
                if fn.endswith(".woff2"):
                    z.write(os.path.join(font_info["dir"], fn), f"OEBPS/fonts/{fn}")
                    manifest.append(f"<item id='f-{fn[:-6]}' href='fonts/{fn}' media-type='font/woff2'/>")
        for name in sorted(set(imgs.values())):
            z.write(work.p("img", name), f"OEBPS/{name}")
            manifest.append(f"<item id='i-{name[:-4]}' href='{name}' media-type='image/jpeg'/>")
        title_body = f"<h1>{esc(meta['title'])}</h1><p style='text-align:center'>{esc(meta['author'])}</p>"
        z.writestr("OEBPS/title.xhtml", xhtml(meta["title"], title_body), compress_type=zipfile.ZIP_DEFLATED)
        manifest.append("<item id='title' href='title.xhtml' media-type='application/xhtml+xml'/>")
        files.append(("title", "title.xhtml", meta["title"]))
        for key, label, items in chapters:
            fn = f"{key}.xhtml"
            body = f"<h2>{esc(label)}</h2>" + x(_items_html(items, imgs, "", fi))
            z.writestr(f"OEBPS/{fn}", xhtml(label, body), compress_type=zipfile.ZIP_DEFLATED)
            manifest.append(f"<item id='c-{key}' href='{fn}' media-type='application/xhtml+xml'/>")
            files.append((f"c-{key}", fn, label))
        nav = "".join(f"<li><a href='{fn}'>{esc(lbl)}</a></li>" for _, fn, lbl in files)
        z.writestr("OEBPS/nav.xhtml", xhtml("Contents", f"<nav epub:type='toc'><ol>{nav}</ol></nav>"),
                   compress_type=zipfile.ZIP_DEFLATED)
        spine = "".join(f"<itemref idref='{i}'/>" for i, _, _ in files)
        opf = ("<?xml version='1.0' encoding='utf-8'?><package xmlns='http://www.idpf.org/2007/opf' version='3.0' "
               "unique-identifier='bid'><metadata xmlns:dc='http://purl.org/dc/elements/1.1/'>"
               f"<dc:identifier id='bid'>{bid}</dc:identifier><dc:title>{esc(meta['title'])}</dc:title>"
               f"<dc:creator>{esc(meta['author'])}</dc:creator><dc:language>en</dc:language>"
               f"<dc:source>{esc(meta['source'])}</dc:source><dc:rights>{esc(meta['rights'])}</dc:rights>"
               f"<meta property='dcterms:modified'>{meta['modified']}</meta></metadata>"
               f"<manifest>{''.join(manifest)}</manifest><spine>{spine}</spine></package>")
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(path + ".part", path)
    return path


def review_html(work, meta, pages, report, thumbs_scale=0.4):
    """Scan beside reconstruction, low-confidence words marked. For proofing, not for reading."""
    d = work.p("out", "review")
    os.makedirs(d, exist_ok=True)
    rows = []
    for p in pages:
        thumb = f"s{p['n']:04d}.jpg"
        tp = os.path.join(d, thumb)
        if not os.path.exists(tp):
            im = Image.open(work.p("gray", f"{p['n']:04d}.png"))
            im.resize((int(im.width * thumbs_scale), int(im.height * thumbs_scale))).convert("L").save(tp, quality=70)
        dropped = set(p.get("drop", []))
        lines = []
        for i, ln in enumerate(p["lines"]):
            ws = " ".join((f"<mark title='conf {w['conf']}" + (f"; we read {esc(w['was'])}" if w.get('was') else "")
                           + f"'>{esc(w['t'])}</mark>" if w["conf"] < 80 else esc(w["t"])) for w in ln["words"])
            cls = " class='furn'" if i in dropped else ""
            lines.append(f"<div{cls}>{ws}</div>")
        low = sum(1 for ln in p["lines"] for w in ln["words"] if w["conf"] < 80)
        rows.append(f"<section><h3>scan p.{p['n']} · {p['kind']}" + (f" · printed {esc(p['label'])}" if p.get('label') else "")
                    + f" · {low} low-confidence</h3><div class='pair'><img src='{thumb}' alt='scan page {p['n']}'>"
                    f"<div class='rec'>{''.join(lines)}</div></div></section>")
    fonts = "".join(f"<tr><td>{esc(r['family'])}</td><td>{r['score']}</td><td>{r['width_ratio']}</td>"
                    f"<td>{r['pt']}</td><td>{esc(r['why'])}</td></tr>" for r in report.get("fonts", []))
    stats = esc(json.dumps({k: (v if k != "collation" or not v else {x: y for x, y in v.items() if x != "mends"})
                            for k, v in report.items() if k not in ("fonts", "hyphens")}, indent=1))
    doubt = esc(", ".join(report.get("hyphens", {}).get("doubtful", [])[:200]))
    mends = (report.get("collation") or {}).get("mends", [])
    mend_rows = "".join(f"<tr><td>{esc(m['was'])}</td><td>{esc(m['now'])}</td><td>{m['conf']}</td></tr>" for m in mends)
    css = ("body{font:14px/1.4 Georgia,serif;margin:0 16px;background:#f6f4ef;color:#222}"
           ".pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}.pair img{width:100%;border:1px solid #ccc}"
           ".rec{font-size:13px}.furn{color:#999;text-decoration:line-through}mark{background:#ffd76a}"
           "table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:2px 6px}"
           "@media(max-width:700px){.pair{grid-template-columns:1fr}}"
           "@media(prefers-color-scheme:dark){body{background:#1d1b18;color:#e8e2d6}mark{background:#7a5d00;color:#fff}}")
    doc = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' "
           f"content='width=device-width,initial-scale=1'><title>Unscanner review: {esc(meta['title'])}</title>"
           f"<style>{css}</style></head><body><h1>{esc(meta['title'])}: review sheet</h1>"
           f"<p>Left, the scan; right, what the Unscanner read. <mark>Marked</mark> words were read with confidence "
           f"under 80; struck-through lines are page furniture (folios, running heads) left out of the text.</p>"
           f"<h2>Typeface match</h2><p>The closest of the open candidates, not proof of the original face."
           + (" <b>Inconclusive:</b> the top two score within 0.01 of each other." if (report.get("font_margin") or 1) < 0.01 else "")
           + " The point size assumes the PDF states the page's real size; library scans often do not.</p>"
           f"<table><tr><th>family</th><th>score</th><th>width ratio</th><th>pt</th><th>candidate because</th></tr>"
           f"{fonts}</table><h2>Numbers</h2><pre>{stats}</pre><h2>Margin hyphens with no evidence either way</h2>"
           f"<p>{doubt or 'none'}</p><h2>Words mended from the second witness</h2>"
           f"<p>Our reading was unsure and unattested; the Archive's OCR read it as a word the book prints "
           f"elsewhere. Check these first.</p><table><tr><th>we read</th><th>now</th><th>conf</th></tr>{mend_rows}</table>"
           f"{''.join(rows)}</body></html>")
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
    return os.path.join(d, "index.html")


def units_json(work, meta, unit_rows, pages, report):
    labels = {p["n"]: p.get("label") for p in pages}
    for u in unit_rows:
        u["printed"] = [labels[n] for n in u["pages"] if labels.get(n)]
    book = {"slug": meta["slug"], "title": meta["title"], "author": meta["author"],
            "source": {"format": "unscanner", "archive_id": meta.get("ident"), "pdf_sha256": meta.get("pdf_sha256"),
                       "tool": "canon-corpus/unscanner", "font_match": (report.get("fonts") or [{}])[0].get("family")},
            "scheme": {"apparatus": "re-OCR'd from the scan with layout: paragraphs from printed indentation, headings "
                                    "from size and centring, folios and running heads removed by position and "
                                    "recurrence, margin hyphens rejoined by the book's own spellings; italic and small "
                                    "capitals measured from the ink" + (
                                        f"; {report['collation']['mended']} unsure words mended from the Archive's own "
                                        f"OCR (a second witness) where the book attests that reading elsewhere"
                                        if report.get("collation") else ""),
                       "citation": "chapter + paragraph", "resolution": "paragraph",
                       "honesty": f"UNPROOFREAD OCR (tesseract) of a library scan (archive.org {meta.get('ident')}), mean "
                                  f"word confidence {report.get('confidence', {}).get('mean_conf')}: misreadings "
                                  f"stand; paragraph breaks are read from indentation, so a paragraph ending exactly "
                                  f"at a page's foot is detected by the next page's indent; each unit names its "
                                  f"scan pages and printed page labels"},
            "units": unit_rows}
    path = work.p("out", "units.json")
    with open(path + ".part", "w", encoding="utf-8") as f:
        json.dump(book, f, ensure_ascii=False, indent=1)
    os.replace(path + ".part", path)
    return path
