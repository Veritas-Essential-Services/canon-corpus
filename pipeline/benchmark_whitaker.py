#!/usr/bin/env python3
"""
benchmark_whitaker.py -- how much of a real ecclesiastical Latin text the
WORDS port reads, and by what rule. The text is the Clementine Vulgate.

    python3 pipeline/benchmark_whitaker.py --fetch   # the pinned text (once)
    python3 pipeline/benchmark_whitaker.py           # measure; print + write JSON

    In:   data/corpus/benchmark/clementine/<commit[:12]>/*.lat   (GITIGNORED)
          the Whitaker files (build_lemma_spine.py --fetch)
    Out:  data/corpus/benchmark/results.json                    (GITIGNORED)
          The summary that is committed is written by hand from it:
          docs/review/<date>-benchmark.md (numbers, and unknown forms with
          counts; never running text).

SOURCE AND LICENCE
    The Clementine Vulgate Project's own source files (Michael Tweedale et
    al.), as mirrored at github.com/BibleGet-I-O/Clementine-Vulgate, pinned
    to a commit; the 73 books in src/iso-encoded, which are the project's
    own codepage-1252 files. (The mirror's src/utf8 copies were converted
    as Latin-1, so every oe ligature there is a C1 control character: not
    used.) The text is public domain. The
    project's words (vulsearch.sourceforge.net, Wayback 2022-11-21, sha256
    below): "The text has been released into the public domain." It
    requests, without licence, acknowledgment, error reports and that
    modifications be made clear. This script modifies nothing on disk; it
    strips the markup (\\ [ ] / and <speaker> labels) in memory to count words.

    The pin is one sha256 over the sorted list of (file name, file sha256):
    any file changed, added or missing is a hard stop.

WHAT IS MEASURED, for four states of the port (2026-09-26)
    A  plain   -- stem + ending, uniques, enclitics (the port that morning)
    B  rules   -- + SYNCOPE, SLURY, FIXES, TRICKS (the port by noon)
    C  +roman  -- + Roman numerals and the non-enclitic TACKONs
    D  +found  -- + what this benchmark sent back to the Ada for: stem keys
                  as makedict writes them (one-stem superlatives, comparatives
                  and ordinals: pessimus, interior, vicesimus) and the PACKONs
                  (quidam, quicumque, quisquam)
    A-C key stems by slot, as the port did before D. The -ve fold fix is in
    all four (it cannot be switched off; it touches very few forms).
    per distinct form and per running token:
      * unknown: no analysis at all; and "guess only": nothing but WORDS's
        two-words guess, which the lemma spine never takes;
      * resolved to one candidate lemma or to several (a candidate is a
        distinct dictionary form, two-words guesses left out);
      * needing a rule: every analysis reached by one (no plain reading),
        by the rule (`via`, its first step: kind, table/rule);
      * the commonest unknowns, and whether each is ever written lower-case
        in the text (if never, it is most likely a proper name).
"""

import argparse
import collections
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import whitaker as W  # noqa: E402
import whitaker_tricks as T  # noqa: E402

REPO_URL = "https://github.com/BibleGet-I-O/Clementine-Vulgate"
COMMIT = "d57e2cde0cceda0d073ea9efc1fee616bcfeb2c1"
RAW = "https://raw.githubusercontent.com/BibleGet-I-O/Clementine-Vulgate/" + COMMIT + "/src/iso-encoded/"
BOOKS = ("Gn Ex Lv Nm Dt Jos Jdc Rt 1Rg 2Rg 3Rg 4Rg 1Par 2Par Esr Neh Tob Jdt Est Job Ps Pr Ecl "
         "Ct Sap Sir Is Jr Lam Bar Ez Dn Os Joel Am Abd Jon Mch Nah Hab Soph Agg Zach Mal 1Mcc "
         "2Mcc Mt Mc Lc Jo Act Rom 1Cor 2Cor Gal Eph Phlp Col 1Thes 2Thes 1Tim 2Tim Tit Phlm "
         "Hbr Jac 1Ptr 2Ptr 1Jo 2Jo 3Jo Jud Apc").split()
