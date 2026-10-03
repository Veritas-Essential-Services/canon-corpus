#!/usr/bin/env python3
"""Strong's numbers against the dictionaries keyed to them: which numbers no
dictionary entry covers, and which entries carry no number.

Reads the committed data/strongs/ (table + witnesses), BDB's source TSV
(data/corpus/lexicons/, gitignored) and, where it has been built, Thayer's
split entries (data/books/thayer-entries.json, PR #7; built only where the OCR
lives). Writes docs/strongs-coverage/: REPORT.md and one TSV per list. Every
list is facts about PD dictionaries (Strong's 1890, BDB 1906, Thayer 1889):
numbers, entry ids and printed headwords, never definitions.

    python3 pipeline/strongs_coverage.py           # write the report
    python3 pipeline/strongs_coverage.py --check   # the report is what the data gives
"""
import collections
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_strongs as B  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "strongs-coverage")
THAYER = os.path.join(ROOT, "data", "books", "thayer-entries.json")
POINTED = re.compile(r"[ְ-ׇּׁׂ]")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def tsv(rows, head):
    return "\t".join(head) + "\n" + "".join("\t".join(str(c) for c in r) + "\n" for r in rows)


def keys_of(u):
    ks = []
    for ln in u.get("links", []):
        if ln.get("kind") == "strongs":
            k, _ = B.normalize(ln["target"].split(":", 1)[1])
            if k:
                ks.append(k)
    if not ks and (u.get("lex") or {}).get("strongs"):     # as build_witnesses reads it
        k, _ = B.normalize(u["lex"]["strongs"])
        if k:
            ks.append(k)
    return list(dict.fromkeys(ks))


def bdb_part(table, wit, bdb_units):
    tab = {t["strongs"]: t for t in table}
    own = {r["strongs"] for r in wit if r["witnesses"].get("bdb")}
    shared = {r["strongs"] for r in wit if r["witnesses"].get("bdb-shared")}
    sem = [t for t in table if t["lang"] in ("hbo", "arc")]
    no_own = [t for t in sem if t["strongs"] not in own]
    lists, facts = {}, {}
    lists["hebrew-numbers-no-bdb-entry"] = (
        [(t["strongs"], t["lang"], t["lemma"], "shared" if t["strongs"] in shared else "none")
         for t in no_own],
        ("strongs", "lang", "lemma", "bdb"))
    facts["semitic_numbers"] = len(sem)
    facts["with_own_bdb_entry"] = len(sem) - len(no_own)
    facts["only_listed_beside_another_word"] = sum(1 for t in no_own if t["strongs"] in shared)
    facts["no_bdb_entry_at_all"] = sum(1 for t in no_own if t["strongs"] not in shared)
    facts["no_bdb_by_lang"] = dict(collections.Counter(t["lang"] for t in no_own
                                                       if t["strongs"] not in shared))
    facts["no_bdb_proper_names"] = sum(1 for t in no_own if t["strongs"] not in shared
                                       and t.get("proper_name"))
    if bdb_units is None:
        return lists, facts
    # entries with no number
    unkeyed = [u for u in bdb_units if not keys_of(u)]
    lemma = lambda u: (u.get("lex") or {}).get("lemma") or ""
    words = [u for u in unkeyed if POINTED.search(lemma(u))]
    lists["bdb-entries-no-strongs"] = (
        [(u["id"].split(":")[1], lemma(u), "word" if u in words else "root or unpointed",
          re.sub(r"\s+", " ", u["text"])[:60]) for u in unkeyed],
        ("bdb", "headword", "kind", "opening (first 60 characters)"))
    facts["bdb_entries"] = len(bdb_units)
    facts["bdb_entries_no_strongs"] = len(unkeyed)
    facts["bdb_entries_no_strongs_pointed_word"] = len(words)
    facts["bdb_entries_no_strongs_see_also"] = sum(1 for u in words if re.search(r"\bsee\b", u["text"][:200]))
    # keyed entries whose numbers spell none of the entry's headwords
    # The source's keys, before data/strongs/bdb-key-overrides.jsonl: each row
    # says which kind it is, and where the key is a slip, what the build uses.
    ov = B.read_bdb_overrides()
    sus, arc_only_heb = [], []
    for u in bdb_units:
        ks = [k for k in keys_of(u) if k in tab]
        if not ks:
            continue
        r = ov.get(u["id"])
        fix = ("override: " + (r["own"] or "drop " + " ".join(r["drop"]))) if r else ""
        want = "arc" if B._bdb_no(u["id"]) >= B.BDB_ARAMAIC_FROM else "hbo"
        if want == "arc" and not any(tab[k]["lang"] == "arc" for k in ks):
            arc_only_heb.append((u["id"].split(":")[1], lemma(u), " ".join(ks),
                                 fix or ("root" if ROOT_ENTRY.search(u["text"][:80]) else "the word's Hebrew number, shared")))
        if not POINTED.search(lemma(u)):
            continue
        heads = B._bdb_heads(u)
        if not any(B._heb_skeleton(tab[k]["lemma"]) in heads for k in ks):
            sus.append((u["id"].split(":")[1], lemma(u),
                        " ".join(f"{k}={tab[k]['lemma']}" for k in ks), fix or suspect_kind(u, ks, heads, tab)))
    lists["bdb-aramaic-entries-hebrew-numbers-only"] = (arc_only_heb, ("bdb", "headword", "numbers", "kind"))
    lists["bdb-keys-not-spelling-headword"] = (sus, ("bdb", "headword", "numbers=Strong's lemma", "kind"))
    facts["bdb_aramaic_entries_hebrew_numbers_only"] = len(arc_only_heb)
    facts["bdb_aramaic_hebrew_only_kinds"] = dict(collections.Counter(r[3].split(":")[0] for r in arc_only_heb))
    facts["bdb_keys_not_spelling_headword"] = len(sus)
    facts["bdb_suspect_kinds"] = dict(collections.Counter(r[3].split(":")[0] for r in sus))
    return lists, facts


