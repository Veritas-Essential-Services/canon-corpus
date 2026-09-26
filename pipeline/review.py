#!/usr/bin/env python3
"""
review.py -- Adam's review sheets: rendered from the data, answered in the
"Adam:" column, applied back as override rows.

    python pipeline/review.py render [--check] [--force] [SHEET ...]
    python pipeline/review.py apply SHEET [--dry-run] [--no-build] [--today YYYY-MM-DD]
    python pipeline/review.py status [SHEET ...]

    SHEET is a sheet's path (or just its file name); none means every sheet.

THE SHEETS (SHEETS below)
    docs/review/2026-09-26-lemma-flags.md    the flagged hymn tokens (lemma spine, D3)
        rows: the tokens named in its notes file, plus any token flagged since
        answers -> data/lemmas/adam-reviewed.jsonl (README-lemma-spine.md s.8)
    docs/review/2026-09-26-thomas-lemma-flags.md   the same, for the hymns
        printed from Britt 1922 (no draft: README-lemma-spine.md s.3b)
        answers -> data/lemmas/adam-reviewed.jsonl (the same file)
    docs/review/2026-09-26-thomas-cuts.md    every clause cut of those hymns
        rows: one per stanza; answers ok / draft→ / `cut: 1, 2-3; note: why`
        answers -> data/hymn-sources/cut-reviewed.jsonl (README-hymn-jsonl.md s.9d)
    docs/review/2026-09-26-adoro-collation.md   Adoro te's received Latin
        against Britt 1922, one row per difference (build_hymn_corpus.collate)
        answers ok (received stands) / britt / draft→, `; note: …` optional
        answers -> data/hymn-sources/collation-reviewed.jsonl (README-hymn-jsonl.md s.10)
    docs/review/2026-09-26-john1-drafts.md   the John 1 house drafts
        rows: every gloss-override row, and one plain line per verse
        answers -> data/nt/gloss-overrides.jsonl, data/nt/prose-order.jsonl
                   (README-nt-jsonl.md s.12, s.14)

    What the data cannot say (the sheets' prose, and the lemma sheet's
    Whitaker / Why / Recommend cells and the row `ok` writes) is kept in a
    notes file beside each sheet, `<sheet>.notes.json`. Everything else is
    rendered from the data, so `render` is byte-identical while the data is
    unchanged, and `render --check` says whether the sheet on disk is.

ANSWERS (README-lemma-spine.md s.8b, README-nt-jsonl.md s.15)
    ok / ✓            the recommendation (lemma sheet) or the draft (John 1)
    keep              lemma sheet only: the draft value, as the answer
    draft→            leave it a draft: nothing is written, the row stays open
    draft→ <value>    John 1 only: revise the draft, still a draft
    a string          a lemma (or a Whitaker key) / a gloss / a prose_order
    field: value; …   lemma_key, lemma, parsing, note / gloss, plain_form
    as row N          lemma sheet only: row N's answer
    Anything else is ambiguous, and `apply` stops and names the row before
    writing anything. A row with no answer is never touched.

    An answered row gets provenance `adam-reviewed` and `reviewed_on` (the
    device clock's date). Applying the same sheet twice changes nothing: a row
    whose override already says what the answer says is left as it is,
    reviewed_on included. `apply` then rebuilds what the rows feed
    (build_hymn_corpus.py / build_nt_corpus.py) and runs their --check; a
    build that refuses puts the override files back as they were.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
# Greek and macrons in messages must print on a Windows console or a pipe (cp1252 by default).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import lemma_spine as L  # noqa: E402
import strongs_gloss as G  # noqa: E402
import build_nt_corpus as B  # noqa: E402
import build_hymn_corpus as HB  # noqa: E402

REVIEWED = "adam-reviewed"
ACCEPT = {"ok", "okay", "✓", "✔"}
DRAFT_ARROW = re.compile(r"^draft\s*(→|->)\s*", re.I)
FIELD = re.compile(r"(?:^|;)\s*`?(lemma_key|lemma|parsing|note|gloss|plain_form|cut)`?\s*[:=]\s*")
AS_ROW = re.compile(r"^as row (\d+)\.?$", re.I)
NONE_WORDS = {"none", "null", "—", "-"}
# a bare answer that starts like one of these and says more is not a value
HEDGES = {"ok", "okay", "yes", "no", "keep", "accept", "reject", "maybe", "draft", "not",
          "either", "both", "tbd", "todo", "?", "✓", "✔", "✗", "x", "as", "same", "see"}


class Stop(Exception):
    """An answer that cannot be read without guessing."""


def jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def dump_jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def clean(v):
    """A value as Adam may have typed it in markdown: `code`, *italic*, "quoted"."""
    v = v.strip()
    for a, b in (("`", "`"), ("*", "*"), ('"', '"'), ("“", "”")):
        if len(v) >= 2 and v.startswith(a) and v.endswith(b):
            v = v[1:-1].strip()
    return v


def fields_of(ans, allowed):
    """`key: value; key: value` -> dict, or None when the answer is not in
    that form. A key outside `allowed`, or given twice, is a Stop."""
    marks = list(FIELD.finditer(ans))
    if not marks:
        return None
    if ans[:marks[0].start()].strip():
        raise Stop(f"{ans[:marks[0].start()].strip()!r} comes before the first `field:`")
    out = {}
    for m, nxt in zip(marks, marks[1:] + [None]):
        k = m.group(1)
        v = clean(ans[m.end(): nxt.start() if nxt else len(ans)].rstrip().rstrip(";"))
        if k not in allowed:
            raise Stop(f"`{k}` is not a field this sheet sets (it sets {', '.join(allowed)})")
        if k in out:
            raise Stop(f"`{k}` is given twice")
        if not v:
            raise Stop(f"`{k}` has no value")
        out[k] = v
    return out


def hedged(ans):
    """True when a bare answer reads as a comment, not a value."""
    words = re.findall(r"[\w✓✔✗?]+", ans.lower())
    return ("?" in ans or " or " in f" {ans.lower()} " or "→" in ans or "->" in ans
            or (len(words) > 1 and words[0] in HEDGES))


def table_cells(line):
    return [c.strip() for c in line.strip()[1:-1].split("|")]


# =============================================================================
# The lemma sheet
# =============================================================================

BATCH_WORKS = tuple(f"hymns:{k}" for k, h in HB.HYMNS.items() if "source_file" not in h)
PRINTED_WORKS = tuple(f"hymns:{k}" for k, h in HB.HYMNS.items() if "source_file" in h)


class LemmaSheet:
    name = "2026-09-26-lemma-flags.md"
    builds = ("build_hymn_corpus.py",)
    # the hymns whose flags this sheet lists (the answers file is shared)
    WORKS = BATCH_WORKS
    HEADER = ("| # | Hymn · stanza · clause uid | Form, in its line | Draft lemma · parse | "
              "Whitaker's candidates | Why flagged | Recommend | Adam: |\n"
              "|---|---|---|---|---|---|---|---|\n")
    ORDER = ("lemma", "lemma_key", "parsing", "note")

    def __init__(self, root=ROOT):
        self.root = root
        self.path = os.path.join(root, "docs", "review", self.name)
        self.notes_path = self.path[:-3] + ".notes.json"
        self.out = L.OVERRIDES

    def load(self):
        hyd = os.path.join(self.root, "data", "hymns")
        self.notes = json.loads(read_text(self.notes_path))
        self.all_tokens = jsonl(os.path.join(hyd, "tokens.jsonl"))
        self.passages = {p["uid"]: p for p in jsonl(os.path.join(hyd, "passages.jsonl"))}
        self.tokens = [t for t in self.all_tokens if self.passages[t["passage_uid"]]["work"] in self.WORKS]
        self.texts = {w["passage_uid"]: w["text"] for w in jsonl(os.path.join(hyd, "witnesses.jsonl"))
                      if w["name"] == "la.1"}
        self.works = json.loads(read_text(os.path.join(hyd, "manifest.json")))["works"]
        self.analyses = {r["form"]: r["analyses"]
                         for r in jsonl(os.path.join(self.root, "data", "lemmas", "whitaker-la",
                                                     "hymns.analyses.jsonl"))}
        self.overrides = L.load_overrides(self.out)
        noted = {r["address"]: r for r in self.notes["rows"]}
        by_addr = {t["address"]: t for t in self.tokens}
        gone = [a for a in noted if a not in by_addr]
        if gone:
            raise SystemExit(f"{self.notes_path}: rows for tokens that no longer exist: {gone}")
        self.rows = []
        for t in self.tokens:
            if t["address"] in noted or t["review"] or t["address"] in self.overrides:
                self.rows.append(self._row(t, noted.get(t["address"])))
        for n, r in enumerate(self.rows, 1):
            r["n"] = n
        self.by_addr = {r["address"]: r for r in self.rows}

    def _row(self, t, note):
        lp, pp = t["provenance"]["lemma"], t["provenance"]["parsing"]
        # what the resolver said before any answer (an answer keeps it under `was`)
        l_status = (lp["was"] if lp["source"] == REVIEWED else lp)["status"]
        p_status = (pp["was"] if pp["source"] == REVIEWED else pp)["status"]
        undrafted = lp["draft"] is None and pp["draft"] is None
        keep = {}
        if l_status in ("disagree", "ambiguous", "unknown") and not undrafted:
            keep["lemma"] = lp["draft"]
        if p_status == "disagree" and not undrafted:
            keep["parsing"] = pp["draft"]
        return {"address": t["address"], "token": t, "note": note, "keep": keep,
                "undrafted": undrafted,
                "lemma_flag": l_status in ("disagree", "ambiguous", "unknown"),
                "ok": (note or {}).get("ok"), "analyses": self.analyses.get(t["search_key"], [])}

    def label(self, r):
        return f"row {r['n']} ({r['address']} {r['token']['surface']})"

    # -- render --------------------------------------------------------------
    def adam_cell(self, r):
        ov = self.overrides.get(r["address"])
        if not ov:
            return ""
        f = {k: ov[k] for k in self.ORDER if k in ov}
        if r["ok"] is not None and f == r["ok"]:
            return "ok"
        if r["keep"] and f == r["keep"]:
            return "keep"
        return "; ".join(f"{k}: {v}" for k, v in f.items())

    def render(self):
        out = [self.notes["intro"], self.HEADER]
        for r in self.rows:
            t, p = r["token"], self.passages[r["token"]["passage_uid"]]
            hymn = " ".join(self.works[p["work"]]["title"].split()[:2])
            lines = self.texts[t["passage_uid"]].split("\n")
            line = lines[t["line"] - p["lines"][0]]
            lp, pp = t["provenance"]["lemma"], t["provenance"]["parsing"]
            nt = r["note"] or {"whitaker": self.candidates(r),
                               "why": "; ".join(t["review"] or []) or self.why_answered(r),
                               "recommend": "—"}
            cells = [str(r["n"]),
                     f"{hymn} · {p['stanza']} · `{t['passage_uid']}` ({t['address'].rsplit('.', 1)[1]})",
                     f"**{t['surface']}** · *{line}*",
                     "— (no draft)" if r["undrafted"] else f"{lp['draft']} · {pp['draft']}",
                     nt["whitaker"], nt["why"], nt["recommend"]]
            adam = self.adam_cell(r)
            # this sheet's empty Adam cell is "| |" (the John 1 sheet's is "|  |")
            out.append("| " + " | ".join(cells) + " | " + (adam + " |" if adam else "|") + "\n")
        out.append(self.notes["outro"])
        return "".join(out)

    def candidates(self, r):
        """Whitaker's entries for the form, by key: what a `lemma_key` answer names."""
        keys = sorted({a["key"] for a in r["analyses"]
                       if "TWO_WORDS" not in {v["kind"] for v in a.get("via") or []}})
        return " · ".join(f"`{k}`" for k in keys) if keys else "none"

    def why_answered(self, r):
        """An answered row keeps its reason on the sheet (the token's own
        `review` was cleared by the answer)."""
        if not r["undrafted"]:
            return "—"
        lp = r["token"]["provenance"]["lemma"]
        st = (lp["was"] if lp["source"] == REVIEWED else lp)["status"]
        return {"ambiguous": "lemma: several Whitaker entries, and no draft to choose among them",
                "unknown": "lemma: Whitaker has no analysis, and there is no draft",
                "disagree": "lemma: Whitaker reaches this form only by prefix/suffix word formation"}.get(st, "—")

    # -- read the sheet --------------------------------------------------------
    def answers(self, text):
        """[(row, answer)] for every row of the sheet on disk."""
        out = []
        for line in text.split("\n"):
            if not re.match(r"\|\s*\d+\s*\|", line):
                continue
            c = table_cells(line)
            m = re.search(r"`(wh-[0-9A-Z]+)` \((t\d+)\)", c[1])
            addr = m and f"{m.group(1)}/la.1.{m.group(2)}"
            if addr not in self.by_addr:
                raise SystemExit(f"sheet row {c[0]}: {addr or c[1]!r} is not a row of this sheet; "
                                 "re-render it (review.py render)")
            r = self.by_addr[addr]
            surface = re.match(r"\*\*(.*?)\*\*", c[2])
            if not surface or surface.group(1) != r["token"]["surface"]:
                raise SystemExit(f"sheet row {c[0]}: the form is not {r['token']['surface']!r} any more; "
                                 "re-render it (review.py render)")
            out.append((r, " | ".join(c[7:]).strip() if len(c) > 7 else ""))
        return out

    # -- interpret -------------------------------------------------------------
    def interpret(self, r, ans, done):
        """-> ("write", fields) or ("defer", None). Raises Stop."""
        a = ans.strip()
        low = a.rstrip(".").strip().lower()
        if low in ACCEPT:
            if not r["ok"]:
                raise Stop("there is no recommendation on this row to accept; write the answer")
            return "write", dict(r["ok"])
        if low == "keep":
            if not r["keep"]:
                raise Stop("nothing on this row was flagged, so there is no draft value to keep")
            return "write", dict(r["keep"])
        m = DRAFT_ARROW.match(a)
        if m:
            if a[m.end():].strip():
                raise Stop("a lemma answer has no draft state: write the value, or `draft→` alone")
            return "defer", None
        m = AS_ROW.match(a)
        if m:
            src = next((x for x in self.rows if x["n"] == int(m.group(1))), None)
            if src is None or src is r or src["address"] not in done or done[src["address"]][0] != "write":
                raise Stop(f"row {m.group(1)} has no answer of its own to copy")
            return "write", dict(done[src["address"]][1])
        f = fields_of(a, self.ORDER)
        if f is None:
            if hedged(a):
                raise Stop(f"{a!r} reads as a comment, not a value")
            if "lemma" not in r["keep"] and not r["lemma_flag"]:
                raise Stop("this row is flagged for its parsing: write `parsing: …` or `lemma: …`")
            key = self.whitaker_key(r, a, strict=False)
            f = {"lemma_key": key} if key else {"lemma": clean(a)}
        if "lemma_key" in f:
            f["lemma_key"] = self.whitaker_key(r, f["lemma_key"], strict=True)
        if not {"lemma", "lemma_key", "parsing"} & set(f):
            raise Stop("the answer sets none of lemma, lemma_key, parsing")
        return "write", {k: f[k] for k in self.ORDER if k in f}

    def whitaker_key(self, r, v, strict):
        """One of Whitaker's keys for this form, matched with spacing folded
        (a markdown key's double space is easily lost)."""
        fold = lambda s: " ".join(clean(s).split())  # noqa: E731
        keys = sorted({a["key"] for a in r["analyses"]})
        hit = [k for k in keys if fold(k) == fold(v)]
        if hit:
            return hit[0]
        if strict:
            raise Stop(f"lemma_key {v!r} is not one of Whitaker's analyses of this form: {keys}")
        return None

    def row_for(self, r, fields, today):
        ov = self.overrides.get(r["address"])
        new = {"address": r["address"], "surface": r["token"]["surface"], **fields}
        old = {k: v for k, v in (ov or {}).items() if k != "reviewed_on"}
        new["reviewed_on"] = ov["reviewed_on"] if ov and old == new else today
        if "note" in new:
            new["note"] = new.pop("note")
        return new

    def validate(self, r, row):
        """The build's own check, before anything is written."""
        t = r["token"]
        lp, pp = t["provenance"]["lemma"], t["provenance"]["parsing"]
        resolved = (L.resolve_undrafted(r["analyses"]) if r["undrafted"]
                    else L.resolve(lp["draft"], pp["draft"], r["analyses"]))
        try:
            L.apply_override(resolved, t["surface"], r["analyses"], row)
        except ValueError as e:
            raise Stop(str(e))

    def plan(self, answers, today):
        """-> (changes {address: row}, report, stops)."""
        done, changes, stops = {}, {}, []
        report = {"answered": 0, "applied": 0, "to_apply": 0, "deferred": 0, "ambiguous": 0}
        for r, ans in answers:
            if not ans:
                continue
            report["answered"] += 1
            try:
                kind, f = self.interpret(r, ans, done)
                done[r["address"]] = (kind, f)
                if kind == "defer":
                    report["deferred"] += 1
                    continue
                row = self.row_for(r, f, today)
                self.validate(r, row)
            except Stop as e:
                stops.append(f"{self.label(r)}: {e}")
                report["ambiguous"] += 1
                continue
            if self.overrides.get(r["address"]) == row:
                report["applied"] += 1
            else:
                report["to_apply"] += 1
                changes[r["address"]] = row
        return changes, report, stops

    def write(self, changes):
        rows = dict(self.overrides)
        rows.update(changes)
        order = {t["address"]: i for i, t in enumerate(self.all_tokens)}
        return {self.out: dump_jsonl(sorted(rows.values(), key=lambda x: order.get(x["address"], 1e9)))}

    def status_extra(self):
        return f"{len(self.overrides)} rows in {os.path.relpath(self.out, self.root)}"