# sha256 over "name<TAB>sha256\n" for the 73 files, sorted by name (measured 2026-09-26)
PIN = "8002776ae05d72fcec447dac1b890728423096ffd22970771cbb419b0536b990"
CACHE = os.path.join(ROOT, "data", "corpus", "benchmark", "clementine", COMMIT[:12])
RESULTS = os.path.join(ROOT, "data", "corpus", "benchmark", "results.json")
LICENCE = {
    "license": "public-domain",
    "statement": "The text has been released into the public domain.",
    "requests": ("acknowledge the source; report typographical errors to the project maintainer; "
                 "make clear any modifications (requests only, not a licence)"),
    "evidence": {"url": "http://web.archive.org/web/20221121145231/https://vulsearch.sourceforge.net/index.html",
                 "sha256": "3fb9ee615f898863ec08d4be3b46cc0334ddf2fce0970f49198197952951a368"},
    "attribution": "The Clementine Vulgate Project (vulsearch.sourceforge.net)",
}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def digest(cache=CACHE):
    lines = []
    for b in sorted(BOOKS):
        with open(os.path.join(cache, b + ".lat"), "rb") as f:
            lines.append(f"{b}.lat\t{sha256(f.read())}\n")
    return sha256("".join(lines).encode("ascii"))


def fetch(cache=CACHE):
    os.makedirs(cache, exist_ok=True)
    for b in BOOKS:
        p = os.path.join(cache, b + ".lat")
        if os.path.exists(p):
            continue
        print(f"  fetch {b}.lat")
        with urllib.request.urlopen(RAW + b + ".lat", timeout=120) as r:
            blob = r.read()
        with open(p + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(p + ".tmp", p)
    d = digest(cache)
    if PIN is not None and d != PIN:
        raise SystemExit(f"HARD STOP: Clementine text digest {d} != pinned {PIN}")
    print(f"  digest {d}")
    return d


# ---------------------------------------------------------------------------
# The text: one verse per line, `chapter:verse text`
# ---------------------------------------------------------------------------

REF = re.compile(r"^\s*\d+:\d+\s+")
SPEAKER = re.compile(r"<[^>]*>")
WORD = re.compile(r"[^\W\d_]+")


def tokens(cache=CACHE):
    for b in BOOKS:
        with open(os.path.join(cache, b + ".lat"), encoding="cp1252") as f:
            for line in f:
                line = SPEAKER.sub(" ", REF.sub("", line))
                for t in WORD.findall(line):
                    yield t


def raw_form(t):
    """The form as written, lower-cased, diacritics off, ligatures opened;
    j and v kept (Roman numerals are read from it)."""
    s = unicodedata.normalize("NFD", t)
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    return s.replace("æ", "ae").replace("œ", "oe")


# ---------------------------------------------------------------------------
# Measuring
# ---------------------------------------------------------------------------

def _kinds(a):
    return [v["kind"] for v in a.get("via") or []]


def label(step):
    bits = [step["kind"]]
    if step.get("table"):
        bits.append(step["table"])
    if step.get("rule") and step["kind"] not in ("TWO_WORDS",):
        bits.append(step["rule"])
    if step.get("fix"):
        bits.append("-" + step["fix"] if step["kind"] == "SUFFIX" else step["fix"] + "-")
    if step.get("tackon"):
        bits.append("-" + step["tackon"])
    return " / ".join(bits)


def analyses(Xs, state, form):
    """Xs: (stems keyed by slot, stems keyed as makedict writes them)."""
    X = Xs[state == "D"]
    X.use_tackons = X.use_roman = state in "CD"
    X.use_packons = state == "D"
    w = W.fold(form)
    if state == "A":
        res = T.parse_plain(X, w)
    else:
        res = T.parse_latin_word(X, w, raw=form)
    return [X._describe(a) for a in res]


def classify(A):
    """(status, n_candidates, rule labels) for one form's analyses."""
    if not A:
        return "unknown", 0, []
    real = [a for a in A if "TWO_WORDS" not in _kinds(a)]
    if not real:
        return "guess-only", 0, sorted({label(a["via"][0]) for a in A})
    cands = {a["key"] for a in real}
    needs = all(a.get("via") for a in real)
    labels = sorted({label(a["via"][0]) for a in real}) if needs else []
    return ("rule" if needs else "plain"), len(cands), labels


def measure(Xs, counts, lower_seen, state):
    t0 = time.time()
    tot_tok = sum(counts.values())
    out = {"forms": len(counts), "tokens": tot_tok}
    status_f, status_t = collections.Counter(), collections.Counter()
    cand_f, cand_t = collections.Counter(), collections.Counter()
    rule_f, rule_t = collections.Counter(), collections.Counter()
    kind_f, kind_t = collections.Counter(), collections.Counter()
    unknown = collections.Counter()
    per_form = {}
    for form, n in counts.items():
        st, nc, labels = classify(analyses(Xs, state, form))
        per_form[form] = (st, nc, labels)
        status_f[st] += 1
        status_t[st] += n
        if st in ("plain", "rule"):
            k = "one" if nc == 1 else "several"
            cand_f[k] += 1
            cand_t[k] += n
        for lab in labels:
            if st == "rule":
                rule_f[lab] += 1
                rule_t[lab] += n
        for kd in sorted({lab.split(" / ")[0] for lab in labels}) if st == "rule" else []:
            kind_f[kd] += 1
            kind_t[kd] += n
        if st in ("unknown", "guess-only"):
            unknown[form] = n
    out.update({
        "status_forms": dict(status_f), "status_tokens": dict(status_t),
        "candidates_forms": dict(cand_f), "candidates_tokens": dict(cand_t),
        "rule_kind_forms": dict(kind_f), "rule_kind_tokens": dict(kind_t),
        "rule_forms": dict(rule_f.most_common()), "rule_tokens": dict(rule_t.most_common()),
        "top_unknown": [{"form": f, "count": c, "ever_lower": f in lower_seen,
                         "status": per_form[f][0]} for f, c in unknown.most_common(200)],
        "seconds": round(time.time() - t0, 1),
    })
    return out, per_form


def pct(a, b):
    return f"{100.0 * a / b:.2f}%" if b else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--states", default="ABCD")
    args = ap.parse_args()
    if args.fetch:
        fetch()
    d = digest()
    if PIN is not None and d != PIN:
        raise SystemExit(f"HARD STOP: Clementine text digest {d} != pinned {PIN}")
    counts, lower_seen = collections.Counter(), set()
    for t in tokens():
        f = raw_form(t)
        counts[f] += 1
        if t[:1].islower():
            lower_seen.add(f)
    X = (W.Whitaker(stems_by_slot=True), W.Whitaker())
    res = {"source": {"repo": REPO_URL, "commit": COMMIT, "path": "src/iso-encoded/*.lat", "encoding": "cp1252", "books": len(BOOKS),
                      "digest_sha256": d, **LICENCE},
           "whitaker_commit": W.COMMIT, "states": {}}
    forms = {}
    for s in args.states:
        r, forms[s] = measure(X, counts, lower_seen, s)
        res["states"][s] = r
        F, N = r["forms"], r["tokens"]
        print(f"[{s}] {F} forms / {N} tokens in {r['seconds']} s")
        for st in ("plain", "rule", "guess-only", "unknown"):
            print(f"    {st:10} forms {r['status_forms'].get(st, 0):6} {pct(r['status_forms'].get(st, 0), F):>7}"
                  f"   tokens {r['status_tokens'].get(st, 0):7} {pct(r['status_tokens'].get(st, 0), N):>7}")
        for k in ("one", "several"):
            print(f"    cand {k:7} forms {r['candidates_forms'].get(k, 0):6}   tokens {r['candidates_tokens'].get(k, 0):7}")
        for k, v in sorted(r["rule_kind_forms"].items(), key=lambda kv: -kv[1]):
            print(f"    rule {k:10} forms {v:6}   tokens {r['rule_kind_tokens'][k]:7}")
    last = args.states[-1]
    if "A" in forms and last != "A":
        moved = collections.Counter((forms["A"][f][0], forms[last][f][0]) for f in counts)
        res[f"transitions_A_to_{last}"] = {f"{a}->{c}": n for (a, c), n in sorted(moved.items())}
        lost = [f for f in counts if forms["A"][f][0] == "plain" and forms[last][f][0] != "plain"]
        res["plain_lost"] = lost
        print(f"  A -> {last}", res[f"transitions_A_to_{last}"], "plain lost:", len(lost))
    if "C" in forms and "D" in forms:
        gained = collections.Counter()
        for f, n in counts.items():
            if forms["C"][f][0] in ("unknown", "guess-only") and forms["D"][f][0] in ("plain", "rule"):
                gained["forms"] += 1
                gained["tokens"] += n
        res["C_to_D_newly_read"] = dict(gained)
        print("  C -> D newly read", dict(gained))
    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS + ".tmp", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    os.replace(RESULTS + ".tmp", RESULTS)
    print(f"  wrote {RESULTS}")


if __name__ == "__main__":
    main()
