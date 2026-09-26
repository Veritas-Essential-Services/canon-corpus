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
    - the columns: every hymn clause shows the render_plain() line; every
      Greek verse shows render_wooden() over its glosses (a marked gap for a
      word with none), its plain line through build_nt_corpus.render_plain()
      where it has a prose_order ("not yet ordered" where not), a
      "draft — awaiting Adam's review" badge on exactly the columns built on
      a draft layer (and never on the hymns), and the KJV verse of the same uid as a separate, labelled witness column
      (or says the gitignored KJV build is absent); every source a page
      section draws on has its licence in the rights section, the KJV's
      Crown patent note included;
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
hman = data["hymns"]["manifest"]
printed = {w for w, v in hman["works"].items() if v.get("source_file")}
missing = [c["citation"] for c in clauses if c["work"] not in printed
           and html.escape(H.render_plain(toks[c["uid"] + "/la.1"], wit[c["uid"] + "/en.plain"]))
           not in page]
check("every batch-hymn clause shows its render_plain() line", not missing, missing[:3])
check("the three printed hymns are on the page, each with a table-of-contents link",
      printed == {"hymns:lauda-sion", "hymns:sacris-solemniis", "hymns:verbum-supernum"}
      and all(f'<section id="{w.split(":")[1]}">' in page and f'href="#{w.split(":")[1]}"' in page
              for w in printed))
empty_bad = []
for c in (c for c in clauses if c["work"] in printed):
    block = page[page.index(f'id="{c["uid"]}"'):]
    block = block[:block.index('</div></div>', block.index('<div class="col col-elegant'))]
    why = hman["works"][c["work"]]["not_stored"]
    if not all(f'empty: {html.escape(why[n])}' in block for n in ("en.wooden", "en.plain", "en.elegant")):
        empty_bad.append(c["citation"])
check("every printed-hymn clause shows wooden, plain and elegant empty, each with the manifest's reason",
      not empty_bad, empty_bad[:3])
why_bad = [c["citation"] for c in clauses if c["work"] in printed and
           f'<p class="why">{"joined" if c["lines"][1] > c["lines"][0] else "stands alone"}: '
           f'{html.escape(c["cut"]["why"])}</p>' not in page[page.index(f'id="{c["uid"]}"'):][:4000]]
check("every printed-hymn clause shows why it was cut there (a one-line clause is not called a join)",
      not why_bad, why_bad[:3])
lit = [w for w in data["hymns"]["witnesses"] if w["name"] == "en.literal"]
check("every stanza's literal prose is on the page (Britt 1922)",
      all(html.escape(w["text"]) in page for w in lit) and len(lit) == 6 + 25, len(lit))
pst = [p for p in data["hymns"]["passages"] if p["unit"] == "stanza" and p["work"] in printed]
check("every printed stanza names its printed page",
      all(f'{html.escape(p["citation"])} &middot; {p["uid"]} &middot; printed p. {p["page"]}' in page
          for p in pst), len(pst))
hy_tok = {t["address"]: t for t in data["hymns"]["tokens"]}
nolem = [a for a, t in hy_tok.items() if t["lemma"] is None]
check("a word with no lemma carries Whitaker's candidates in its popover (when WORDS has any)",
      nolem and all(embedded[a].get("candidates") == hy_tok[a]["provenance"]["lemma"].get("whitaker")
                    for a in nolem), len(nolem))
check("... and the popover says so rather than leaving the lemma out", "(none yet: see review)" in page)
check("every hymn clause has wooden, plain and elegant columns",
      page.count('class="col col-wooden') - len(data["nt"]["passages"]) == len(clauses))
nt_html = page[page.index('id="john-1"'):page.index('id="marks"')]
nt_wit, nt_toks = R.index(data["nt"])
nt_verses = data["nt"]["passages"]
wooden_bad, gaps_seen = [], 0
for v in nt_verses:
    tk = nt_toks[v["uid"] + "/grc.byz"]
    block = nt_html[nt_html.index(f'id="{v["uid"]}"'):]
    block = block[:block.index('<div class="col col-plain')]
    shown = [dict(t, gloss=R.GAP) if not t.get("gloss") else t for t in tk]
    words = [html.unescape(w) for w in re.findall(r'<span class="w[^"]*">([^<]*)</span>', block)]
    # the wooden column is render_wooden() over the tokens, a gap for each word with no gloss
    if " ".join(words) != H.render_wooden(shown) or len(words) != len(tk):
        wooden_bad.append(v["citation"])
    gaps_seen += block.count('class="w gap"')
check("every Greek verse's wooden column is render_wooden() over its glosses, in Greek order",
      not wooden_bad, wooden_bad[:3])
n_none = sum(1 for t in data["nt"]["tokens"] if not t.get("gloss"))
check("... and each word with no gloss is a marked gap, never a made-up word", gaps_seen == n_none,
      (gaps_seen, n_none))
check("the wooden column is labelled as Strong's dictionary glosses, not a translation",
      nt_html.count("dictionary glosses, not a translation") == len(nt_verses)
      and "strongs-1890 (PD)" in nt_html)