# a root heading in BDB's Aramaic part: "√ of following", "root of ..."
ROOT_ENTRY = re.compile(r"√|\broot\b|\bverb\b")


def suspect_kind(u, ks, heads, tab):
    """Why a key that spells no form of the headword is not a slip. Order
    matters: the first that fits is the row's kind."""
    sk = [B._heb_skeleton(tab[k]["lemma"]) for k in ks]
    if any(re.search(r"[\s\u05be]", tab[k]["lemma"].strip()) for k in ks):
        return "compound name"                 # Allon-bachuth under bakuth
    if re.search(r"\bsee\b", u["text"][:120]):
        return "cross-reference"               # "see ..." to the word keyed
    if any(s[:2] in {h[:2] for h in heads} or any(h[:2] in s for h in heads) for s in sk):
        return "related form"                  # plural, variant, derivative
    return "word the entry names"              # a reading it corrects, a cognate


def greek_part(table, wit):
    tab = [t for t in table if t["lang"] == "grc"]
    used = [t for t in tab if not t.get("not_used")]
    w = {r["strongs"]: r["witnesses"] for r in wit}
    facts = {"greek_numbers": len(tab), "greek_numbers_used": len(used)}
    for name in ("tbesg", "lsj", "thayer"):
        facts[f"with_{name}"] = sum(1 for t in used if w.get(t["strongs"], {}).get(name))
    lists = {}
    if os.path.exists(THAYER):
        with open(THAYER, encoding="utf-8") as f:
            units = json.load(f)["units"]
        linked = collections.defaultdict(list)
        unlinked = []
        for u in units:
            ks = keys_of(u)
            for k in ks:
                linked[k].append(u["id"])
            if not ks:
                lex = u.get("lex") or {}
                unlinked.append((u["id"].split(":", 1)[1], lex.get("headword_read") or lex.get("headword") or "",
                                 " ".join(lex.get("strongs_candidates") or [])))
        lists["thayer-entries-no-strongs"] = (unlinked, ("thayer entry", "headword", "candidates"))
        lists["greek-numbers-no-thayer-entry"] = (
            [(t["strongs"], t["lemma"]) for t in used if t["strongs"] not in linked],
            ("strongs", "lemma"))
        facts["thayer_entries"] = len(units)
        facts["thayer_entries_no_strongs"] = len(unlinked)
        facts["greek_numbers_no_thayer_entry"] = len(lists["greek-numbers-no-thayer-entry"][0])
        facts["thayer_built_here"] = True
    else:
        facts["thayer_built_here"] = False
        lists["greek-numbers-no-tbesg-or-lsj"] = (
            [(t["strongs"], t["lemma"]) for t in used
             if not w.get(t["strongs"], {}).get("tbesg") and not w.get(t["strongs"], {}).get("lsj")],
            ("strongs", "lemma"))
    return lists, facts


