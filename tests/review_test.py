#!/usr/bin/env python3
"""
review_test.py -- pipeline/review.py, end to end, on a TEMP COPY of the repo.

Run:  python3 tests/review_test.py

The real sheets and override files are never written: everything below
happens in a copy (pipeline/, tests/, docs/review/, data/ without the big
gitignored files; the NT's pinned inputs when data/corpus/ holds them).

WHAT IT ASSERTS
    1. `render --check`: both sheets are byte-identical to what the data renders.
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
    return {f: raw(os.path.join(d, f)) for f in sorted(os.listdir(d))}


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
    check("render --check: both sheets are byte-identical to what the data renders",
          rc == 0 and out.count("byte-identical") == 2, out)
    rc, out = review(tmp, "status")
    check("status: every row open before any answer",
          "24 rows, 0 answered" in out and "24 open" in out and "155 rows, 0 answered" in out, out)

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
              changed_rows(nt_before["tokens.jsonl"], nt_after["tokens.jsonl"], "address") == want)
        check("witnesses.jsonl changes for exactly the two en.plain witnesses",
              changed_rows(nt_before["witnesses.jsonl"], nt_after["witnesses.jsonl"], "address")
              == {f"{V1}/en.plain", f"{V2}/en.plain"})
        check("passages and alignments are untouched",
              all(nt_before[f] == nt_after[f] for f in ("passages.jsonl", "alignments.jsonl")))
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
