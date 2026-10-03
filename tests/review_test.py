#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
review_test.py -- pipeline/review.py, end to end, on a TEMP COPY of the repo.

Run:  python3 tests/review_test.py

The real sheets and override files are never written: everything below
happens in a copy (pipeline/, tests/, docs/review/, data/ without the big
gitignored files; the NT's pinned inputs when data/corpus/ holds them).

WHAT IT ASSERTS
    1. `render --check`: all five sheets are byte-identical to what the data renders.
    2. The lemma sheet: a few answers filled in (ok, ✓, keep, explicit fields,
       a bare Whitaker key with its double space lost, `as row N`, draft→),
       then `apply`:
       - exactly the answered rows are written to adam-reviewed.jsonl, dated
         --today, in token order; the deferred and unanswered rows are not;
       - the rebuilt tokens.jsonl changes for exactly those tokens, the other
         JSONL files not at all, and the build's --check passes;
       - a second apply (another day) changes nothing, reviewed_on included;
       - `render` then shows the answers, and applying the rendered sheet is
         also a no-op; `status` counts answered and open;
       - lemma_spine_test.py and hymn_corpus_test.py still pass on the copy.
    3. Ambiguous answers stop the run before anything is written, naming the
       row: a bare string on a parsing flag, "ok?", a key Whitaker does not
       have. `render` refuses to overwrite answers not yet applied.
    3b. The printed hymns (Lauda Sion, Sacris solemniis, Verbum supernum):
       the cut sheet -- ok, draft->, a re-cut with its note; the re-cut
       clauses get fresh uids that supersede the old ones and nothing else
       moves; a second apply is a no-op; bad spans, a new join with no
       reason, and a second re-cut stop the run. Then their lemma sheet: a
       bare Whitaker key, a lemma WORDS lacks; `as row N` onto the wrong
       word and `keep` (there is no draft) stop the run.
    3c. The Adoro te collation sheet: ok, britt with a note, draft->; the
       answers file gets exactly those rows, the four JSONL files do not move
       (only the manifest's collation counts), a comment stops the run, and
       `ok` on every row makes the source verified, dated by the answers.
    3d. The printed hymns' gloss override layer: a draft row replaces one
       dictionary gloss (kept under `was`), nothing else moves, the manifest
       declares the layer, the reader badges the column; a row whose surface
       does not match stops the build.
    4. The John 1 sheet (when the NT inputs are fetched): ✓, a replacement
       gloss, explicit gloss + plain_form, `draft→ value` (still a draft),
       draft→ alone, an accepted plain line and a new prose_order; the same
       checks, and nt_corpus_test.py still passes; then its own ambiguities
       (a bare gloss on a row with a plain_form, an English plain line, an
       order missing positions).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
import build_nt_corpus as B  # noqa: E402
import build_hymn_corpus as H  # noqa: E402

PASS, FAIL = 0, []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)[:400]) if detail != "" and not cond else ""))


def copy_repo():
    tmp = tempfile.mkdtemp(prefix="review-test-")
    skip = shutil.ignore_patterns("__pycache__", "*.tmp", "lemmas.jsonl", "corpus", "markdown", "*.json.bak")
    for d in ("pipeline", "tests", os.path.join("docs", "review"), "data"):
        shutil.copytree(os.path.join(REPO, d), os.path.join(tmp, d), ignore=skip,
                        ignore_dangling_symlinks=True)
    for f in os.listdir(os.path.join(tmp, "data", "books")) if os.path.isdir(os.path.join(tmp, "data", "books")) else []:
        if f != "manifest.json":
            os.remove(os.path.join(tmp, "data", "books", f))
    shutil.copy(os.path.join(REPO, ".gitignore"), tmp)     # lemma_spine_test reads it
    nt_inputs = all(os.path.isdir(c) for c in B.CACHE.values())
    for c in B.CACHE.values():
        if os.path.isdir(c):
            shutil.copytree(c, os.path.join(tmp, os.path.relpath(c, REPO)))
    return tmp, nt_inputs


