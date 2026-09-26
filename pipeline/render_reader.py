#!/usr/bin/env python3
"""
render_reader.py -- the reverse-interlinear reader (launch plan D5), as ONE
self-contained static HTML file: inline CSS and JS, no network, no web fonts.

    python3 pipeline/render_reader.py              # -> build/reader/reader.html
    python3 pipeline/render_reader.py --out PATH   # somewhere else

    Test: tests/reader_test.py.  Mark-form choice: docs/reader-agreement-marks.md

WHAT IT SHOWS
    Three datasets through one renderer: Adoro te and Pange lingua
    (data/hymns/, Latin, one row per clause) and John 1:1-18 (data/nt/,
    Greek, one row per verse). Per passage: the original, every word a button
    whose popover carries lemma, parsing and translit; then the four columns,
    wooden / plain / elegant / singable, as far as the data carries them. A
    column the data cannot fill is shown EMPTY with its reason. Nothing is
    faked: the Greek's glosses are Strong's DICTIONARY glosses (README-nt-jsonl
    s.12) except where an override row replaces one, a word with no gloss
    shows as a gap, and its plain line is rendered only where a prose_order
    exists. A column built on a DRAFT layer (a house gloss or prose_order
    awaiting Adam's review) carries a visible badge saying so. Beside the Greek, the KJV verse under the same uid is a
    separate, labelled witness column (data/books/kjv.witnesses.json, a
    gitignored build: absent, the column says so).

NOTHING IS STORED, NOTHING IS NEW
    `wooden` and `plain` are rendered here by the corpus's own renderers,
    build_hymn_corpus.render_wooden() and render_plain(), exactly as the
    validator renders them. Greek parsing words come from
    build_nt_corpus.describe_parsing(). The agreement marks are a RENDERING
    RULE over the house draft's `syntax` notes ("modifies cor", "agrees with
    cor", "antecedent Deitas"): the Column Question (2026-09-15, s.4) says the
    information is already in the parse table, and it is. Nothing is written
    back to data/.

DETERMINISTIC
    Same inputs, same bytes: no clock, no randomness, sorted keys. The footer
    carries the sha256 of every data file the page was built from.
"""

import argparse
import hashlib
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import build_hymn_corpus as H  # noqa: E402
import build_nt_corpus as N  # noqa: E402

OUT = os.path.join(ROOT, "build", "reader", "reader.html")
FILES = ("passages", "witnesses", "tokens", "alignments")
COLUMNS = ("wooden", "plain", "elegant", "singable")
KJV_BUILD = ("data", "books", "kjv.witnesses.json")   # gitignored; build_witnesses.py
GAP = "\u2014"   # a Greek word with no gloss, in the wooden line
DRAFT_BADGE = "draft \u2014 awaiting Adam\u2019s review"   # on a column built on a draft layer

# The works, in reading order. `data` is the folder under data/.
WORKS = (
    {"id": "adoro-te", "data": "hymns", "work": "hymns:adoro-te", "lang": "la"},
    {"id": "pange-lingua", "data": "hymns", "work": "hymns:pange-lingua", "lang": "la"},
    {"id": "john-1", "data": "nt", "work": "John.1.1-18", "lang": "grc"},
)

# What each column is for (the Column Question, s.2: the three-word test).
COLUMN_JOB = {
    "wooden": "trains the ear: the glosses in the original's order",
    "plain": "checks the understanding: the same glosses in English order",
    "elegant": "feeds the memory: quotable, accurate prose",
    "singable": "feeds the voice: metrical, fits the tune",
}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_dataset(name, root=ROOT):
    d = os.path.join(root, "data", name)
    out = {}
    for f in FILES:
        with open(os.path.join(d, f + ".jsonl"), encoding="utf-8") as fh:
            out[f] = [json.loads(line) for line in fh if line.strip()]
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as fh:
        out["manifest"] = json.load(fh)
    return out


def load_kjv(uids, root=ROOT):
    """({uid: {witness: text}} for `uids`, sha256) from the KJV witness build,
    or (None, None) when that gitignored build is absent."""
    path = os.path.join(root, *KJV_BUILD)
    if not os.path.exists(path):
        return None, None
    with open(path, "rb") as fh:
        blob = fh.read()
    doc = json.loads(blob.decode("utf-8"))
    want = set(uids)
    out = {u["uid"]: {w: v.get("text") for w, v in u["witnesses"].items()}
           for u in doc["units"] if u["uid"] in want}
    return out, hashlib.sha256(blob).hexdigest()


def index(ds):
    wit = {w["address"]: w for w in ds["witnesses"]}
    toks = {}
    for t in ds["tokens"]:
        toks.setdefault(t["passage_uid"] + "/" + t["witness"], []).append(t)
    for v in toks.values():
        v.sort(key=lambda t: t["position"])
    return wit, toks


# ---------------------------------------------------------------------------
# Agreement marks: a rendering rule over the draft's syntax notes
# ---------------------------------------------------------------------------

# The phrases in `syntax` that say "this word goes with that one". Deliberately
# narrow: `complementary with quit` (an infinitive) is government, not
# agreement, so a bare "with" counts only at the head of the note or after
# "ablative absolute".
LINK_RE = re.compile(r"(?:\bmodifies|\bagrees with|\brefers to|\bantecedent"
                     r"|\bablative absolute with|^with)\s+([^\W\d_]+)")


