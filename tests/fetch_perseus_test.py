#!/usr/bin/env python3
"""Offline checks for pipeline/fetch_perseus.py's gates (no network, no corpus).

    python3 tests/fetch_perseus_test.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import fetch_perseus as fp

PASS = []

def ok(cond, msg):
    if not cond:
        sys.exit(f"FAIL: {msg}")
    PASS.append(msg)

def tei(title_extra="", years="1920-1925", note=""):
    return (f"""<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>
<title>The Histories {title_extra}</title><author>Herodotus</author><editor>A. D. Godley</editor>
</titleStmt><sourceDesc><bibl><author>Herodotus</author><editor>A.D. Godley</editor>
<date>{years}</date></bibl></sourceDesc></fileDesc>{note}</teiHeader>
<text><body>tlg0016.tlg001.perseus-eng2 In Egypt</body></text></TEI>""").encode()

SHELF = {"_surname": ["herodotus"], "_translators": {"h": "A. D. Godley"}}

def refused(data, shelf, prefix):
    try:
        fp._check(data, "tlg0016.tlg001.perseus-eng2", "A. D. Godley", "h", shelf)
    except RuntimeError as e:
        return str(e).startswith(prefix)
    return False

# a plain early Loeb passes, and records its years
r, misses = fp._check(tei(), "tlg0016.tlg001.perseus-eng2", "A. D. Godley", "h", SHELF)
ok(not misses and r["source_years"] == [1920, 1925], "plain 1920-25 file kept with its years")
ok("modernized" not in r, "plain file carries no modernized flag")

# a Perseus-modernized file is refused without a stated reason ...
mod = tei("Modernized by Perseus", note="<encodingDesc><p>This text was modernized by Steven Ott, to remove archaisms.</p></encodingDesc>")
ok(refused(mod, SHELF, "RIGHTS: the header says the text was modernized"), "modernized file refused without _rights_checked")
# ... and kept with one, the phrase and the reason recorded
kept = dict(SHELF, _rights_checked={"h": "modernized witness, put to Adam"})
r, misses = fp._check(mod, "tlg0016.tlg001.perseus-eng2", "A. D. Godley", "h", kept)
ok(not misses and "Modernized by Perseus" in r["modernized"], "modernized file kept with a reason, phrase recorded")
ok(r["rights_override"] == "modernized witness, put to Adam", "the reason is recorded as rights_override")

# a later printing is refused without a reason (the gate is fail-closed at 1930)
ok(refused(tei(years="1919 1958"), SHELF, "RIGHTS: source year 1958"), "1958 printing refused without _rights_checked")
ok(refused(tei(years=""), SHELF, "RIGHTS: no year"), "no year in sourceDesc refused without _rights_checked")

# the rights block a kept finding carries
b = fp.rights_block({"markup_licence_repo": "CC BY-SA 4.0 (repository README)", "url": "https://example/x.xml",
                     "modernized": "Modernized by Perseus"})
ok(b["redistribute_whole"] is False and b["share_alike"] is True, "rights block: share-alike, not redistributed whole")
ok(b["license"].startswith("CC BY-SA 4.0") and b["source_url"] == "https://example/x.xml", "rights block: licence and source")
ok("modernized text" in b["attribution"], "rights block names the modernized layer in the attribution")
b = fp.rights_block({"markup_licence_in_file": "https://creativecommons.org/licenses/by-sa/4.0/",
                     "markup_licence_repo": "CC BY-SA 4.0 (repository README)"})
ok(b["license"].startswith("https://creativecommons.org"), "rights block prefers the licence stated in the file")
ok("modernized" not in b["attribution"], "unmodernized file's attribution names only the markup")

print(f"fetch_perseus_test: {len(PASS)} checks passed")
