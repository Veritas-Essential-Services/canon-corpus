#!/usr/bin/env python3
# prov: 2026-10-17 claude-opus-5-5 drafted
# fable_review: pending
"""
select_treasury.py -- turn the Schoolroom Treasury candidate pool into a
poetry-section layer, so every poem in the pool is in the Poetry Hoard.

    python3 pipeline/select_treasury.py --fetch   # fetch the pool's books into data/corpus/gitenberg/ and pin them
    python3 pipeline/select_treasury.py           # write data/poetry/selections/treasury.jsonl
    python3 pipeline/build_poetry.py              # then build as usual (mints the new uids once)

    Input:  data/poetry/pool/pool.jsonl        (the candidates, one per poem)
            data/poetry/pool/rows/<pg>.jsonl   (each book's own title, author and first line)
            data/poetry/pool/sources.json      (each book's year and how it was checked)
            data/poetry/poets.json             (canonical poet names and aliases)
    Output: data/poetry/selections/treasury.jsonl   (COMMITTED; the build's input)
            data/poetry/sources.json                (pool books added and pinned by sha256)

WHICH POEMS
    Every verse candidate in the pool. Prose pieces (speeches from the readers
    and speakers) are left for a later declamation layer. A candidate already
    in the AO list or the heroic addendum is the same poem and is not repeated.

WHERE THE TEXT COMES FROM
    Of the books that print a poem, the first whose year was read from the
    book itself (and is before 1931) is tried first. The cut begins at the
    poem's FIRST LINE as that book prints it, not at its title, so a contents
    list or an index of first lines (which carry page numbers) never wins: the
    occurrence chosen is the one with the poem's title standing just above it.
    The rule is written into the selection row and the build replays it. A
    candidate no book yields a clean cut for stays in the layer, linked out,
    with the reason.

THE LAYER
    Tag `treasury`; no year or term (Adam culls the pool first, grading comes
    after); `status: "candidate"`; one Mnemonicon pack per source book.
"""
import argparse
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
import build_poetry as B  # noqa: E402

POOL = os.path.join(B.DATA, "pool")
OUT = os.path.join(B.SEL, "treasury.jsonl")
ANON = {"", "anon", "anonymous", "unknown", "author unknown", "old ballad", "old song", "traditional",
        "old rhyme", "nursery rhyme", "old english", "old carol", "folk song"}
