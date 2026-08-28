#!/usr/bin/env python3
"""fetch_sources.py — manifest-driven fetcher for the structured shelves.

Three libraries (canon-corpus owns ALL fetching since the 2026-07-22
extraction from patrimonium — patrimonium's mine_names.py keeps its own
copy of the miner corpus, but the structure layer fetches here):

  PERSEUS   — TEI XML with canonical citations born-in (CTS URNs).
              Source: PerseusDL/canonical-greekLit + canonical-latinLit on GitHub.
  CCEL      — ThML XML with scripture references pre-tagged (scripRef).
              Source: ccel.org; URL pattern /ccel/<initial>/<author>/<work>.xml
  GUTENBERG — plain .txt by ebook id (KJV, Shakespeare, the verse/prose shelf).

These manifests ARE the collection: commit history is the acquisitions
ledger. Downloads land in data/corpus/ (gitignored, refetchable).
Resumable: existing files are skipped.

Run:  python3 pipeline/fetch_sources.py            # fetch everything missing
      python3 pipeline/fetch_sources.py --list     # show the manifests
"""
import os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "data", "corpus")

RAW = "https://raw.githubusercontent.com/PerseusDL/{repo}/master/data/{path}"

# slug -> (repo, path, note)   — PD status verified per edition, see notes
PERSEUS = {
    "iliad-butler": ("canonical-greekLit",
        "tlg0012/tlg001/tlg0012.tlg001.perseus-eng4.xml",
        "Homer, Iliad — Samuel Butler 1898 (PD); urn ...tlg0012.tlg001.perseus-eng4"),
    "odyssey-eng4": ("canonical-greekLit",
        "tlg0012/tlg002/tlg0012.tlg002.perseus-eng4.xml",
        "Homer, Odyssey — English (eng4; translator recorded from TEI header at structure time)"),
    "aeneid-williams": ("canonical-latinLit",
        "phi0690/phi003/phi0690.phi003.perseus-eng2.xml",
        "Virgil, Aeneid — Theodore C. Williams 1910 (PD); urn ...phi0690.phi003.perseus-eng2"),
}

# Gutenberg .txt shelf (structured by structure_texts.py's converters).
# IDs are the acquisitions ledger. The first four migrated here from
# patrimonium's mine_names.py GUTENBERG dict at extraction (2026-07-22).
GUTENBERG_EXTRA = {
    "kjv_bible": 10,              # King James Version (verse-exact scheme)
    "shakespeare": 100,           # Complete Works (drama converter)
    "paradise_lost": 20,          # Milton
    "divine_comedy": 8800,        # Dante, tr. Cary
    "paradise_regained": 58,      # Milton
    "beowulf": 16328,             # tr. Gummere
    "gilgamesh": 11000,           # Old Babylonian, tr. Jastrow & Clay
    "faust": 14591,               # Goethe, tr. Bayard Taylor (original metres)
    "treasure_island": 120,       # Stevenson
}
GUTENBERG_TXT = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"

CCEL_XML = "https://ccel.org/ccel/{initial}/{author}/{work}.xml"

# slug -> (author, work, note)  — all probed 200 on 2026-07-21
CCEL = {
    "owen-mort":        ("owen", "mort", "Of the Mortification of Sin in Believers"),
    "owen-temptation":  ("owen", "temptation", "Of Temptation"),
    "owen-communion":   ("owen", "communion", "Of Communion with God"),
    "owen-glory":       ("owen", "glory", "Meditations on the Glory of Christ"),
    "flavel-fountain":  ("flavel", "fountain", "The Fountain of Life"),
    "bunyan-pilgrim":   ("bunyan", "pilgrim", "The Pilgrim's Progress"),
    "bunyan-holy_war":  ("bunyan", "holy_war", "The Holy War"),
    "edwards-affections": ("edwards", "affections", "Religious Affections"),
    "edwards-works1":   ("edwards", "works1", "Works of Jonathan Edwards, vol. 1 (1834 ed.)"),
}

