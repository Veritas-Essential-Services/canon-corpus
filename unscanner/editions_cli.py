# prov: 2026-10-20 claude-opus-5-5 drafted
# fable_review: pending
"""python3 -m unscanner editions collate|merge — two or more scans of one book, made one text.

Built 2026-10-20 on Brewer's Character Sketches vol. 6 (Toronto 1892 and Cornell 1896 scans, each
read by tesseract and by the Archive's own engine). Adam: "Can you build all this into the
unscanner?" The method, in order (unscanner/README.md, "Several scans of one book"):

  collate   1. each scan through `unscanner run` first (OCR, layout, book.json);
            2. editions.collate: align every engine's words on the base scan, vote; a word the
               engines agree on is kept, a majority mends, the rest go to review;
            3. learned.decide: the rules learned from Adam's answers clear what they can (roman
               numerals, æ, small capitals, c/e, ll/U, stock abbreviations, ...);
            4. smallcaps.decide: a word that looks like small capitals, or a headword before its
               bracket, is cut from each scan and reread capitals-only;
            5. the Proof Desk page (proof_desk.html) for whatever is left, with every rule's answer
               shown and changeable.
  merge     every answer put in place (files ranked lowest first: rules, Claude's reads, Adam's
            picks), page furniture out, margin and column breaks rejoined (layout rules 6, 6b-6d),
            dashes set (rule 7) -> merged.json (paragraphs, with their pages) and merged.txt.
"""
import argparse
import json
import os
import re

from . import editions as E
from . import learned as LR
from . import smallcaps as SC

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def _pairs(vals):
    out = {}
    for v in vals or []:
        k, _, path = v.partition("=")
        out[k] = path
    return out


def word_test(lexicon):
    """A word of the book's language: the lexicon, or a lexicon word with a common ending."""
    def word(k):
        if len(k) < 3:
            return False
        if k in lexicon:
            return True
        for suf in ("s", "es", "d", "ed", "ing", "ly", "er", "est"):
            st = k[:-len(suf)]
            if k.endswith(suf) and len(st) >= 3 and (st in lexicon or st + "e" in lexicon):
                return True
        return False
    return word


def collate(a):
    scans = _pairs(a.scan)
    djvu = _pairs(a.djvu)
    base = a.base
    assert base in scans, f"--base {base} must be one of --scan's names"
    data = {}
    for name, d in scans.items():
        data[name] = {"tess": E.load_tesseract(d)}
        if name in djvu:
            data[name]["djvu"] = E.load_djvu(djvu[name])
        else:
            data[name]["djvu"] = {}
    lexicon = E.load_lexicon(REPO, a.brewer)
    result = E.collate(data, base, lexicon)
    os.makedirs(a.out, exist_ok=True)
    json.dump(result, open(os.path.join(a.out, "collation.json"), "w"), ensure_ascii=False)
    review = E.review_data(result, scans, a.volume)
    json.dump(review, open(os.path.join(a.out, "review.json"), "w"), ensure_ascii=False)
    recs = {f"v{a.volume}-p{r['page']}-i{r['index']}": r for r in result["review"] + result["mends"]}
    word = word_test(lexicon)
    cleared = {}
    for it in review["items"]:
        pick, rule = LR.decide(it, word, lexicon)
        if pick is None and it["id"] in recs:
            sc = SC.decide(recs[it["id"]], scans)
            if sc:
                pick, rule = sc, "smallcaps-reread"
        if pick is None:
            continue
        if it["kind"] == "spot":
            if pick.strip() == (it["result"] or "").strip():
                cleared[it["id"]] = [pick, "confirms-fix:" + rule]
        else:
            cleared[it["id"]] = [pick, rule]
    json.dump(cleared, open(os.path.join(a.out, "rule-clears.json"), "w"), ensure_ascii=False, indent=0)
    for it in review["items"]:
        if it["id"] in cleared:
            it["rule"] = {"pick": cleared[it["id"]][0], "name": cleared[it["id"]][1]}
    names = sorted({v[1] for v in cleared.values()})
    page = open(os.path.join(HERE, "proof_desk.html"), encoding="utf-8").read()
    payload = {"rules": {n: n for n in names}, "volumes": [review]}
    js = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    open(os.path.join(a.out, "proof-desk.html"), "w", encoding="utf-8").write(page.replace("__DATA__", js))
    left = sum(1 for it in review["items"] if it["id"] not in cleared)
    print(f"{result['stats'].get('words', 0)} words; {len(review['items'])} on the desk, "
          f"{len(cleared)} cleared by rule, {left} left -> {a.out}")