# =============================================================================
# The John 1 sheet
# =============================================================================

class NTSheet:
    name = "2026-09-26-john1-drafts.md"
    builds = ("build_nt_corpus.py",)
    TABLE = ("| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |\n"
             "|---|---|---|---|---|---|---|\n")
    GLOSS_FIELDS = ("gloss", "plain_form")

    def __init__(self, root=ROOT):
        self.root = root
        self.path = os.path.join(root, "docs", "review", self.name)
        self.notes_path = self.path[:-3] + ".notes.json"

    def load(self):
        ntd = os.path.join(self.root, "data", "nt")
        self.notes = json.loads(read_text(self.notes_path))
        self.passages = jsonl(os.path.join(ntd, "passages.jsonl"))
        self.tokens = jsonl(os.path.join(ntd, "tokens.jsonl"))
        self.witnesses = {w["address"]: w for w in jsonl(os.path.join(ntd, "witnesses.jsonl"))}
        self.ov_list = jsonl(G.OVERRIDES)
        self.po_list = jsonl(B.PROSE_ORDERS)
        self.overrides = G.load_overrides(G.OVERRIDES)
        self.orders = B.load_prose_orders(B.PROSE_ORDERS)
        self.tok_by = {t["address"]: t for t in self.tokens}
        self.verse_toks = {}
        for t in self.tokens:
            self.verse_toks.setdefault(t["passage_uid"], []).append(t)
        self.rows = {}
        for p in self.passages:
            self.rows[p["uid"]] = {"kind": "order", "key": p["uid"], "passage": p}
            for t in self.verse_toks[p["uid"]]:
                if t["address"] in self.overrides:
                    self.rows[t["address"]] = {"kind": "gloss", "key": t["address"], "token": t,
                                               "passage": p}

    def label(self, r):
        cit = r["passage"]["citation"].split(":", 1)[1].replace("John.", "John ").replace(".", ":")
        if r["kind"] == "order":
            return f"{cit} plain line ({r['key']})"
        return f"{cit} #{r['token']['position']} {r['token']['surface']} ({r['key']})"

    # -- render --------------------------------------------------------------
    def render(self):
        n_ov = len(self.ov_list)
        d_ov = sum(1 for r in self.ov_list if r.get("draft"))
        n_po = len(self.po_list)
        d_po = sum(1 for r in self.po_list if r.get("draft"))
        gloss_rows = (f"{n_ov} rows, layer `house`, all `draft: true`" if d_ov == n_ov else
                      f"{n_ov} rows: {d_ov} `draft: true` (layer `house`), {n_ov - d_ov} reviewed")
        order_rows = (f"{n_po} verses, source `house-draft`, all draft" if d_po == n_po else
                      f"{n_po} verses: {d_po} `house-draft`, {n_po - d_po} reviewed")
        out = [self.notes["intro"].replace("{gloss_rows}", gloss_rows).replace("{order_rows}", order_rows)]
        blocks = []
        for p in self.passages:
            uid, toks = p["uid"], self.verse_toks[p["uid"]]
            greek = self.witnesses[f"{uid}/{B.WITNESS}"]["text"]
            plain = self.witnesses.get(f"{uid}/{B.PLAIN}")
            po = self.orders.get(uid)
            b = [f"## {p['book']} {p['chapter']}:{p['verse']}", "",
                 f"`{p['citation']}` · `{uid}`", "", f"> {greek}", "",
                 "**Wooden** (draft glosses in Greek order): " + " ".join(t["gloss"] or "—" for t in toks), ""]
            if plain and po:
                b += ["**Plain:** " + B.render_plain(toks, plain), "",
                      f"`prose_order` {json.dumps(po['prose_order'], ensure_ascii=False)} · "
                      f"`absorbed` {json.dumps(po['absorbed'])}", "",
                      "**Adam (plain line):** " + ("" if po.get("draft") else "✓")]
            else:
                b += ["**Plain:** not yet ordered"]
            b += ["", self.TABLE.rstrip("\n")]
            for t in toks:
                ov = self.overrides.get(t["address"])
                if not ov:
                    continue
                was = t["provenance"]["gloss"]["was"]["value"]
                b.append("| " + " | ".join([
                    str(t["position"]), t["surface"], was if was is not None else "—",
                    ov.get("gloss", t["gloss"] or ""), ov.get("plain_form") or "", ov.get("note", ""),
                    "" if ov.get("draft") else "✓"]) + " |")
            blocks.append("\n".join(b))
        out.append("\n\n\n".join(blocks) + "\n")
        return "".join(out)

    # -- read the sheet --------------------------------------------------------
    def answers(self, text):
        out, uid = [], None
        for line in text.split("\n"):
            m = re.match(r"`kjv:[^`]+` · `(wh-[0-9A-Z]+)`", line)
            if m:
                uid = m.group(1)
                if uid not in self.rows:
                    raise SystemExit(f"sheet: {uid} is not a verse of this sheet; re-render it")
                continue
            if line.startswith("**Adam (plain line):**"):
                out.append((self.rows[uid], line[len("**Adam (plain line):**"):].strip()))
                continue
            if uid and re.match(r"\|\s*\d+\s*\|", line):
                c = table_cells(line)
                addr = f"{uid}/{B.WITNESS}.t{int(c[0]):02d}"
                r = self.rows.get(addr)
                if not r or r["token"]["surface"] != c[1]:
                    raise SystemExit(f"sheet: {uid} #{c[0]} {c[1]} is not a draft row of this sheet any "
                                     "more; re-render it (review.py render)")
                out.append((r, " | ".join(c[6:]).strip() if len(c) > 6 else ""))
        return out

    # -- interpret -------------------------------------------------------------
    def interpret(self, r, ans):
        """-> ("accept"|"defer"|"revise"|"replace", value)."""
        a = ans.strip()
        if a.rstrip(".").strip().lower() in ACCEPT:
            return "accept", None
        m = DRAFT_ARROW.match(a)
        if m:
            rest = a[m.end():].strip()
            if not rest:
                return "defer", None
            return "revise", self.value(r, rest)
        return "replace", self.value(r, a)

    def value(self, r, a):
        if r["kind"] == "order":
            return self.order(r, a)
        f = fields_of(a, self.GLOSS_FIELDS + ("note",))
        if f is None:
            if hedged(a):
                raise Stop(f"{a!r} reads as a comment, not a gloss")
            if self.overrides[r["key"]].get("plain_form"):
                raise Stop("this row has a plain_form too: write `gloss: …` and/or `plain_form: …`")
            f = {"gloss": clean(a)}
        for k in self.GLOSS_FIELDS:
            if k in f and f[k].lower() in NONE_WORDS:
                if k == "gloss":
                    raise Stop("a gloss cannot be removed here; to drop a draft, delete its row "
                               "from data/nt/gloss-overrides.jsonl (the dictionary gloss comes back)")
                f[k] = None
            elif k in f and (len(re.split(r"[ -]", f[k])) > 4 or re.search(r"[<>()\[\]:?|]", f[k])):
                raise Stop(f"{f[k]!r} is not a word gloss (at most four words, no markup)")
        return f

    def order(self, r, a):
        a = a.replace("`", "")
        lists = re.findall(r"\[[^\]]*\]", a)
        if not lists:
            raise Stop("write the plain line as a prose_order: [positions and \"supplied words\"]")
        try:
            order = json.loads(lists[0])
            absorbed = json.loads(lists[1]) if len(lists) > 1 else None
        except ValueError:
            raise Stop("the prose_order is not a list of positions and \"quoted\" words")
        if len(lists) > 2 or (absorbed is not None and "absorbed" not in a):
            raise Stop("write it as [order] absorbed [positions]")
        n = len(self.verse_toks[r["key"]])
        if absorbed is None:
            used = [x for x in order if B._is_pos(x)]
            missing = [i for i in range(1, n + 1) if i not in used]
            if missing:
                raise Stop(f"positions {missing} are not in the order: say `absorbed {missing}` "
                           "if a neighbour carries them")
            absorbed = []
        if any(not B._is_pos(x) and not (isinstance(x, str) and x and x.strip() == x) for x in order) \
                or not all(B._is_pos(x) for x in absorbed):
            raise Stop("the prose_order holds positions and supplied words only")
        prob = B.permutation_problems(n, order, absorbed)
        if prob:
            raise Stop(f"not a permutation of the verse's {n} tokens: {prob}")
        return {"prose_order": order, "absorbed": absorbed}

    # -- rows ------------------------------------------------------------------
    KEYS = {"gloss": ("address", "surface", "gloss", "plain_form", "layer",
                      "draft", "drafted_on", "reviewed_on", "note"),
            "order": ("passage_uid", "citation", "prose_order", "absorbed", "plain_override",
                      "source", "draft", "drafted_on", "reviewed_on", "note")}
    DATES = ("draft", "drafted_on", "reviewed_on")

    def row_for(self, r, kind, val, today):
        """The row the answer makes. Unchanged in substance -> the old row,
        its date included (a second apply is a no-op)."""
        old = self.overrides[r["key"]] if r["kind"] == "gloss" else self.orders[r["key"]]
        draft = kind == "revise"
        new = {k: v for k, v in old.items() if k not in self.DATES}
        for k, v in (val or {}).items():
            if v is None:
                new.pop(k, None)
            else:
                new[k] = v
        if r["kind"] == "gloss":
            new["layer"] = "house" if draft else REVIEWED
        else:
            new["source"] = "house-draft" if draft else REVIEWED
        if new == {k: v for k, v in old.items() if k not in self.DATES} and bool(old.get("draft")) == draft:
            return old
        if draft:
            new.update(draft=True, drafted_on=today)
        else:
            new["reviewed_on"] = today
        return {k: new[k] for k in self.KEYS[r["kind"]] if k in new}

    def validate(self, r, row):
        if r["kind"] == "gloss":
            t = r["token"]
            path = self._tmp(row, self.ov_list, "address")
            try:
                G.load_overrides(path)
                G.apply_override(None, None, {}, t["surface"], row)
            except ValueError as e:
                raise Stop(str(e))
            finally:
                os.remove(path)
        else:
            path = self._tmp(row, self.po_list, "passage_uid")
            try:
                B.load_prose_orders(path)
            except ValueError as e:
                raise Stop(str(e))
            finally:
                os.remove(path)

    def _tmp(self, row, rows, key):
        import tempfile
        fd, path = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(dump_jsonl([row if x[key] == row[key] else x for x in rows]))
        return path

    def plan(self, answers, today):
        changes, stops = {}, []
        report = {"answered": 0, "applied": 0, "to_apply": 0, "deferred": 0, "ambiguous": 0}
        for r, ans in answers:
            if not ans:
                continue
            report["answered"] += 1
            try:
                kind, val = self.interpret(r, ans)
                if kind == "defer":
                    report["deferred"] += 1
                    continue
                row = self.row_for(r, kind, val, today)
                self.validate(r, row)
            except Stop as e:
                stops.append(f"{self.label(r)}: {e}")
                report["ambiguous"] += 1
                continue
            old = self.overrides[r["key"]] if r["kind"] == "gloss" else self.orders[r["key"]]
            if old == row:
                report["applied"] += 1
            else:
                report["to_apply"] += 1
                changes[r["key"]] = (r["kind"], row)
        return changes, report, stops

    def write(self, changes):
        out = {}
        g = {k: row for k, (kind, row) in changes.items() if kind == "gloss"}
        o = {k: row for k, (kind, row) in changes.items() if kind == "order"}
        if g:
            out[G.OVERRIDES] = dump_jsonl([g.get(x["address"], x) for x in self.ov_list])
        if o:
            out[B.PROSE_ORDERS] = dump_jsonl([o.get(x["passage_uid"], x) for x in self.po_list])
        return out

    def status_extra(self):
        rg = sum(1 for r in self.ov_list if not r.get("draft"))
        ro = sum(1 for r in self.po_list if not r.get("draft"))
        return (f"glosses {rg}/{len(self.ov_list)} reviewed, plain lines {ro}/{len(self.po_list)} "
                "reviewed, in the data")


