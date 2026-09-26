#!/usr/bin/env python3
"""
mnemonicon_pack_test.py -- the validator for exports/mnemonicon/*.json
(launch plan C5, first link).

Run:  python3 tests/mnemonicon_pack_test.py

Checks each committed pack against what the Mnemonicon's import expects
(`The Mnemonicon Website/site/app.js`: importFiles, repairPiece, pieceSig;
sync.js: toRow), that it says what the corpus says, that a regeneration is
byte-identical, and that the licence gate refuses anything not public domain.
The page itself is exercised by tests/mnemonicon_pack_browser_test.js.
"""
import copy
import importlib.util
import json
import os
import re
import sys
import uuid
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")
OUT = os.path.join(REPO, "exports", "mnemonicon")
MNEMONICON = os.environ.get("MNEMONICON_DIR") or os.path.join(REPO, "..", "The Mnemonicon Website")

spec = importlib.util.spec_from_file_location("export_mnemonicon_pack", os.path.join(PIPE, "export_mnemonicon_pack.py"))
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)

PASS, FAIL = 0, []


def check(name, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
        print(f"ok    {name}")
    else:
        FAIL.append(name)
        print(f"FAIL  {name}" + (f"\n        {detail}" if detail != "" else ""))


# The piece shape: newPiece() + the fields sync's toPiece() adds.
KEYS = {"id", "createdAt", "updatedAt", "title", "source", "category", "translation",
        "text", "notes", "tags", "srs", "history"}
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
EXPECT = {"adoro-te": (7, 23), "pange-lingua": (6, 12),     # (stanzas, clauses)
          "lauda-sion": (12, 45), "sacris-solemniis": (7, 17), "verbum-supernum": (6, 12)}
N_PIECES = sum(n for n, _ in EXPECT.values())                # 38


def categories():
    """The Mnemonicon's own category list, read from its page when reachable."""
    page = os.path.join(MNEMONICON, "site", "index.html")
    if not os.path.exists(page):
        print("note  Mnemonicon repo not reachable; using the category list as of 2026-09-26")
        return {"Poetry", "Scripture", "Monologue", "Catechism", "List", "Song", "Other"}
    html = open(page, encoding="utf-8").read()
    sel = re.search(r'<select id="f-category">(.*?)</select>', html, re.S)
    return set(re.findall(r"<option>([^<]+)</option>", sel.group(1)))


def sig(p):
    """app.js pieceSig: title, source, text (CRLF folded, trailing space cut)."""
    return "\0".join([p["title"], p.get("source") or "", str(p.get("text") or "").replace("\r\n", "\n").rstrip()])


def iso(s):
    try:
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except (TypeError, ValueError):
        return False


def validate(pieces, cats):
    """Every expectation the import and the rest of the app put on a piece."""
    errs = []
    if not isinstance(pieces, list):
        return ["not an array (the import takes an array of pieces)"]
    for i, p in enumerate(pieces):
        at = f"[{i}] {p.get('title')!r}" if isinstance(p, dict) else f"[{i}]"
        if not isinstance(p, dict):
            errs.append(f"{at}: not an object"); continue
        if set(p) != KEYS:
            errs.append(f"{at}: keys {sorted(set(p) ^ KEYS)} differ from a piece's")
        if not (isinstance(p.get("id"), str) and UUID.match(p["id"])):
            errs.append(f"{at}: id is not a uuid")
        if not (isinstance(p.get("title"), str) and p["title"].strip()):
            errs.append(f"{at}: no title (the import skips it)")
        if not (isinstance(p.get("text"), str) and p["text"].strip()):
            errs.append(f"{at}: no text")
        for k in ("source", "translation", "notes"):
            if not isinstance(p.get(k), str):
                errs.append(f"{at}: {k} is not a string")
        if "\n" in (p.get("translation") or "") or "\n" in (p.get("source") or ""):
            errs.append(f"{at}: translation/source must be one line (an <input> in the form)")
        if p.get("category") not in cats:
            errs.append(f"{at}: category {p.get('category')!r} is not one the form offers")
        tags = p.get("tags")
        if not (isinstance(tags, list) and all(isinstance(t, str) and t == t.strip().lower() and t for t in tags)):
            errs.append(f"{at}: tags must be trimmed lower-case strings (as the form saves them)")
        s = p.get("srs")
        if not (isinstance(s, dict) and set(s) == {"reps", "ease", "interval", "due"}
                and s["reps"] == 0 and s["interval"] == 0 and s["ease"] == 2.5 and iso(s["due"])):
            errs.append(f"{at}: srs is not a new learning piece's schedule")
        if p.get("history") != []:
            errs.append(f"{at}: history must start empty")
        if not (iso(p.get("createdAt")) and p.get("updatedAt") == p.get("createdAt")):
            errs.append(f"{at}: createdAt/updatedAt")
    ids = [p.get("id") for p in pieces if isinstance(p, dict)]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    sigs = [sig(p) for p in pieces if isinstance(p, dict) and isinstance(p.get("title"), str)]
    if len(sigs) != len(set(sigs)):
        errs.append("duplicate title+source+text: the import would drop one")
    return errs


def import_into(bank, incoming):
    """app.js importFiles, line for line: returns how many were added."""
    known = {p["id"] for p in bank}
    sigs = {sig(p) for p in bank}
    added = 0
    for p in incoming:
        if not (p and p.get("id") and p.get("title")) or p["id"] in known or sig(p) in sigs:
            continue
        bank.append(p); known.add(p["id"]); sigs.add(sig(p)); added += 1
    return added


cats = categories()
check("the Mnemonicon offers the category a hymn is filed under", X.CATEGORY in cats, sorted(cats))
passages, witnesses, manifest = data = X.load()

print("\n## the committed packs")
all_ids = set()
for slug, (n_st, n_cl) in EXPECT.items():
    path = os.path.join(OUT, X.filename(slug, "stanza"))
    raw = open(path, "rb").read()
    pieces = json.loads(raw.decode("utf-8"))
    check(f"{slug}: {n_st} pieces, one per stanza", len(pieces) == n_st, len(pieces))
    errs = validate(pieces, cats)
    check(f"{slug}: every piece is one the import takes as-is", not errs, errs)
    check(f"{slug}: LF only, ends in a newline", b"\r" not in raw and raw.endswith(b"}\n]\n"))
    pb, _ = X.build(slug, data=data)
    check(f"{slug}: regenerating is byte-identical", X.render(pb) == raw)
    all_ids |= {p["id"] for p in pieces}

    stanzas = sorted((p for p in passages.values() if p["work"] == f"hymns:{slug}" and p["unit"] == "stanza"),
                     key=lambda p: p["stanza"])
    ok_ids = all(p["id"] == str(uuid.uuid5(X.NAMESPACE, st["uid"])) for p, st in zip(pieces, stanzas))
    check(f"{slug}: each id is uuid5 of its stanza uid (stable for ever)", ok_ids)
    ok_text = all(p["text"].split("\n") == [" ".join(witnesses[c + "/la.1"]["text"].split("\n")) for c in st["clauses"]]
                  for p, st in zip(pieces, stanzas))
    check(f"{slug}: text is the la.1 reading of record, one line per clause", ok_text)
    check(f"{slug}: tags are latin, hymn, {slug}", all(p["tags"] == ["latin", "hymn", slug] for p in pieces))
    check(f"{slug}: notes carry the citation and uid", all(st["citation"] in p["notes"] and st["uid"] in p["notes"]
                                                           for p, st in zip(pieces, stanzas)))

    used = [witnesses[f"{st['uid']}/{X.HYMNS[slug]['witness']}"] for st in stanzas]
    srcs = {w["source"] for w in used}
    check(f"{slug}: one English witness throughout ({', '.join(srcs)})", len(srcs) == 1)
    src = manifest["sources"][srcs.pop()]
    check(f"{slug}: that witness's licence is PD ({src['license']}: {src.get('license_basis')})", src["license"] == "PD")
    check(f"{slug}: the default is the witness the data marks singable", X.HYMNS[slug]["witness"] == "en.singable"
          and all(w["role"] == "singable" for w in used))
    check(f"{slug}: notes carry that English and its edition", all(X.english(w) in p["notes"] and src["edition"] in p["notes"]
                                                                   for p, w in zip(pieces, used)))
    check(f"{slug}: translation names the witness on one line", all(p["translation"] == X.LABELS[w["source"]] for p, w in zip(pieces, used)))
    unverified = not src.get("verified")
    check(f"{slug}: an unverified English says so in its notes" if unverified else f"{slug}: a verified English makes no such caveat",
          all(("not yet checked" in p["notes"]) == unverified for p in pieces))

    cl, _ = X.build(slug, by="clause", data=data)
    check(f"{slug}: --by clause gives {n_cl} pieces, all valid", len(cl) == n_cl and not validate(cl, cats), len(cl))
    check(f"{slug}: clause ids are their clause uids', distinct from the stanzas'",
          [p["id"] for p in cl] == [str(uuid.uuid5(X.NAMESPACE, c)) for st in stanzas for c in st["clauses"]]
          and not ({p["id"] for p in cl} & {p["id"] for p in pieces}))
    vs, _ = X.build(slug, lines="verse", data=data)
    check(f"{slug}: --lines verse keeps the printed verse lines",
          all(p["text"].count("\n") + 1 == st["lines"][1] for p, st in zip(vs, stanzas)))
    check(f"{slug}: --lines verse keeps ids and words", [p["id"] for p in vs] == [p["id"] for p in pieces]
          and all(a["text"].split() == b["text"].split() for a, b in zip(vs, pieces)))

check("no id is shared between the hymns", len(all_ids) == N_PIECES)
for slug in ("lauda-sion", "sacris-solemniis", "verbum-supernum"):
    pk, used = X.build(slug, data=data)
    la_src = {witnesses[c + "/la.1"]["source"] for st in passages.values()
              if st["work"] == f"hymns:{slug}" and st["unit"] == "stanza" for c in st["clauses"]}
    check(f"{slug}: Latin and English both from Britt 1922, both PD and verified against the scan",
          la_src == {"britt-1922-latin"} and "Britt 1922" in used["label"]
          and all(manifest["sources"][k]["license"] == "PD" and manifest["sources"][k]["verified"]
                  for k in la_src | {used["source"]}))
    lit, lu = X.build(slug, witness_name="en.literal", data=data)
    check(f"{slug}: Britt's literal prose (PD) may be chosen instead",
          lu["source"] == "britt-1922-prose-corpus-christi" and not validate(lit, cats))

print("\n## importing, as app.js does it")
packs = [json.load(open(os.path.join(OUT, X.filename(s, "stanza")), encoding="utf-8")) for s in EXPECT]
bank = [{"id": "11111111-1111-4111-8111-111111111111", "title": "A card's own", "source": "", "text": "x"}]
added = sum(import_into(bank, p) for p in copy.deepcopy(packs))
check(f"a first import adds all {N_PIECES}", added == N_PIECES, added)
check("a second import adds nothing", sum(import_into(bank, p) for p in copy.deepcopy(packs)) == 0)
regen = [X.build(s, data=X.load())[0] for s in EXPECT]
check("a regenerated file adds nothing", sum(import_into(bank, p) for p in regen) == 0)
rekeyed = copy.deepcopy(packs)
for pk in rekeyed:
    for p in pk:
        p["id"] = str(uuid.uuid4())
check("a re-keyed copy (sync on a second card) adds nothing: title+source+text", sum(import_into(bank, p) for p in rekeyed) == 0)
other, _ = X.build("pange-lingua", witness_name="en.literal", data=data)
for p in other:
    p["id"] = str(uuid.uuid4())
check("swapping the English witness does not make a re-keyed piece new", import_into(bank, other) == 0)

print("\n## the licence gate")
lit, used = X.build("pange-lingua", witness_name="en.literal", data=data)
check("Britt's literal prose (PD) may be chosen instead", used["source"] == "britt-1922-prose" and not validate(lit, cats))


def refused(fn):
    try:
        fn()
    except X.LicenceRefused as e:
        return str(e)
    return None


for licence in ("own", "free-grant", "CC BY-SA", None):
    m = copy.deepcopy(manifest)
    if licence is None:
        m["sources"]["hopkins-1918"].pop("license")
    else:
        m["sources"]["hopkins-1918"]["license"] = licence
    msg = refused(lambda: X.build("adoro-te", data=(passages, witnesses, m)))
    check(f"a witness licensed {licence!r} is refused, not exported", msg and "not PD" in msg, msg)
m = copy.deepcopy(manifest)
m["sources"]["roman-missal-received"]["license"] = "own"
check("the Latin passes the same gate", refused(lambda: X.build("pange-lingua", data=(passages, witnesses, m))))
w2 = copy.deepcopy(witnesses)
for st in (p for p in passages.values() if p["work"] == "hymns:pange-lingua" and p["unit"] == "stanza"):
    w = copy.deepcopy(w2[st["clauses"][0] + "/en.elegant"])
    w.update(address=st["uid"] + "/en.elegant", passage_uid=st["uid"])
    w2[w["address"]] = w
msg = refused(lambda: X.build("pange-lingua", witness_name="en.elegant", data=(passages, w2, manifest)))
check("the house's own prose (en.elegant, `own`) is refused by name", msg and "house-elegant" in msg, msg)
plain = next(w for w in witnesses.values() if w["name"] == "en.plain")
check("a generated witness (en.plain) is refused", refused(lambda: X.gate(plain, manifest)))
m = copy.deepcopy(manifest)
del m["sources"]["caswall-1849-britt-1922"]
check("a witness whose source is not in the manifest is refused", refused(lambda: X.build("pange-lingua", data=(passages, witnesses, m))))

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
