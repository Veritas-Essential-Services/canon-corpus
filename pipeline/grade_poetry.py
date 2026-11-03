#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted (Adam: "start with the graded mega poetry book")
"""Grade every poem in the hoard into the Schoolroom Treasury's five bands, and write the volume.

Reads the built poetry catalogs (ao, addendum-heroic, collections, treasury), the hosted texts,
the candidate pool and the hand-kept book table data/poetry/graded/book-bands.json. Writes:

  data/poetry/graded/graded.jsonl     one row per poem (uid): band, why, length, difficulty, rank
  data/poetry/graded/graded.csv       the same, flat, with a blank keep? column for Adam's cull
  data/poetry/graded/volume/<band>-N.md   the reading edition: every poem of the band, in full
                                          where hosted, as a line that links out where not
  data/poetry/graded/CONTENTS.md      counts per band and the first poems of each

Placement (plan, "Grading": the earliest year that most of the readers placed it, AO's year where
AO lists it), in this order:
  1. AO year (1-12), else the heroic addendum's year: Years 1-3 / 4-6 / 7-9 / 10-12.
  2. Otherwise the books the poem was found in vote with their band (book-bands.json). The band is
     the lower median of the votes: the earliest band by which at least half the placing books
     had it. General anthologies (vote: false) do not vote.
  3. A poem found only in general anthologies goes to Years 10-12, marked so.
Nothing here is a cull: every poem is placed, and Adam culls.

Run: python3 pipeline/grade_poetry.py [--check]   (--check: fail if the committed files differ)
"""
import csv, io, json, os, re, sys, statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build_poetry import read_parts  # noqa: E402

P = os.path.join(ROOT, "data", "poetry")
OUT = os.path.join(P, "graded")
BANDS = ["nursery", "y1-3", "y4-6", "y7-9", "y10-12"]
SHARD = 4_000_000


def ao_band(year):
    if not isinstance(year, int):
        return None
    return "y1-3" if year <= 3 else "y4-6" if year <= 6 else "y7-9" if year <= 9 else "y10-12"