# =============================================================================
# The printed hymns: their lemma flags, and their clause cuts
# =============================================================================

class ThomasLemmaSheet(LemmaSheet):
    """The flagged tokens of the hymns printed from Britt 1922. Same columns,
    same answers, same answers file as the lemma sheet; these tokens have no
    draft, so `keep` has nothing to keep and a bare answer is a lemma."""
    name = "2026-09-26-thomas-lemma-flags.md"
    WORKS = PRINTED_WORKS


class CutSheet:
    """Every clause cut of the printed hymns, one row per stanza (README-hymn-
    jsonl.md s.9d). Answers go to data/hymn-sources/cut-reviewed.jsonl, which
    build_hymn_corpus.py applies."""
    name = "2026-09-26-thomas-cuts.md"
    builds = ("build_hymn_corpus.py",)
    HEADER = ("| # | Hymn · stanza | The cut: clause, lines, Latin | Why | Adam: |\n"
              "|---|---|---|---|---|\n")
    FIELDS = ("cut", "note")

    def __init__(self, root=ROOT):
        self.root = root
        self.path = os.path.join(root, "docs", "review", self.name)
        self.notes_path = self.path[:-3] + ".notes.json"
        self.out = os.path.join(root, "data", "hymn-sources", "cut-reviewed.jsonl")

    def load(self):
        hyd = os.path.join(self.root, "data", "hymns")
        self.notes = json.loads(read_text(self.notes_path))
        passages = jsonl(os.path.join(hyd, "passages.jsonl"))
        self.by_uid = {p["uid"]: p for p in passages}
        self.texts = {w["passage_uid"]: w["text"] for w in jsonl(os.path.join(hyd, "witnesses.jsonl"))
                      if w["name"] == "la.1"}
        self.overrides = HB.load_cut_reviews(self.out)
        self.rows = []
        for p in passages:
            if p["unit"] != "stanza" or p["work"] not in PRINTED_WORKS:
                continue
            slug = p["work"].split(":", 1)[1]
            draft = [[a, b] for a, b, _ in HB.HYMNS[slug]["clauses"][p["stanza"]]]
            self.rows.append({"key": p["citation"], "stanza": p, "draft": draft,
                              "short": " ".join(HB.HYMNS[slug]["title"].split()[:2]).rstrip(","),
                              "clauses": [self.by_uid[u] for u in p["clauses"]]})
        for n, r in enumerate(self.rows, 1):
            r["n"] = n
        self.by_stanza_uid = {r["stanza"]["uid"]: r for r in self.rows}

    def label(self, r):
        return f"row {r['n']} ({r['key']})"

    @staticmethod
    def fmt(cut):
        return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in cut)

    # -- render --------------------------------------------------------------
    def adam_cell(self, r):
        ov = self.overrides.get(r["key"])
        if not ov:
            return ""
        if ov["cut"] == r["draft"] and not ov.get("note"):
            return "ok"
        return f"cut: {self.fmt(ov['cut'])}" + (f"; note: {ov['note']}" if ov.get("note") else "")

    def render(self):
        out = [self.notes["intro"], self.HEADER]
        for r in self.rows:
            st = r["stanza"]
            cut, why = [], []
            for c in r["clauses"]:
                a, b = c["lines"]
                span = f"l.{a}" if a == b else f"ll.{a}-{b}"
                latin = " / ".join(self.texts[c["uid"]].split("\n"))
                cut.append(f"c{c['clause']} {span}: *{latin}*")
                why.append(f"c{c['clause']}: {c['cut']['why']}")
            adam = self.adam_cell(r)
            cells = [str(r["n"]), f"{r['short']} {st['stanza']} `{st['uid']}`", "<br>".join(cut),
                     "<br>".join(why)]
            out.append("| " + " | ".join(cells) + " | " + (adam + " |" if adam else "|") + "\n")
        out.append(self.notes["outro"])
        return "".join(out)

    # -- read the sheet --------------------------------------------------------
    def answers(self, text):
        out = []
        for line in text.split("\n"):
            if not re.match(r"\|\s*\d+\s*\|", line):
                continue
            c = table_cells(line)
            m = re.search(r"`(wh-[0-9A-Z]+)`", c[1])
            if not m or m.group(1) not in self.by_stanza_uid:
                raise SystemExit(f"sheet row {c[0]}: {c[1]!r} is not a stanza of this sheet; "
                                 "re-render it (review.py render)")
            out.append((self.by_stanza_uid[m.group(1)], " | ".join(c[4:]).strip() if len(c) > 4 else ""))
        return out

    # -- interpret -------------------------------------------------------------
    def parse_cut(self, r, v):
        cut = []
        for part in v.replace("–", "-").split(","):
            m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", part)
            if not m:
                raise Stop(f"{v!r} is not a cut: write the clauses' lines in order, e.g. `cut: 1, 2-3, 4-6`")
            a = int(m.group(1))
            cut.append([a, int(m.group(2) or a)])
        prob = HB.partition_problem(cut, r["stanza"]["lines"][1])
        if prob:
            raise Stop(f"cut {v!r}: {prob}")
        return cut

    def interpret(self, r, ans):
        """-> ("write", {cut, note?}) or ("defer", None). Raises Stop."""
        a = ans.strip()
        if a.rstrip(".").strip().lower() in ACCEPT:
            return "write", {"cut": r["draft"]}
        m = DRAFT_ARROW.match(a)
        if m:
            if a[m.end():].strip():
                raise Stop("a cut has no draft state to revise: write the cut, or `draft→` alone")
            return "defer", None
        f = fields_of(a, self.FIELDS)
        if f is None:
            if hedged(a):
                raise Stop(f"{a!r} reads as a comment, not a cut")
            raise Stop("write `ok`, or `cut: 1, 2-3, 4-6` (and `; note: why`)")
        cut = self.parse_cut(r, f["cut"]) if "cut" in f else r["draft"]
        new_joins = [(x, y) for x, y in cut if y > x and [x, y] not in r["draft"]]
        if new_joins and not f.get("note"):
            raise Stop(f"lines {', '.join(f'{x}-{y}' for x, y in new_joins)} are a new join: "
                       "give its grammatical reason as `; note: …`")
        ov = self.overrides.get(r["key"])
        if ov and ov["cut"] != r["draft"] and cut != ov["cut"]:
            raise Stop("this stanza was re-cut once already and its clause uids re-issued; a second "
                       "re-cut is a hand decision (edit data/hymn-sources/cut-reviewed.jsonl and the registry)")
        out = {"cut": cut}
        if f.get("note"):
            out["note"] = f["note"]
        return "write", out

    def row_for(self, r, fields, today):
        ov = self.overrides.get(r["key"])
        new = {"stanza": r["key"], **fields}
        old = {k: v for k, v in (ov or {}).items() if k != "reviewed_on"}
        new["reviewed_on"] = ov["reviewed_on"] if ov and old == new else today
        if "note" in new:
            new["note"] = new.pop("note")
        return new

    def validate(self, r, row):
        slug = r["key"].split(":", 1)[1].split(".")[0]
        draft = HB.HYMNS[slug]["clauses"][r["stanza"]["stanza"]]
        try:
            HB.effective_cut(r["key"], draft, row, r["stanza"]["lines"][1])
        except SystemExit as e:
            raise Stop(str(e))

    def plan(self, answers, today):
        changes, stops = {}, []
        report = {"answered": 0, "applied": 0, "to_apply": 0, "deferred": 0, "ambiguous": 0}
        for r, ans in answers:
            if not ans:
                continue
            report["answered"] += 1
            try:
                kind, f = self.interpret(r, ans)
                if kind == "defer":
                    report["deferred"] += 1
                    continue
                row = self.row_for(r, f, today)
                self.validate(r, row)
            except Stop as e:
                stops.append(f"{self.label(r)}: {e}")
                report["ambiguous"] += 1
                continue
            if self.overrides.get(r["key"]) == row:
                report["applied"] += 1
            else:
                report["to_apply"] += 1
                changes[r["key"]] = row
        return changes, report, stops

    def write(self, changes):
        rows = dict(self.overrides)
        rows.update(changes)
        order = {r["key"]: i for i, r in enumerate(self.rows)}
        return {self.out: dump_jsonl(sorted(rows.values(), key=lambda x: order.get(x["stanza"], 1e9)))}

    def status_extra(self):
        recut = sum(1 for r in self.rows if r["key"] in self.overrides
                    and self.overrides[r["key"]]["cut"] != r["draft"])
        return f"{len(self.overrides)} rows in {os.path.relpath(self.out, self.root)} ({recut} re-cut)"