LONGEST = 900            # a cut longer than this has run into the next poems


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[’'`]", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def words(s, n):
    return " ".join(fold(s).split()[:n])


# ---------------------------------------------------------------------------
# Poets: the pool's spellings to the section's canonical names
# ---------------------------------------------------------------------------

def poet_table():
    poets = json.load(open(os.path.join(B.DATA, "poets.json"), encoding="utf-8"))["poets"]
    exact, by_surname = {}, {}
    for name, p in poets.items():
        for a in [name] + p.get("aliases", []):
            exact[fold(a)] = name
        sur = fold(name).split()[-1] if fold(name) else ""
        by_surname.setdefault(sur, set()).add(name)
    return poets, exact, by_surname


def canonical(author, poets, exact, by_surname):
    """(name, died). An unrecorded poet keeps the book's spelling, tidied."""
    a = re.sub(r"\(.*?\)|\[.*?\]", "", author or "")
    a = re.sub(r"^\s*(?:by|from)\s+", "", a, flags=re.I)
    a = re.sub(r",?\s*\d{3,4}\s*[-–]\s*\d{0,4}\s*$", "", a).strip(" .,;:—–-")
    f = fold(a)
    if f in ANON or not f:
        return "Anonymous", None
    if f in exact:
        n = exact[f]
        return n, poets[n].get("died")
    toks = f.split()
    cands = by_surname.get(toks[-1], set())
    if len(toks) == 1 and len(cands) == 1:                    # "Macaulay"
        n = next(iter(cands))
        return n, poets[n].get("died")
    if len(toks) >= 2 and cands:                              # "W. Wordsworth", "H. W. Longfellow"
        hit = [n for n in cands if fold(n).split()[0][0] == toks[0][0]]
        if len(hit) == 1:
            return hit[0], poets[hit[0]].get("died")
    return a, None


# ---------------------------------------------------------------------------
# Books
# ---------------------------------------------------------------------------

def pool_books():
    return {b["pg_id"]: b for b in json.load(open(os.path.join(POOL, "sources.json"), encoding="utf-8"))
            if b.get("pg_id") and b.get("fetched") and b.get("shelf") != "church"}


def book_rows():
    out = {}
    d = os.path.join(POOL, "rows")
    for f in sorted(os.listdir(d)):
        out[int(f.split(".")[0])] = B.read_jsonl(os.path.join(d, f))
    return out


def edition_year(b):
    y = b.get("year")
    return y if y and b.get("year_checked") == "text" and y < B.PD_BEFORE else None


def work_name(b):
    w = b["title"]
    if b["pg_id"] == 66619:     # the transcription is the 1931 impression of the unchanged 1900 first edition
        w += " (first edition 1900; this file is its 1931 impression, the same text)"
    return w


def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:  # noqa: BLE001 -- retried, then reported
            time.sleep(2 ** k)
    return None


def fetch_and_pin(books):
    """Fetch every pool book not yet in sources.json into the build's corpus
    and pin it. A book already pinned is the build's to fetch (--fetch)."""
    path = os.path.join(B.DATA, "sources.json")
    src = json.load(open(path, encoding="utf-8"))
    os.makedirs(B.CORPUS, exist_ok=True)
    bad = []
    for n, b in sorted(books.items()):
        key = str(n)
        if key in src["books"]:
            continue
        url = f"https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt"
        blob = get(url)
        if not blob and b.get("raw_url"):
            url, blob = b["raw_url"], get(b["raw_url"])
        if not blob:
            bad.append(n)
            continue
        B.write_atomic(B.book_path(key), blob)
        head = blob[:6000].decode("utf-8", errors="replace")
        src["books"][key] = {
            "title": b["title"], "raw_url": url, "gutenberg_url": B.gutenberg_url(n),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "copyrighted_header": bool(re.search(r"COPYRIGHTED\s+PROJECT\s+GUTENBERG", head, re.I)),
        }
        print(f"  pinned {n:>6}  {len(blob):>9,} bytes  {b['title'][:60]}")
        time.sleep(1)
    src["books"] = dict(sorted(src["books"].items(), key=lambda kv: int(kv[0])))
    B.write_atomic(path, (json.dumps(src, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    for n in bad:
        print(f"  FAILED {n}")
    return not bad


# ---------------------------------------------------------------------------
# Cutting
# ---------------------------------------------------------------------------

def loose(line):
    """A whole line as a pattern, allowing Gutenberg's _italic_ underscores
    and any indentation or trailing space."""
    core = r"[\s_]+".join(re.escape(w) for w in line.strip().strip("_").split())
    return r"^[\s_]*" + core + r"[\s_]*$"


def member_row(entry, rows):
    """The book's own row for this candidate: same first line, else same
    title and author surname, else same title."""
    fl8 = words(entry.get("first_line"), 8)
    for r in rows:
        if fl8 and len(fl8.split()) >= 4 and words(r.get("first_line"), 8) == fl8:
            return r
    t, s = fold(entry["title"]), (fold(entry.get("author")).split() or [""])[-1]
    for r in rows:
        if fold(r["title"]) == t and s and s in fold(r.get("author")):
            return r
    same = [r for r in rows if fold(r["title"]) == t]
    return same[0] if len(same) == 1 else None


def try_cut(lines, row, next_row, surname):
    """(text, rule) or (None, why), cut with the build's own extract()."""
    fl = (row.get("first_line") or "").strip()
    if len(fold(fl).split()) < 2:
        return None, "no usable first line"
    pat = loose(fl)
    hits = [i for i, l in enumerate(lines) if re.search(pat, l)]
    if not hits:
        return None, "first line not found as a line of its own"
    want = B.norm(row["title"])
    pick = None
    for k, i in enumerate(hits):
        if B._in_contents(lines, i):
            continue
        above = [B._clean_heading(l) for l in lines[max(0, i - 8):i] if l.strip()]
        if want and any(want == a or (len(want) > 8 and want in a) for a in above):
            pick = k
            break
        if pick is None and k == 0 and len(hits) == 1:
            pick = k                      # an untitled rhyme: its one occurrence
    if pick is None:
        return None, "no occurrence of the first line under its title"
    rule = {"first_line": pat, "occurrence": pick}
    text, how = B.extract(lines, row["title"], rule)
    if text is None:
        return None, how
    body = text.split("\n")
    # an attribution line at the foot ("--Keats", "JOHN KEATS", "Anonymous")
    last = body[-1].strip()
    alone = len(body) > 2 and not body[-2].strip()          # the last line stands as a stanza of its own
    if len(body) > 2 and len(last) <= 50 and (
            re.match(r"^[—–-]", last) or (surname and surname in fold(last) and len(fold(last).split()) <= 5)
            or fold(last) in ANON
            or (alone and re.fullmatch(r"(?:[A-Z]\.\s?){1,3}(?:[A-Z][a-z]+\.?)?", last))      # "R. H.", "L. W."
            or (alone and re.fullmatch(r"\((?:Condensed|Abridged|Abbreviated)\.?\)|.*\((?:Condensed|Abridged)\)", last))
            or (alone and re.match(r"^From the [A-Z][a-z]+ of ", last))):
        rule["end"] = loose(last)
        text, how = B.extract(lines, row["title"], rule)
        if text is None:
            return None, how
    # run into the next poem of the book?
    if next_row:
        nt, nfl = B.norm(next_row["title"]), fold(next_row.get("first_line"))
        for l in text.split("\n"):
            if (nfl and len(nfl.split()) >= 3 and fold(l) == nfl) or (nt and len(nt) > 3 and B._clean_heading(l) == nt):
                return None, "the cut runs into the next poem"
    n = text.count("\n") + 1
    if n < 2:
        return None, "the cut is a single line"
    if n > LONGEST:
        return None, f"the cut is {n} lines: it has run on"
    if B._prose(text):
        return None, "the cut reads as prose"
    if "[" in text or text[0].islower():
        return None, "the cut holds an editor's bracketed note"
    return text, rule


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="fetch and pin the pool's books first")
    a = ap.parse_args()
    books = pool_books()
    if a.fetch and not fetch_and_pin(books):
        print("  some fetches failed; rerun (resumable)")
    sources = B.load_sources()["books"]
    rows = book_rows()
    poets, exact, by_surname = poet_table()
    pool = B.read_jsonl(os.path.join(POOL, "pool.jsonl"))

    taken = set()                                           # citations already in the AO list or the addendum
    for layer in ("ao", "addendum-heroic"):
        for r in B.read_jsonl(os.path.join(B.SEL, f"{layer}.jsonl")):
            taken.add(B.citation(r))
    loaded = {}

    def lines_of(n):
        if n not in loaded:
            s = sources.get(str(n))
            loaded[n] = B.read_book(str(n), s)[0] if s else None
        return loaded[n]

    order = lambda n: (0 if edition_year(books.get(n, {})) else 1, n)   # noqa: E731
    out, used, stats = [], {}, {"verse": 0, "prose": 0, "already": 0, "cut": 0, "link": 0}
    for e in pool:
        if e["kind"] == "prose":
            stats["prose"] += 1
            continue
        if e.get("also_in"):
            stats["already"] += 1
            continue
        stats["verse"] += 1
        poet, died = canonical(e.get("author"), poets, exact, by_surname)
        sur = (fold(poet).split() or [""])[-1] if poet != "Anonymous" else ""
        sel = {"poet": poet, "poet_died": died, "title": e["title"], "year": None, "term": None,
               "order": None, "pool_id": e["pool_id"], "n_books": e["n_books"], "books": e["books"]}
        tried = []
        for n in sorted(e["books"], key=order):
            b = books.get(n)
            if not b or str(n) not in sources or sources[str(n)].get("copyrighted_header"):
                tried.append(f"#{n} not pinned")
                continue
            lines = lines_of(n)
            if lines is None:
                tried.append(f"#{n} not fetched")
                continue
            rs = rows.get(n, [])
            r = member_row(e, rs)
            if not r:
                tried.append(f"#{n} no row")
                continue
            nxt = next((x for x in rs if x["order"] == r["order"] + 1), None)
            text, rule = try_cut(lines, r, nxt, sur)
            if text is None:
                tried.append(f"#{n} {rule}")
                continue
            sel["pd_source"] = {"gutenberg": n, "work": work_name(b), "edition_year": edition_year(b) or (
                1900 if n == 66619 else None)}
            if fold(r["title"]) != fold(e["title"]):
                sel["printed_title"] = r["title"]
            sel["extract"] = rule
            sel["first_line"] = r["first_line"].strip()
            sel["notes"] = f"Cut from #{n} at its first line, \"{r['first_line'].strip()}\"; in {e['n_books']} of the pool's books."
            break
        if "pd_source" not in sel:
            n = sorted(e["books"], key=order)[0]
            b = books.get(n, {})
            sel["pd_source"] = {"gutenberg": n, "work": b.get("title") or f"PG #{n}", "edition_year": edition_year(b)}
            sel["no_text_reason"] = "no clean cut: " + "; ".join(tried)[:300]
            sel["notes"] = f"In {e['n_books']} of the pool's books; not cut yet."
            stats["link"] += 1
        else:
            stats["cut"] += 1
        cit = B.citation(sel)
        if cit in taken or cit in used:
            sel["variant"] = B.slug(words(e.get("first_line") or e["pool_id"], 4)) or e["pool_id"]
            cit = B.citation(sel)
            if cit in taken or cit in used:
                sel["variant"] = e["pool_id"]
                cit = B.citation(sel)
        used[cit] = True
        out.append(sel)
    B.write_atomic(OUT, B.jsonl(out))
    print(f"  {stats['verse']} verse candidates: {stats['cut']} cut, {stats['link']} linked out; "
          f"{stats['already']} already in AO or the addendum; {stats['prose']} prose pieces left for later")
    print(f"  wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
