#!/usr/bin/env python3
"""
remint_maxims_test.py -- pipeline/remint_maxims.py, end to end, on a TEMP COPY.

Run:  python3 tests/remint_maxims_test.py

The real registry and maxims are never written: the script runs against copies
of data/maxims/ and data/uids/ in a temp directory.

WHAT IT ASSERTS
    1. The dry run (the default) writes nothing: registry, source and output
       byte-identical, no output file made; it says what it would mint.
    2. --write mints exactly one uid per maxim, under `maxims:<ref>`, and
       changes no other registry entry; the source file is untouched.
    3. Each record is a passage/maxim Hoard record: wh- uid from the registry,
       the old id and the ref in legacy[], the words, dates, status and
       visibility as filed; kept founders carry the ruled kept_basis and no
       invented kept_on; drafts carry none.
    4. A second --write mints nothing and writes the same bytes; --check
       passes, and fails on a hand-edited output or a missing uid.
    5. Unknown fields, malformed ids, missing refs and dangling supersedes stop
       the run before anything is written.
    6. When the house checkout is beside this repo (../wordhoard), every record
       passes the served library's own Hoard.validate, run in node.
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
SCRIPT = os.path.join(REPO, "pipeline", "remint_maxims.py")
HOARD = os.environ.get("CANON_HOARD_JS") or os.path.join(REPO, "..", "wordhoard", "packages", "core", "hoard", "hoard.js")

PASS, FAIL = 0, []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)[:400]) if detail != "" and not cond else ""))


def run(tmp, *args):
    p = subprocess.run([sys.executable, SCRIPT,
                        "--src", os.path.join(tmp, "maxims", "maxims-original.jsonl"),
                        "--manifest", os.path.join(tmp, "maxims", "maxims-original.manifest.json"),
                        "--out", os.path.join(tmp, "maxims", "maxims-original.hoard.jsonl"),
                        "--uids", os.path.join(tmp, "uids", "wordhoard.uids.json"), *args],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def read(p, mode="rb"):
    with open(p, mode) as f:
        return f.read()


def fresh():
    tmp = tempfile.mkdtemp(prefix="remint-")
    shutil.copytree(os.path.join(REPO, "data", "maxims"), os.path.join(tmp, "maxims"))
    shutil.copytree(os.path.join(REPO, "data", "uids"), os.path.join(tmp, "uids"))
    out = os.path.join(tmp, "maxims", "maxims-original.hoard.jsonl")
    if os.path.exists(out):
        os.remove(out)   # the test starts from before any real --write
    return tmp


def main():
    UID_RE = re.compile(r"^wh-[0-9A-HJKMNP-TV-Z]{10}$")
    src_rows = [json.loads(l) for l in read(os.path.join(REPO, "data", "maxims", "maxims-original.jsonl"), "r").splitlines() if l.strip()]
    tmp = fresh()
    try:
        P = lambda *x: os.path.join(tmp, *x)
        src, uids, out = P("maxims", "maxims-original.jsonl"), P("uids", "wordhoard.uids.json"), P("maxims", "maxims-original.hoard.jsonl")
        before_src, before_uids = read(src), read(uids)
        reg0 = json.loads(before_uids)["uids"]

        # 1. dry run
        code, log = run(tmp)
        check("dry run: exits 0", code == 0, log)
        check("dry run: the source is untouched", read(src) == before_src)
        check("dry run: the registry is untouched", read(uids) == before_uids)
        check("dry run: no output file", not os.path.exists(out))
        check("dry run: says what it would mint, and that nothing was written",
              "DRY RUN" in log and log.count("(would mint)") == len(src_rows) and "Nothing was written" in log, log)

        # 2. write
        code, log = run(tmp, "--write")
        check("write: exits 0", code == 0, log)
        check("write: the source is untouched", read(src) == before_src)
        reg1 = json.loads(read(uids))["uids"]
        added = {k: v for k, v in reg1.items() if k not in reg0}
        check("write: exactly one new registry entry per maxim, under maxims:<ref>",
              sorted(added) == sorted("maxims:" + r["ref"] for r in src_rows), sorted(added))
        check("write: no other registry entry changed", all(reg1[k] == v for k, v in reg0.items()) and len(reg1) == len(reg0) + len(src_rows))
        recs = [json.loads(l) for l in read(out, "r").splitlines() if l.strip()]
        check("write: one Hoard record per maxim", len(recs) == len(src_rows))

        # 3. the records
        by_old = {r["legacy"][0]["id"]: r for r in recs}
        for s in src_rows:
            r = by_old.get(s["uid"])
            tag = s["ref"]
            check(f"{tag}: the old id is kept in legacy[], never as the key", r is not None and r["uid"] != s["uid"]
                  and r["legacy"][0] == {"room": "canon-corpus", "id": s["uid"], "file": "data/maxims/maxims-original.jsonl"}
                  and {"room": "vault", "id": s["ref"]} in r["legacy"])
            if r is None:
                continue
            check(f"{tag}: a wh- uid, the registry's for maxims:{s['ref']}", UID_RE.match(r["uid"]) and reg1["maxims:" + s["ref"]] == r["uid"])
            check(f"{tag}: kind passage, type maxim, citation maxims:{s['ref']}", r["kind"] == "passage" and r["type"] == "maxim" and r["citation"] == "maxims:" + s["ref"])
            b = r["body"]
            check(f"{tag}: words, dates, taxonomy and ancestors as filed",
                  b["text"] == s["text"] and b["coined_on"] == s["coined_on"] and b["coined_precision"] == s["coined_precision"]
                  and b["note"] == s.get("note") and b["form"] == s.get("form") and b["scope"] == s.get("scope")
                  and b["subjects"] == s.get("subjects") and b["ancestors"] == s.get("ancestors"))
            check(f"{tag}: status, visibility, author and revision as filed",
                  r["status"] == s["status"] and r["scope"]["visibility"] == s["visibility"] and r["provenance"]["author"] == s["author"]
                  and r["provenance"]["origin"] == s["provenance"] and r["lineage"]["revision"] == s["revision"] and r["lineage"]["supersedes"] is None)
            check(f"{tag}: never shareable, own licence", r["rights"] == {"license": "own", "shareable": False, "redistribute_whole": False})
            if s["status"] == "kept":
                check(f"{tag}: kept on the ruled founding basis, with no invented kept_on",
                      b["kept_basis"].startswith("founding record") and b["kept_on"] is None)
            else:
                check(f"{tag}: a {s['status']} carries no kept_basis", b["kept_basis"] is None and b["kept_on"] is None)

        # 4. idempotent; --check
        first = read(out)
        code, log = run(tmp, "--write")
        check("rewrite: mints nothing", code == 0 and "0 to mint" in log and json.loads(read(uids))["uids"] == reg1, log)
        check("rewrite: the same bytes", read(out) == first)
        code, log = run(tmp, "--check")
        check("--check: passes on what --write made", code == 0 and log.startswith("ok"), log)
        text = read(out, "r")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text.replace('"status":"kept"', '"status":"retired"', 1))
        code, log = run(tmp, "--check")
        check("--check: fails on a hand-edited record", code == 1 and "does not match" in log, log)
        with open(out, "wb") as f:
            f.write(first.replace(b"\n", b"\r\n"))
        code, log = run(tmp, "--check")
        check("--check: a CRLF checkout of the same records still passes", code == 0, log)
        with open(uids, "wb") as f:
            f.write(before_uids)
        code, log = run(tmp, "--check")
        check("--check: fails when the registry has no uid yet (and mints nothing)", code == 1 and "run --write" in log and read(uids) == before_uids, log)

        # 5. nothing guessed
        def broken(mutate, label, needle):
            t2 = fresh()
            try:
                p = os.path.join(t2, "maxims", "maxims-original.jsonl")
                rows = [json.loads(l) for l in read(p, "r").splitlines() if l.strip()]
                mutate(rows)
                with open(p, "w", encoding="utf-8", newline="\n") as f:
                    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
                u0 = read(os.path.join(t2, "uids", "wordhoard.uids.json"))
                code, log = run(t2, "--write")
                check(f"stops: {label}", code != 0 and needle in log and read(os.path.join(t2, "uids", "wordhoard.uids.json")) == u0
                      and not os.path.exists(os.path.join(t2, "maxims", "maxims-original.hoard.jsonl")), log)
            finally:
                shutil.rmtree(t2, ignore_errors=True)
        broken(lambda rows: rows[0].__setitem__("mood", "wry"), "an unknown field", "unknown field")
        broken(lambda rows: rows[0].__setitem__("uid", "maxim-1"), "an id not of the form ak-maxim-NNNN", "not an ak-maxim-NNNN id")
        broken(lambda rows: rows[0].pop("ref"), "a record with no ref", "needs a ref")
        broken(lambda rows: rows[1].__setitem__("supersedes", "ak-maxim-0099"), "a supersedes that names nothing here", "not in this file")
        broken(lambda rows: rows[0].__setitem__("coined_on", "2026-09"), "a date that does not fit its precision", "does not fit precision")

        # 6. the served library agrees
        node = shutil.which("node")
        if node and os.path.exists(HOARD):
            js = ("const H=require(process.argv[1]);const fs=require('fs');"
                  "const rs=fs.readFileSync(process.argv[2],'utf8').split(/\\r?\\n/).filter(Boolean).map(JSON.parse);"
                  "const bad=rs.map(r=>[r.uid,H.validate(r)]).filter(x=>!x[1].ok).map(x=>x[0]+': '+x[1].errors.join('; '));"
                  "console.log(JSON.stringify({n:rs.length,bad}));")
            p = subprocess.run([node, "-e", js, os.path.abspath(HOARD), out], capture_output=True, text=True, encoding="utf-8")
            try:
                res = json.loads(p.stdout)
            except ValueError:
                res = {"n": 0, "bad": [p.stderr]}
            check("hoard.js: every record passes the served Hoard.validate", res["n"] == len(src_rows) and not res["bad"], res)
        else:
            print("skip hoard.js validation (no node, or no ../wordhoard checkout; set CANON_HOARD_JS)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{PASS} passed, {len(FAIL)} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
