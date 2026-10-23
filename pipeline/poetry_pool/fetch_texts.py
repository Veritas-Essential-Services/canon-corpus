#!/usr/bin/env python3
"""Fetch the candidate pool's Gutenberg texts into data/corpus/pool-texts/ (gitignored).

The texts are not committed: every one is re-fetchable by its Project
Gutenberg id from data/poetry/pool/sources.json. Resumable; a file already
present is skipped.

    python3 pipeline/poetry_pool/fetch_texts.py
"""
import json, os, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "data", "corpus", "pool-texts")


def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:  # noqa: BLE001 -- retried, then reported
            time.sleep(2 ** k)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    books = json.load(open(os.path.join(ROOT, "data", "poetry", "pool", "sources.json"), encoding="utf-8"))
    bad = []
    for b in books:
        if not b.get("fetched"):
            continue
        n = b["pg_id"]
        p = os.path.join(OUT, f"{n}.txt")
        if os.path.exists(p):
            continue
        blob = get(f"https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt") or (get(b["raw_url"]) if b.get("raw_url") else None)
        if not blob:
            bad.append(n)
            continue
        with open(p + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(p + ".tmp", p)
        print(f"  fetched {n:>6}  {b['title'][:60]}")
    print("  FAILED: " + ", ".join(map(str, bad)) if bad else "  all present")


if __name__ == "__main__":
    main()
