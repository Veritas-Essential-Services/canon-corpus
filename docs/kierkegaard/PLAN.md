---
model_log:
  - date: 2026-11-03
    model: Claude, project thread "Plan the full Kierkegaard shelf"
    did: wrote the plan, the renewal checks, the SKS build
---

# Kierkegaard in the Armarium: the whole plan

Asked by Adam, 2026-11-03: "make a plan to ingest Kierkegaard with the titles we
have access to, and ask the Hong family in Minnesota if we can use their
translations until the Swenson and Lowrie editions come into the public domain."

US public domain is the only test (Adam, 2026-10-10), and every 1931-63 US work
whose copyright was never renewed is in (Adam, 2026-11-03).

## The short version

1. **All of Kierkegaard in Danish is shelved now.** The Royal Danish Library
   released the whole critical edition, *Søren Kierkegaards Skrifter* (SKS,
   1997-2013), as TEI under **CC0** (github.com/kb-dk/SKS_tei). This PR builds
   SKS vols 1-16, every published and posthumous work: **87 books, 10,195
   paragraphs, 648 of Kierkegaard's own footnotes**, cited by SKS page
   (`sks-kg:23.2` = the 2nd paragraph beginning on SKS 9, page 23). The
   journals, papers and letters (SKS 17-28) are the same format and are the
   next wave.
2. **English that is free today:** Hollander's *Selections* (1923, shelved), the
   Swensons' *Works of Love* (1946, never renewed; raw text shelved), the
   Swensons' *Philosophical Fragments* (1936) and *Edifying Discourses I* (1943),
   both never renewed but with no free scan yet.
3. **Four Lowrie volumes may be free today** (first published in London
   1939-41, never registered or renewed in the US): *Christian Discourses*,
   *The Point of View*, *Training in Christianity*, *For Self-Examination*.
   They need Adam's ruling. My lean: they are free (reasoning below).
4. **Everything else opens year by year, 2033 to 2054** (table below).
5. **The Hong translations belong to "Postscript, Inc."**, not to Princeton and
   not (directly) to the family. Howard Hong assigned his copyrights to it in
   1994-95 (US Copyright Office recordations V3048P333 and V3073P240), and the
   later Princeton volumes are registered in its name. Princeton publishes them
   and runs the permissions desk. The draft request is in
   [permission-request-DRAFT.md](permission-request-DRAFT.md). **Nothing has
   been sent.**

## What is shelved, after this PR

| Shelf | What | Status |
|---|---|---|
| `sks-*` (87 books, `pipeline/build_sks.py`) | SKS 1-16, Danish, CC0 | **built** (this PR) |
| `hollander` | *Selections from the Writings of Kierkegaard* (1923), PG 60333 | shelved (lane C, round 32) |
| `swenson-lowrie` | *Works of Love* (1946), DLI scan, raw text | shelved (PR #74); not yet converted |
| `swenson-lowrie` `_pending` | *Philosophical Fragments* (1936), *Edifying Discourses I* (1943) | free in law, no free scan |
| `swenson-lowrie` `_waiting` | 18 more Swenson and Lowrie volumes | on the release queue with their dates |

## Every work, every English edition we could use, and when

"Free now" = US public domain today. A year = the 1 January it opens. Renewal
numbers are from the Stanford Copyright Renewal Database (searched 2026-11-03);
the Swenson/Lowrie rows were checked against the printed CCE in PR #74 (wordhoard
`docs/research/2026-11-03-kierkegaard-swenson-lowrie.md`).

