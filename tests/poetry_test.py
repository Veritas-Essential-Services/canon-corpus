#!/usr/bin/env python3
# prov: 2026-10-06 claude-opus-5-5 drafted
# prov: 2026-11-03 claude-opus-5-5 added the declamations layer
# fable_review: pending
"""
poetry_test.py -- the validator for the poetry section (pipeline/build_poetry.py).

Run:  python3 tests/poetry_test.py

Offline. Checks the committed catalogs, texts and Mnemonicon packs against
each other, against the identity registry and against the Mnemonicon's import
rules; checks the rights rule never hosts what it may not; and exercises the
text cutter on small inline fixtures. If the pinned Gutenberg books are
fetched (data/corpus/gitenberg/), it also rebuilds and asserts byte-identical.
"""
import importlib.util
import json
import os
import re
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


B = load("build_poetry", os.path.join(REPO, "pipeline", "build_poetry.py"))
import wh_uid as U  # noqa: E402

PASS, FAIL = 0, []


def check(name, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
        print(f"ok    {name}")
    else:
        FAIL.append(name)
        print(f"FAIL  {name}" + (f"\n        {str(detail)[:600]}" if detail != "" else ""))


def rj(path):
    return B.read_jsonl(path)


DATA = B.DATA
cats = {layer: B.read_parts(os.path.join(DATA, f"catalog-{layer}")) for layer in B.LAYERS}
sels = {layer: rj(os.path.join(B.SEL, f"{layer}.jsonl")) for layer in B.LAYERS}
texts = {t["uid"]: t for base in B.text_bases() for t in B.read_parts(os.path.join(DATA, base))}
reg = U.WhUidRegistry(B.UIDS)
sources = B.load_sources()["books"]

print("## selections and catalogs")
for layer in B.LAYERS:
    check(f"{layer}: a catalog row for every selection row", len(cats[layer]) == len(sels[layer]),
          (len(cats[layer]), len(sels[layer])))
    need = {"year", "poet", "title"}
    bad = [s for s in sels[layer] if not need <= set(s) or not str(s["title"]).strip()]
    check(f"{layer}: every selection has year, poet and a title", not bad, bad[:3])
    check(f"{layer}: every row is tagged with its layer", all(layer in r["tags"] and r["layer"] == layer for r in cats[layer]))
    check(f"{layer}: every row has rights with a reason in words",
          all(r["rights"]["us"] in ("pd", "in-copyright", "uncertain") and len(r["rights"]["basis"]) > 30
              and r["rights"]["elsewhere"] for r in cats[layer]))
    check(f"{layer}: every row is hosted or linked, and a linked row has somewhere to go",
          all(r["host"] in ("full", "link") and (r["host"] == "full" or r["link"]) for r in cats[layer]))
check("the addendum is marked as proposals", all(r.get("status") == "proposed" for r in cats["addendum-heroic"]))
check("the treasury is marked as candidates, each tied to its pool entry",
      all(r.get("status") == "candidate" and r.get("pool_id") for r in cats["treasury"]))
_tsel = {B.citation(s): s for s in sels["treasury"]}
_bad = [r["citation"] for r in cats["treasury"] if r["host"] == "full"
        and B.norm(texts[r["uid"]]["text"].split("\n")[0]) != B.norm(_tsel[r["citation"]]["first_line"])]
check("a hosted treasury poem begins at the first line its book prints", not _bad, _bad[:5])
check("a collections row names its collection, and a hosted one is in that collection's pack",
      all(r.get("collection") and r.get("collection_title") and r["collection"] in r["tags"]
          and (r["host"] != "full" or r["pack"] == f"collection-{r['collection']}") for r in cats["collections"]))
check("the AO layer carries no addendum tag, and the addendum no AO tag",
      all("addendum-heroic" not in r["tags"] for r in cats["ao"])
      and all("ao" not in r["tags"] for r in cats["addendum-heroic"]))
check("the addendum's rows say heroic, adventurous, vocational or song",
      all(r.get("kind") in ("heroic", "adventurous", "vocational", "song") for r in cats["addendum-heroic"]))

print("\n## rights: the gate")
allrows = [r for rows in cats.values() for r in rows]
check("nothing is hosted that is not US public domain",
      all(r["rights"]["us"] == "pd" for r in allrows if r["host"] == "full"),
      [r["citation"] for r in allrows if r["host"] == "full" and r["rights"]["us"] != "pd"][:5])
late = [r for r in allrows if (r.get("first_pub") or {}).get("year") and r["first_pub"]["year"] >= B.PD_BEFORE]
check(f"every poem first published {B.PD_BEFORE} or later is linked out ({len(late)})",
      all(r["host"] == "link" and r["rights"]["us"] == "in-copyright" for r in late))
def _pin(t):
    s = sources.get(str(t["source"]["gutenberg"])) or {}
    return (s.get("mirror") or {}) if t["source"].get("copy") == "mirror" else s


check("a hosted text names a pinned, non-COPYRIGHTED Gutenberg book (or its pinned mirror copy)",
      all(str(t["source"]["gutenberg"]) in sources and not sources[str(t["source"]["gutenberg"])].get("copyrighted_header")
          and t["source"]["sha256"] and t["source"]["sha256"] == _pin(t).get("sha256") for t in texts.values()))
r, host = B.rights({"poet": "X", "poet_died": 1960, "first_pub": {"work": "W", "year": 1935}, "pd_source": None}, None, False, None)
check("a 1935 poem is in copyright and linked", r["us"] == "in-copyright" and host == "link", r)
r, host = B.rights({"poet": "X", "poet_died": 1960, "first_pub": {"year": 1920},
                    "pd_source": {"gutenberg": 1, "work": "W", "edition_year": 1955}}, None, False, "no cut")
check("a pre-1931 poem with no cut text is not hosted", host == "link", r)
r, host = B.rights({"poet": "X", "poet_died": 1960, "first_pub": {"year": 1920},
                    "pd_source": {"gutenberg": 1, "work": "W", "edition_year": 1920}}, None, True, None)
check("a 1920 printing is hosted, with the life+70 caveat for a poet who died 1960",
      r["us"] == "pd" and host == "full" and "2031" in r["elsewhere"], r)

print("\n## identity")
for layer in B.LAYERS:
    check(f"{layer}: each uid is the registry's uid for its citation",
          all(reg.map.get(r["citation"]) == r["uid"] for r in cats[layer]))
by_cit = {}
for row in allrows:
    by_cit.setdefault(row["citation"], set()).add(row["uid"])
check("one citation, one uid, across the layers", all(len(v) == 1 for v in by_cit.values()))

print("\n## texts")
hosted = {r["uid"] for r in allrows if r["host"] == "full"}
check("a text for every hosted poem, and none for a linked one", set(texts) == hosted,
      (len(set(texts) - hosted), len(hosted - set(texts))))
check("no text is empty, and none keeps Gutenberg's underscores or [Illustration] lines",
      all(t["text"].strip() and "_" not in t["text"] and "[Illustration" not in t["text"] for t in texts.values()))
check("texts are LF, no trailing spaces, no doubled blank lines",
      all("\r" not in t["text"] and all(l == l.rstrip() for l in t["text"].split("\n")) and "\n\n\n" not in t["text"]
          for t in texts.values()))
_verse = [t for t in texts.values() if t["citation"].startswith("poetry:")]
check("no hosted poem reads as wrapped prose", not [t for t in _verse if B._prose(t["text"])],
      [t["citation"] for t in _verse if B._prose(t["text"])][:5])

big = sorted(os.path.relpath(p, REPO) for p in B.built_paths() if os.path.getsize(p) > 5_000_000)
check("every committed catalog, texts part and pack is under 5 MB", not big, big)

print("\n## packs")
X = load("mnemonicon_pack_test_helpers", os.path.join(REPO, "pipeline", "export_mnemonicon_pack.py"))
cats_ok = {"Poetry", "Scripture", "Monologue", "Catechism", "List", "Song", "Other"}
packs = {}
for f in sorted(os.listdir(B.PACKS)):
    raw = open(os.path.join(B.PACKS, f), "rb").read()
    packs[f] = (raw, json.loads(raw.decode("utf-8")))
check("there are packs", len(packs) > 0, len(packs))
KEYS = {"id", "createdAt", "updatedAt", "title", "source", "category", "translation", "text", "notes", "tags", "srs", "history"}
for f, (raw, pieces) in packs.items():
    errs = []
    for p in pieces:
        if set(p) != KEYS:
            errs.append(f"{p.get('title')}: keys")
        if p["category"] not in cats_ok:
            errs.append(f"{p['title']}: category {p['category']}")
        if "\n" in p["source"] or "\n" in p["translation"]:
            errs.append(f"{p['title']}: one-line fields")
        if p["tags"] != [t.strip().lower() for t in p["tags"]]:
            errs.append(f"{p['title']}: tags")
        if p["srs"] != {"reps": 0, "ease": 2.5, "interval": 0, "due": p["createdAt"]} or p["history"] != []:
            errs.append(f"{p['title']}: srs/history")
    ids = [p["id"] for p in pieces]
    sigs = ["\0".join([p["title"], p["source"], p["text"].rstrip()]) for p in pieces]
    if len(ids) != len(set(ids)) or len(sigs) != len(set(sigs)):
        errs.append("duplicate id or title+source+text")
    if not raw.endswith(b"}\n]\n") or b"\r" in raw:
        errs.append("format")
    check(f"{f}: {len(pieces)} pieces the Mnemonicon import takes as-is", not errs, errs[:5])

ids_ok = True
for f, (_, pieces) in packs.items():
    for p in pieces:
        uidline = p["notes"].rsplit("· ", 1)[-1].split("\n")[0]
        whole = str(uuid.uuid5(B.NAMESPACE, uidline))
        parts = p["title"].rsplit(", part ", 1)
        if len(parts) == 2:
            k = parts[1].split(" of ")[0]
            ids_ok &= p["id"] == str(uuid.uuid5(B.NAMESPACE, f"{uidline}#part{k}"))
        else:
            ids_ok &= p["id"] == whole
check("every piece id is uuid5 of its poem's wh-uid (a re-import adds nothing)", ids_ok)
in_packs = {p["notes"].rsplit("· ", 1)[-1].split("\n")[0] for _, ps in packs.values() for p in ps}
check("every hosted poem is in a pack", in_packs == hosted, (len(hosted - in_packs), len(in_packs - hosted)))
check("a long poem is banked in parts of whole stanzas, each part within reach",
      all(p["text"].count("\n") + 1 <= B.PART + 40 for _, ps in packs.values() for p in ps if ", part " in p["title"]))

print("\n## declamations")
D = load("select_declamations", os.path.join(REPO, "pipeline", "select_declamations.py"))
dec, dsel = cats["declamations"], {B.citation(dict(r, layer="declamations")): r for r in sels["declamations"]}
check("declamations: every row is a candidate tied to its pool entry (or named in the plan)",
      all(r.get("status") == "candidate" and (r.get("pool_id") or r.get("named_in_plan")) for r in dec))
check("declamations: every citation is declamations:<author>.<title>, and is no poem's",
      all(r["citation"].startswith("declamations:") for r in dec)
      and not [r for l, rows in cats.items() if l != "declamations" for r in rows if r["citation"].startswith("declamations:")])
check("declamations: every row records its source audiences, and a McGuffey row its reader and lesson",
      all(isinstance((r.get("grade_hint") or {}).get("audiences"), list) for r in dec)
      and all(r["grade_hint"].get("mcguffey_reader") == D.MCGUFFEY[r["pd_source"]["gutenberg"]]
              and re.fullmatch(r"[IVXLC]+|\d+", r["grade_hint"].get("lesson") or "")
              for r in dec if r["pd_source"]["gutenberg"] in D.MCGUFFEY and r["host"] == "full"),
      [r["citation"] for r in dec if r["pd_source"]["gutenberg"] in D.MCGUFFEY and r["host"] == "full"
       and not (r.get("grade_hint") or {}).get("lesson")][:5])
check("declamations: cut from the pinned mirror copy, and from a pre-1931 printing",
      all(r["pd_source"].get("copy") == "mirror" and r["pd_source"]["edition_year"] < B.PD_BEFORE for r in dec))
check("declamations: a linked-out row says why", all(r["host"] == "full" or dsel[r["citation"]].get("no_text_reason")
                                                     for r in dec))
_dt = {r["uid"]: texts[r["uid"]]["text"] for r in dec if r["host"] == "full"}
_bad = [r["citation"] for r in dec if r["host"] == "full" and B.norm(_dt[r["uid"]].split("\n")[0])[:40]
        != B.norm(re.sub(r"^\d{1,2}\.\s+", "", dsel[r["citation"]]["first_line"]))[:40]]
check("declamations: a hosted piece begins at the first line the row records", not _bad, _bad[:5])
_bad = [r["citation"] for r in dec if r["host"] == "full" and (
    re.search(r"DEFINITIONS|EXERCISES|^#{2,}$|ECLECTIC SERIES|THIRD READER|\t|^Notes?\.--|^NOTES?\b", _dt[r["uid"]], re.M)
    or D.BIO.match(_dt[r["uid"]]))]
check("declamations: no hosted text keeps a reader's apparatus (notes, definitions, running heads) or "
      "opens with the editor's life of the author", not _bad, _bad[:5])
_bad = [r["citation"] for r in dec if r["host"] == "full" and r["form"] == "prose"
        and any(len(p.split("\n")) > 1 and not all(l.startswith("  ") for l in p.split("\n"))
                for p in _dt[r["uid"]].split("\n\n"))]
check("declamations: a prose piece is one line per paragraph (a quotation set as verse keeps its lines)", not _bad, _bad[:5])
check(f"declamations: every hosted piece is {D.MIN_WORDS} to {D.MAX_WORDS} words",
      all(D.MIN_WORDS <= r["words"] <= D.MAX_WORDS for r in dec if r["host"] == "full"))
_other = {B.norm(t["text"].split("\n")[0])[:40] for t in texts.values() if t["citation"].startswith("poetry:")}
_bad = [r["citation"] for r in dec if r["host"] == "full" and B.norm(_dt[r["uid"]].split("\n")[0])[:40] in _other]
check("declamations: no piece repeats a poem another layer already hosts", not _bad, _bad[:5])
_named = {r["named_in_plan"]: r for r in dec if r.get("named_in_plan")}
check("declamations: the plan's Gettysburg Address, Patrick Henry and Crispin's Day are hosted",
      len(_named) == 3 and all(r["host"] == "full" for r in _named.values())
      and any("Gettysburg" in k for k in _named) and any("Patrick Henry" in k for k in _named)
      and any("Crispin" in k for k in _named), sorted(_named))
_dp = [p for f, (_, ps) in packs.items() if f.startswith("declamation-") for p in ps]
check("declamations: packs are one per source book, filed as Monologue",
      _dp and all(p["category"] == "Monologue" for p in _dp)
      and {f"declamation-pg{r['pd_source']['gutenberg']}.json" for r in dec if r["host"] == "full"}
      == {f for f in packs if f.startswith("declamation-")})
check(f"declamations: a long prose piece is banked in parts of whole paragraphs, none much over {B.PROSE_PART} words",
      all(len(p["text"].split()) <= B.PROSE_PART * 3 // 2 for p in _dp if ", part " in p["title"]))

print("\n## the cutter, on fixtures")
book = """CONTENTS

  THE OWL
  THE BROOK
  THE EAGLE


THE OWL

First printed in 1830.


1

  When cats run home and light is come,
  And dew is cold upon the ground,

2

  When merry milkmaids click the latch,
  And rarely smells the new-mown hay,


THE BROOK

  I come from haunts of coot and hern,
  I make a sudden sally

THE EAGLE

  He clasps the crag with crooked hands;
""".split("\n")
t, how = B.extract(book, "The Owl")
check("the contents list is passed over, the editor's note dropped, stanza numbers become breaks",
      t is not None and t.split("\n")[0].startswith("When cats") and "First printed" not in t and "\n\n" in t
      and "1" not in t.split("\n"), t)
t, _ = B.extract(book, "The Brook")
check("a cut stops at the next capitals heading", t is not None and "EAGLE" not in t and "sally" in t, t)
t, _ = B.extract(book, "anything", {"first_line": r"^\s*He clasps the crag"})
check("first_line starts an untitled poem at its first line", t is not None and t.startswith("He clasps"), t)
t, _ = B.extract(book, "The Owl", {"end": r"merry milkmaids"})
check("end stops before the matching line", t is not None and "milkmaids" not in t and "dew is cold" in t, t)
prose = ["THE SEAL", ""] + ["all these things happened several years ago at a place called the north east point of"] * 6
t, why = B.extract(prose, "The Seal")
check("prose after a heading is refused, not hosted", t is None, why)
fake = B.book_path("0")
os.makedirs(os.path.dirname(fake), exist_ok=True)
with open(fake, "w") as f:
    f.write("*** This is a COPYRIGHTED Project Gutenberg eBook ***\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\nTHE OWL\n")
try:
    lines, why = B.read_book("0", {})
finally:
    os.remove(fake)
check("a COPYRIGHTED Gutenberg eBook is refused", lines is None and "COPYRIGHTED" in why, why)

reader = """LESSON IX.

THE OWL AND THE BOY.
1. An owl sat on a tree. A boy saw
him, and said, "Good day."

	THIRD READER. 	9
2. The owl said nothing.
Boy. Why not?
Owl. Owls do not talk.

LESSON X.
""".split("\n")
t, _ = B.extract(reader, "x", {"first_line": r"^1\. An owl", "end": r"^LESSON X\.", "gap": 99, "keep_headings": True,
                               "reflow": True, "para_numbers": True, "join_pages": True, "drop": r"^\s*\d*\s*\t"})
check("prose: paragraph numbers dropped, a page's running head dropped, wrapped lines joined",
      t == 'An owl sat on a tree. A boy saw him, and said, "Good day."\n\nThe owl said nothing. Boy. Why not? Owl. Owls do not talk.', t)
t, _ = B.extract(reader, "x", {"first_line": r"^2\. The owl", "end": r"^LESSON X\.", "gap": 99, "keep_headings": True,
                               "reflow": True, "join_pages": True, "speakers": True})
check("prose: with `speakers`, each speaker's line is its own paragraph",
      t == "2. The owl said nothing.\n\nBoy. Why not?\n\nOwl. Owls do not talk.", t)
speech = """IV.

          AGAINST DELAY.

Sir, we have done everything that could be done to avert the storm which is
now coming on. We have petitioned; we have remonstrated; we have supplicated;
we have prostrated ourselves before the throne, and have implored its
interposition to arrest the tyrannical hands of the ministry and Parliament.

[Transcriber's Note: a note
on two lines.]

     "Lay on, Macduff,
     And damn'd be him that first cries, 'Hold, enough!'"

There is no retreat but in submission and slavery! Our chains are forged!
                                     P. Henry.


                                   V.
""".split("\n")
_fl = "Sir, we have done everything that could be done to avert the storm which is"
t, info = D.cut(speech, 7211, {"title": "Against Delay", "first_line": _fl},
                {"title": "Against Delay", "first_line": _fl, "order": 4},
                {"title": "Next", "first_line": "Nothing here at all", "order": 5})
check("declamations cutter: starts under the heading, stops above the signature, skips the transcriber's note, "
      "keeps a verse quotation's lines",
      t is not None and t.startswith("Sir, we have done everything that could be done to avert") and t.endswith("forged!")
      and "Transcriber" not in t and "\n\n     \"Lay on, Macduff,\n     And damn'd" in t
      and info["signed"] == "P. Henry." and info["form"] == "prose", (t, info))
t2, _ = B.extract(speech, "x", info["extract"])
check("declamations cutter: the stored rule replays to the same text", t2 == t, t2)
mcg = """XIX. A SPEECH. (115)

Patrick Henry, 1736-1799, was born in Virginia.
###


It is natural for man to indulge in the illusions of hope. We are apt to shut
our eyes against a painful truth, and listen to the song of that siren till she
transforms us into beasts.


NOTES.--Siren, a sea nymph.
""".split("\n")
_, info = D.cut(mcg, 16751, {}, {"title": "A Speech", "first_line": "Patrick Henry, 1736-1799, was born in Virginia.",
                                 "order": 1}, None)
check("declamations cutter: McGuffey's life of the author is passed over (kept as the headnote), NOTES end the cut",
      isinstance(info, dict) and info["first_line"].startswith("It is natural") and "born" in info["headnote"]
      and info["lesson"] == "XIX", info)
check("declamations: two printings of a speech are one piece, a salutation aside",
      D.same_piece("Mr. President, It is natural for man to indulge in the illusions of hope.",
                   "It is natural for man to indulge in the illusions of hope. We are apt to")
      and not D.same_piece("Mr. President and Gentlemen of the Union League:--It was my good fortune",
                           "Mr. President and Gentlemen of the Union League:--I am glad to be here"))

print("\n## rebuild")
if all(os.path.exists(B.book_path(n)) for n in sources):
    reg2 = U.WhUidRegistry(B.UIDS)
    c2, t2, _ = B.build(reg2)
    blobs = B.render_all(c2, t2)
    stale = [os.path.relpath(p, REPO) for p, b in blobs.items() if not os.path.exists(p) or open(p, "rb").read() != b]
    check("a rebuild mints 0 uids", reg2.minted == 0, reg2.minted)
    check("a rebuild is byte-identical", not stale, stale[:5])
    extra = sorted(os.path.relpath(p, REPO) for p in B.built_paths() - set(blobs))
    check("no stale catalog, texts or pack files", not extra, extra[:5])
else:
    print("note  pinned books not fetched (python3 pipeline/build_poetry.py --fetch); full rebuild check skipped")
_mirrors = [n for n, s in sources.items() if s.get("mirror")]
if _mirrors and all(os.path.exists(B.book_path(n, True)) for n in _mirrors):
    reg3 = U.WhUidRegistry(B.UIDS)
    c3, t3, _ = B.build(reg3, layers=("declamations",))
    blobs = B.render_all(c3, t3)
    stale = [os.path.relpath(p, REPO) for p, b in blobs.items() if not os.path.exists(p) or open(p, "rb").read() != b]
    check("declamations: a rebuild of the layer mints 0 and is byte-identical", reg3.minted == 0 and not stale,
          (reg3.minted, stale[:5]))
    extra = sorted(os.path.relpath(p, REPO) for p in B.built_paths(("declamations",)) - set(blobs))
    check("declamations: no stale catalog, texts or pack files", not extra, extra[:5])
else:
    print("note  mirror copies not fetched (python3 pipeline/build_poetry.py --fetch); declamations rebuild check skipped")

print(f"\n{PASS} passed, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