def run(root, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return p.returncode, p.stdout + p.stderr


def review(root, *args):
    return run(root, os.path.join("pipeline", "review.py"), *args)


def raw(path):
    with open(path, "rb") as f:
        return f.read()


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def by(path, key):
    return {r[key]: r for r in jsonl(path)}


def snapshot(d):
    """{path relative to d: bytes}, every file under d (data/nt/ is sharded by book)."""
    out = {}
    for base, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(base, f)
            out[os.path.relpath(p, d).replace(os.sep, "/")] = raw(p)
    return dict(sorted(out.items()))


def changed_rows(before, after, key):
    """Keys whose row differs between two JSONL blobs."""
    a = {r[key]: r for r in (json.loads(x) for x in before.decode("utf-8").splitlines() if x)}
    b = {r[key]: r for r in (json.loads(x) for x in after.decode("utf-8").splitlines() if x)}
    return {k for k in set(a) | set(b) if a.get(k) != b.get(k)}


def fill_lemma(path, answers):
    """answers: {row number: text} into the Adam: column."""
    out = []
    for line in open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n"):
        m = re.match(r"\| (\d+) \|", line)
        if m and int(m.group(1)) in answers:
            line = line[:line.rstrip().rstrip("|").rstrip().rfind("|") + 1] + f" {answers[int(m.group(1))]} |"
        out.append(line)
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))


def fill_nt(path, answers):
    """answers: {(uid, position): text, (uid, "plain"): text}."""
    out, uid = [], None
    for line in open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n"):
        m = re.match(r"`kjv:[^`]+` · `(wh-[0-9A-Z]+)`", line)
        if m:
            uid = m.group(1)
        if line.startswith("**Adam (plain line):**") and (uid, "plain") in answers:
            line = "**Adam (plain line):** " + answers[(uid, "plain")]
        m = re.match(r"\| (\d+) \|", line)
        if uid and m and (uid, int(m.group(1))) in answers:
            line = line[:line.rstrip().rstrip("|").rstrip().rfind("|") + 1] + f" {answers[(uid, int(m.group(1)))]} |"
        out.append(line)
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))


def adam_cells(path):
    cells = {}
    for line in open(path, encoding="utf-8").read().split("\n"):
        m = re.match(r"\| (\d+) \|", line)
        if m:
            cells[int(m.group(1))] = line.rstrip().rstrip("|").rsplit("|", 1)[1].strip()
    return cells