def agreement_groups(clauses):
    """`clauses` is a stanza's clauses in order, each a list of tokens.
    Returns ({address: group index}, stats). A link resolves to the one token
    in the same clause whose search_key matches the named word (or the word
    with enclitic -que); failing that,
    the one such token elsewhere in the stanza (contemplans, in Adoro st1 c4,
    agrees with cor in c3). Two candidates, or none, and no mark is drawn:
    a missing mark is honest, a wrong one is the lie the marks exist to stop."""
    parent = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            a = parent[a]
        return a

    stats = {"links": 0, "drawn": 0, "cross_clause": 0, "unresolved": 0}
    flat = [(ci, t) for ci, toks in enumerate(clauses) for t in toks]
    for ci, t in flat:
        for m in LINK_RE.finditer(t.get("syntax") or ""):
            stats["links"] += 1
            keys = {H.search_key(m.group(1)), H.search_key(m.group(1)) + "que"}  # Sanguinisque
            same = [u for cj, u in flat if cj == ci and u is not t and u["search_key"] in keys]
            wide = [u for cj, u in flat if u is not t and u["search_key"] in keys]
            hit = same if len(same) == 1 else (wide if not same and len(wide) == 1 else [])
            if not hit:
                stats["unresolved"] += 1
                continue
            stats["drawn"] += 1
            stats["cross_clause"] += hit[0] not in clauses[ci]
            parent[find(t["address"])] = find(hit[0]["address"])
    order = [t["address"] for _, t in flat if t["address"] in parent]
    roots, marks = {}, {}
    for a in order:
        r = find(a)
        roots.setdefault(r, len(roots) + 1)
        marks[a] = roots[r]
    return marks, stats


# ---------------------------------------------------------------------------
# HTML pieces
# ---------------------------------------------------------------------------

def e(s):
    return html.escape(str(s), quote=True)


def mark_html(marks, address):
    g = marks.get(address)
    if not g:
        return "", ""
    return f' ag g{(g - 1) % 6 + 1}', f'<sup class="ag-i" aria-label="agreement group {g}">{g}</sup>'


def original_html(witness, tokens, punct, marks):
    """The witness text with each word a button. Punctuation stays outside the
    button, exactly where the text has it; a word the tokens don't account for
    is a hard stop, never a silent skip."""
    queue = list(tokens)
    lines = []
    for line in witness["text"].split("\n"):
        parts = []
        for chunk in line.split():
            core = chunk.strip(punct)
            if not core:
                parts.append(e(chunk))
                continue
            t = queue.pop(0)
            if core != t["surface"]:
                raise SystemExit(f"{witness['address']}: text word {core!r} != token {t['surface']!r}")
            i = chunk.index(core)
            cls, sup = mark_html(marks, t["address"])
            parts.append(f'{e(chunk[:i])}<button type="button" class="tok{cls}" '
                         f'data-a="{e(t["address"])}">{e(core)}{sup}</button>{e(chunk[i + len(core):])}')
        lines.append(" ".join(parts))
    if queue:
        raise SystemExit(f"{witness['address']}: {len(queue)} tokens not in the text")
    return "<br>".join(lines)


def column_html(name, body, source=None, empty=None, note=None, badge=None):
    if empty:
        return (f'<div class="col col-{name} empty"><span class="cl">{name}</span>'
                f'<span class="cv">empty: {e(empty)}</span></div>')
    src = f' <span class="src">{e(source)}</span>' if source else ""
    nt = f' <span class="note">{e(note)}</span>' if note else ""
    bd = f' <span class="draft-badge">{e(badge)}</span>' if badge else ""
    return (f'<div class="col col-{name}{" draft" if badge else ""}"><span class="cl">{name}{src}{bd}</span>'
            f'<span class="cv">{body}{nt}</span></div>')


def wooden_html(tokens, marks, gaps=()):
    """render_wooden(), one token at a time, so each gloss can carry its mark;
    the joined text is asserted equal to render_wooden() on the whole clause.
    `gaps` are the addresses standing in for a word with no gloss."""
    parts = []
    for t in tokens:
        cls, sup = mark_html(marks, t["address"])
        if t["address"] in gaps:
            cls += " gap"
        parts.append(f'<span class="w{cls}">{e(H.render_wooden([t]))}{sup}</span>')
    if " ".join(H.render_wooden([t]) for t in tokens) != H.render_wooden(tokens):
        raise SystemExit("wooden: per-token render disagrees with render_wooden()")
    return " ".join(parts)


def payload(t, lang):
    """The popover. Every field the token has that a student would ask about,
    plus where the lemma and parsing came from."""
    prov = t.get("provenance") or {}
    pg = prov.get("gloss") or {}
    p = {
        "surface": t["surface"],
        "lemma": t.get("lemma"),
        "lemma_key": t.get("lemma_key"),
        "parsing": t.get("parsing"),
        "translit": t.get("translit"),
        "gloss": t.get("gloss"),
        "syntax": t.get("syntax"),
        "lemma_source": (prov.get("lemma") or {}).get("source"),
        "parsing_source": (prov.get("parsing") or {}).get("source"),
        "gloss_source": pg.get("source"),
        "gloss_rule": pg.get("rule"),
        "gloss_draft": bool(pg.get("draft")),
        "gloss_was": (pg.get("was") or {}).get("value"),
        "review": t.get("review"),
        "lang": lang,
    }
    if lang == "grc" and t.get("parsing"):
        p["parsing_words"] = N.describe_parsing(t["parsing"])
    return p


