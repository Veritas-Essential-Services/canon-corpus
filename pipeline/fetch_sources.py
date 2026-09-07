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

# ---------------------------------------------------------------- Lexicons
#
# Reference works keyed by lemma rather than linear texts (structured by
# structure_texts.py's lexicon converters). All three underlying works are
# public domain; the rights line of the exact edition was read, per the
# 2026-07-26 standing rule, and is recorded per entry below.
#
# THAYER'S is here too, but it is not a fetch -- it is an OCR job, and the
# only one in this repo. The 1889 lexicon is PD and scanned (archive.org
# greekenglishlexi00grimuoft, 760pp, NOT_IN_COPYRIGHT), but no machine-readable
# edition exists: that scan's own text layer contains ZERO Greek codepoints --
# every Greek word came out as mangled Latin ("edris" for elpis). Abbott-Smith
# 1922 fails identically. So on 2026-09-06 the PDF was re-OCR'd with tesseract
# grc+eng at 300dpi, recovering 552,594 Greek characters, and the page text
# lives in data/corpus/lexicons/thayer-pages.json (gitignored with the rest of
# the corpus; regenerate with the recipe in CLAUDE.md).
#
# slug -> (url, local filename, note)
LEXICONS = {
    "strongs-hebrew": (
        "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml",
        "strongs-hebrew.xml",
        "Strong's Hebrew Dictionary (James Strong, 1890 — PD). OpenScriptures "
        "HebrewLexicon transcription; markup CC BY 4.0, dictionary text PD. "
        "8,674 entries = the complete H1–H8674 numbering (verified 2026-09-06)."),
    "strongs-greek": (
        "https://raw.githubusercontent.com/openscriptures/strongs/master/"
        "greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml",
        "strongs-greek.xml",
        "Strong's Greek Dictionary (James Strong, 1890 — PD). OpenScriptures "
        "strongs repo. 5,624 entries = the complete G1–G5624 numbering "
        "(verified 2026-09-06). Unicode Greek intact."),
    # STEPBible Greek. CC BY 4.0 — NOT public domain, and the only non-PD
    # material in this repo. Adam's call, 2026-09-06: collect and use, do not
    # redistribute in whole. The licence permits redistribution; the
    # maintainers ASK that people be pointed at github.com/STEPBible instead
    # so corrections flow from one source. Honored structurally, not just in
    # prose: these land in data/corpus/ and build to data/books/*.json, both
    # gitignored, so only the manifest pointer is ever committed. The built
    # books carry rights.redistribute_whole = false; anything serving this
    # corpus must respect it.
    "tbesg-greek": (
        "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
        "TBESG%20-%20Translators%20Brief%20lexicon%20of%20Extended%20Strongs%20for%20Greek%20-%20STEPBible.org%20CC%20BY.txt",
        "tbesg-greek.txt",
        "Translators Brief lexicon of Extended Strongs for Greek — Abbott-Smith "
        "(1922, PD) definitions edited to extended Strong's by Tyndale House. "
        "CC BY 4.0. 9,550 entries."),
    "tflsj-greek-0-5624": (
        "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
        "TFLSJ%20%200-5624%20-%20Translators%20Formatted%20full%20LSJ%20Bible%20lexicon%20-%20STEPBible.org%20CC%20BY.txt",
        "tflsj-greek-0-5624.txt",
        "Full Liddell-Scott-Jones, Bible edition, G0-G5624 — LSJ edited by "
        "Tyndale House scholars. CC BY 4.0. 5,709 entries, 2.17M Greek chars."),
    "tflsj-greek-extra": (
        "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
        "TFLSJ%20extra%20-%20Translators%20Formatted%20full%20LSJ%20Bible%20lexicon%20-%20STEPBible.org%20CC%20BY.txt",
        "tflsj-greek-extra.txt",
        "Full LSJ, the G6000+ extras (LXX and variant vocabulary beyond Strong's "
        "range). CC BY 4.0. 3,840 entries."),
    "bdb-hebrew": (
        "https://raw.githubusercontent.com/eliranwong/unabridged-BDB-Hebrew-lexicon/"
        "master/unabridged-BDB-Hebrew-lexicon.csv.zip",
        "bdb-hebrew.tsv",
        "Brown-Driver-Briggs, A Hebrew and English Lexicon of the Old Testament "
        "(1906 — PD), UNABRIDGED. Repo states 'Public domain document'; formatting "
        "by Eliran Wong from Bible Analyzer data, scripture refs parsed by Stephen "
        "Ku et al. 10,022 entries, median 1,184 chars (the real thing, not the "
        "2.7MB abridged outline in OpenScriptures/HebrewLexicon)."),
}


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

def fetch_lexicon(url, dest):
    """Same as fetch(), but a .zip source is unpacked to `dest` — the BDB
    ships zipped and its inner filename is not stable enough to rely on, so
    take the single largest member."""
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "skip"
    if not url.endswith(".zip"):
        return fetch(url, dest)
    import io, zipfile
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        blob = r.read()
    zf = zipfile.ZipFile(io.BytesIO(blob))
    members = [m for m in zf.infolist()
               if not m.is_dir() and "__MACOSX" not in m.filename]
    if not members:
        raise RuntimeError(f"no usable member in {url}")
    biggest = max(members, key=lambda m: m.file_size)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(zf.read(biggest))
    return f"{biggest.file_size:,} bytes (unzipped {biggest.filename})"


def main():
    if "--list" in sys.argv:
        for slug, (repo, path, note) in PERSEUS.items():
            print(f"perseus/{slug}: {note}")
        for slug, (author, work, note) in CCEL.items():
            print(f"ccel/{slug}: {note}")
        for slug, (url, fn, note) in LEXICONS.items():
            print(f"lexicon/{slug}: {note}")
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
    for slug, (url, fn, note) in LEXICONS.items():
        dest = os.path.join(CORPUS, "lexicons", fn)
        try:
            print(f"lexicon/{slug}: {fetch_lexicon(url, dest)}")
        except Exception as e:
            failures.append(slug); print(f"lexicon/{slug}: FAIL {e}")
        time.sleep(0.5)
    print("DONE" + (f" ({len(failures)} failures: {failures})" if failures else " — all fetched/present"))

if __name__ == "__main__":
    main()