tmp, nt_inputs = copy_repo()
try:
    REV = os.path.join(tmp, "docs", "review")
    LEMMA = os.path.join(REV, "2026-09-26-lemma-flags.md")
    JOHN = os.path.join(REV, "2026-09-26-john1-drafts.md")
    OVR = os.path.join(tmp, "data", "lemmas", "adam-reviewed.jsonl")
    HYD = os.path.join(tmp, "data", "hymns")
    NTD = os.path.join(tmp, "data", "nt")
    try:
        H.find_source()
        latin = True
    except SystemExit:
        latin = False

    print("--- render")
    rc, out = review(tmp, "render", "--check")
    check("render --check: all five sheets are byte-identical to what the data renders",
          rc == 0 and out.count("byte-identical") == 5, out)
    rc, out = review(tmp, "status")
    check("status: every row open before any answer",
          "24 rows, 0 answered" in out and "24 open" in out and "155 rows, 0 answered" in out
          and "198 rows, 0 answered" in out and "25 rows, 0 answered" in out, out)

    if not latin:
        print("skip  the Latin shelf is not reachable (WORDHOARD_LATIN_DIR); the lemma apply did not run")
    else:
        print("\n--- the lemma sheet: apply")
        SUI = "-, sui  PRON"
        fill_lemma(LEMMA, {1: "ok", 2: "✓", 3: "draft→", 5: "keep",
                           9: "lemma: pellicānus, -ī m.; parsing: voc sg; note: WORDS has no pelican",
                           14: "`mundus, mundi N (2nd) M`", 18: "as row 1"})
        before, ov_before = snapshot(HYD), raw(OVR)
        rc, out = review(tmp, "apply", LEMMA, "--today", "2026-09-27")
        check("apply runs, rebuilds, and the hymn build's --check passes",
              rc == 0 and "CHECK PASSED" in out, out)
        rows = by(OVR, "address")
        want = {"wh-54JF0Y5SAS/la.1.t02", "wh-54JF0Y5SAS/la.1.t06", "wh-0861J9FP9P/la.1.t05",
                "wh-DZFZPFNWFA/la.1.t02", "wh-G1VG74Z7Q5/la.1.t10", "wh-6BK80FRWKN/la.1.t17"}
        check("exactly the six answered rows are written (not the draft→ row, not the 17 unanswered)",
              set(rows) == want, sorted(rows))
        check("... each adam-reviewed on --today", all(r["reviewed_on"] == "2026-09-27" for r in rows.values()))
        check("ok writes the recommendation (row 1: keep sē, join to -, sui)",
              rows["wh-54JF0Y5SAS/la.1.t02"] == {"address": "wh-54JF0Y5SAS/la.1.t02", "surface": "se",
                                                 "lemma": "sē", "lemma_key": SUI, "reviewed_on": "2026-09-27"})
        check("✓ is ok, the recommendation's note included (row 2)",
              rows["wh-54JF0Y5SAS/la.1.t06"].get("note") == "house spelling; WORDS spells with j")
        check("keep writes the draft value for what was flagged (row 5: parsing adv)",
              {k: v for k, v in rows["wh-0861J9FP9P/la.1.t05"].items() if k != "reviewed_on"}
              == {"address": "wh-0861J9FP9P/la.1.t05", "surface": "et", "parsing": "adv"})
        check("explicit fields are taken as written (row 9)",
              rows["wh-DZFZPFNWFA/la.1.t02"]["lemma"] == "pellicānus, -ī m."
              and rows["wh-DZFZPFNWFA/la.1.t02"]["parsing"] == "voc sg"
              and rows["wh-DZFZPFNWFA/la.1.t02"]["note"] == "WORDS has no pelican")
        check("a bare Whitaker key, its double space lost in markdown, is matched to the real key (row 14)",
              rows["wh-G1VG74Z7Q5/la.1.t10"].get("lemma_key") == "mundus, mundi  N (2nd) M"
              and "lemma" not in rows["wh-G1VG74Z7Q5/la.1.t10"])
        check("`as row 1` copies row 1's answer (row 18)",
              rows["wh-6BK80FRWKN/la.1.t17"]["lemma_key"] == SUI and rows["wh-6BK80FRWKN/la.1.t17"]["lemma"] == "sē")
        after = snapshot(HYD)
        check("tokens.jsonl changes for exactly the answered tokens",
              changed_rows(before["tokens.jsonl"], after["tokens.jsonl"], "address") == want,
              changed_rows(before["tokens.jsonl"], after["tokens.jsonl"], "address") ^ want)
        check("passages, witnesses and alignments are untouched",
              all(before[f] == after[f] for f in ("passages.jsonl", "witnesses.jsonl", "alignments.jsonl")))
        toks = by(os.path.join(HYD, "tokens.jsonl"), "address")
        t = toks["wh-G1VG74Z7Q5/la.1.t10"]
        check("an answered token carries it: lemma_key set, provenance adam-reviewed with the date, flag cleared",
              t["lemma_key"] == "mundus, mundi  N (2nd) M" and t["review"] is None
              and t["provenance"]["lemma"]["source"] == "adam-reviewed"
              and t["provenance"]["lemma"]["reviewed_on"] == "2026-09-27"
              and t["provenance"]["lemma"]["was"]["status"] == "ambiguous")
        check("the draft→ row is still flagged, as it was",
              toks["wh-Q7RW8M6N3G/la.1.t05"]["review"] and toks["wh-Q7RW8M6N3G/la.1.t05"]["provenance"]["lemma"]["source"] != "adam-reviewed")
        man = json.load(open(os.path.join(HYD, "manifest.json"), encoding="utf-8"))
        check("the hymn manifest now declares adam-reviewed and checksums the file",
              "adam-reviewed" in man["sources"] and "adam-reviewed.jsonl" in man["inputs_sha256"])

        print("\n--- the lemma sheet: idempotent")
        ov1, hy1 = raw(OVR), snapshot(HYD)
        rc, out = review(tmp, "apply", LEMMA, "--today", "2026-09-28")
        check("a second apply, another day, writes nothing and still passes --check",
              rc == 0 and "0 to write" in out and "wrote" not in out and "CHECK PASSED" in out, out)
        check("... the override file and the hymn JSONL are byte-identical, reviewed_on kept",
              raw(OVR) == ov1 and snapshot(HYD) == hy1)
        rc, out = review(tmp, "status", LEMMA)
        check("status: 7 answered (6 applied, 1 kept as a draft), 17 open",
              "24 rows, 7 answered (6 applied, 0 to apply, 1 kept as drafts, 0 ambiguous), 17 open" in out, out)
        rc, out = review(tmp, "render", LEMMA)
        cells = adam_cells(LEMMA)
        check("render shows what is applied: ok, keep, the fields; the draft→ row open again",
              rc == 0 and cells[1] == "ok" and cells[2] == "ok" and cells[5] == "keep" and cells[18] == "ok"
              and cells[14] == "ok"   # the bare key was row 14's recommendation
              and cells[9] == "lemma: pellicānus, -ī m.; parsing: voc sg; note: WORDS has no pelican"
              and cells[3] == "" and cells[4] == "", {k: cells[k] for k in (1, 2, 3, 5, 9, 14, 18)})
        rc, out = review(tmp, "apply", LEMMA, "--today", "2026-09-29", "--no-build")
        check("applying the rendered sheet is a no-op too", rc == 0 and "0 to write" in out and raw(OVR) == ov1, out)
        rc, out = review(tmp, "render", "--check", LEMMA)
        check("render --check: byte-identical again", rc == 0 and "byte-identical" in out, out)
        for test in ("lemma_spine_test.py", "hymn_corpus_test.py"):
            rc, out = run(tmp, os.path.join("tests", test))
            check(f"{test} still passes with Adam's answers applied", rc == 0, out.strip().splitlines()[-1:])

        print("\n--- the lemma sheet: ambiguous answers stop the run")
        for ans, row, why in (({12: "adv"}, "row 12", "parsing"), ({20: "ok?"}, "row 20", "comment"),
                              ({13: "lemma_key: nos  PRON"}, "row 13", "not one of Whitaker"),
                              ({22: "fides; lemma: fidēs"}, "row 22", "before the first")):
            shutil.copy(LEMMA, LEMMA + ".bak")
            fill_lemma(LEMMA, ans)
            rc, out = review(tmp, "apply", LEMMA, "--today", "2026-09-27")
            check(f"{list(ans.values())[0]!r} stops the run, naming {row} ({why}), writing nothing",
                  rc == 2 and "STOPPED" in out and row in out and why in out and raw(OVR) == ov1
                  and snapshot(HYD) == hy1, out)
            if row == "row 12":
                rc, out = review(tmp, "render", LEMMA)
                check("render refuses to overwrite an answer that is not applied yet",
                      rc != 0 and "not applied" in out and adam_cells(LEMMA)[12] == "adv", out)
            shutil.move(LEMMA + ".bak", LEMMA)

        print("\n--- the printed hymns: the cut sheet")
        CUTS = os.path.join(REV, "2026-09-26-thomas-cuts.md")
        TLEM = os.path.join(REV, "2026-09-26-thomas-lemma-flags.md")
        CUTF = os.path.join(tmp, "data", "hymn-sources", "cut-reviewed.jsonl")
        REG = os.path.join(tmp, "data", "uids", "wordhoard.uids.json")
        P = lambda: {p["citation"]: p for p in jsonl(os.path.join(HYD, "passages.jsonl"))}  # noqa: E731
        p0, reg0 = P(), json.load(open(REG, encoding="utf-8"))
        st10 = [p0[f"hymns:lauda-sion.st10.c{i}"]["uid"] for i in range(1, 6)]
        for ans, row, why in (({3: "cut: 1, 2-3, 4-5"}, "row 3", "covers 5 of 6"),
                              ({4: "cut: 1-3, 4-6"}, "row 4", "new join"),
                              ({5: "maybe join 2-3?"}, "row 5", "comment")):
            shutil.copy(CUTS, CUTS + ".bak")
            fill_lemma(CUTS, ans)
            rc, out = review(tmp, "apply", CUTS, "--today", "2026-09-27")
            check(f"cut sheet: {list(ans.values())[0]!r} stops the run, naming {row} ({why}), writing nothing",
                  rc == 2 and "STOPPED" in out and row in out and why in out and not os.path.exists(CUTF), out)
            shutil.move(CUTS + ".bak", CUTS)
        fill_lemma(CUTS, {1: "ok", 2: "draft→",
                          10: "cut: 1-4, 5, 6, 7-8; note: Quantum (l.4) answers Tantum (l.3)"})
        rc, out = review(tmp, "apply", CUTS, "--today", "2026-09-27")
        check("cut sheet: apply runs, rebuilds, and the build's --check passes",
              rc == 0 and "CHECK PASSED" in out, out)
        rows = by(CUTF, "stanza")
        check("cut sheet: exactly the two answered stanzas are written (not the draft→ one)",
              sorted(rows) == ["hymns:lauda-sion.st1", "hymns:lauda-sion.st10"], sorted(rows))
        check("cut sheet: ok writes the draft cut; a re-cut writes its spans and its note",
              rows["hymns:lauda-sion.st1"] == {"stanza": "hymns:lauda-sion.st1",
                                               "cut": [[1, 1], [2, 3], [4, 4], [5, 6]], "reviewed_on": "2026-09-27"}
              and rows["hymns:lauda-sion.st10"]["cut"] == [[1, 4], [5, 5], [6, 6], [7, 8]]
              and rows["hymns:lauda-sion.st10"]["note"].startswith("Quantum"))
        p1, reg1 = P(), json.load(open(REG, encoding="utf-8"))
        c = [p1.get(f"hymns:lauda-sion.st10.c{i}") for i in range(1, 6)]
        check("re-cut: st10 is now four clauses with the reviewed lines",
              [x["lines"] for x in c[:4]] == [[1, 4], [5, 5], [6, 6], [7, 8]] and c[4] is None)
        check("re-cut: every clause whose lines changed has a fresh uid that supersedes the old one",
              all(c[i]["uid"] != st10[i] and c[i]["cut"]["supersedes"] == st10[i]
                  and reg1["superseded"][st10[i]] == c[i]["uid"] for i in range(4)), [x["cut"] for x in c[:4]])
        check("re-cut: the old uids are never reused, and the dropped c5 keeps its citation's uid",
              reg1["uids"]["hymns:lauda-sion.st10.c5"] == st10[4] and not set(st10) & {x["uid"] for x in p1.values()})
        check("re-cut: the joined clause says why, from the note, and is adam-reviewed",
              c[0]["cut"]["why"] == "Adam's cut: Quantum (l.4) answers Tantum (l.3)"
              and c[0]["cut"]["review"] == "adam-reviewed" and c[0]["cut"]["reviewed_on"] == "2026-09-27")
        check("ok: st1's clauses keep their uids, now adam-reviewed",
              all(p1[k]["uid"] == p0[k]["uid"] and p1[k]["cut"]["review"] == "adam-reviewed"
                  for k in p0 if k.startswith("hymns:lauda-sion.st1.c")))
        check("nothing else moved: every other passage is byte-for-byte as it was",
              all(p1[k] == p0[k] for k in p0 if not k.startswith(("hymns:lauda-sion.st1.", "hymns:lauda-sion.st10"))))
        hy2 = snapshot(HYD)
        rc, out = review(tmp, "apply", CUTS, "--today", "2026-09-28")
        check("cut sheet: a second apply writes nothing, --check passes, the JSONL byte-identical",
              rc == 0 and "0 to write" in out and "CHECK PASSED" in out and snapshot(HYD) == hy2, out)
        rc, out = review(tmp, "render", CUTS)
        cells = adam_cells(CUTS)
        check("cut sheet: render shows ok, the re-cut, and the draft→ row open again",
              rc == 0 and cells[1] == "ok" and cells[2] == ""
              and cells[10] == "cut: 1-4, 5, 6, 7-8; note: Quantum (l.4) answers Tantum (l.3)", cells.get(10))
        shutil.copy(CUTS, CUTS + ".bak")
        fill_lemma(CUTS, {10: "cut: 1-3, 4-8; note: again"})
        rc, out = review(tmp, "apply", CUTS, "--today", "2026-09-29")
        check("cut sheet: a second, different re-cut of the same stanza stops the run",
              rc == 2 and "row 10" in out and "re-cut once already" in out, out)
        shutil.move(CUTS + ".bak", CUTS)

        print("\n--- the printed hymns: the lemma sheet")
        rc, out = review(tmp, "render", "--force", TLEM)     # the re-cut re-addressed st10's tokens
        ov_before = {r["address"] for r in jsonl(OVR)}
        fill_lemma(TLEM, {1: "lemma: Sion; note: proper name, indeclinable",
                          2: "`canticum, cantici N (2nd) N`", 4: "draft→"})
        rc, out = review(tmp, "apply", TLEM, "--today", "2026-09-27")
        check("thomas lemma sheet: apply runs, rebuilds, and the build's --check passes",
              rc == 0 and "CHECK PASSED" in out, out)
        rows = {r["address"]: r for r in jsonl(OVR) if r["address"] not in ov_before}
        toks = {t["address"]: t for t in jsonl(os.path.join(HYD, "tokens.jsonl"))}
        sion = next(a for a, r in rows.items() if r["surface"] == "Sion")
        cant = next(a for a, r in rows.items() if r["surface"] == "canticis")
        check("thomas lemma sheet: exactly the two answered rows are written, beside the other sheet's",
              len(rows) == 2 and ov_before <= {r["address"] for r in jsonl(OVR)})
        check("a bare Whitaker key (double space lost) becomes lemma_key, its lemma Whitaker's",
              rows[cant]["lemma_key"] == "canticum, cantici  N (2nd) N"
              and toks[cant]["lemma"] == "canticum, cantici" and toks[cant]["review"] is None
              and toks[cant]["provenance"]["lemma"]["source"] == "adam-reviewed")
        check("a lemma for a word WORDS lacks is taken as written",
              toks[sion]["lemma"] == "Sion" and toks[sion]["lemma_key"] is None and toks[sion]["review"] is None)
        for ans, row, why in (({3: "as row 2"}, "row 3", "not one of Whitaker"),
                              ({5: "keep"}, "row 5", "no draft value")):
            shutil.copy(TLEM, TLEM + ".bak")
            fill_lemma(TLEM, ans)
            rc, out = review(tmp, "apply", TLEM, "--today", "2026-09-27")
            check(f"thomas lemma sheet: {list(ans.values())[0]!r} stops the run, naming {row} ({why})",
                  rc == 2 and row in out and why in out, out)
            shutil.move(TLEM + ".bak", TLEM)
        for test in ("lemma_spine_test.py", "hymn_corpus_test.py"):
            rc, out = run(tmp, os.path.join("tests", test))
            check(f"{test} still passes with the cut and lemma answers applied", rc == 0,
                  out.strip().splitlines()[-1:])

        print("\n--- the Adoro te collation sheet")
        COLL = os.path.join(REV, "2026-09-26-adoro-collation.md")
        COLF = os.path.join(tmp, "data", "hymn-sources", "collation-reviewed.jsonl")
        MAN = os.path.join(HYD, "manifest.json")
        rms = lambda: json.load(open(MAN, encoding="utf-8"))["sources"]["roman-missal-received"]  # noqa: E731
        shutil.copy(COLL, COLL + ".bak")
        fill_lemma(COLL, {3: "maybe?"})
        rc, out = review(tmp, "apply", COLL, "--today", "2026-09-27")
        check("collation sheet: 'maybe?' stops the run, naming row 3, writing nothing",
              rc == 2 and "row 3" in out and not os.path.exists(COLF), out)
        shutil.move(COLL + ".bak", COLL)
        jl = {f: raw(os.path.join(HYD, f)) for f in os.listdir(HYD) if f.endswith(".jsonl")}
        fill_lemma(COLL, {8: "ok", 25: "britt; note: no Amen, as Britt", 1: "draft→"})
        rc, out = review(tmp, "apply", COLL, "--today", "2026-09-27")
        check("collation sheet: apply runs, rebuilds, and the build's --check passes",
              rc == 0 and "CHECK PASSED" in out, out)
        rows = jsonl(COLF)
        check("collation sheet: exactly the two answered rows are written, in sheet order",
              [(r["id"].rsplit(":", 1)[1], r["reading"], r["reviewed_on"]) for r in rows]
              == [("spelling", "received", "2026-09-27"), ("word", "britt", "2026-09-27")]
              and rows[1]["note"] == "no Amen, as Britt", rows)
        check("collation sheet: the four JSONL files are byte-identical (the text is never edited)",
              all(raw(os.path.join(HYD, f)) == b for f, b in jl.items()))
        rv = rms()["collation"]["hymns:adoro-te"]["review"]
        check("collation sheet: the manifest counts 2 answered (1 received, 1 britt), 23 open, not verified",
              (rv["answered"], rv["received"], rv["britt"], rv["open"]) == (2, 1, 1, 23)
              and rms()["verified"] is False, rv)
        rc, out = review(tmp, "render", COLL)
        cells = adam_cells(COLL)
        check("collation sheet: render shows the answers and the draft→ row open again",
              cells[8] == "received" and cells[25] == "britt; note: no Amen, as Britt" and cells[1] == "", cells)
        fill_lemma(COLL, {n: "ok" for n in range(1, 26) if n != 25})
        fill_lemma(COLL, {25: "ok"})
        rc, out = review(tmp, "apply", COLL, "--today", "2026-09-28")
        rec = rms()
        check("collation sheet: ok on every row makes the source verified, dated by the latest answer",
              rc == 0 and rec["verified"] is True and rec["verified_on"] == "2026-09-28"
              and rec["collation"]["hymns:adoro-te"]["review"]["open"] == 0, (out, rec.get("verified")))
        rc, out = run(tmp, os.path.join("tests", "hymn_corpus_test.py"))
        check("hymn_corpus_test.py still passes with the collation answered", rc == 0,
              out.strip().splitlines()[-1:])

        print("\n--- the printed hymns' gloss override layer (no sheet yet: a row by hand)")
        GOV = os.path.join(HYD, "gloss-overrides.jsonl")
        T = lambda: {t["address"]: t for t in jsonl(os.path.join(HYD, "tokens.jsonl"))}  # noqa: E731
        t0 = T()
        lauda = next(a for a, t in t0.items() if t["surface"] == "Lauda" and t["gloss"])
        open(GOV, "w", encoding="utf-8", newline="\n").write(json.dumps(
            {"address": lauda, "surface": "Lauda", "gloss": "praise", "layer": "house", "draft": True,
             "drafted_on": "2026-09-27", "note": "the sense in a hymn"}) + "\n")
        rc, out = run(tmp, os.path.join("pipeline", "build_hymn_corpus.py"))
        t1 = T()
        man = json.load(open(os.path.join(HYD, "manifest.json"), encoding="utf-8"))
        check("a gloss override row replaces that token's dictionary gloss, the dictionary one kept under was",
              rc == 0 and t1[lauda]["gloss"] == "praise" and t1[lauda]["provenance"]["gloss"]["draft"] is True
              and t1[lauda]["provenance"]["gloss"]["was"]["value"] == t0[lauda]["gloss"], out[-300:])
        check("... nothing else moves, and the manifest declares the layer and counts the row",
              all(t1[a] == t0[a] for a in t0 if a != lauda) and "house" in man["sources"]
              and man["gloss"]["overrides"] == dict(man["gloss"]["overrides"], applied=1, draft=1)
              and "gloss-overrides.jsonl" in man["inputs_sha256"])
        rc, out = run(tmp, os.path.join("pipeline", "render_reader.py"), "--out", os.path.join(tmp, "r.html"))
        page_t = open(os.path.join(tmp, "r.html"), encoding="utf-8").read() if rc == 0 else ""
        check("... and the reader badges that clause's wooden column as a draft",
              rc == 0 and page_t[page_t.index(f'id="{lauda.split("/")[0]}"'):].split('col col-plain')[0]
              .count('class="draft-badge"') == 1, out[-300:])
        open(GOV, "w", encoding="utf-8", newline="\n").write(json.dumps(
            {"address": lauda, "surface": "Laudo", "gloss": "praise", "layer": "house",
             "reviewed_on": "2026-09-27"}) + "\n")
        rc, out = run(tmp, os.path.join("pipeline", "build_hymn_corpus.py"), "--check")
        check("a gloss override whose surface does not match stops the build", rc != 0 and "gloss overrides" in out,
              out[-300:])
        open(GOV, "w", encoding="utf-8", newline="\n").write("")

    if not nt_inputs:
        print("\nskip  the NT's pinned inputs are not fetched (build_nt_corpus.py --fetch); the John 1 apply did not run")
    else:
        print("\n--- the John 1 sheet: apply")
        V1, V2, V3, V5 = "wh-AGJ6YAF47Q", "wh-N7Z29E6SEG", "wh-1AR8W4B50X", "wh-85ADTVKTWW"
        V9, V10, V14 = "wh-4FCS8SH6DF", "wh-H3QSAJKTMQ", "wh-C3YWSV9ZB6"
        a = lambda u, n: f"{u}/grc.byz.t{n:02d}"  # noqa: E731
        new_order = [1, "the", 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17]
        fill_nt(JOHN, {(V1, 2): "✓", (V1, 10): "toward", (V5, 13): "gloss: overcame; plain_form: did-not-overcome",
                       (V14, 7): "draft→ tented", (V9, 10): "draft→", (V2, "plain"): "ok",
                       (V1, "plain"): f"`{json.dumps(new_order, ensure_ascii=False)}` · `absorbed` [11]"})
        nt_before = snapshot(NTD)
        rc, out = review(tmp, "apply", JOHN, "--today", "2026-09-27")
        check("apply runs, rebuilds, and the NT build's --check passes", rc == 0 and "CHECK PASSED" in out, out)
        ov = by(os.path.join(NTD, "gloss-overrides.jsonl"), "address")
        po = by(os.path.join(NTD, "prose-order.jsonl"), "passage_uid")
        nt_after = snapshot(NTD)
        want = {a(V1, 2), a(V1, 10), a(V5, 13), a(V14, 7)}
        check("gloss-overrides.jsonl: exactly the four written rows change, in place, 137 rows still",
              changed_rows(nt_before["gloss-overrides.jsonl"], nt_after["gloss-overrides.jsonl"], "address") == want
              and len(ov) == 137 and list(ov) == [json.loads(x)["address"] for x in
                                                  nt_before["gloss-overrides.jsonl"].decode().splitlines()])
        check("✓ accepts the draft: layer adam-reviewed, reviewed_on, no draft, the gloss and the note kept",
              ov[a(V1, 2)]["layer"] == "adam-reviewed" and ov[a(V1, 2)]["reviewed_on"] == "2026-09-27"
              and "draft" not in ov[a(V1, 2)] and "drafted_on" not in ov[a(V1, 2)]
              and ov[a(V1, 2)]["gloss"] == "beginning" and ov[a(V1, 2)]["note"])
        check("a string replaces the gloss, now Adam's", ov[a(V1, 10)]["gloss"] == "toward"
              and ov[a(V1, 10)]["layer"] == "adam-reviewed")
        check("explicit gloss + plain_form", ov[a(V5, 13)]["gloss"] == "overcame"
              and ov[a(V5, 13)]["plain_form"] == "did-not-overcome")
        check("draft→ value revises the draft and keeps it a draft (layer house, drafted_on --today)",
              ov[a(V14, 7)]["gloss"] == "tented" and ov[a(V14, 7)]["draft"] is True
              and ov[a(V14, 7)]["layer"] == "house" and ov[a(V14, 7)]["drafted_on"] == "2026-09-27")
        check("draft→ alone leaves the row exactly as it was", ov[a(V9, 10)]["draft"] is True
              and ov[a(V9, 10)]["drafted_on"] == "2026-09-26")
        check("prose-order.jsonl: the accepted line is adam-reviewed, the new order is taken, nothing else moves",
              po[V2]["source"] == "adam-reviewed" and po[V2]["reviewed_on"] == "2026-09-27" and "draft" not in po[V2]
              and po[V1]["prose_order"] == new_order and po[V1]["absorbed"] == [11]
              and po[V1]["source"] == "adam-reviewed"
              and changed_rows(nt_before["prose-order.jsonl"], nt_after["prose-order.jsonl"], "passage_uid") == {V1, V2})
        check("tokens.jsonl changes for exactly the four tokens",
              changed_rows(nt_before["John/tokens.jsonl"], nt_after["John/tokens.jsonl"], "address") == want)
        check("witnesses.jsonl changes for exactly the two en.plain witnesses",
              changed_rows(nt_before["John/witnesses.jsonl"], nt_after["John/witnesses.jsonl"], "address")
              == {f"{V1}/en.plain", f"{V2}/en.plain"})
        check("passages and alignments are untouched",
              all(nt_before[f] == nt_after[f] for f in nt_before
                  if f.endswith(("passages.jsonl", "alignments.jsonl"))))
        man = json.load(open(os.path.join(NTD, "manifest.json"), encoding="utf-8"))
        check("the NT manifest declares adam-reviewed (licence own) and counts the drafts left",
              man["sources"]["adam-reviewed"]["license"] == "own" and man["drafts"]["gloss_override_rows"] == 134
              and man["drafts"]["prose_orders"] == 16)

        print("\n--- the John 1 sheet: idempotent")
        nt1 = snapshot(NTD)
        rc, out = review(tmp, "apply", JOHN, "--today", "2026-09-28")
        check("a second apply writes nothing, --check passes, the NT JSONL byte-identical",
              rc == 0 and "0 to write" in out and "CHECK PASSED" in out and snapshot(NTD) == nt1, out)
        rc, out = review(tmp, "status", JOHN)
        check("status: 7 answered (6 applied, 1 kept as a draft), 148 open",
              "155 rows, 7 answered (6 applied, 0 to apply, 1 kept as drafts, 0 ambiguous), 148 open" in out
              and "glosses 3/137 reviewed, plain lines 2/18" in out, out)
        rc, out = review(tmp, "render", JOHN)
        text = open(JOHN, encoding="utf-8").read()
        check("render: the header counts the reviewed rows, a reviewed row shows ✓, the revised draft shows open",
              rc == 0 and "137 rows: 134 `draft: true` (layer `house`), 3 reviewed" in text
              and "| 2 | ἀρχῇ | commencement | beginning |  | " in text and "| 7 | ἐσκήνωσεν | dwell | tented |" in text
              and re.search(r"\| 7 \| ἐσκήνωσεν .*\|  \|$", text, re.M), out)
        rc, out = review(tmp, "apply", JOHN, "--today", "2026-09-29", "--no-build")
        check("applying the rendered sheet is a no-op", rc == 0 and "0 to write" in out and snapshot(NTD) == nt1, out)
        rc, out = run(tmp, os.path.join("tests", "nt_corpus_test.py"))
        check("nt_corpus_test.py still passes with Adam's answers applied", rc == 0, out.strip().splitlines()[-3:])

        print("\n--- the John 1 sheet: ambiguous answers stop the run")
        for ans, where, why in (({(V10, 16): "recognised"}, "John 1:10 #16", "plain_form too"),
                                ({(V3, "plain"): "All things came to be through him"}, "John 1:3 plain line",
                                 "prose_order"),
                                ({(V3, "plain"): "[1, 4, 2, 3, 5, 6, 7, 9, 10, 8, 11]"}, "John 1:3 plain line",
                                 "[12]"),
                                ({(V1, 3): "was or is"}, "John 1:1 #3", "comment")):
            shutil.copy(JOHN, JOHN + ".bak")
            fill_nt(JOHN, ans)
            rc, out = review(tmp, "apply", JOHN, "--today", "2026-09-27")
            check(f"{list(ans.values())[0]!r} stops the run, naming {where}, writing nothing",
                  rc == 2 and where in out and why in out and snapshot(NTD) == nt1, out)
            shutil.move(JOHN + ".bak", JOHN)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\nthe real sheets and override files were not touched:",
      "yes" if not subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", "data", "docs/review/*.md"],
                                  capture_output=True, text=True).stdout.strip() else "CHANGED")
print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