def source_label(manifest, key):
    s = manifest["sources"].get(key, {})
    return f'{key} ({s.get("license", "?")})'


# ---------------------------------------------------------------------------
# The two dataset shapes
# ---------------------------------------------------------------------------

def render_hymn(work, ds, tok_payload, used, stats):
    wit, toks = index(ds)
    man = ds["manifest"]
    passages = [p for p in ds["passages"] if p["work"] == work["work"]]
    by_uid = {p["uid"]: p for p in passages}
    stanzas = sorted((p for p in passages if p["unit"] == "stanza"), key=lambda p: p["stanza"])
    out = []
    for st in stanzas:
        clauses = [by_uid[u] for u in st["clauses"]]
        ctoks = [toks[c["uid"] + "/la.1"] for c in clauses]
        marks, s = agreement_groups(ctoks)
        for k, v in s.items():
            stats[k] = stats.get(k, 0) + v
        rows = []
        for c, tk in zip(clauses, ctoks):
            la = wit[c["uid"] + "/la.1"]
            used.add(la["source"])
            for t in tk:
                tok_payload[t["address"]] = payload(t, "la")
                used.update(v["source"] for v in (t.get("provenance") or {}).values()
                            if (v or {}).get("source") in man["sources"])
            cols = []
            ww = wit.get(c["uid"] + "/en.wooden")
            if ww and all(t.get("gloss") for t in tk):
                used.add(ww["source"])
                cols.append(column_html("wooden", wooden_html(tk, marks), source_label(man, ww["source"])))
            else:
                cols.append(column_html("wooden", "", empty="no token glosses"))
            pw = wit.get(c["uid"] + "/en.plain")
            if pw:
                used.add(pw["source"])
                plain = H.render_plain(tk, pw)
                same = "same words as the wooden line" if plain == H.render_wooden(tk) else None
                cols.append(column_html("plain", e(plain), source_label(man, pw["source"]), note=same))
            else:
                cols.append(column_html("plain", "", empty="no prose order stored"))
            ew = wit.get(c["uid"] + "/en.elegant")
            if ew:
                used.add(ew["source"])
                cols.append(column_html("elegant", e(ew["text"]).replace("\n", "<br>"),
                                        source_label(man, ew["source"])))
            else:
                cols.append(column_html("elegant", "", empty="not drafted for this clause"))
            cut = (c.get("cut") or {}).get("why")
            rows.append(
                f'<div class="clause" id="{e(c["uid"])}">'
                f'<div class="cite">{e(c["citation"])} <span class="uid">{e(c["uid"])}</span>'
                f' <span class="ln">ll. {c["lines"][0]}&ndash;{c["lines"][1]}</span></div>'
                f'<p class="orig" lang="la">{original_html(la, tk, H.PUNCT, marks)}</p>'
                + (f'<p class="why">joined: {e(cut)}</p>' if cut else "")
                + f'<div class="cols">{"".join(cols)}</div></div>')
        stanza_cols = []
        sw = wit.get(st["uid"] + "/en.singable")
        if sw:
            used.add(sw["source"])
            stanza_cols.append(column_html("singable", e(sw["text"]).replace("\n", "<br>"),
                                           source_label(man, sw["source"])))
        else:
            stanza_cols.append(column_html("singable", "", empty="no singable version for this stanza"))
        lw = wit.get(st["uid"] + "/en.literal")
        if lw:
            used.add(lw["source"])
            stanza_cols.append(column_html("literal", e(lw["text"]).replace("\n", "<br>"),
                                           source_label(man, lw["source"]),
                                           note="stanza prose; the PD candidate for elegant"))
        out.append(
            f'<section class="stanza" id="{e(st["uid"])}"><h3>Stanza {st["stanza"]}'
            f' <span class="uid">{e(st["citation"])} &middot; {e(st["uid"])}</span></h3>'
            + "".join(rows)
            + f'<div class="stanza-cols">{"".join(stanza_cols)}</div></section>')
    title = man["works"][work["work"]]["title"]
    return title, "".join(out)