def norm_title(t):
    t = (t or "").lower()
    t = re.sub(r"\(.*?\)|\[.*?\]", " ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"^(the|a|an) ", "", t.strip())
    return re.sub(r"\s+", " ", t).strip()


def surname(name):
    parts = re.sub(r"[^A-Za-z \-]", " ", name or "").split()
    return parts[-1].lower() if parts else ""


VOWELS = re.compile(r"[aeiouy]+")
ARCHAIC = {"thee", "thou", "thy", "thine", "ye", "hath", "doth", "art", "ere", "o'er", "e'er", "ne'er", "nay",
           "yea", "whence", "thence", "hither", "thither", "wherefore", "betwixt", "anon", "oft", "wert", "hast",
           "shalt", "wilt", "dost", "didst", "'tis", "'twas", "methinks", "perchance", "albeit", "erst", "yon"}


def syllables(w):
    w = w.lower().strip("'")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    return max(1, len(VOWELS.findall(w)))


def measure(text):
    """(lines, words per line, syllables per word, long-word share, archaic share) of a poem."""
    lines = [l for l in text.split("\n") if l.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    if not lines or not words:
        return None
    syl = [syllables(w) for w in words]
    return {
        "lines": len(lines),
        "wpl": len(words) / len(lines),
        "spw": sum(syl) / len(words),
        "long": sum(1 for s in syl if s >= 3) / len(words),
        "arch": sum(1 for w in words if w.lower() in ARCHAIC) / len(words),
    }


MD_START = re.compile(r"^(\s*)([#>*+\-]|\d+[.)])")


def verse_line(l):
    """One line of verse as Markdown: indentation kept (em spaces), a hard break, nothing read as markup."""
    if not l.strip():
        return ""
    lead = len(l) - len(l.lstrip(" "))
    body = MD_START.sub(lambda m: m.group(1) + "\\" + m.group(2), l.lstrip(" "))
    return "\u2003" * (lead // 2) + body.replace("*", "\\*").replace("_", "\\_") + "  "


def length_mark(n):
    if n is None:
        return None
    return "very short" if n <= 8 else "short" if n <= 20 else "medium" if n <= 60 else "long" if n <= 200 else "very long"


def main(check=False):
    table = json.load(open(os.path.join(OUT, "book-bands.json"), encoding="utf-8"))
    books = {int(k): v for k, v in table["books"].items()}
    labels = {b: table["bands"][b]["label"] for b in BANDS}
    pool = [json.loads(l) for l in open(os.path.join(P, "pool", "pool.jsonl"), encoding="utf-8") if l.strip()]
    by_pool = {r["pool_id"]: r for r in pool}
    pool_key = defaultdict(list)
    for r in pool:
        if r["kind"] == "verse":
            pool_key[(norm_title(r["title"]), surname(r["author"]))].append(r)

    texts = {t["uid"]: t for t in read_parts(os.path.join(P, "texts"))}
    rows = {}
    for layer in ["catalog-ao", "catalog-addendum-heroic", "catalog-collections", "catalog-treasury"]:
        for r in read_parts(os.path.join(P, layer)):
            rows.setdefault(r["uid"], []).append(r)

    measures = {u: measure(t["text"]) for u, t in texts.items()}
    # difficulty: a composite, cut at the corpus's own thirds so the marks mean "easier / middle / harder
    # than most poems in the hoard", not a reading-age claim
    def score(m):
        return m["spw"] * 2 + m["long"] * 4 + m["arch"] * 10 + min(m["wpl"], 14) / 7
    scores = sorted(score(m) for m in measures.values() if m)
    lo, hi = scores[len(scores) // 3], scores[2 * len(scores) // 3]

    out = []
    for uid, rs in rows.items():
        r0 = sorted(rs, key=lambda r: ["ao", "addendum-heroic", "collections", "treasury"].index(r["layer"]))[0]
        layers = sorted({r["layer"] for r in rs})
        ao = next((r for r in rs if r["layer"] == "ao"), None)
        her = next((r for r in rs if r["layer"] == "addendum-heroic"), None)
        tre = next((r for r in rs if r["layer"] == "treasury"), None)
        prow = by_pool.get(tre.get("pool_id")) if tre else None
        if prow is None:
            cands = pool_key.get((norm_title(r0["title"]), surname(r0["poet"])), [])
            prow = max(cands, key=lambda c: c["n_books"]) if cands else None
        found_in = sorted(prow["books"]) if prow else []
        votes = sorted((books[b]["band"] for b in found_in if b in books and books[b].get("vote", True)),
                       key=BANDS.index)
        if ao and ao_band(ao.get("year")):
            band, why = ao_band(ao["year"]), f"AmblesideOnline Year {ao['year']}"
        elif her and ao_band(her.get("year")):
            band, why = ao_band(her["year"]), f"heroic addendum, Year {her['year']}"
        elif votes:
            band = votes[(len(votes) - 1) // 2]
            c = Counter(votes)
            why = "placed by " + ", ".join(f"{c[b]} {labels[b]}" for b in BANDS if c[b]) + \
                  (" book" if len(votes) == 1 else " books")
        elif found_in:
            band, why = "y10-12", "general anthologies only"
        else:
            band, why = "y10-12", "no placing book (collection or AO supplement)"
        m = measures.get(uid)
        diff = None
        if m:
            s = score(m)
            diff = 1 if s < lo else 3 if s >= hi else 2
        flags = []
        if m and band in ("nursery", "y1-3") and m["lines"] > 100:
            flags.append("long for its band")
        if m and band == "y4-6" and m["lines"] > 300:
            flags.append("long for its band")
        out.append({
            "uid": uid,
            "citation": r0["citation"],
            "title": r0["title"],
            "poet": r0["poet"],
            "poet_died": r0.get("poet_died"),
            "band": band,
            "why": why,
            "layers": layers,
            "ao_year": ao.get("year") if ao else None,
            "found_in": found_in,
            "n_books": len(found_in) if found_in else (tre or {}).get("n_books") or 0,
            "host": "full" if uid in texts else "link",
            "link": r0.get("link"),
            "lines": m["lines"] if m else None,
            "length": length_mark(m["lines"] if m else None),
            "difficulty": diff,
            "flags": flags,
            "pool_id": prow["pool_id"] if prow else None,
        })

    # order within a band: AO's own order first (year, term, order), then the most-printed first
    def order(x):
        r = next((r for r in rows[x["uid"]] if r["layer"] == "ao"), None)
        if r and isinstance(r.get("year"), int):
            return (BANDS.index(x["band"]), 0, r["year"], r.get("term") or 0, r.get("order") or 0, "")
        return (BANDS.index(x["band"]), 1, -x["n_books"], 0, 0, x["title"].lower())
    out.sort(key=order)
    for i, x in enumerate(out, 1):
        x["rank"] = i

    files = {}
    files["graded.jsonl"] = "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in out)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["keep?", "band", "rank", "title", "poet", "why", "n_books", "lines", "length", "difficulty",
                "host", "layers", "flags", "uid", "citation", "pool_id"])
    for x in out:
        w.writerow(["", labels[x["band"]], x["rank"], x["title"], x["poet"] or "", x["why"], x["n_books"],
                    x["lines"] or "", x["length"] or "", x["difficulty"] or "", x["host"], ";".join(x["layers"]),
                    ";".join(x["flags"]), x["uid"], x["citation"], x["pool_id"] or ""])
    files["graded.csv"] = buf.getvalue()

    # the reading edition
    dmark = {1: "easier", 2: "middle", 3: "harder", None: "not measured"}
    for b in BANDS:
        mine = [x for x in out if x["band"] == b]
        head = (f"# The Schoolroom Treasury: {labels[b]} (ages {table['bands'][b]['ages']})\n\n"
                f"Draft for Adam's cull, built by `pipeline/grade_poetry.py`. {len(mine)} poems, "
                f"{sum(1 for x in mine if x['host'] == 'full')} printed in full. Every text is cut from a pre-1931 "
                f"printing (US public domain); the source line under each poem names it. Do not edit by hand.\n\n")
        parts, cur = [], head
        for x in mine:
            t = texts.get(x["uid"])
            died = f" (d. {x['poet_died']})" if x.get("poet_died") else ""
            block = f"## {x['title']}\n\n*{x['poet'] or 'Anonymous'}{died}*  ·  {x['why']}"
            block += f"  ·  {x['length'] or 'length unknown'}, {dmark[x['difficulty']]}\n\n"
            if t:
                lines = t["text"].split("\n")
                block += "\n".join((l.replace("  ", " ") + "  ") if l.strip() else "" for l in lines).rstrip() + "\n\n"
                src = t.get("source") or {}
                block += f"<sub>{src.get('work', '')} ({src.get('edition_year', '')}), Project Gutenberg #{src.get('gutenberg', '')} · {x['uid']}</sub>\n\n"
            else:
                block += f"Not printed here: [read it]({x['link']}) · {x['uid']}\n\n"
            if len((cur + block).encode()) > SHARD:
                parts.append(cur)
                cur = f"# The Schoolroom Treasury: {labels[b]} (continued)\n\n"
            cur += block
        parts.append(cur)
        for i, p in enumerate(parts, 1):
            name = f"volume/{b}.md" if len(parts) == 1 else f"volume/{b}-{i}.md"
            files[name] = p

    c = Counter(x["band"] for x in out)
    lines = ["# The Schoolroom Treasury — graded draft", "",
             "Built by `pipeline/grade_poetry.py` from every poem in the hoard (AO, heroic addendum, collections, "
             "treasury). One mega book, graded by band inside it (Adam, 2026-10-07). Nothing is culled yet: "
             "`graded.csv` has a blank `keep?` column for that.", "",
             "| Band | Ages | Poems | Printed in full | Why placed (top reasons) |", "|---|---|---|---|---|"]
    for b in BANDS:
        mine = [x for x in out if x["band"] == b]
        whys = Counter(re.sub(r"(placed by |, )\d+ ", r"\1", x["why"]).replace(" books", " book")
                       if x["why"].startswith("placed") else x["why"].split(",")[0] for x in mine)
        top = "; ".join(f"{k} ({v})" for k, v in whys.most_common(3))
        files_b = [n for n in files if n.startswith(f"volume/{b}")]
        link = ", ".join(f"[{os.path.basename(n)}]({n})" for n in sorted(files_b))
        lines.append(f"| {labels[b]} ({link}) | {table['bands'][b]['ages']} | {c[b]} | "
                     f"{sum(1 for x in mine if x['host'] == 'full')} | {top} |")
    lines += ["", f"Total: {len(out)} poems, {sum(1 for x in out if x['host'] == 'full')} printed in full.", "",
              "Difficulty is relative to the hoard itself (thirds of a word-length, line-length and archaism "
              "score), not a reading age. Length: very short ≤8 lines, short ≤20, medium ≤60, long ≤200.", "",
              "## Flags", ""]
    fl = [x for x in out if x["flags"]]
    lines.append(f"{len(fl)} poems flagged for a second look (long or hard for a young band):")
    lines.append("")
    for x in fl[:60]:
        lines.append(f"- {labels[x['band']]}: *{x['title']}* ({x['poet'] or 'anon.'}) — {', '.join(x['flags'])}, {x['lines']} lines; {x['why']}")
    if len(fl) > 60:
        lines.append(f"- … and {len(fl) - 60} more in `graded.csv` (column `flags`).")
    files["CONTENTS.md"] = "\n".join(lines) + "\n"

    bad = []
    for name, blob in files.items():
        path = os.path.join(OUT, name)
        if check:
            if not os.path.exists(path) or open(path, encoding="utf-8").read() != blob:
                bad.append(name)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(blob)
    if not check:
        vol = os.path.join(OUT, "volume")
        for f in os.listdir(vol):
            if "volume/" + f not in files:
                os.remove(os.path.join(vol, f))
    if bad:
        sys.exit("graded files differ from a rebuild: " + ", ".join(bad))
    print(f"{len(out)} poems graded: " + ", ".join(f"{labels[b]} {c[b]}" for b in BANDS))


if __name__ == "__main__":
    main(check="--check" in sys.argv)
