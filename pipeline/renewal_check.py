#!/usr/bin/env python3
"""Was a 1931-1963 US book's copyright renewed? An offline search of the renewal records.

    python3 pipeline/renewal_check.py --fetch                    # the renewal records, pinned (~140 MB, gitignored)
    python3 pipeline/renewal_check.py "Roy J. Snell" "The Magic Curtain"
    python3 pipeline/renewal_check.py --surname snell            # every renewal naming the surname, 1931-1963 works
    python3 pipeline/renewal_check.py --reg A5267                # a registration number

Why this exists (2026-11-03, Adam: "I want everything that was not renewed"):
a US book published 1931-1963 with a copyright notice is US public domain if
its copyright was not renewed in its 28th year. The renewals are printed in
the Catalog of Copyright Entries (1950-1977) and kept in the Copyright
Office's database (1978 on). NYPL transcribed and parsed all of them into one
dataset (github.com/NYPL/cce-renewals, CC0), the same records Stanford's
Copyright Renewal Database searches, with every registration number and date
split out so that a MISSING match can be trusted. It is pinned here by commit.

The search is deliberately loose, so that a miss means something: a renewal
row is a candidate when its author field or its full printed text names the
surname AND it shares at least half of the title's significant words (or the
registration number matches). Every candidate is printed; a person reads them
and decides. An empty result is "no renewal found", never "not renewed for
certain": the transcriptions have gaps, and a book renewed under a different
title or under its publisher's name alone can slip past a title search.

Not answered here, on purpose:
  - whether the book carried a notice or was registered at all (a 1931-1963
    book with no notice is public domain anyway);
  - URAA restoration: a book first published abroad by a foreign author can
    be US copyright again whatever its renewal says (17 USC 104A). A shelf
    records that check by hand, per book, beside the renewal search.
"""
import argparse, csv, glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
REPO = "https://github.com/NYPL/cce-renewals.git"
PIN = "ebb615621f255694a562faf0a2db1b1cc4cfaabf"   # 2019-05-01, the dataset's last commit
DIR = os.path.join(ROOT, "data", "corpus", "cce-renewals")

STOP = set("a an and the of in on to for by with from at as or its his her their our your into upon "
           "le la les de du des der die das und".split())

csv.field_size_limit(10**8)


def fetch():
    if os.path.isdir(os.path.join(DIR, ".git")):
        have = subprocess.run(["git", "-C", DIR, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        if have == PIN:
            print("have", PIN); return
    os.makedirs(os.path.dirname(DIR), exist_ok=True)
    if not os.path.isdir(DIR):
        subprocess.run(["git", "clone", "-q", REPO, DIR], check=True)
    subprocess.run(["git", "-C", DIR, "fetch", "-q", "origin", PIN], check=False)
    subprocess.run(["git", "-C", DIR, "checkout", "-q", PIN], check=True)
    print("pinned", PIN)


def norm(s):
    return re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower().replace("'", ""))


def words(s):
    return [w for w in norm(s).split() if w not in STOP and len(w) > 1]


_ROWS = None


def rows():
    """Every renewal row, (file, author, title, oreg, odat, rid, rdat, full_text),
    with its normalised text and word set, computed once."""
    global _ROWS
    if _ROWS is not None:
        return _ROWS
    files = sorted(glob.glob(os.path.join(DIR, "data", "*.tsv")))
    if not files:
        sys.exit(f"no renewal records in {DIR}: run --fetch")
    out = []
    for f in files:
        with open(f, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                row = (os.path.basename(f),
                       r.get("author") or r.get("auth") or "",
                       r.get("title") or r.get("titl") or "",
                       r.get("oreg") or "", r.get("odat") or "",
                       r.get("id") or "", r.get("rdat") or r.get("dreg") or "",
                       (r.get("full_text") or "") + " " + (r.get("claimants") or "") + " " + (r.get("note") or r.get("notes") or ""))
                blob = " " + norm(row[1] + " " + row[2] + " " + row[7]) + " "
                out.append((row, blob, set(words(row[2] + " " + row[7]))))
    _ROWS = out
    return out


def surname_of(author):
    a = re.sub(r"\(.*?\)", " ", author)
    parts = [p for p in norm(a).split() if p not in ("jr", "sr", "ii", "iii", "tr", "ed", "rev", "dr", "sir")]
    return parts[-1] if parts else ""


def search(author=None, title=None, reg=None, surname=None):
    sn = (surname or (surname_of(author) if author else "")).lower()
    tw = set(words(title)) if title else set()
    need = max(1, (len(tw) + 1) // 2) if tw else 0
    regn = re.sub(r"[^A-Z0-9]", "", reg.upper()) if reg else None
    hits = []
    for row, blob, rw in rows():
        f, au, ti, oreg, odat, rid, rdat, full = row
        if regn and re.sub(r"[^A-Z0-9]", "", oreg.upper()) == regn:
            hits.append(("reg", row)); continue
        if not sn:
            continue
        if f" {sn} " not in blob:
            continue
        if tw:
            got = tw & rw
            if len(got) >= need:
                hits.append((f"title {len(got)}/{len(tw)}", row))
        else:
            hits.append(("surname", row))
    return hits


def full_hits(hits):
    """The candidates that carry EVERY significant word of the title."""
    out = []
    for why, row in hits:
        m = re.match(r"title (\d+)/(\d+)", why)
        if why == "reg" or (m and m.group(1) == m.group(2)):
            out.append((why, row))
    return out


def verdict(author, title, reg=None):
    """One line for a shelf's evidence note."""
    hits = search(author=author, title=title, reg=reg)
    if not hits:
        return "no renewal found", []
    return f"{len(hits)} candidate renewal(s): read them", hits


def show(hits, limit=60):
    for why, (f, au, ti, oreg, odat, rid, rdat, full) in hits[:limit]:
        print(f"  [{why}] {f}: {au} | {ti[:90]} | reg {oreg} {odat} -> {rid} {rdat}")
    if len(hits) > limit:
        print(f"  ... {len(hits) - limit} more")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--surname")
    ap.add_argument("--reg")
    ap.add_argument("author", nargs="?")
    ap.add_argument("title", nargs="?")
    a = ap.parse_args()
    if a.fetch:
        fetch(); return
    hits = search(author=a.author, title=a.title, reg=a.reg, surname=a.surname)
    if a.surname and not a.title:
        hits = [h for h in hits if h[1][4][:4].isdigit() and 1931 <= int(h[1][4][:4]) <= 1963 or not h[1][4]]
    print(f"{len(hits)} candidate(s)")
    show(hits, 200)


if __name__ == "__main__":
    main()
