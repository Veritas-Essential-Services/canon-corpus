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

WHAT IS MEASURED, for seven states of the port (2026-09-26)
    A  plain   -- stem + ending, uniques, enclitics (the port that morning)
    B  rules   -- + SYNCOPE, SLURY, FIXES, TRICKS (the port by noon)
    C  +roman  -- + Roman numerals and the non-enclitic TACKONs
    D  +found  -- + what this benchmark sent back to the Ada for: stem keys
                  as makedict writes them (one-stem superlatives, comparatives
                  and ordinals: pessimus, interior, vicesimus) and the PACKONs
                  (quidam, quicumque, quisquam)
    E  +caps   -- + WORDS's capitalisation rule (parse.adb Is_Capitalized):
                  no TRICKS on a word written capitalised, as a name
    F  +names  -- + the house proper-names table (proper_names.py), consulted
                  for a capitalised form
    G  +house  -- + the house supplement (data/lemmas/house-supplement.jsonl)
    A-C key stems by slot, as the port did before D. The -ve fold fix is in
    all of them (it cannot be switched off; it touches very few forms).
    From E on a form is read as it is written each time: a form written both
    ways is analysed twice, capitalised and not, and each token counts under
    its own spelling. A form's own status (the "forms" columns) is that of
    the spelling it is written in most (lower-case on a tie).
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


def cased_form(t):
    """raw_form with the case kept (Æ opens to Ae), for Is_Capitalized."""
    s = unicodedata.normalize("NFD", t)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.replace("Æ", "Ae").replace("æ", "ae").replace("Œ", "Oe").replace("œ", "oe")


def as_written(form, cap):
    """A spelling of `form` that is capitalised (Is_Capitalized) or not."""
    return form[:1].upper() + form[1:] if cap else form


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


def analyses(Xs, state, form, cap=False):
    """Xs: {"slot": stems keyed by slot, "D": stems keyed as makedict writes
    them, "house": the same with the house supplement, "names": the
    proper-names table}. `cap`: the form is written capitalised."""
    X = Xs["slot"] if state in "ABC" else Xs["house"] if state == "G" else Xs["D"]
    X.use_tackons = X.use_roman = state in "CDEFG"
    X.use_packons = state in "DEFG"
    X.use_caps = state in "EFG"
    X.names = Xs["names"] if state in "FG" else {}
    w = W.fold(form)
    if state == "A":
        res = T.parse_plain(X, w)
    else:
        res = T.parse_latin_word(X, w, raw=as_written(form, cap) if state in "EFG" else form)
    return [X._describe(a) for a in res]


def _house(a):
    return a.get("form_by") == "house-names" and "names" or a.get("house") and "house" or None


def classify(A):
    """(status, n_candidates, rule labels) for one form's analyses. A form
    read plainly only by the names table is "names", only by the house
    supplement "house"; by any WORDS entry, "plain"."""
    if not A:
        return "unknown", 0, []
    real = [a for a in A if "TWO_WORDS" not in _kinds(a)]
    if not real:
        return "guess-only", 0, sorted({label(a["via"][0]) for a in A})
    cands = {a["key"] for a in real}
    plain = [a for a in real if not a.get("via")]
    labels = [] if plain else sorted({label(a["via"][0]) for a in real})
    if not plain:
        return "rule", len(cands), labels
    by = {_house(a) for a in plain}
    return ("plain" if None in by else "names" if "names" in by else "house"), len(cands), labels


READ = ("plain", "rule", "names", "house")


def measure(Xs, counts, lower_seen, state, cased=None):
    """`cased`: {form: Counter({capitalised?: tokens})}; from state E on each
    spelling is analysed apart. Before E, one analysis per form."""
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
        if state in "EFG" and cased is not None:
            variants = sorted(cased[form].items(), key=lambda kv: (-kv[1], kv[0]))
        else:
            variants = [(False, n)]
        for vi, (cap, vn) in enumerate(variants):
            st, nc, labels = classify(analyses(Xs, state, form, cap))
            if vi == 0:                         # the form's own status: its commonest spelling
                per_form[form] = (st, nc, labels)
                status_f[st] += 1
                if st in READ:
                    cand_f["one" if nc == 1 else "several"] += 1
                if st == "rule":
                    for lab in labels:
                        rule_f[lab] += 1
                    for kd in sorted({lab.split(" / ")[0] for lab in labels}):
                        kind_f[kd] += 1
            status_t[st] += vn
            if st in READ:
                cand_t["one" if nc == 1 else "several"] += vn
            if st == "rule":
                for lab in labels:
                    rule_t[lab] += vn
                for kd in sorted({lab.split(" / ")[0] for lab in labels}):
                    kind_t[kd] += vn
            if st in ("unknown", "guess-only"):
                unknown[form] += vn
    out.update({
        "status_forms": dict(status_f), "status_tokens": dict(status_t),
        "candidates_forms": dict(cand_f), "candidates_tokens": dict(cand_t),
        "rule_kind_forms": dict(kind_f), "rule_kind_tokens": {k: kind_t[k] for k in kind_f},
        "rule_forms": dict(rule_f.most_common()), "rule_tokens": dict(rule_t.most_common()),
        "top_unknown": [{"form": f, "count": c, "ever_lower": f in lower_seen,
                         "status": per_form[f][0]} for f, c in unknown.most_common(200)],
        "seconds": round(time.time() - t0, 1),
    })
    return out, per_form