badge = html.escape(R.DRAFT_BADGE)
plain_bad, badge_bad = [], []
for v in nt_verses:
    tk = nt_toks[v["uid"] + "/grc.byz"]
    block = nt_html[nt_html.index(f'id="{v["uid"]}"'):]
    wooden = block[block.index('<div class="col col-wooden'):block.index('<div class="col col-plain')]
    plain = block[block.index('<div class="col col-plain'):block.index('<div class="col col-elegant')]
    pw = nt_wit.get(v["uid"] + "/en.plain")
    if pw is None:
        if "empty: not yet ordered" not in plain or badge in plain:
            plain_bad.append(v["citation"])
    elif (f'<span class="cv">{html.escape(R.N.render_plain(tk, pw))}' not in plain
          or "house-draft (own)" not in plain):
        plain_bad.append(v["citation"])
    # the badge is on exactly the columns built on a draft layer
    drafted = any(t["provenance"]["gloss"].get("draft") for t in tk)
    if (badge in wooden) != drafted or (badge in plain) != bool(pw and pw.get("draft")):
        badge_bad.append(v["citation"])
    if (badge in wooden) != ('class="col col-wooden draft"' in wooden):
        badge_bad.append(v["citation"])
check("every Greek verse with a prose_order shows its render_plain() line, labelled house-draft (own); "
      "one without says 'not yet ordered'", not plain_bad, plain_bad[:3])
n_plain = sum(1 for w in data["nt"]["witnesses"] if w["name"] == "en.plain")
check("... and today all 18 verses have one", n_plain == len(nt_verses), n_plain)
check("a column built on a draft layer carries the badge 'draft — awaiting Adam’s review', "
      "and no other column does", not badge_bad, badge_bad[:3])
n_badges = nt_html.count(f'<span class="draft-badge">{badge}</span>')
check("... on the Greek: every wooden and every plain column today (36)", n_badges == 2 * len(nt_verses),
      n_badges)
check("... and never on the hymns",
      'class="draft-badge"' not in page[page.index('id="adoro-te"'):page.index('id="john-1"')])
check("the badge is visible in both themes (its colours are defined for light and dark)",
      page.count("--draft-bg:") == 3 and page.count("--draft-fg:") == 3 and ".draft-badge{" in page)
check("... and the page explains the Greek columns, drafts included", "About the Greek columns" in nt_html
      and "not a contextual translation" in nt_html and "prose_order" in nt_html
      and "house drafts awaiting Adam&#39;s review" in nt_html)
nm = data["nt"]["manifest"]
check("the explanation's counts are the manifest's",
      f'{nm["counts"]["tokens_with_gloss"]} of {nm["counts"]["tokens"]} Greek tokens carry a gloss' in nt_html
      and all(f"{k} {n}" in nt_html for k, n in nm["gloss"]["by_rule"].items()))
nt_by_addr = {t["address"]: t for t in data["nt"]["tokens"]}
check("every Greek popover names where its gloss came from: Strong's with its rule, or the override "
      "layer with the dictionary gloss it replaced and whether it is a draft",
      all((p.get("gloss_source") == "strongs-1890" and p.get("gloss_rule") and not p["gloss_draft"]
           and p["gloss_was"] is None)
          if nt_by_addr[a]["provenance"]["gloss"]["kind"] == "dictionary" else
          (p.get("gloss_source") == nt_by_addr[a]["provenance"]["gloss"]["source"]
           and p["gloss_draft"] == bool(nt_by_addr[a]["provenance"]["gloss"].get("draft"))
           and p["gloss_was"] == nt_by_addr[a]["provenance"]["gloss"]["was"]["value"])
          for a, p in embedded.items() if p["lang"] == "grc" and p.get("gloss")))
check("... and the popover prints the draft mark", "draft, awaiting Adam" in page)

# ---- the KJV column: a separate witness under the same uid ---------------------
kjv, kjv_sha = R.load_kjv([v["uid"] for v in nt_verses])
cols = re.findall(r'<div class="col col-kjv[^"]*">', nt_html)
check("every Greek verse has a KJV column", len(cols) == len(nt_verses), len(cols))
if kjv is None:
    print("skip  data/books/kjv.witnesses.json is not built here (gitignored): the KJV text checks")
    print("      did not run. structure_texts.py, then build_witnesses.py, builds it.")
    check("... shown empty, with the reason", nt_html.count("kjv.witnesses.json is gitignored") == len(nt_verses))
else:
    fw = nm["facing_witness"]
    missing_kjv = [v["citation"] for v in nt_verses
                   if not kjv.get(v["uid"], {}).get(fw["name"])
                   or html.escape(kjv[v["uid"]][fw["name"]]) not in nt_html]
    check("every verse shows its kjv.plain text, found by the verse's uid", not missing_kjv, missing_kjv[:3])
    check("... labelled as its own witness, with its licence and what it translates",
          nt_html.count(f'{fw["name"]} ({fw["license"]})') >= len(nt_verses)
          and nt_html.count("a separate witness: the KJV translates the Textus Receptus") == len(nt_verses))
    check("the KJV column is not the elegant column", all(
        "empty: none stored" in nt_html[nt_html.index(f'id="{v["uid"]}"'):][:20000].split('col-kjv')[0]
        for v in nt_verses))
    check("the Crown patent note travels with it, in the column's explanation and in the rights",
          fw["rights_note"] == "Crown patent: KJV print not for UK"
          and html.escape(fw["rights_note"]) in nt_html
          and html.escape(fw["rights_note"]) in page[page.index('id="rights"'):])
    check("the KJV build's sha256 is in the footer", kjv_sha in page[page.index("<footer>"):])
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