def kinds(c):
    return ", ".join(f"{v:,} {k}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


def report(facts, lists):
    f = facts
    L = ["# Strong's numbers against BDB and Thayer",
         "",
         "Built by `pipeline/strongs_coverage.py` from the committed `data/strongs/` and the",
         "dictionaries' sources. Rerun it after any rebuild; `--check` fails if this page is stale.",
         "Each list below is a TSV beside this file.",
         "",
         "## Hebrew and Aramaic: Strong's against BDB",
         "",
         f"- {f['semitic_numbers']:,} Hebrew and Aramaic numbers. {f['with_own_bdb_entry']:,} have a BDB entry of their own.",
         f"- {f['only_listed_beside_another_word']:,} appear only in an entry for another word (`bdb-shared`):",
         "  BDB files them under a related word, a spelling or a root.",
         f"- {f['no_bdb_entry_at_all']:,} appear in no BDB entry at all ({', '.join(f'{v:,} {k}' for k, v in sorted(f['no_bdb_by_lang'].items()))}),",
         f"  {f['no_bdb_proper_names']:,} of them proper names. List: `hebrew-numbers-no-bdb-entry.tsv`.",
         ""]
    if "bdb_entries" in f:
        L += [f"- {f['bdb_entries']:,} BDB entries; {f['bdb_entries_no_strongs']:,} carry no Strong's number. "
              f"{f['bdb_entries_no_strongs'] - f['bdb_entries_no_strongs_pointed_word']:,} of those are roots",
              "  or unpointed headings (Strong's numbers words, not roots); "
              f"{f['bdb_entries_no_strongs_pointed_word']:,} are pointed words,",
              f"  {f['bdb_entries_no_strongs_see_also']:,} of them cross-references (\"see ...\"). List: `bdb-entries-no-strongs.tsv`.",
              f"- {f['bdb_aramaic_entries_hebrew_numbers_only']:,} entries in BDB's Aramaic part list only Hebrew numbers",
              "  (the Hebrew cognate). They count as `bdb-shared` unless an override row says otherwise:",
              "  " + kinds(f["bdb_aramaic_hebrew_only_kinds"]) + ". A root heading (\"√ of following\")",
              "  is no word, so no Aramaic number is its own. The rest list the Hebrew number of the same word",
              "  (Strong's numbers a name once, and כֹּר \"Aramaic the same\"); they stay shared, except where",
              "  BDB has no Hebrew entry for the word (H8674 Tattenai): there the override table makes",
              "  the Aramaic entry its own. Slips are in the override table too.",
              "  List: `bdb-aramaic-entries-hebrew-numbers-only.tsv`, with each row's kind.",
              f"- {f['bdb_keys_not_spelling_headword']:,} pointed entries list numbers none of whose Strong's lemmas spells the",
              "  entry's headword, even with plene and defective spellings, -yahu/-yah, and final letters folded.",
              "  By kind: " + kinds(f["bdb_suspect_kinds"]) + ".",
              "  `suspect_kind()` tries compound name, cross-reference, related form, then word the entry",
              "  names, and the first that fits is the row's kind. All but `override` stand",
              "  as the source keys them: plurals, variants and derivatives (`תְּאֻנִים` under H8383),",
              "  compound names, cross-references, and words the entry names (a reading it corrects, the",
              "  word its lemma field also prints). `override` rows are slips in the source's key, e.g.",
              "  BDB7322 קֹדֶשׁ keyed to H6994 (קָטֹן), not H6944. Every entry here for which some Strong's",
              "  lemma spells the headword was read by hand; the slips found are",
              f"  `data/strongs/bdb-key-overrides.jsonl` ({f['bdb_overrides']} rows, each with its reason, the source",
              "  untouched). List: `bdb-keys-not-spelling-headword.tsv`, with each row's kind.",
              ""]
    L += ["### Fixed in this pass (PR #10)",
          "",
          "- **BDB's Aramaic part keyed to the Hebrew word.** It often lists the Hebrew cognate first",
          "  (Aramaic אֶבֶן \"stone\" is `H68_H69`), and the first number was taken as the entry's own, so",
          "  Aramaic entries counted as witnesses of the Hebrew word. Now an entry's own number is in its",
          "  own language: 180 Aramaic entries are now keyed to the Aramaic number they list, and the 87",
          "  that list only Hebrew numbers no longer count as the Hebrew word's entry. The other way round,",
          "  5 Hebrew entries list only an Aramaic number (BDB734, the Hebrew lion, gives H744, the",
          "  Aramaic word): they no longer count as the Aramaic word's entry.",
          "- **The first number was not always the headword's.** Where another listed number spells the",
          "  headword, that one is the entry's own: BDB842 תְּאַשּׁוּר is H8391, not H839 listed first;",
          "  BDB1292 בּוֺקֵר \"herdsman\" is H951, not H941 (Buzi). 68 entries changed (58 Hebrew, 10 Aramaic).",
          "- Together 340 BDB entries changed which number they witness, against PR #10 at 0819e9a.",
          "  (The counts in these first two items were measured against that commit; those below are",
          "  read from the data on every run.)",
          f"- **Slips in BDB's key, overridden.** {f['bdb_overrides']} rows. {f['ov_slips']} entries ({f['ov_slips_hbo']} Hebrew, "
          f"{f['ov_slips'] - f['ov_slips_hbo']} Aramaic) are keyed to a word",
          "  they are not about, most by one digit (BDB7322 קֹדֶשׁ H6994 for H6944, BDB578 H8396 Tabor",
          "  for H8386). `data/strongs/bdb-key-overrides.jsonl` gives each its own number and why;",
          f"  {f['ov_dropped']} slipped keys are dropped, and a related word the source also lists stays shared.",
          f"  {f['ov_drop_only']} more Aramaic entry only drops a slip (BDB9800 עֲשַׂב keyed H6611 Pethahiah), and {f['ov_cross_lang']}",
          "  names that occur only in the Aramaic of Ezra (Achmetha, Asnappar, Shethar-bozenai,",
          "  Tattenai), which Strong's numbers once, as Hebrew, now have their BDB entry as their own.",
          f"- **Aramaic words tagged Hebrew.** {f['arc_by_note']} numbers whose printed derivation opens \"(Aramaic)\" read as",
          "  Hebrew: the markup tags proper names `x-pn` in place of a language (H1841 Daniel, H3567",
          "  Cyrus). The printed note now wins (`lang_from: derivation` on the row), so BDB's Aramaic",
          "  entries for them are their own entries. Of the 87 Aramaic entries counted above as listing",
          "  only Hebrew numbers, 26 were these words (counted before this rule).",
          "",
          "## Greek: Strong's against Thayer",
          "",
          f"- {f['greek_numbers']:,} Greek numbers, {f['greek_numbers_used']:,} in use (101 are \"Not Used\").",
          f"- In the committed links: TBESG {f['with_tbesg']:,}, LSJ {f['with_lsj']:,}, Thayer {f['with_thayer']:,}"
          + (" (Thayer's links are filled in by a build where its entries exist)." if not f["with_thayer"] else "."),
          ""]
    if f["thayer_built_here"]:
        L += [f"- Thayer's split entries (PR #7): {f['thayer_entries']:,}; {f['thayer_entries_no_strongs']:,} carry no Strong's",
              "  number. List: `thayer-entries-no-strongs.tsv`.",
              f"- {f['greek_numbers_no_thayer_entry']:,} Greek numbers in use have no Thayer entry. List:",
              "  `greek-numbers-no-thayer-entry.tsv`.",
              ""]
    else:
        L += ["- **Thayer's split entries are not in this build.** `thayer-entries` (PR #7) is built only on",
              "  Adam's PC, where the OCR is. Its manifest records 5,486 entries, 5,092 linked to one Strong's",
              "  number by headword and 14 matching more than one (left unlinked), so about 394 entries carry",
              "  no number. Run `python3 pipeline/strongs_coverage.py` there to fill in both Thayer lists.",
              "- Meanwhile `greek-numbers-no-tbesg-or-lsj.tsv` lists the Greek numbers in use that neither",
              f"  STEPBible lexicon keys ({len(lists['greek-numbers-no-tbesg-or-lsj'][0]):,}).",
              ""]
    return "\n".join(L)


def build():
    table = read_jsonl(os.path.join(B.OUT, "strongs.jsonl"))
    wit = read_jsonl(os.path.join(B.OUT, "witnesses.jsonl"))
    bdb_units, _ = B._units_for(*B.WITNESSES["bdb"])
    lists, facts = bdb_part(table, wit, bdb_units)
    gl, gf = greek_part(table, wit)
    lists.update(gl)
    facts.update(gf)
    files = {f"{name}.tsv": tsv(sorted(rows, key=lambda r: B.sort_key(r[0]) if re.match(r"^[HG]\d", str(r[0]))
                                       else (0, int(re.sub(r"\D", "", str(r[0])) or 0), str(r[0]))), head)
             for name, (rows, head) in lists.items()}
    # the override table and the language rule, read whether or not BDB is here
    ov = list(B.read_bdb_overrides().values())
    facts["bdb_overrides"] = len(ov)
    slips = [r for r in ov if r["own"] and not r.get("own_lang_differs")]
    facts["ov_slips"] = len(slips)
    facts["ov_slips_hbo"] = sum(B._bdb_no(r["bdb"]) < B.BDB_ARAMAIC_FROM for r in slips)
    facts["ov_dropped"] = sum(len(r["drop"]) for r in slips)
    facts["ov_drop_only"] = sum(not r["own"] for r in ov)
    facts["ov_cross_lang"] = sum(bool(r.get("own_lang_differs")) for r in ov)
    facts["arc_by_note"] = sum(t.get("lang_from") == "derivation" for t in table)
    files["REPORT.md"] = report(facts, lists) + "\n"
    return files


def main():
    files = build()
    if "--check" in sys.argv:
        bad = [n for n, t in files.items()
               if not os.path.exists(os.path.join(OUT, n)) or open(os.path.join(OUT, n), encoding="utf-8").read() != t]
        for n in bad:
            print("DIFF", n)
        sys.exit(1 if bad else 0)
    os.makedirs(OUT, exist_ok=True)
    for n, t in files.items():
        tmp = os.path.join(OUT, n + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(t)
        os.replace(tmp, os.path.join(OUT, n))
        print("wrote", os.path.relpath(os.path.join(OUT, n), ROOT))


if __name__ == "__main__":
    main()
