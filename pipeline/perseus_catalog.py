#!/usr/bin/env python3
"""Catalog of the gathered Perseus repositories -- WITHOUT unpacking them.
Reads each textgroup's and work's __cts__.xml straight out of the zips and
writes perseus_catalog.csv: repo, CTS URN, author, work title, edition or
translation, language, file, size. Gathered 2026-09-28 from PerseusDL on
GitHub (master branch zips). Licence: CC BY-SA 4.0 -- anything built on it
carries the same licence; keep Word Hoard layers separate, cite by URN."""
import csv, re, zipfile, xml.etree.ElementTree as ET
NS = {"ti": "http://chs.harvard.edu/xmlns/cts", "dc": "http://purl.org/dc/elements/1.1/"}
rows = []
for repo in ("canonical-greekLit", "canonical-latinLit"):
    z = zipfile.ZipFile(repo + ".zip")
    names = z.namelist(); sizes = {i.filename: i.file_size for i in z.infolist()}
    groups = {}
    for n in names:
        if n.endswith("__cts__.xml") and n.count("/") == 3:
            r = ET.fromstring(z.read(n)); g = r.find("ti:groupname", NS)
            groups[r.get("urn")] = g.text.strip() if g is not None and g.text else ""
    for n in names:
        if n.endswith("__cts__.xml") and n.count("/") == 4:
            r = ET.fromstring(z.read(n)); work = r.get("urn")
            t = r.find("ti:title", NS); title = t.text.strip() if t is not None and t.text else ""
            for kind in ("edition", "translation", "commentary"):
                for e in r.findall("ti:" + kind, NS):
                    urn = e.get("urn"); lang = e.get("{http://www.w3.org/XML/1998/namespace}lang") or r.get("{http://www.w3.org/XML/1998/namespace}lang") or ""
                    lab = e.find("ti:label", NS)
                    f = n.rsplit("/", 1)[0] + "/" + urn.split(":")[-1] + ".xml"
                    rows.append([repo, urn, groups.get(work.rsplit(".", 1)[0], ""), title, kind,
                                 (lab.text or "").strip() if lab is not None else "", lang, f, sizes.get(f, "")])
with open("perseus_catalog.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["repo", "urn", "author", "work", "kind", "label", "lang", "file", "bytes"]); w.writerows(rows)
from collections import Counter
print(len(rows), "editions/translations;", Counter((r[0], r[4]) for r in rows))
print("authors:", len({(r[0], r[2]) for r in rows}), " works:", len({r[1].rsplit('.', 1)[0] for r in rows}))
print("missing files:", sum(1 for r in rows if r[8] == ""))
