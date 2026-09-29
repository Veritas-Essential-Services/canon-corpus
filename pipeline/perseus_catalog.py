#!/usr/bin/env python3
"""Catalog of the gathered Perseus repositories -- WITHOUT converting them.
Reads each textgroup's and work's __cts__.xml and writes perseus_catalog.csv:
repo, CTS URN, author, work title, edition or translation, language, file,
size. Licence: CC BY-SA 4.0 -- anything built on it carries the same licence;
keep Word Hoard layers separate, cite by URN.

    python3 pipeline/perseus_catalog.py --fetch   # shallow-clone the repos, then catalog
    python3 pipeline/perseus_catalog.py           # catalog what is already here

The repos land in data/corpus/perseus/<repo>/ (gitignored, ~1.1 GB for all
three). 2026-09-28 gathered them as GitHub master-branch zips; both zips were
cut off partway (no central directory; see _to_delete/). A shallow clone is
resumable where a 400 MB zip is not, so --fetch clones. A zip named
<repo>.zip, here or in data/corpus/perseus/, is still read if no clone exists.
The commit each clone was cataloged at is written beside the CSV."""
import csv, json, os, subprocess, sys, zipfile, xml.etree.ElementTree as ET
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HERE, "..", "data", "corpus", "perseus")
REPOS = ("canonical-greekLit", "canonical-latinLit")
EXTRA = ("lexica",)  # fetched for the dictionaries (LSJ, Lewis & Short); no __cts__ works to catalog
NS = {"ti": "http://chs.harvard.edu/xmlns/cts", "dc": "http://purl.org/dc/elements/1.1/"}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def fetch():
    os.makedirs(DEST, exist_ok=True)
    for repo in REPOS + EXTRA:
        path = os.path.join(DEST, repo)
        if os.path.isdir(os.path.join(path, ".git")):
            print(repo, "kept", flush=True)
            continue
        subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/PerseusDL/{repo}", path], check=True)


class Source:
    """One repo, read from a clone if there is one, else from its zip."""
    def __init__(self, repo):
        self.dir = os.path.join(DEST, repo)
        if os.path.isdir(os.path.join(self.dir, "data")):
            self.zip, self.prefix = None, repo + "/"
            self.sizes = {}
            for root, _, files in os.walk(os.path.join(self.dir, "data")):
                for f in files:
                    p = os.path.join(root, f)
                    self.sizes[self.prefix + os.path.relpath(p, self.dir).replace(os.sep, "/")] = os.path.getsize(p)
            self.commit = subprocess.run(["git", "-C", self.dir, "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip() or None
        else:
            z = next((p for p in (repo + ".zip", os.path.join(DEST, repo + ".zip")) if os.path.exists(p)), None)
            if z is None:
                sys.exit(f"{repo}: no clone in {DEST} and no {repo}.zip; run with --fetch")
            self.zip = zipfile.ZipFile(z)
            self.sizes = {i.filename: i.file_size for i in self.zip.infolist()}
            self.commit = None
        self.names = list(self.sizes)

    def read(self, name):
        if self.zip:
            return self.zip.read(name)
        with open(os.path.join(self.dir, name.split("/", 1)[1]), "rb") as f:
            return f.read()


def catalog():
    rows, pinned = [], {}
    for repo in REPOS:
        src = Source(repo)
        pinned[repo] = src.commit
        # a zip's paths start with "<repo>-master/", a clone's with "<repo>/";
        # either way a textgroup's __cts__ sits 3 slashes deep and a work's 4
        groups = {}
        for n in src.names:
            if n.endswith("__cts__.xml") and n.count("/") == 3:
                r = ET.fromstring(src.read(n)); g = r.find("ti:groupname", NS)
                groups[r.get("urn")] = g.text.strip() if g is not None and g.text else ""
        for n in src.names:
            if n.endswith("__cts__.xml") and n.count("/") == 4:
                r = ET.fromstring(src.read(n)); work = r.get("urn")
                t = r.find("ti:title", NS); title = t.text.strip() if t is not None and t.text else ""
                for kind in ("edition", "translation", "commentary"):
                    for e in r.findall("ti:" + kind, NS):
                        urn = e.get("urn"); lang = e.get(XML_LANG) or r.get(XML_LANG) or ""
                        lab = e.find("ti:label", NS)
                        f = n.rsplit("/", 1)[0] + "/" + urn.split(":")[-1] + ".xml"
                        rows.append([repo, urn, groups.get(work.rsplit(".", 1)[0], ""), title, kind,
                                     (lab.text or "").strip() if lab is not None else "", lang, f, src.sizes.get(f, "")])
    os.makedirs(DEST, exist_ok=True)
    out = os.path.join(DEST, "perseus_catalog.csv")
    with open(out + ".tmp", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["repo", "urn", "author", "work", "kind", "label", "lang", "file", "bytes"]); w.writerows(rows)
    os.replace(out + ".tmp", out)
    with open(os.path.join(DEST, "perseus_catalog.pinned.json"), "w", encoding="utf-8") as fh:
        json.dump(pinned, fh, indent=1)
    print(out)
    print(len(rows), "editions/translations;", Counter((r[0], r[4]) for r in rows))
    print("authors:", len({(r[0], r[2]) for r in rows}), " works:", len({r[1].rsplit('.', 1)[0] for r in rows}))
    print("missing files:", sum(1 for r in rows if r[8] == ""))
    return rows


if __name__ == "__main__":
    if "--fetch" in sys.argv:
        fetch()
    catalog()