def render_nt(work, ds, tok_payload, used, stats, kjv=None):
    wit, toks = index(ds)
    man = ds["manifest"]
    verses = sorted(ds["passages"], key=lambda p: (p["chapter"], p["verse"]))
    gl = man.get("gloss") or {}
    fw = man.get("facing_witness") or {}
    n_gloss = sum(1 for t in ds["tokens"] if t.get("gloss"))
    n_dict = sum(1 for t in ds["tokens"]
                 if (t.get("provenance") or {}).get("gloss", {}).get("kind") == "dictionary")
    n_draft = sum(1 for t in ds["tokens"] if (t.get("provenance") or {}).get("gloss", {}).get("draft"))
    plains = [w for w in ds["witnesses"] if w["name"] == N.PLAIN]
    n_plain_draft = sum(1 for w in plains if w.get("draft"))
    out = []
    for v in verses:
        gw = wit[v["uid"] + "/grc.byz"]
        used.add(gw["source"])
        tk = toks[v["uid"] + "/grc.byz"]
        for t in tk:
            tok_payload[t["address"]] = payload(t, "grc")
            used.update(v["source"] for v in (t.get("provenance") or {}).values()
                        if (v or {}).get("source") in man["sources"])
        cols = []
        # wooden: the glosses in Greek order, through the hymns' render_wooden().
        gaps = {t["address"] for t in tk if not t.get("gloss")}
        if len(gaps) < len(tk):
            shown = [dict(t, gloss=GAP) if t["address"] in gaps else t for t in tk]
            srcs = sorted({(t.get("provenance") or {}).get("gloss", {}).get("source")
                           for t in tk if t.get("gloss")} - {None})
            drafted = sum(1 for t in tk if (t.get("provenance") or {}).get("gloss", {}).get("draft"))
            note = "dictionary glosses, not a translation"
            if drafted:
                note = (f"dictionary glosses, not a translation, except {drafted} contextual "
                        f"house gloss{'es' if drafted > 1 else ''} (draft)")
            if gaps:
                note += f"; {len(gaps)} word{'s' if len(gaps) > 1 else ''} with no gloss shown as {GAP}"
            cols.append(column_html("wooden", wooden_html(shown, {}, gaps),
                                    ", ".join(source_label(man, k) for k in srcs), note=note,
                                    badge=DRAFT_BADGE if drafted else None))
        else:
            cols.append(column_html("wooden", "", empty="no gloss yet"))
        # plain: needs prose_order, which only an en.plain witness carries.
        pw = wit.get(v["uid"] + "/en.plain")
        if pw and pw.get("prose_order") and not gaps:
            used.add(pw["source"])
            cols.append(column_html("plain", e(N.render_plain(tk, pw)), source_label(man, pw["source"]),
                                    badge=DRAFT_BADGE if pw.get("draft") else None))
        else:
            cols.append(column_html("plain", "", empty="not yet ordered (no prose_order for the Greek)"))
        cols.append(column_html("elegant", "", empty="none stored"))
        cols.append(column_html("singable", "", empty="prose"))
        # The KJV: a second witness of the verse, not a column generated from the Greek.
        text = (kjv or {}).get(v["uid"], {}).get(fw.get("name", "kjv.plain")) if kjv is not None else None
        label = f'{fw.get("name", "kjv.plain")} ({fw.get("license", "?")})'
        if text:
            used.add("facing:kjv")
            cols.append(column_html("kjv", e(text), label, note="a separate witness: the KJV "
                                    "translates the Textus Receptus, not this Greek"))
        elif kjv is None:
            cols.append(column_html("kjv", "", empty="the KJV witness build is not on this machine "
                                    "(data/books/kjv.witnesses.json is gitignored; build_witnesses.py)"))
        else:
            cols.append(column_html("kjv", "", empty="no KJV text under this uid"))
        out.append(
            f'<div class="clause verse" id="{e(v["uid"])}">'
            f'<div class="cite">{e(v["citation"])} <span class="uid">{e(v["uid"])}</span></div>'
            f'<p class="orig" lang="grc">{original_html(gw, tk, N.PUNCT, {})}</p>'
            f'<div class="cols">{"".join(cols)}</div></div>')
    by_rule = gl.get("by_rule") or {}
    rules = ", ".join(f"{k} {n}" for k, n in by_rule.items())
    why_none = "; ".join(f"{n}: {r}" for r, n in (gl.get("none_by_reason") or {}).items())
    kjv_li = (
        f'<li><b>KJV</b> is not one of the four columns. It is the same verse in another witness '
        f'(<code>{e(fw.get("name", "kjv.plain"))}</code>, same uid), shown for comparison. The KJV '
        f'translates the Textus Receptus, not the Robinson&ndash;Pierpont text above it, so it '
        f'cannot stand in for <b>elegant</b>. Public domain in the US; in the UK it is under the '
        f'Crown patent (&ldquo;{e(fw.get("rights_note", ""))}&rdquo;): see Sources &amp; rights.</li>'
        if kjv is not None else
        f'<li><b>KJV</b>: the verse&#39;s KJV witness lives in a gitignored build '
        f'(<code>data/books/kjv.witnesses.json</code>) that is not on this machine, so that column '
        f'is empty here.</li>')
    why = (
        f'<div class="why-empty"><h3>About the Greek columns</h3><ul>'
        f'<li><b>wooden</b> is generated from token glosses and is never stored. {n_gloss} of '
        f'{len(ds["tokens"])} Greek tokens carry a gloss. {n_dict} are <b>dictionary glosses</b> '
        f'from Strong&#39;s 1890 entry for each word&#39;s Strong&#39;s number, chosen by a fixed rule '
        f'({e(rules)}). Those are <b>not a contextual translation</b>: a word gets the same gloss in '
        f'every verse (an article or pronoun varies only with its person, number, gender and case). '
        + (f'{len(ds["tokens"]) - n_gloss} have none and show as {GAP} ({e(why_none)}). '
           if n_gloss < len(ds["tokens"]) else "")
        + f'A reviewed or house layer (<code>data/nt/gloss-overrides.jsonl</code>, '
        f'{(gl.get("overrides") or {}).get("applied", 0)} rows applied) replaces them word by '
        f'word with a contextual gloss, the dictionary one kept'
        + (f'; {n_draft} of those rows are <b>house drafts awaiting Adam&#39;s review</b>, and a '
           f'wooden column that uses one is badged' if n_draft else "")
        + '.</li>'
        + (f'<li><b>plain</b> walks a <code>prose_order</code>, the order of the glosses in English '
           f'(the hymns&#39; convention). {len(plains)} of {len(verses)} verses have one'
           + (f'; {n_plain_draft} are <b>house drafts awaiting Adam&#39;s review</b> and are badged'
              if n_plain_draft else "")
           + '. A verse without one is shown as not yet ordered rather than guessed.</li>'
           if plains else
           f'<li><b>plain</b> needs a <code>prose_order</code>, the order of the glosses in English. '
           f'The Greek has none yet, so plain is shown as not yet ordered rather than guessed.</li>')
        + f'<li><b>elegant</b>: no house or public-domain prose rendering is stored.</li>'
        f'{kjv_li}'
        f'<li><b>singable</b>: this is prose.</li>'
        f'<li>No agreement marks: they are drawn from the draft&#39;s syntax notes, and the Greek '
        f'has none yet.</li></ul></div>')
    return man["selection"]["title"] + " (John 1:1&ndash;18)", why + "".join(out)


