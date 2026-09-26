#!/usr/bin/env python3
"""
reader_test.py -- the reverse-interlinear reader (launch plan D5):
pipeline/render_reader.py -> build/reader/reader.html.

Run:  python3 tests/reader_test.py

Offline, no browser: renders the page twice into a temp folder and checks
    - it is deterministic: the same bytes twice;
    - it is self-contained: no external script, stylesheet, font, image or
      fetch, no @import, no url();
    - every token in data/hymns and data/nt is on the page exactly once, as a
      button whose address has a popover payload (lemma, parsing, translit
      keys present), and no payload is orphaned;
    - `plain` and `wooden` are stored nowhere: no key of that name in any
      record of either dataset, nor in the page's embedded payload;
    - the columns: every hymn clause shows the render_plain() line, the Greek
      shows its wooden/plain columns EMPTY (it has no glosses), and every
      source a page section draws on has its licence in the rights section;
    - the agreement marks: the Column Question's own case (meum, totum and
      contemplans with cor) is drawn, and marks never reach the Greek.
"""
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, PIPE)
    spec.loader.exec_module(mod)
    return mod


R = load("render_reader")
H = R.H

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


def keys_named(obj, name):
    if isinstance(obj, dict):
        return any(k == name or keys_named(v, name) for k, v in obj.items())
    if isinstance(obj, list):
        return any(keys_named(v, name) for v in obj)
    return False


# ---- render twice, through the CLI, as a user would -------------------------
tmp = tempfile.mkdtemp(prefix="reader-test-")
blobs = []
for n in (1, 2):
    out = os.path.join(tmp, f"r{n}", "reader.html")
    r = subprocess.run([sys.executable, os.path.join(PIPE, "render_reader.py"), "--out", out],
                       capture_output=True, text=True, encoding="utf-8")
    check(f"render {n} exits 0", r.returncode == 0, r.stderr[-400:])
    with open(out, "rb") as f:
        blobs.append(f.read())
check("deterministic: the same bytes twice", blobs[0] == blobs[1],
      [hashlib.sha256(b).hexdigest()[:12] for b in blobs])
in_proc, payload, stats = R.build_page()
check("... and the same bytes in-process", in_proc == blobs[0])
page = blobs[0].decode("utf-8")
check("the default output is gitignored (build/)",
      "build/" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read().split())

# ---- self-contained -----------------------------------------------------------
check("no external script, stylesheet, image or frame",
      not re.search(r"<(?:script|img|iframe|link|source|video|audio)\b[^>]*\b(?:src|href)=", page, re.I))
check("no @import, url(), @font-face", not re.search(r"@import|url\(|@font-face", page, re.I))
check("no fetch / XHR / WebSocket in the script",
      not re.search(r"\bfetch\(|XMLHttpRequest|WebSocket|EventSource", page))
check("a viewport meta, for the phone", 'name="viewport"' in page)
check("light and dark themes are both defined",
      "prefers-color-scheme:dark" in page and ':root[data-theme="dark"]' in page)

# ---- every token has a popover ----------------------------------------------
data = {k: R.load_dataset(k) for k in ("hymns", "nt")}
all_tokens = [t for k in data for t in data[k]["tokens"]]
buttons = [html.unescape(a) for a in re.findall(r'<button type="button" class="tok[^"]*" data-a="([^"]+)"', page)]
m = re.search(r'<script type="application/json" id="tok-data">(.*?)</script>', page, re.S)
embedded = json.loads(m.group(1).replace("<\\/", "</")) if m else {}
addrs = {t["address"] for t in all_tokens}
check("every token is on the page as a button", set(buttons) == addrs,
      f"{len(addrs - set(buttons))} missing, {len(set(buttons) - addrs)} extra")
check("... exactly once", len(buttons) == len(set(buttons)) == len(all_tokens), len(buttons))
check("every button has a popover payload", all(a in embedded for a in buttons),
      [a for a in buttons if a not in embedded][:3])
check("no orphan payloads", set(embedded) == set(buttons))
need = ("surface", "lemma", "parsing", "translit")
check("every payload carries surface, lemma, parsing, translit",
      all(all(k in p for k in need) for p in embedded.values()))
check("every payload's surface is its token's surface",
      all(embedded[t["address"]]["surface"] == t["surface"] for t in all_tokens))
grc = [p for p in embedded.values() if p["lang"] == "grc"]
check("every Greek payload has translit, lemma and parsing in words",
      grc and all(p["translit"] and p["lemma"] and p.get("parsing_words") for p in grc), len(grc))
check("the embedded payload is the in-process one", embedded == payload)

