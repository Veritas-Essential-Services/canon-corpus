#!/usr/bin/env python3
"""press_build.py -- the Press: set a catalogued Puritan classic as a book.

    python3 pipeline/press_build.py --list                # the catalog and each title's state
    python3 pipeline/press_build.py owen-mortification    # fetch (if needed), set, export, QA
    python3 pipeline/press_build.py --ready               # every title whose source is ready
    python3 pipeline/press_build.py --qa-report           # rewrite docs/press/QA.md from built books

Reads pipeline/press_catalog.json (which titles, from which PD edition) and
pipeline/press_rules/<slug>.json (that book's corrections, each with its
evidence -- rule 2: fixes live in rules that rerun, never in the source).
Writes data/press/<slug>/ (gitignored, rebuildable):
    <slug>.md     Pandoc Markdown, the master file
    <slug>.epub   EPUB 3 (Pandoc, pipeline/press_style.css)
    <slug>.html   one-page HTML preview, same stylesheet
    qa.json       the checks below, as numbers and lists
Every write is temp-file + rename (rule 5).

QA (the "small step from publish-ready" gate):
  - scripture references found, tagged, and any that fail the KJV versification
  - footnotes defined vs referenced
  - leftover markup or entity debris in the text (<, &amp;, stray brackets)
  - unbalanced quotation marks per paragraph (flagged, not "fixed")
  - words the spelling list does not know and the book uses only once or
    twice: the proofing worklist (pipeline/press_proof.py collates them
    against the scan)
"""
import hashlib, json, os, re, subprocess, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import press_render

CATALOG = os.path.join(HERE, "press_catalog.json")
RULES = os.path.join(HERE, "press_rules")
SRC = os.path.join(ROOT, "data", "corpus", "press")
OUT = os.path.join(ROOT, "data", "press")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}
PRESS_VERSION = "press-1"