# ---------------------------------------------------------------------------
# Sources and rights
# ---------------------------------------------------------------------------

def facing_rights_html(fw):
    """The KJV column's rights, from the NT manifest's facing_witness block."""
    basis = "; ".join(f'{b["where"]}: {b["says"]}' for b in fw.get("license_basis") or [])
    fields = [("what", fw.get("what")), ("licence", fw.get("license")), ("basis", basis),
              ("rights note", fw.get("rights_note")), ("scope", fw.get("scope")),
              ("translates", fw.get("translates")), ("file", fw.get("file"))]
    dl = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in fields if b)
    return (f'<div class="source"><h4>{e(fw["name"])} <span class="lic lic-{e(fw.get("license"))}">'
            f'{e(fw.get("license"))}</span></h4><dl>{dl}</dl></div>')


def rights_html(manifest, keys):
    rows = []
    for k in sorted(k for k in keys if k in manifest["sources"]):
        s = manifest["sources"][k]
        basis = s.get("license_basis")
        if isinstance(basis, list):
            basis = "; ".join(f'{b["where"]}: {b["says"]}' for b in basis)
        fields = [("what", s.get("what")), ("edition", s.get("edition")),
                  ("licence", s.get("license")), ("basis", basis),
                  ("attribution", s.get("attribution")), ("source", s.get("source_url")),
                  ("verified", ("yes" + (f', {s["verified_on"]}' if s.get("verified_on") else ""))
                   if s.get("verified") else "no"),
                  ("open", s.get("open"))]
        dl = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in fields if b)
        rows.append(f'<div class="source"><h4>{e(k)} <span class="lic lic-{e(s.get("license"))}">'
                    f'{e(s.get("license"))}</span></h4><dl>{dl}</dl></div>')
    return "".join(rows)


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------