# =============================================================================
# The collation of a batch hymn's received Latin against a PD printing
# =============================================================================

class CollationSheet:
    """Every difference between Adoro te's received Latin and Britt 1922's
    printing, one row per difference (README-hymn-jsonl.md s.10). Rows come
    from build_hymn_corpus.collate() over the committed data, so the sheet is
    what the data says. Answers go to data/hymn-sources/collation-reviewed.jsonl;
    the build counts them in the manifest and never edits the text."""
    name = "2026-09-26-adoro-collation.md"
    builds = ("build_hymn_corpus.py",)
    HEADER = ("| # | St · line | Difference id | Received (the corpus) | Britt 1922 | Kind | Adam: |\n"
              "|---|---|---|---|---|---|---|\n")
    ANSWER = re.compile(r"^(ok|okay|✓|✔|received|keep|britt)\.?\s*(?:;\s*`?note`?\s*[:=]\s*(.+))?$", re.I)

    def __init__(self, root=ROOT):
        self.root = root
        self.path = os.path.join(root, "docs", "review", self.name)
        self.notes_path = self.path[:-3] + ".notes.json"
        self.out = os.path.join(root, "data", "hymn-sources", "collation-reviewed.jsonl")

    def load(self):
        hyd = os.path.join(self.root, "data", "hymns")
        self.notes = json.loads(read_text(self.notes_path))
        doc = json.loads(read_text(os.path.join(self.root, "data", "hymn-sources",
                                                HB.COLLATIONS["adoro-te"])))
        self.diffs, self.stats = HB.collate(doc, *(jsonl(os.path.join(hyd, f"{k}.jsonl"))
                                                   for k in ("passages", "witnesses", "tokens")))
        self.overrides = HB.load_collation_reviews(self.out)
        self.rows = [dict(d, n=n) for n, d in enumerate(self.diffs, 1)]
        self.by_id = {r["id"]: r for r in self.rows}

    def label(self, r):
        return f"row {r['n']} ({r['id']})"

    # -- render --------------------------------------------------------------
    def adam_cell(self, r):
        ov = self.overrides.get(r["id"])
        if not ov:
            return ""
        return ov["reading"] + (f"; note: {ov['note']}" if ov.get("note") else "")

    def render(self):
        k = {}
        for d in self.diffs:
            k[d["kind"]] = k.get(d["kind"], 0) + 1
        counts = ", ".join(f"{n} {kind}" for kind, n in sorted(k.items(), key=lambda x: (-x[1], x[0])))
        s = self.stats
        out = [self.notes["intro"].replace("{counts}", counts).replace("{n}", str(len(self.diffs)))
               .replace("{words}", f"{s['received_words']} received words, {s['printed_words']} printed; "
                                   f"{s['paired']} paired, {s['identical']} identical to the character"),
               self.HEADER]
        show = lambda v: f"*{v}*" if v else "— (absent)"  # noqa: E731
        for r in self.rows:
            cells = [str(r["n"]), f"{r['stanza']} · l.{r['line']} (p. {r['page']})", f"`{r['id']}`",
                     show(r["received"]), show(r["britt"]), r["kind"]]
            adam = self.adam_cell(r)
            out.append("| " + " | ".join(cells) + " | " + (adam + " |" if adam else "|") + "\n")
        out.append(self.notes["outro"])
        return "".join(out)

    # -- read the sheet --------------------------------------------------------
    def answers(self, text):
        out = []
        for line in text.split("\n"):
            if not re.match(r"\|\s*\d+\s*\|", line):
                continue
            c = table_cells(line)
            m = re.fullmatch(r"`([^`]+)`", c[2])
            if not m or m.group(1) not in self.by_id:
                raise SystemExit(f"sheet row {c[0]}: {c[2]!r} is not a difference of this sheet; "
                                 "re-render it (review.py render)")
            out.append((self.by_id[m.group(1)], " | ".join(c[6:]).strip() if len(c) > 6 else ""))
        return out

    # -- interpret -------------------------------------------------------------
    def interpret(self, r, ans):
        """-> ("write", {reading, note?}) or ("defer", None). Raises Stop."""
        a = ans.strip()
        m = DRAFT_ARROW.match(a)
        if m:
            if a[m.end():].strip():
                raise Stop("a collation answer has no draft state: write the reading, or `draft→` alone")
            return "defer", None
        m = self.ANSWER.match(a)
        if not m:
            raise Stop(f"{a!r}: write `ok` (the received reading stands) or `britt` (Britt's), "
                       "optionally `; note: …`")
        out = {"reading": "britt" if m.group(1).lower() == "britt" else "received"}
        if m.group(2):
            out["note"] = clean(m.group(2))
        return "write", out

    def row_for(self, r, fields, today):
        ov = self.overrides.get(r["id"])
        new = {"id": r["id"], **fields}
        old = {k: v for k, v in (ov or {}).items() if k != "reviewed_on"}
        new["reviewed_on"] = ov["reviewed_on"] if ov and old == new else today
        if "note" in new:
            new["note"] = new.pop("note")
        return new

    def plan(self, answers, today):
        changes, stops = {}, []
        report = {"answered": 0, "applied": 0, "to_apply": 0, "deferred": 0, "ambiguous": 0}
        for r, ans in answers:
            if not ans:
                continue
            report["answered"] += 1
            try:
                kind, f = self.interpret(r, ans)
                if kind == "defer":
                    report["deferred"] += 1
                    continue
                row = self.row_for(r, f, today)
            except Stop as e:
                stops.append(f"{self.label(r)}: {e}")
                report["ambiguous"] += 1
                continue
            if self.overrides.get(r["id"]) == row:
                report["applied"] += 1
            else:
                report["to_apply"] += 1
                changes[r["id"]] = row
        return changes, report, stops

    def write(self, changes):
        rows = dict(self.overrides)
        rows.update(changes)
        order = {r["id"]: i for i, r in enumerate(self.rows)}
        return {self.out: dump_jsonl(sorted(rows.values(), key=lambda x: order.get(x["id"], 1e9)))}

    def status_extra(self):
        b = sum(1 for r in self.overrides.values() if r["reading"] == "britt")
        return (f"{len(self.overrides)} rows in {os.path.relpath(self.out, self.root)} "
                f"({b} for Britt's reading)")