def check_attestation(rows, counts):
    """Every house row's `attested` counts are the Vulgate's, form for form
    (a wrong count is a hard stop: the justification rests on it)."""
    bad = [(r["id"], f, n, counts.get(f, 0)) for r in rows for f, n in r["attested"].items()
           if counts.get(f, 0) != n]
    if bad:
        raise SystemExit(f"HARD STOP: house-supplement attestation differs from the Vulgate: {bad}")
    return {"rows": len(rows), "forms": sum(len(r["attested"]) for r in rows), "checked": True}


def pct(a, b):
    return f"{100.0 * a / b:.2f}%" if b else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--states", default="ABCDEFG")
    args = ap.parse_args()
    if args.fetch:
        fetch()
    d = digest()
    if PIN is not None and d != PIN:
        raise SystemExit(f"HARD STOP: Clementine text digest {d} != pinned {PIN}")
    counts, lower_seen = collections.Counter(), set()
    cased = collections.defaultdict(collections.Counter)
    for t in tokens():
        f = raw_form(t)
        counts[f] += 1
        cased[f][T.is_capitalized(cased_form(t))] += 1
        if t[:1].islower():
            lower_seen.add(f)
    import proper_names
    X = {"slot": W.Whitaker(stems_by_slot=True), "D": W.Whitaker(),
         "house": W.Whitaker(house_supplement=True), "names": proper_names.load()}
    attested = check_attestation(X["house"].house_rows, counts)
    res = {"source": {"repo": REPO_URL, "commit": COMMIT, "path": "src/iso-encoded/*.lat", "encoding": "cp1252", "books": len(BOOKS),
                      "digest_sha256": d, **LICENCE},
           "whitaker_commit": W.COMMIT, "states": {}}
    forms = {}
    for s in args.states:
        r, forms[s] = measure(X, counts, lower_seen, s, cased)
        res["states"][s] = r
        F, N = r["forms"], r["tokens"]
        print(f"[{s}] {F} forms / {N} tokens in {r['seconds']} s")
        for st in ("plain", "names", "house", "rule", "guess-only", "unknown"):
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
    res["house_attestation"] = attested
    for a, b in (("D", "E"), ("E", "F"), ("F", "G"), ("D", "G")):
        if a in forms and b in forms:
            moved = collections.Counter((forms[a][f][0], forms[b][f][0]) for f in counts)
            tok = collections.Counter()
            for f, n in counts.items():
                tok[(forms[a][f][0], forms[b][f][0])] += n
            res[f"transitions_{a}_to_{b}"] = {f"{x}->{y}": [moved[(x, y)], tok[(x, y)]]
                                              for (x, y) in sorted(moved) if x != y}
            print(f"  {a} -> {b}", res[f"transitions_{a}_to_{b}"])
    if "E" in forms:
        never = [f for f in counts if f not in lower_seen]
        res["never_lower_rule_read"] = {
            s: {"forms": sum(1 for f in never if forms[s][f][0] == "rule"),
                "tokens": sum(counts[f] for f in never if forms[s][f][0] == "rule"),
                "by_kind": dict(collections.Counter(lab.split(" / ")[0] for f in never if forms[s][f][0] == "rule"
                                                    for lab in forms[s][f][2]))}
            for s in args.states if s in "DEFG"}
        print("  never lower-case, read only by a rule:", res["never_lower_rule_read"])
    if "F" in forms and "G" in forms:
        # the supplement must add nothing to a form a WORDS entry already reads
        gained = []
        for f in counts:
            if forms["F"][f][0] == "plain":
                if len(analyses(X, "G", f)) != len(analyses(X, "F", f)):
                    gained.append(f)
        res["house_touched_plain_forms"] = gained
        print("  plain forms the supplement added readings to:", gained)
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