CSS = """
:root{--bg:#fbf8f2;--fg:#1f1b16;--muted:#6b6257;--card:#fffdf8;--line:#e3dccf;--accent:#7a2e1f;
--chip:#f1ebdf;--empty:#9a8f80;--pop:#fffdf8;--shadow:0 6px 24px rgba(0,0,0,.18);
--g1:#b3261e;--g2:#1f5fa8;--g3:#1d7a3a;--g4:#8a4bb0;--g5:#b35c00;--g6:#007a7a;
--draft-bg:#f6d9a8;--draft-fg:#5a3a00}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15130f;--fg:#ece5d8;--muted:#a79d8e;
--card:#1e1b16;--line:#3a342b;--accent:#e39a7f;--chip:#2a251e;--empty:#877d6f;--pop:#221e18;
--shadow:0 6px 24px rgba(0,0,0,.6);--g1:#ff8a80;--g2:#82b1ff;--g3:#7fd99a;--g4:#d5a6f5;--g5:#ffb866;--g6:#5fe0e0;
--draft-bg:#6b4a12;--draft-fg:#ffe2b0}}
:root[data-theme="dark"]{--bg:#15130f;--fg:#ece5d8;--muted:#a79d8e;--card:#1e1b16;--line:#3a342b;
--accent:#e39a7f;--chip:#2a251e;--empty:#877d6f;--pop:#221e18;--shadow:0 6px 24px rgba(0,0,0,.6);
--g1:#ff8a80;--g2:#82b1ff;--g3:#7fd99a;--g4:#d5a6f5;--g5:#ffb866;--g6:#5fe0e0;
--draft-bg:#6b4a12;--draft-fg:#ffe2b0}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,"Times New Roman",serif}
main,header,footer{max-width:60rem;margin:0 auto;padding:0 16px}
header{padding-top:20px}
h1{font-size:1.6rem;margin:.2em 0}
h2{font-size:1.3rem;margin:1.6em 0 .4em;color:var(--accent)}
h3{font-size:1.05rem;margin:1.2em 0 .5em}
.lede{color:var(--muted);margin:.3em 0 1em}
.controls{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;padding:8px max(16px,calc((100% - 60rem)/2 + 16px));
border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--bg);z-index:5}
.controls fieldset{border:0;margin:0;padding:0;display:flex;gap:4px;align-items:center;flex-wrap:wrap}
.controls legend{float:left;font-size:.8rem;color:var(--muted);margin-right:4px}
.seg{font:inherit;font-size:.85rem;padding:4px 10px;border:1px solid var(--line);background:var(--card);
color:var(--fg);border-radius:14px;cursor:pointer}
.seg[aria-pressed="true"]{background:var(--accent);color:var(--bg);border-color:var(--accent)}
nav.toc{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
nav.toc a{color:var(--accent);background:var(--chip);padding:3px 10px;border-radius:12px;text-decoration:none;font-size:.9rem}
.stanza{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:4px 12px 12px;margin:14px 0}
.clause{border-top:1px dashed var(--line);padding:10px 0}
.stanza h3+.clause{border-top:0}
.verse{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:10px 0}
.cite{font-size:.78rem;color:var(--muted);font-family:ui-monospace,Consolas,monospace;overflow-wrap:anywhere}
.uid{opacity:.75}
.stanza h3 .uid{font:400 .72rem ui-monospace,Consolas,monospace;color:var(--muted);overflow-wrap:anywhere}
.orig{font-size:1.25rem;line-height:1.9;margin:.3em 0}
.orig[lang="grc"]{font-family:"Gentium Plus","SBL Greek","Palatino Linotype",Palatino,"Times New Roman",serif}
.tok{font:inherit;color:inherit;background:none;border:0;padding:0 1px;margin:0;cursor:pointer;
border-bottom:1px dotted var(--muted);border-radius:2px}
.tok:hover,.tok:focus-visible,.tok.on{background:var(--chip);outline:none}
.why{font-size:.8rem;color:var(--muted);margin:.2em 0 .5em;font-style:italic}
.cols,.stanza-cols{display:grid;grid-template-columns:1fr;gap:6px}
.stanza-cols{margin-top:10px;border-top:1px solid var(--line);padding-top:10px}
.col{display:grid;grid-template-columns:5.2rem 1fr;gap:8px;align-items:baseline}
.cl{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);overflow-wrap:anywhere}
.cl .src{display:block;text-transform:none;letter-spacing:0;font-size:.68rem;opacity:.85}
.cv{min-width:0;overflow-wrap:anywhere}
.col.empty .cv{color:var(--empty);font-style:italic;font-size:.9rem}
.w.gap{color:var(--empty)}
.col-kjv{border-top:1px dotted var(--line);padding-top:6px}
.draft-badge{display:inline-block;margin-left:4px;text-transform:none;letter-spacing:0;font-size:.68rem;
font-family:ui-sans-serif,system-ui,sans-serif;padding:0 6px;border-radius:8px;background:var(--draft-bg);color:var(--draft-fg)}
.col.draft .cv{border-left:3px solid var(--draft-bg);padding-left:6px}
.note{display:block;font-size:.75rem;color:var(--muted);font-style:italic}
.col-singable .cv,.col-literal .cv{font-size:.95rem}
.why-empty{background:var(--chip);border-radius:10px;padding:4px 14px;font-size:.92rem}
.why-empty ul{padding-left:1.1em}
sup.ag-i{font-size:.62em;line-height:0;margin-left:1px;color:var(--accent);font-family:ui-sans-serif,system-ui,sans-serif;font-weight:600}
body[data-marks="colour"] sup.ag-i,body[data-marks="off"] sup.ag-i{display:none}
body[data-marks="colour"] .ag{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:4px}
body[data-marks="colour"] .ag.g1{color:var(--g1);text-decoration-color:var(--g1)}
body[data-marks="colour"] .ag.g2{color:var(--g2);text-decoration-color:var(--g2)}
body[data-marks="colour"] .ag.g3{color:var(--g3);text-decoration-color:var(--g3)}
body[data-marks="colour"] .ag.g4{color:var(--g4);text-decoration-color:var(--g4)}
body[data-marks="colour"] .ag.g5{color:var(--g5);text-decoration-color:var(--g5)}
body[data-marks="colour"] .ag.g6{color:var(--g6);text-decoration-color:var(--g6)}
body[data-marks="colour"] .tok.ag{border-bottom:0}
.sources{display:grid;grid-template-columns:1fr;gap:10px}
.source{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 12px;font-size:.85rem}
.source h4{margin:.4em 0;font-family:ui-monospace,Consolas,monospace;font-size:.85rem;overflow-wrap:anywhere}
.source dl{display:grid;grid-template-columns:5.5rem 1fr;gap:2px 8px;margin:0}
.source dt{color:var(--muted)}
.source dd{margin:0;min-width:0;overflow-wrap:anywhere}
.lic{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.7rem;padding:1px 6px;border-radius:8px;background:var(--chip);color:var(--fg)}
.lic-PD{background:#2e7d32;color:#fff}.lic-own{background:#5d4037;color:#fff}.lic-free-grant{background:#b26a00;color:#fff}
footer{color:var(--muted);font-size:.78rem;padding-bottom:40px;overflow-wrap:anywhere}
code{font-family:ui-monospace,Consolas,monospace;font-size:.88em}
#pop{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);width:min(30rem,calc(100% - 24px));
background:var(--pop);color:var(--fg);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);
padding:10px 14px 12px;z-index:20;max-height:60vh;overflow:auto}
#pop[hidden]{display:none}
#pop .ps{font-size:1.35rem;margin:0 1.6rem .2em 0}
#pop dl{display:grid;grid-template-columns:5.2rem 1fr;gap:3px 8px;margin:0;font-size:.9rem}
#pop dt{color:var(--muted)}#pop dd{margin:0;min-width:0;overflow-wrap:anywhere}
#pop .x{position:absolute;top:6px;right:8px;font:inherit;font-size:1.3rem;background:none;border:0;color:var(--muted);cursor:pointer}
@media (min-width:720px){
.controls{position:sticky;top:0}
.cols{grid-template-columns:repeat(3,1fr);gap:10px}
.verse .cols{grid-template-columns:repeat(2,1fr)}
.verse .col-kjv{grid-column:1/-1}
.col{grid-template-columns:1fr;gap:2px}
.stanza-cols{grid-template-columns:1fr 1fr}
.sources{grid-template-columns:1fr 1fr}
}
"""