SHEETS = (LemmaSheet, ThomasLemmaSheet, CutSheet, NTSheet, CollationSheet)


# =============================================================================
# Commands
# =============================================================================

def pick(names):
    if not names:
        return [S() for S in SHEETS]
    out = []
    for n in names:
        base = os.path.basename(n)
        S = next((S for S in SHEETS if S.name == base), None)
        if S is None:
            raise SystemExit(f"{n}: not a review sheet this tool knows ({', '.join(S.name for S in SHEETS)})")
        out.append(S())
    return out


def today_from_clock():
    """The device clock (CLAUDE.md: dates come from the machine, never a sandbox)."""
    return datetime.date.today().isoformat()


def cmd_render(a):
    bad = 0
    for s in pick(a.sheets):
        s.load()
        text = s.render()
        rel = os.path.relpath(s.path, s.root)
        on_disk = read_text(s.path) if os.path.exists(s.path) else None
        if a.check:
            ok = on_disk == text
            print(f"  {rel}: {'byte-identical' if ok else 'DIFFERS from the data'}")
            bad += not ok
            continue
        if on_disk == text:
            print(f"  {rel}: unchanged")
            continue
        if on_disk is not None and not a.force:
            # answers Adam has written but not applied would be lost
            _, rep, _ = s.plan(s.answers(on_disk), today_from_clock())
            if rep["to_apply"] or rep["ambiguous"]:
                raise SystemExit(f"{rel}: {rep['to_apply'] + rep['ambiguous']} answers are not applied yet; "
                                 "run `review.py apply` first (or render --force to drop them)")
        write_atomic(s.path, text)
        print(f"  {rel}: written")
    if bad:
        raise SystemExit(1)