# Calvin's Commentaries (Calvin Translation Society, 45 vols.) — CCEL's
# "Calvin's Commentaries—Complete" collection. Manifest-Ingest pilot library
# (Word Hoard vault, "Armarium Libraries" 2026-08-28): biggest, best-structured,
# uniformly-formatted CCEL corpus — if the ThML parser survives this, it
# survives the rest of the launch list. Slugs + volume titles confirmed
# against CCEL's own work-info page 2026-08-28; calcom01 probed 200 same day.
CALVIN_COMMENTARIES = {
    "calvin-com01": "Genesis 1-23",
    "calvin-com02": "Genesis 24-50",
    "calvin-com03": "Harmony of the Law, Vol. 1",
    "calvin-com04": "Harmony of the Law, Vol. 2",
    "calvin-com05": "Harmony of the Law, Vol. 3",
    "calvin-com06": "Harmony of the Law, Vol. 4",
    "calvin-com07": "Joshua",
    "calvin-com08": "Psalms 1-35",
    "calvin-com09": "Psalms 36-66",
    "calvin-com10": "Psalms 67-92",
    "calvin-com11": "Psalms 93-119",
    "calvin-com12": "Psalms 119-150",
    "calvin-com13": "Isaiah 1-16",
    "calvin-com14": "Isaiah 17-32",
    "calvin-com15": "Isaiah 33-48",
    "calvin-com16": "Isaiah 49-66",
    "calvin-com17": "Jeremiah-Lamentations 1-9",
    "calvin-com18": "Jeremiah-Lamentations 10-19",
    "calvin-com19": "Jeremiah-Lamentations 20-29",
    "calvin-com20": "Jeremiah-Lamentations 30-47",
    "calvin-com21": "Jeremiah-Lamentations 48-52",
    "calvin-com22": "Ezekiel 1-12",
    "calvin-com23": "Ezekiel 13-20",
    "calvin-com24": "Daniel 1-6",
    "calvin-com25": "Daniel 7-12",
    "calvin-com26": "Hosea",
    "calvin-com27": "Joel-Amos-Obadiah",
    "calvin-com28": "Jonah-Micah-Nahum",
    "calvin-com29": "Habakkuk-Zephaniah-Haggai",
    "calvin-com30": "Zechariah-Malachi",
    "calvin-com31": "Harmony of the Gospels, Vol. 1",
    "calvin-com32": "Harmony of the Gospels, Vol. 2",
    "calvin-com33": "Harmony of the Gospels, Vol. 3",
    "calvin-com34": "John 1-11",
    "calvin-com35": "John 12-21",
    "calvin-com36": "Acts 1-13",
    "calvin-com37": "Acts 14-28",
    "calvin-com38": "Romans",
    "calvin-com39": "1 Corinthians 1-14",
    "calvin-com40": "1 Corinthians 15-16, 2 Corinthians",
    "calvin-com41": "Galatians-Ephesians",
    "calvin-com42": "Philippians-Colossians-Thessalonians",
    "calvin-com43": "Timothy, Titus, Philemon",
    "calvin-com44": "Hebrews",
    "calvin-com45": "Catholic Epistles",
}
for _i in range(1, 46):
    _slug = f"calvin-com{_i:02d}"
    CCEL[_slug] = ("calvin", f"calcom{_i:02d}",
                   f"Commentary on {CALVIN_COMMENTARIES[_slug]} (Calvin Translation Society ed.)")

UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "skip"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if len(data) < 1000:
        raise RuntimeError(f"suspiciously small ({len(data)} bytes): {url}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return f"{len(data):,} bytes"

def main():
    if "--list" in sys.argv:
        for slug, (repo, path, note) in PERSEUS.items():
            print(f"perseus/{slug}: {note}")
        for slug, (author, work, note) in CCEL.items():
            print(f"ccel/{slug}: {note}")
        return
    failures = []
    for slug, (repo, path, note) in PERSEUS.items():
        dest = os.path.join(CORPUS, "perseus", slug + ".xml")
        try:
            print(f"perseus/{slug}: {fetch(RAW.format(repo=repo, path=path), dest)}")
        except Exception as e:
            failures.append(slug); print(f"perseus/{slug}: FAIL {e}")
        time.sleep(0.5)
    for slug, (author, work, note) in CCEL.items():
        dest = os.path.join(CORPUS, "ccel", slug + ".xml")
        url = CCEL_XML.format(initial=author[0], author=author, work=work)
        try:
            print(f"ccel/{slug}: {fetch(url, dest)}")
        except Exception as e:
            failures.append(slug); print(f"ccel/{slug}: FAIL {e}")
        time.sleep(1.0)   # be polite to CCEL
    for slug, gid in GUTENBERG_EXTRA.items():
        dest = os.path.join(CORPUS, slug + ".txt")
        try:
            print(f"gutenberg/{slug}: {fetch(GUTENBERG_TXT.format(id=gid), dest)}")
        except Exception as e:
            failures.append(slug); print(f"gutenberg/{slug}: FAIL {e}")
        time.sleep(0.5)
    print("DONE" + (f" ({len(failures)} failures: {failures})" if failures else " — all fetched/present"))

if __name__ == "__main__":
    main()