JS = r"""
(function(){
var T=JSON.parse(document.getElementById('tok-data').textContent);
var root=document.documentElement, body=document.body, pop=document.getElementById('pop');
function get(k){try{return localStorage.getItem(k)}catch(_){return null}}
function put(k,v){try{localStorage.setItem(k,v)}catch(_){}}
function press(group,val){document.querySelectorAll('button[data-'+group+']').forEach(function(b){
  b.setAttribute('aria-pressed',String(b.getAttribute('data-'+group)===val))})}
function theme(v){if(v==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',v);press('theme',v);put('reader.theme',v)}
function marks(v){body.setAttribute('data-marks',v);press('marks',v);put('reader.marks',v)}
theme(get('reader.theme')||'auto');marks(get('reader.marks')||'sup');
document.querySelectorAll('[data-theme]').forEach(function(b){if(b.tagName==='BUTTON')b.addEventListener('click',function(){theme(b.getAttribute('data-theme'))})});
document.querySelectorAll('[data-marks]').forEach(function(b){if(b.tagName==='BUTTON')b.addEventListener('click',function(){marks(b.getAttribute('data-marks'))})});
var on=null;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function row(k,v){return v==null||v===''?'':'<dt>'+k+'</dt><dd>'+esc(v)+'</dd>'}
function show(btn){var p=T[btn.getAttribute('data-a')];if(!p)return;
  if(on)on.classList.remove('on');on=btn;btn.classList.add('on');
  var tl=p.translit!=null?p.translit:(p.lang==='la'?'(Latin script: none needed)':null);
  pop.innerHTML='<button class="x" type="button" aria-label="Close">&times;</button>'+
   '<p class="ps" lang="'+p.lang+'">'+esc(p.surface)+'</p><dl>'+
   row('lemma',p.lemma)+row('key',p.lemma_key)+row('parsing',p.parsing)+row('in words',p.parsing_words)+
   row('translit',tl)+row('gloss',p.gloss==null?'(none yet)':p.gloss)+row('syntax',p.syntax)+
   row('lemma from',p.lemma_source)+row('parse from',p.parsing_source)+
   row('gloss from',p.gloss_source?p.gloss_source+(p.gloss_rule?' ('+p.gloss_rule+')':'')+
     (p.gloss_draft?' \u2014 draft, awaiting Adam\u2019s review':''):null)+
   row('dictionary gloss',p.gloss_was)+
   row('review',p.review==null?null:(typeof p.review==='string'?p.review:JSON.stringify(p.review)))+
   row('address',btn.getAttribute('data-a'))+'</dl>';
  pop.hidden=false;pop.querySelector('.x').addEventListener('click',hide)}
function hide(){pop.hidden=true;if(on){on.classList.remove('on');on.focus();on=null}}
document.addEventListener('click',function(ev){var b=ev.target.closest('button.tok');
  if(b){show(b);return}if(!pop.hidden&&!pop.contains(ev.target))hide()});
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&!pop.hidden)hide()});
})();
"""