def _answers(path):
    """{id: text} from an answers file: {id: text}, {id: [text, rule]}, or {id: {"pick": text}}."""
    d = json.load(open(path, encoding="utf-8"))
    out = {}
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, list):
            v = v[0]
        elif isinstance(v, dict):
            v = v.get("pick")
        if v is not None:
            out[k] = v
    return out


def merge(a):
    result = json.load(open(a.collation, encoding="utf-8"))
    answers = {}
    for path in a.answers:                  # lowest rank first: a later file overrides
        answers.update(_answers(path))
    base = E.load_tesseract(a.base_dir)
    book = json.load(open(os.path.join(a.base_dir, "book.json"), encoding="utf-8"))
    fix = None
    if a.fixes:
        from . import fixes as FX
        prof = json.load(open(a.fixes, encoding="utf-8"))
        lexicon = {w.lower() for w in E.load_lexicon(REPO, a.brewer)}
        fix = FX.fixer(prof, FX.Evidence(book, lexicon))
    paras, log = E.merged_text(result, answers, a.volume, base, a.base, book, fix)
    os.makedirs(a.out, exist_ok=True)
    json.dump({"volume": a.volume, "paragraphs": paras, "log": log},
              open(os.path.join(a.out, "merged.json"), "w"), ensure_ascii=False)
    with open(os.path.join(a.out, "merged.txt"), "w", encoding="utf-8") as f:
        for g in paras:
            f.write(g["text"] + "\n\n")
    left = re.findall(r"\b\w+- \w+", " ".join(g["text"] for g in paras))
    print(f"{len(paras)} paragraphs, {len(answers)} answers applied; rejoined "
          f"{log['joined'] + log.get('joined_webster', 0) + log['joined_unattested']}, "
          f"hyphens kept {log['kept'] + log.get('kept_webster', 0) + log.get('kept_unattested', 0)}; "
          f"breaks still open: {len(left)} {left[:12]}; fix library changed {len(log.get('fixes', []))} words -> {a.out}")


def add_parser(sub):
    e = sub.add_parser("editions", help="several scans of one book -> one text (collate, then merge)")
    es = e.add_subparsers(dest="ecmd", required=True)
    c = es.add_parser("collate", help="vote the scans' words; rules clear; build the Proof Desk")
    c.add_argument("--scan", action="append", required=True, help="NAME=unscanner work dir (repeat)")
    c.add_argument("--djvu", action="append", help="NAME=the Archive's _djvu.xml for that scan (repeat)")
    c.add_argument("--base", required=True, help="the scan whose words and lines the text follows")
    c.add_argument("--volume", required=True, help="volume number, for the review ids (v6-p261-i13)")
    c.add_argument("--brewer", help="Brewer's Dictionary paragraphs (.json.gz) to add to the lexicon")
    c.add_argument("--out", required=True)
    m = es.add_parser("merge", help="answers in place, breaks rejoined, dashes set -> merged text")
    m.add_argument("--collation", required=True)
    m.add_argument("--base-dir", required=True, help="the base scan's unscanner work dir")
    m.add_argument("--base", required=True, help="the base scan's name, as at collate")
    m.add_argument("--volume", required=True)
    m.add_argument("--answers", nargs="+", required=True, help="answer files, lowest rank first")
    m.add_argument("--fixes", help="a fixes-profile.json (python -m unscanner fixes profile): apply its rules in play")
    m.add_argument("--brewer", help="Brewer's Dictionary paragraphs, added to the lexicon (with --fixes)")
    m.add_argument("--out", required=True)
    return e


def dispatch(a):
    if a.ecmd == "collate":
        collate(a)
    elif a.ecmd == "merge":
        merge(a)
