#!/usr/bin/env python3
"""ingest_adler.py — acquire + structure the Adler "Great Books" public-domain
shelf into the canon-corpus structure layer, using the SAME converters as
structure_texts.py. Standalone: touches none of the committed pipeline dicts.

Place this file in canon-corpus/pipeline/ next to structure_texts.py and run:

    python3 pipeline/ingest_adler.py            # fetch + structure everything missing
    python3 pipeline/ingest_adler.py --list     # just show the shelf

It reads pipeline/adler_shelf.json (the acquisitions ledger — commit history is
the ledger), downloads each Gutenberg .txt into data/corpus/adler/ (gitignored,
refetchable), and writes one structured JSON per book into data/books/ — where
armarium.py build picks it up automatically, exactly like every other book.

FIRST PASS: every book routes through the prose (paragraph) converter, so
full-text search works immediately for the whole shelf. Verse/drama/dialogue
fine-structure (true lineation, speaker turns) is the flagged later refinement,
same as the existing Gutenberg verse/drama shelf.

PUBLIC DOMAIN ONLY: every id here was verified to fetch a real PD Gutenberg
edition. No inbox, no private texts — the same posture as the hosted backend.
"""
import os, sys, json, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import structure_texts as st

CORPUS = os.path.join(HERE, "..", "data", "corpus", "adler")
BOOKS = os.path.join(HERE, "..", "data", "books")
LEDGER = os.path.join(HERE, "adler_shelf.json")
TXT = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}


def fetch(gid, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "skip"
    req = urllib.request.Request(TXT.format(id=gid), headers=UA)
    data = urllib.request.urlopen(req, timeout=90).read()
    if len(data) < 1000:
        raise RuntimeError(f"suspiciously small ({len(data)} bytes)")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "wb").write(data)
    return f"{len(data):,} bytes"


def main():
    ledger = json.load(open(LEDGER, encoding="utf-8"))
    if "--list" in sys.argv:
        for slug, b in ledger.items():
            print(f"  pg{b['gutenberg_id']:<6} [{b['kind']:9}] vol {b.get('adler_volume','?'):>2} — {b['title']}")
        print(f"{len(ledger)} books")
        return
    os.makedirs(CORPUS, exist_ok=True)
    os.makedirs(BOOKS, exist_ok=True)
    st.CORPUS = CORPUS
    force = "--force" in sys.argv
    total = 0
    for slug, b in ledger.items():
        src = os.path.join(CORPUS, slug + ".txt")
        out = os.path.join(BOOKS, slug + ".json")
        try:
            state = fetch(b["gutenberg_id"], src)
        except Exception as e:
            print(f"  FETCH FAIL {slug}: {e}")
            continue
        if os.path.exists(out) and not force:
            book = json.load(open(out, encoding="utf-8"))
            print(f"  {slug}: {len(book['units'])} units (kept)")
            total += len(book["units"])
            continue
        book = st.convert_gutenberg_prose(src, slug, b["title"], b["author"], b["chapre"])
        seen = {}
        for u in book["units"]:
            if u["id"] in seen:
                seen[u["id"]] += 1
                u["id"] = f"{u['id']}~{seen[u['id']]}"
            else:
                seen[u["id"]] = 1
        # annotate scheme with Adler provenance + refinement flag
        book["scheme"]["adler_volume"] = b.get("adler_volume")
        if b.get("refine"):
            book["scheme"]["honesty"] += " — verse/drama/dialogue: paragraph-level first pass, fine-structure pending"
        with open(out + ".tmp", "w", encoding="utf-8") as f:
            json.dump(book, f, ensure_ascii=False)
        os.replace(out + ".tmp", out)
        total += len(book["units"])
        print(f"  {slug}: {len(book['units'])} units — {book['title']} [{state}]")
    print(f"ADLER SHELF: {len(ledger)} books, {total:,} units into data/books/")


if __name__ == "__main__":
    main()