| Work (Danish, year) | SKS | Earliest English we could host | Opens |
|---|---|---|---|
| Om Begrebet Ironi (1841) | 1 | Capel 1965; Hong 1989 | none before 2061 |
| Af en endnu Levendes Papirer (1838) | 1 | Hong (Watkin) 1990 | not in view |
| Enten-Eller (1843) | 2-3 | Swensons + Lowrie 1944 (R517166); bits in Hollander 1923 | 2040 (Hollander free now) |
| Frygt og Bæven (1843) | 4 | Payne, OUP London 1939 (British, restored); Lowrie 1941 (R458284) | 2035 (Payne), 2037 (Lowrie) |
| Gjentagelsen (1843) | 4 | Lowrie 1941 (R458283) | 2037 |
| Philosophiske Smuler (1844) | 4 | Swenson 1936, A102052, **not renewed** | **free now**, needs a scan |
| Begrebet Angest (1844) | 4 | Lowrie 1944 (R517164) | 2040 |
| Forord (1844) | 4 | Nichol 1989; Hong 1997 | not in view |
| The eighteen Upbuilding Discourses (1843-44) | 5 | Swensons, *Edifying Discourses* I 1943 (**not renewed**), II 1944, III 1945, IV 1946 (renewed) | I **free now**; II 2040, III 2041, IV 2042 |
| Tre Taler ved tænkte Leiligheder (1845) | 5 | Swenson 1941 (R447259) | 2037 |
| Stadier paa Livets Vei (1845) | 6 | Lowrie 1940 (R432046) | 2036 |
| Afsluttende uvidenskabelig Efterskrift (1846) | 7 | Swenson/Lowrie 1941 (R443957) | 2037 |
| En literair Anmeldelse (1846) | 8 | Dru, *The Present Age*, OUP 1940 (British, restored) | 2036 |
| Opbyggelige Taler i forskjellig Aand (1847) | 8 | Part 1: Aldworth & Ferrie, *Purify Your Hearts!*, C. W. Daniel, London 1937 (British, restored)*; Steere, *Purity of Heart*, Harper 1938 (R382241). Part 2: Aldworth & Ferrie, *Consider the Lilies*, 1940*. Part 3: Swensons, *Gospel of Suffering* 1947 (R602804) | 2033 / 2034; 2036; 2043 |
| Kjerlighedens Gjerninger (1847) | 9 | Swensons 1946, A5267, **not renewed** | **free now** (shelved) |
| Christelige Taler (1848) | 10 | Lowrie, OUP London 1939 | **may be free now** (ruling), else 2035 |
| Lilien paa Marken og Fuglen under Himlen (1849) | 11 | Lowrie, in *Christian Discourses* 1939 | as above |
| Sygdommen til Døden (1849) | 11 | Lowrie 1941 (R458282) | 2037 |
| Tvende ethisk-religieuse Smaa-Afhandlinger (1849) | 11 | Lowrie, in *The Present Age* 1940 | 2036 |
| Ypperstepræsten / Tolderen / Synderinden (1849) | 11 | Lowrie, in *Christian Discourses* 1939 | as Christian Discourses |
| Indøvelse i Christendom (1850) + En opbyggelig Tale | 12 | Lowrie, OUP London 1941 (DLI scan exists) | **may be free now** (ruling), else 2037 |
| To Taler ved Altergangen om Fredagen (1851) | 12 | Lowrie, in *For Self-Examination* 1941 | as below |
| Om min Forfatter-Virksomhed (1851) | 13 | Lowrie, in *The Point of View* 1939 | **may be free now**, else 2035 |
| Til Selvprøvelse (1851) | 13 | Hongs, Augsburg 1940 (R423433); Lowrie, OUP London 1941 | Lowrie **may be free now**; Hongs 2036 |
| Guds Uforanderlighed (1855) | 13 | Lowrie, in *For Self-Examination* 1941 | as above |
| Øieblikket 1-10, Fædrelandet articles (1854-55) | 13-14 | Lowrie, *Attack upon "Christendom"* 1944 (R517165) | 2040 |
| Bogen om Adler (posth.) | 15 | Lowrie 1955 (RE193879) | 2051 |
| Johannes Climacus (posth.) | 15 | Croxall, London 1958 (British, restored; Croxall's other work renewed) | 2054 |
| Synspunktet for min Forfatter-Virksomhed (1859) | 16 | Lowrie, in *The Point of View* 1939 | **may be free now**, else 2035 |
| Dømmer selv! (1876) | 16 | Lowrie, in *For Self-Examination* 1941 | **may be free now**, else 2037 |
| Den bevæbnede Neutralitet (posth.) | 16 | Hongs 1968 | not in view |
| Krisen og en Krise i en Skuespillerindes Liv (1848) | 14 | Crites 1967 | not in view |
| Journals and papers | 17-27 | Dru, *Journals*, OUP 1938 (British, restored); Hollander 1923 extracts | 2034 (Hollander free now) |
| Letters | 28 | Hongs 1978 | not in view |

\* Aldworth & Ferrie's two C. W. Daniel volumes are from catalogue memory and were
not checked against a title page this session: verify before they go on the queue.

Also checked and left out, with why:

- Bretall, *A Kierkegaard Anthology* (Princeton 1946): renewed R568135; its
  translations are the Swenson/Lowrie/Dru texts anyway.
- LeFevre, *The Prayers of Kierkegaard* (1956): renewed RE224926 for the editing.
- Holmer, *Edifying Discourses: A Selection* (1958): renewed RE308965 for the
  selection; the discourses from Swenson's vol. I inside it are free, the rest
  are not.
- Gerda Andersen, *The Diary* (Philosophical Library 1960): renewed RE379516.
- Croxall, *Meditations from Kierkegaard* (1955): renewed RE161519.
- Every 1959-62 revision (Johnson's Either/Or, Nelson's Point of View, the
  Thulstrup/Hong Fragments, Dru's revised Present Age): renewed for the
  revisions; the free text is the first edition.

## Why I lean "free now" on the four London Lowrie volumes

They came out first in London (Oxford University Press, 1939-41), were never
registered in the US and never renewed. The 1996 URAA restores a foreign work
only if at least one author was then a national or domiciliary of a treaty
country (17 USC 104A(h)(6)(C)). Lowrie was an American citizen living in
Princeton. On that reading nothing restores them, and they are as free as any
other unrenewed book, which is what Adam's 2026-11-03 rule takes in. The risk:
a court could weigh the London place of publication differently, and OUP could
have a US edition with its own registration we have not found. The ledger holds
them to their 95-year days until Adam rules (a decision card is up in the
thread).

## Steps, in order

1. **Done in this PR:** SKS 1-16 in Danish (`pipeline/build_sks.py`,
   `tests/sks_test.py`, `pipeline/sks_pins.json`, 87 manifest entries).
2. **Next wave, same builder:** SKS 17-28 (journals, notebooks, loose papers,
   letters). Check the journal files' structure first (they are dated entries,
   not paragraphs; the id will want the SKS journal signature, e.g. `NB11:48`).
3. **Lowrie's four London volumes:** on Adam's yes, fetch *Training in
   Christianity* from its DLI scan (`in.ernet.dli.2015.165989`) and look for
   scans of the other three. The shelf owner (the `swenson-lowrie` ledger) does
   the fetch.
4. ***Philosophical Fragments* (1936) and *Edifying Discourses I* (1943):** both
   free, neither scanned freely. Two routes: ask HathiTrust for a copyright review
   of `uva.x030214738` and `mdp.39015043654931` (free, slow), or buy a first
   printing and run it through the Unscanner (fast; about $30-60 a copy).
5. **Convert the English we have** (Works of Love 1946, Hollander 1923) and link
   each English paragraph to its SKS paragraph, the way Lightfoot is linked to
   Lake. The Hongs' margins print the first edition's pages, and `pages.sv1`
   already carries them on 2,331 SKS paragraphs, so an alignment has anchors.
6. **Release queue:** add the non-Swenson/Lowrie rows above (Steere 2034, Dru's
   Journals 2034, Payne 2035, Dru's Present Age 2036, the Hongs' 1940
   Self-Examination 2036, Croxall 2054; Aldworth & Ferrie once verified).
7. **The Hong permission ask:** Adam reads, edits and sends the draft himself.
   If granted, the Hong text is a separate shelf with its own rights block
   (`redistribute_whole: false`, the licence terms quoted), never mixed into the
   public-domain books, and each volume comes down on the day its free twin
   opens, or stays if the licence allows.

## Who holds the Hong translations (the answer to "ask the Hong family")

- **Copyright owner of record: Postscript, Inc.** US Copyright Office
  recordations, both "Howard V. Hong" to "Postscript, Inc.", assignments:
  V3048P333 (recorded 1994-11-03, *Søren Kierkegaard's Journals and Papers* and 6
  other titles) and V3073P240 (recorded 1995-01-23, *Kierkegaard's Writings II,
  The Concept of Irony* and 16 other titles). The Princeton volumes from 1995 on
  (*Works of Love*, *Without Authority*, *The Point of View*, *The Book on
  Adler*, *The Moment*) are registered to Postscript, Inc. The earlier volumes
  were registered to Howard V. Hong, then assigned. *Christian Discourses* (1997)
  and the 1980 *Concept of Anxiety* and *Sickness unto Death* are registered to
  Princeton University Press, and *Early Polemical Writings* (1990) to Julia
  Watkin, its translator.
- **Who Postscript, Inc. is:** not found online. It is very likely the Hongs'
  own company, now run by family or by people close to the Hong Kierkegaard
  Library. Its officers and address are a public record at the Minnesota
  Secretary of State (search "Postscript" at mblsportal.sos.state.mn.us). That
  lookup is the one step a browser does better than I can from here.
- **Publisher and permissions desk: Princeton University Press**,
  permissions@press.princeton.edu, or the "Republication Permission Request" form
  at press.princeton.edu. Princeton will know whom to route Postscript's share
  to, and holds the publishing rights itself.
- **Ally: the Howard V. and Edna H. Hong Kierkegaard Library, St. Olaf College**,
  Northfield, Minnesota. Director/Curator Anna Söderquist, HKL@stolaf.edu. Not a
  rights holder as far as the records show (it is co-claimant only on the new
  *Kierkegaard's Journals and Notebooks*, with the Copenhagen centre, which is a
  different translation). It is the natural friend to ask who Postscript, Inc. is
  today and to put in a good word.
- **Term, for the record:** the Hong translations are post-1978 works by
  authors who died in 2007 (Edna) and 2010 (Howard): life plus 70, so 1 January
  2081. Assigning them to a company does not change that.

**Recommendation:** send one email to Princeton's permissions desk, addressed to
Princeton and Postscript, Inc., with the Hong Library copied as a courtesy. Send
a short separate note to the Hong Library asking who speaks for Postscript, Inc.
today. Both drafts are in the draft file.

## Open questions for Adam

1. **Is the Armarium non-commercial?** The draft says so in brackets. I did not
   assume it: no ads, no fees, no sales? Confirm or change the line.
2. **The four London Lowrie volumes:** shelve now, or hold to their dates?
3. **Scope of the Hong ask:** the draft asks only to bridge the gap until each
   Swenson/Lowrie twin opens (what you asked). Some Hong volumes have no free
   twin at all (Concept of Irony, Prefaces, Armed Neutrality, the letters). The
   draft mentions them once, lightly. Strike that paragraph if you'd rather keep
   the ask narrow.
4. **SKS's teiHeader** in each file still says "copyright, restricted" (written
   2004); the repository LICENSE and the Royal Library's portal both say CC0.
   I followed the CC0 and recorded the contradiction in every book's rights
   note. Flagging it once.

Sources: Stanford Copyright Renewal Database (exhibits.stanford.edu/copyrightrenewals);
US Copyright Office public records (publicrecords.copyright.gov); kb-dk/SKS_tei
LICENSE (CC0 1.0) at commit 27a6b11; tekster.kb.dk SKS pages ("Materialet er
dedikeret til public domain"); press.princeton.edu (permissions); wp.stolaf.edu/kierkegaard.