def atomic_write(path, data, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(data)
    os.replace(tmp, path)

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        return dest
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                data = r.read()
            if len(data) < 5000:
                raise RuntimeError(f"only {len(data)} bytes")
            atomic_write(dest, data, "wb")
            return dest
        except Exception as e:
            err = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")

def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def source_file(slug, e):
    s = e["source"]
    if s["kind"] == "ccel":
        return fetch(f"https://ccel.org/ccel/{s['path']}.xml", os.path.join(SRC, slug + ".xml"))
    if s["kind"] == "gutenberg":
        n = s["id"]
        return fetch(f"https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt", os.path.join(SRC, f"pg{n}.txt"))
    if s["kind"] == "ia-extract":
        if "leaves" not in s:
            raise RuntimeError(f"{slug}: the catalog does not yet name the treatise's leaves in its volume")
        import press_abbyy
        ident = s.get("ia") or json.load(open(os.path.join(HERE, f"{s['shelf']}_shelf.json"),
                                              encoding="utf-8"))["internet_archive"][s["volume"]][0]
        press_abbyy.load(ident)
        return os.path.join(SRC, "ia", f"{ident}_abbyy.gz")
    if s["kind"] == "tcp":
        i = s["id"]
        return fetch(f"https://raw.githubusercontent.com/textcreationpartnership/{i}/master/{i}.xml",
                     os.path.join(SRC, "tcp", f"{i}.xml"))
    raise RuntimeError(f"{slug}: source kind {s['kind']!r} is not settable ({s.get('why', '')})")

def load_rules(slug):
    p = os.path.join(RULES, f"{slug}.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}

def apply_rules(doc, rules):
    """Each correction must match exactly `count` times (default 1) across
    the book, or the build stops: a rule that silently stops matching after a
    refetch is a correction quietly lost."""
    applied = []
    for r in rules.get("corrections", []):
        want = r.get("count", 1)
        hits = sum(b.get("md", "").count(r["find"]) for b in doc["blocks"]) + \
            sum(v.count(r["find"]) for v in doc["notes"].values())
        if hits != want:
            raise RuntimeError(f"rule {r['find']!r}: expected {want} match(es), found {hits}")
        for b in doc["blocks"]:
            if "md" in b:
                b["md"] = b["md"].replace(r["find"], r["replace"])
        for k in doc["notes"]:
            doc["notes"][k] = doc["notes"][k].replace(r["find"], r["replace"])
        applied.append(r)
    for sec in rules.get("drop_sections", []):
        doc["blocks"] = [b for b in doc["blocks"] if b.get("section") != sec]
    return applied

# --------------------------------------------------------------------- QA
_WORDS = None
def wordlist():
    global _WORDS
    if _WORDS is None:
        try:
            from spellchecker import SpellChecker
            _WORDS = set(SpellChecker().word_frequency.dictionary)
        except Exception:
            _WORDS = set()
        extra = os.path.join(HERE, "press_words.txt")
        if os.path.exists(extra):
            _WORDS |= {w.strip().lower() for w in open(extra, encoding="utf-8") if w.strip() and not w.startswith("#")}
    return _WORDS

def known(w, words):
    """A word the spelling list lacks only because it is old or British:
    -eth/-est verbs, -our and -ise spellings, -ings/-ments of known stems,
    roman numerals. Such words are not proofing work."""
    if w in words or w.replace("'", "") in words:
        return True
    if re.fullmatch(r"[ivxlc]+", w):
        return True
    cands = {w.replace("our", "or"), w.replace("ise", "ize"), w.replace("isa", "iza"),
             w.replace("lled", "led"), w.replace("lling", "ling"), w.replace("ll", "l")}
    for suf, adds in (("eth", ("", "e", "s")), ("est", ("", "e")), ("edst", ("", "e")),
                      ("st", ("",)), ("ings", ("", "e")), ("ing", ("", "e")), ("ments", ("", "e")),
                      ("ment", ("", "e")), ("ies", ("y",)), ("s", ("",)), ("ness", ("",)), ("ed", ("", "e")),
                      ("ly", ("", "le")), ("ishest", ("ish",)), ("est", ("y",)), ("ency", ("ence", "ent")),
                      ("ancy", ("ance", "ant")), ("ious", ("y",))):
        if w.endswith(suf) and len(w) > len(suf) + 2:
            stem = w[: -len(suf)]
            for a in adds:
                cands.add(stem + a)
                if len(stem) > 2 and stem[-1] == stem[-2]:
                    cands.add(stem[:-1] + a)
    cands |= {c.replace("our", "or") for c in list(cands)}
    for pre in ("un", "dis", "in", "re", "mis", "over", "out", "fore", "be", "en", "im", "non", "self"):
        if w.startswith(pre) and len(w) > len(pre) + 3:
            cands.add(w[len(pre):])
    return any(c in words for c in cands)

def qa(doc, md):
    q = {}
    refs = doc.get("refs", [])
    q["scripture_refs"] = len(refs)
    q["scripture_refs_tagged"] = sum(1 for r in refs if r["ids"])
    q["scripture_verse_ids"] = len({i for r in refs for i in r["ids"]})
    q["ref_problems"] = doc.get("problems", [])
    body = [b["md"] for b in doc["blocks"] if b.get("k") in ("para", "argument", "quote")]
    q["paragraphs"] = len(body)
    page_notes = [n for b in doc["blocks"] if b.get("k") == "pagefoot" for n in b["notes"]]
    text = "\n".join(body + list(doc["notes"].values()) + page_notes)
    plain = press_render.plain(text)
    q["words"] = len(re.findall(r"[A-Za-zÀ-ɏ]+", plain))
    q["footnotes"] = len(doc["notes"])
    q["page_notes"] = len(page_notes)    # notes kept at their page's foot: the scan lost their calls
    # a call can sit in any block: a heading, a list item, a table cell
    every = [b.get("md") or "" for b in doc["blocks"]] + \
        [it for b in doc["blocks"] for it in b.get("items", [])] + \
        [c for b in doc["blocks"] for r in b.get("rows", []) for c in r]
    used = set(re.findall(r"\[\^([^\]]+)\]", "\n".join(every)))
    q["footnotes_unreferenced"] = sorted(set(doc["notes"]) - used)
    q["footnotes_orphaned"] = len(q["footnotes_unreferenced"])
    q["markup_debris"] = [m.group(0) for m in re.finditer(r"&[a-z]+;|<[a-zA-Z/][^>]{0,30}>|\{\.|\]\{(?![.#]|lang=)", plain)][:20]
    unb = []
    for b in doc["blocks"]:
        if b.get("k") != "para":
            continue
        p = press_render.plain(b["md"])
        if p.count("“") != p.count("”"):
            unb.append(f"{b['section']}: “{p.count(chr(0x201c))} ”{p.count(chr(0x201d))} | {p[:60]}")
    q["unbalanced_double_quotes"] = len(unb)
    q["unbalanced_samples"] = unb[:15]
    words = wordlist()
    if words:
        from collections import Counter
        toks = Counter(w.lower() for w in re.findall(r"[A-Za-z][a-z]+(?:'[a-z]+)?", plain)
                       if not w[0].isupper())
        unknown = {w: n for w, n in toks.items() if n <= 2 and len(w) > 2 and not known(w, words)}
        q["unknown_rare_words"] = len(unknown)
        q["unknown_rare_sample"] = sorted(unknown)[:80]
    return q

# --------------------------------------------------------------------- build
def keyed_from(doc):
    """The print edition CCEL keyed its file from (ThML <published>), which is
    often a modern reprint and is not stated in DC.Rights."""
    return ((doc.get("meta") or {}).get("published") or "").rstrip(" .")

def note_on_text(e, slug, doc, applied, src_path):
    s = e["source"]
    if s["kind"] == "ccel":
        where = (f"This text is set from {s['edition']} (ccel.org/ccel/{s['path']}). The Christian Classics "
                 f"Ethereal Library's markup was read for structure, italics, footnotes and scripture "
                 f"references; its own introductions and indexes were not used.")
        keyed = keyed_from(doc)
        if keyed and keyed.lower().split()[0] in ("the", "banner") and "banner" in keyed.lower():
            proofed = os.path.exists(os.path.join(ROOT, "docs", "press", "proof", f"{slug}.md"))
            where += (f" CCEL keyed it from a modern photographic reprint ({keyed}) of that edition; the "
                      f"reprint's own preface and editorial matter were not used. The text "
                      + ("has been proofed" if proofed else "is still to be proofed")
                      + " against a scan of the 19th-century printing itself.")
        elif keyed:
            where += f" CCEL keyed it from {keyed}."
    elif s["kind"] == "gutenberg":
        where = f"This text is set from {s['edition']}, with the Project Gutenberg header and licence removed."
    elif s["kind"] == "tcp":
        where = (f"This text is set from {s['edition']}, as keyed by hand from the page images of the "
                 f"first edition by the Text Creation Partnership (EEBO-TCP {s['id']}, released under CC0). "
                 f"The long s is set as s; every other spelling, capital and stop is the 17th-century "
                 f"printer's. The marginal notes of the original are given as footnotes.")
    else:
        where = f"This text is set from the Internet Archive scan of {s['edition']}, re-read from its OCR and proofed."
    paras = [where,
             f"The text is the source edition's own: spelling, capitalisation and punctuation are kept as "
             f"printed, nothing is modernised or abridged, and the original title page is reproduced. "
             f"Page breaks of the source edition are kept as invisible anchors, so any passage can be "
             f"checked against the scan of its page."]
    gaps = doc.get("gaps") or []
    ill = sum(1 for g in gaps if g[0].startswith("illegible"))
    frn = sum(1 for g in gaps if g[0].startswith("foreign"))
    if ill or frn:
        paras.append(f"Not yet supplied: {ill} place(s) the transcribers could not read in their copy, marked "
                     f"⟨•⟩ (a letter) or ⟨word⟩, and {frn} Greek or Hebrew passage(s) they did not key, marked "
                     f"⟨Greek or Hebrew⟩. Each is to be read from a page image; none is guessed.")
    if doc.get("errata"):
        paras.append("The first edition prints a list of errata; it is not yet applied to the text: "
                     + " ".join(doc["errata"])[:1500])
    pf = sum(len(b["notes"]) for b in doc["blocks"] if b.get("k") == "pagefoot")
    if pf:
        paras.append(f"{pf} footnote(s) are printed at the foot of their page (“Notes to p. …”) because the "
                     f"scan lost the marks that tie them to a word; they are not guessed into a sentence.")
    if e.get("banner_title"):
        paras.append(f"Readers may know this work as *{press_render.plain(e['banner_title'])}*, the title of "
                     f"a modern reprint. This edition does not draw on any modern edition's wording, abridgement, "
                     f"introduction or notes.")
    n_ok = sum(1 for r in doc["refs"] if r["ids"])
    paras.append(f"Scripture references ({n_ok} of {len(doc['refs'])}) are tagged with their King James "
                 f"verse identifiers and gathered in the Index of Scripture References. A reference the "
                 f"King James versification does not have is left as printed and untagged.")
    if applied:
        paras.append(f"Corrections made to the source text ({len(applied)}):")
        for r in applied:
            paras.append(f"- “{r['find']}” → “{r['replace']}”: {r.get('why', '')}")
    else:
        paras.append("No corrections have been made to the source text.")
    paras.append(f"Set by the Canon Corpus Press ({PRESS_VERSION}) from source file sha256 "
                 f"{sha256(src_path)[:16]}….")
    return paras

def convert(slug, e, path):
    k = e["source"]["kind"]
    if k == "ccel":
        import press_thml
        return press_thml.convert(path, slug)
    if k == "gutenberg":
        import press_text
        return press_text.convert_gutenberg(path, slug, e)
    if k == "ia-extract":
        import press_text
        return press_text.convert_ia(path, slug, e)
    if k == "tcp":
        import press_tcp
        return press_tcp.convert(path, slug, e["source"].get("texts"), e["source"].get("span"))
    raise RuntimeError(k)

def build(slug, cat):
    e = cat["titles"][slug]
    path = source_file(slug, e)
    doc = convert(slug, e, path)
    rules = load_rules(slug)
    applied = apply_rules(doc, rules)
    m = {"slug": slug, "title": rules.get("title") or e["title"], "subtitle": rules.get("subtitle"),
         "author": e["author"], "first_published": e.get("first_published"),
         "source_edition": e["source"].get("edition"),
         "rights_line": "The text of this edition is in the public domain.",
         "description": e.get("description")}
    m["note_on_text"] = note_on_text(e, slug, doc, applied, path)
    md = press_render.render(doc, m)
    d = os.path.join(OUT, slug)
    atomic_write(os.path.join(d, f"{slug}.md"), md)
    css = os.path.join(HERE, "press_style.css")
    log = []
    for fmt, ext, extra in (("epub3", "epub", ["--css", css, "--split-level=1"]),
                            ("html5", "html", ["--css", "press_style.css", "--standalone", "--embed-resources"])):
        target = os.path.join(d, f"{slug}.{ext}")
        cmd = [pandoc(), os.path.join(d, f"{slug}.md"), "-f", "markdown", "-t", fmt, "-o", target + ".tmp." + ext,
               "--toc", "--toc-depth=2"] + extra
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=HERE)
        if r.returncode:
            raise RuntimeError(f"pandoc {fmt}: {r.stderr[-800:]}")
        os.replace(target + ".tmp." + ext, target)
        log += [l for l in r.stderr.splitlines() if l.strip()]
    q = qa(doc, md)
    if e["source"]["kind"] == "ccel":
        q["keyed_from"] = keyed_from(doc) or "not stated"
    q["pandoc_warnings"] = log[:30]
    q["corrections_applied"] = len(applied)
    q["source_sha256"] = sha256(path)
    q["md_sha256"] = hashlib.sha256(md.encode("utf-8")).hexdigest()
    q["built"] = time.strftime("%Y-%m-%d")
    q["press"] = PRESS_VERSION
    atomic_write(os.path.join(d, "qa.json"), json.dumps(q, indent=1, ensure_ascii=False))
    return q

def pandoc():
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except Exception:
        return "pandoc"

def qa_report(cat):
    L = ["# The Press — QA of built books", "",
         "Generated by `python3 pipeline/press_build.py --qa-report` from `data/press/*/qa.json` "
         "(the books themselves are gitignored and rebuildable). Numbers only; no book text.", "",
         "Source: ccel, gutenberg (transcriptions), tcp (hand-keyed first edition), ia-extract (OCR of a "
         "scan, proofed by two engines). Page notes: footnotes kept at their page's foot because the scan "
         "lost their call marks. Unread: places marked ⟨•⟩ / ⟨word⟩ / ⟨Greek or Hebrew⟩ that a person must "
         "supply from a page image. Rare unknown words: the proofing worklist. Keyed from: for a CCEL "
         "file, the print edition CCEL says it keyed from (its <published> field, not its rights line); "
         "a Banner of Truth reprint of Goold is a photographic reprint, so the book is proofed against "
         "the 1850s Goold scan.", "",
         "| Book | Source | Keyed from | Words | Paras | Notes | Page notes | Scripture refs (tagged) | KJV ids | Ref problems | Unbalanced “” | Unread | Rare unknown words | Corrections |",
         "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for slug in sorted(cat["titles"]):
        p = os.path.join(OUT, slug, "qa.json")
        if not os.path.exists(p):
            continue
        q = json.load(open(p, encoding="utf-8"))
        mdp = os.path.join(OUT, slug, f"{slug}.md")
        md = open(mdp, encoding="utf-8").read() if os.path.exists(mdp) else ""
        unread = md.count("⟨•⟩") + md.count("⟨word⟩") + md.count("⟨…⟩") + md.count("⟨Greek or Hebrew⟩")
        L.append(f"| {slug} | {cat['titles'][slug]['source']['kind']} | {q.get('keyed_from', '')} | {q['words']:,} | {q['paragraphs']:,} | "
                 f"{q['footnotes']} | {q.get('page_notes', 0)} | "
                 f"{q['scripture_refs']:,} ({q['scripture_refs_tagged']:,}) | {q['scripture_verse_ids']:,} | "
                 f"{len(q['ref_problems'])} | {q['unbalanced_double_quotes']} | {unread} | "
                 f"{q.get('unknown_rare_words', '-')} | {q['corrections_applied']} |")
    atomic_write(os.path.join(ROOT, "docs", "press", "QA.md"), "\n".join(L) + "\n")

def main():
    cat = json.load(open(CATALOG, encoding="utf-8"))
    args = sys.argv[1:]
    if not args or args[0] == "--list":
        for slug, e in cat["titles"].items():
            built = os.path.exists(os.path.join(OUT, slug, "qa.json"))
            print(f"{slug:36} {e['source']['kind']:11} {'BUILT' if built else '':6} {','.join(e['sets'])}")
        return
    if args[0] == "--qa-report":
        return qa_report(cat)
    slugs = [s for s, e in cat["titles"].items() if e["source"]["kind"] in ("ccel", "gutenberg", "ia-extract")] \
        if args[0] == "--ready" else args
    for slug in slugs:
        try:
            q = build(slug, cat)
            print(slug, {k: q[k] for k in ("words", "footnotes", "scripture_refs", "scripture_refs_tagged",
                                           "unbalanced_double_quotes")}, "ref problems:", len(q["ref_problems"]),
                  flush=True)
        except Exception as ex:
            print(slug, "FAILED:", str(ex)[:300], flush=True)
    qa_report(cat)

if __name__ == "__main__":
    main()