def cmd_status(a):
    for s in pick(a.sheets):
        s.load()
        answers = s.answers(read_text(s.path))
        _, rep, stops = s.plan(answers, today_from_clock())
        open_ = len(answers) - rep["answered"]
        print(f"  {os.path.relpath(s.path, s.root)}: {len(answers)} rows, {rep['answered']} answered "
              f"({rep['applied']} applied, {rep['to_apply']} to apply, {rep['deferred']} kept as drafts, "
              f"{rep['ambiguous']} ambiguous), {open_} open")
        print(f"      {s.status_extra()}")
        for m in stops:
            print(f"      ambiguous: {m}")


def run_builds(s, wrote):
    """Rebuild what the override files feed, then its --check. With nothing
    written, only the --check (the committed output must still be what the
    data says)."""
    for b in s.builds:
        for args in (([], ["--check"]) if wrote else (["--check"],)):
            cmd = [sys.executable, os.path.join(s.root, "pipeline", b)] + args
            p = subprocess.run(cmd, cwd=s.root, capture_output=True, text=True, encoding="utf-8",
                               errors="replace")
            tail = (p.stdout + p.stderr).strip().splitlines()[-1:] or [""]
            print(f"  {b} {' '.join(args)}: {tail[0].strip()}")
            if p.returncode:
                return p.stdout + p.stderr
    return None