def build_page(root=ROOT):
    data = {"hymns": load_dataset("hymns", root), "nt": load_dataset("nt", root)}
    kjv, kjv_sha = load_kjv([p["uid"] for p in data["nt"]["passages"]], root)
    tok_payload, sections, stats = {}, [], {}
    used = {"hymns": set(), "nt": set()}
    for w in WORKS:
        ds = data[w["data"]]
        mine = set()
        if w["data"] == "hymns":
            title, body = render_hymn(w, ds, tok_payload, mine, stats)
        else:
            title, body = render_nt(w, ds, tok_payload, mine, stats, kjv)
        used[w["data"]] |= mine
        sections.append((w, title, body, mine))

    blob = json.dumps(tok_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    blob = blob.replace("</", "<\\/")
    toc = "".join(f'<a href="#{w["id"]}">{t}</a>' for w, t, _, _ in sections)
    toc += '<a href="#rights">Sources &amp; rights</a><a href="#marks">About the marks</a>'
    def labels(man, keys):
        out = [source_label(man, k) for k in sorted(keys) if k in man["sources"]]
        if "facing:kjv" in keys:
            fw = man["facing_witness"]
            out.append(f'{fw["name"]} ({fw["license"]}; UK: Crown patent), a separate witness')
        return ", ".join(out)

    works = "".join(
        f'<section id="{w["id"]}"><h2>{t}</h2>'
        f'<p class="lede">Sources: {e(labels(data[w["data"]]["manifest"], mine))}. '
        f'Full rights are under <a href="#rights">Sources &amp; rights</a>.</p>{b}</section>'
        for w, t, b, mine in sections)
    rights = "".join(
        f'<h3>{e(label)}</h3><div class="sources">{rights_html(data[k]["manifest"], used[k])}'
        + (facing_rights_html(data[k]["manifest"]["facing_witness"]) if "facing:kjv" in used[k] else "")
        + '</div>'
        for k, label in (("hymns", "The hymns (data/hymns/manifest.json)"),
                         ("nt", "John 1:1–18 (data/nt/manifest.json)")))
    sums = "".join(f'<br><code>data/{k}/{fn}</code> {h}' for k in ("hymns", "nt")
                   for fn, h in sorted(data[k]["manifest"]["files_sha256"].items()))
    if kjv_sha:
        sums += f'<br><code>{"/".join(KJV_BUILD)}</code> {kjv_sha}'
    s = stats
    marks_note = (
        f'<p>A superscript number, or a colour, ties each word to the words it agrees with, in the '
        f'Latin and in its wooden gloss. Meter scatters words that belong together, and the wooden '
        f'line in English order-of-appearance can say the reverse of the Latin (the Column Question, '
        f'2026-09-15, s.4). The ties are drawn at render time from the draft&#39;s syntax notes '
        f'(&ldquo;modifies&rdquo;, &ldquo;agrees with&rdquo;, &ldquo;refers to&rdquo;, '
        f'&ldquo;antecedent&rdquo;), numbered per stanza. Of {s.get("links", 0)} such notes, '
        f'{s.get("drawn", 0)} are drawn ({s.get("cross_clause", 0)} of them across a clause break) and '
        f'{s.get("unresolved", 0)} are not, because the named word is not in the stanza or is there '
        f'twice. A missing tie is honest; a wrong one would not be. The form is Adam&#39;s choice: '
        f'<b>superscript</b> or <b>colour</b>. See <code>docs/reader-agreement-marks.md</code>.</p>')
    colhelp = "".join(f"<li><b>{c}</b>: {e(j)}</li>" for c, j in COLUMN_JOB.items())
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Word Hoard Reader</title>
<style>{CSS}</style>
</head>
<body data-marks="sup">
<header>
<h1>The Reader</h1>
<p class="lede">A reverse interlinear: the original first, then the columns. Tap any word for its
lemma, parsing and transliteration. Built from <code>canon-corpus</code> data/hymns and data/nt
(launch plan D5). The Hebrew dataset is not built yet.</p>
<ul class="lede">{colhelp}</ul>
</header>
<div class="controls">
<fieldset><legend>Marks</legend>
<button type="button" class="seg" data-marks="sup" aria-pressed="true">Superscript</button>
<button type="button" class="seg" data-marks="colour" aria-pressed="false">Colour</button>
<button type="button" class="seg" data-marks="off" aria-pressed="false">Off</button></fieldset>
<fieldset><legend>Theme</legend>
<button type="button" class="seg" data-theme="auto" aria-pressed="true">Auto</button>
<button type="button" class="seg" data-theme="light" aria-pressed="false">Light</button>
<button type="button" class="seg" data-theme="dark" aria-pressed="false">Dark</button></fieldset>
</div>
<main>
<nav class="toc">{toc}</nav>
{works}
<section id="marks"><h2>About the agreement marks</h2>{marks_note}</section>
<section id="rights"><h2>Sources &amp; rights</h2>
<p class="lede">Every source the page draws on, with its licence as its manifest records it.
Nothing here is under a licence the house gate does not admit (launch plan D4, ADR 0001).</p>
{rights}</section>
</main>
<footer><p>Generated by <code>pipeline/render_reader.py</code> from these files:{sums}</p>
<p><code>wooden</code> and <code>plain</code> are rendered here and stored nowhere.</p></footer>
<div id="pop" role="dialog" aria-label="Word details" hidden></div>
<script type="application/json" id="tok-data">{blob}</script>
<script>{JS}</script>
</body>
</html>
"""
    return page.encode("utf-8"), tok_payload, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    blob, toks, stats = build_page()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    H.write_atomic(a.out, blob)
    print(f"  tokens with a popover {len(toks):>5}")
    print(f"  agreement notes {stats['links']}, drawn {stats['drawn']} "
          f"({stats['cross_clause']} across clauses), unresolved {stats['unresolved']}")
    print(f"  wrote {a.out} ({len(blob):,} bytes)")


if __name__ == "__main__":
    main()