# ---- plain and wooden are stored nowhere -------------------------------------
for k in data:
    recs = [r for f in R.FILES for r in data[k][f]]
    bad = [r.get("address") or r.get("uid") for r in recs
           if keys_named(r, "plain") or keys_named(r, "wooden")]
    check(f"data/{k}: no record stores a `plain` or `wooden` key", not bad, bad[:3])
    check(f"data/{k}/manifest.json: no `plain` or `wooden` key",
          not (keys_named(data[k]["manifest"], "plain") or keys_named(data[k]["manifest"], "wooden")))
check("the page's payload stores no `plain` or `wooden` key",
      not (keys_named(embedded, "plain") or keys_named(embedded, "wooden")))
check("no witness carries plain or wooden TEXT",
      all(w.get("text") is None for k in data for w in data[k]["witnesses"]
          if w["name"] in ("en.plain", "en.wooden")))

# ---- the columns -------------------------------------------------------------
wit, toks = R.index(data["hymns"])
clauses = [p for p in data["hymns"]["passages"] if p["unit"] == "clause"]
missing = [c["citation"] for c in clauses
           if html.escape(H.render_plain(toks[c["uid"] + "/la.1"], wit[c["uid"] + "/en.plain"]))
           not in page]
check("every hymn clause shows its render_plain() line", not missing, missing[:3])
check("every hymn clause has wooden, plain and elegant columns",
      page.count('class="col col-wooden') - len(data["nt"]["passages"]) == len(clauses))
nt_empty = len(re.findall(r'class="col col-(?:wooden|plain) empty"><span class="cl">\w+</span>'
                          r'<span class="cv">empty: no gloss yet', page))
check("the Greek's wooden and plain are shown empty, per verse", nt_empty == 2 * len(data["nt"]["passages"]))
check("... and the page says why", "Why the columns are empty" in page)
check("the Greek has no gloss to render (if this fails, the columns should fill)",
      not any(t.get("gloss") for t in data["nt"]["tokens"]))
sing = [w for w in data["hymns"]["witnesses"] if w["name"] == "en.singable"]
check("every singable stanza is on the page",
      all(html.escape(w["text"]).replace("\n", "<br>") in page for w in sing), len(sing))

rights = page[page.index('id="rights"'):]
for k in data:
    for key in {w["source"] for w in data[k]["witnesses"]} | {
            v.get("source") for t in data[k]["tokens"] for v in (t.get("provenance") or {}).values()} - {None}:
        s = data[k]["manifest"]["sources"].get(key)
        if s is None:
            continue
        ok = f"<h4>{html.escape(key)} " in rights and html.escape(s["license"]) in rights
        check(f"rights: {k}/{key} is listed with its licence ({s['license']})", ok)
check("the Robinson-Pierpont attribution travels with the text",
      html.escape(data["nt"]["manifest"]["sources"]["rp2018-byztxt"]["attribution"]) in rights)
check("Whitaker's attribution travels with the lemmas",
      html.escape(data["hymns"]["manifest"]["sources"]["whitaker-words"]["attribution"]) in rights)

# ---- agreement marks ----------------------------------------------------------
st1 = [p for p in data["hymns"]["passages"] if p["citation"] == "hymns:adoro-te.st1"][0]
marks, _ = R.agreement_groups([toks[u + "/la.1"] for u in st1["clauses"]])
by_surface = {}
for u in st1["clauses"]:
    for t in toks[u + "/la.1"]:
        by_surface.setdefault(t["surface"], marks.get(t["address"]))   # first totum: c3's
check("Adoro st1: meum, totum and contemplans are tied to cor (the Column Question's case)",
      by_surface.get("cor") and all(by_surface.get(w) == by_surface["cor"]
                                    for w in ("meum", "totum", "contemplans")), by_surface)
check("... and te, the object, is not", not by_surface.get("te"))
check("'complementary with quit' is government, not agreement: no mark",
      not R.LINK_RE.search("complementary with quit"))
check("a note naming an absent word draws nothing",
      R.agreement_groups([[{"address": "a", "syntax": "modifies nothing", "search_key": "x"}]])[0] == {})
nt_html = page[page.index('id="john-1"'):page.index('id="marks"')]
check("no agreement mark reaches the Greek", "ag-i" not in nt_html and " ag g" not in nt_html)
check("the marks toggle offers both candidate forms",
      'data-marks="sup"' in page and 'data-marks="colour"' in page)
check("every drawn group has at least two members",
      all(list(marks.values()).count(g) >= 2 for g in set(marks.values())))
check("the two forms are written down for Adam",
      os.path.exists(os.path.join(REPO, "docs", "reader-agreement-marks.md")))

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