def cmd_apply(a):
    (s,) = pick([a.sheet])
    if not os.path.exists(a.sheet):
        raise SystemExit(f"{a.sheet}: no such file")
    if a.today and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.today):
        raise SystemExit("--today is YYYY-MM-DD")
    today = a.today or today_from_clock()
    s.load()
    changes, rep, stops = s.plan(s.answers(read_text(a.sheet)), today)
    if stops:
        print(f"STOPPED: {len(stops)} answer(s) cannot be read without guessing. Nothing was written.")
        for m in stops:
            print(f"  {m}")
        raise SystemExit(2)
    print(f"  {rep['answered']} answered: {rep['to_apply']} to write, {rep['applied']} already applied, "
          f"{rep['deferred']} kept as drafts")
    if a.dry_run:
        return
    files = s.write(changes) if changes else {}
    before = {p: (read_text(p) if os.path.exists(p) else None) for p in files}
    for p, text in files.items():
        write_atomic(p, text)
        print(f"  wrote {os.path.relpath(p, s.root)} ({len(changes)} row(s), reviewed_on {today})")
    if a.no_build:
        return
    err = run_builds(s, bool(files))
    if err:
        for p, text in before.items():
            if text is None:
                os.remove(p)
            else:
                write_atomic(p, text)
        if files:
            print("  the build refused: the override files are back as they were")
        raise SystemExit("BUILD FAILED:\n" + err[-2000:])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render", help="regenerate the sheets from the data")
    r.add_argument("sheets", nargs="*")
    r.add_argument("--check", action="store_true", help="compare, write nothing; exit 1 on a difference")
    r.add_argument("--force", action="store_true", help="overwrite answers not yet applied")
    p = sub.add_parser("apply", help="write the sheet's answers as override rows, then rebuild")
    p.add_argument("sheet")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-build", action="store_true")
    p.add_argument("--today", help="YYYY-MM-DD (default: the device clock)")
    st = sub.add_parser("status", help="answered vs open, per sheet")
    st.add_argument("sheets", nargs="*")
    a = ap.parse_args(argv)
    {"render": cmd_render, "apply": cmd_apply, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
