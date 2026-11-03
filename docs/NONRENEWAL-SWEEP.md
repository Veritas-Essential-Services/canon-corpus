# Non-renewal sweep: US books of 1931-1963 that were never renewed

Started 2026-11-03 on Adam's word: **"I want everything that was not renewed."**

A US book published 1931-1963 with a copyright notice had to be renewed in its
28th year. If it was not, it has been US public domain since. That is the whole
test here, with one exception: a book first published abroad by a foreign
author can have been restored by the URAA (1996) whatever its renewal says, so
every item records who wrote it and where it first appeared.

## How each book is checked

1. `python3 pipeline/renewal_check.py --fetch` once (NYPL's `cce-renewals`,
   CC0, pinned by commit: every renewal 1950-1991, the records Stanford's
   Copyright Renewal Database searches).
2. `python3 pipeline/renewal_check.py "<author>" "<title>"`, then `--title-only`
   (a misspelt surname in the record hides a renewal from the first), and
   where a series or a pen name could hide it, `--surname <name>`. Every candidate is read;
   "no renewal found" is written only when none of them is this book.
3. URAA: American author or first published in the US? Say which, per book.
4. A text: Project Gutenberg (which clears 1931-1963 books the same way), or
   an archive.org scan that is not a lending-library copy.
5. The evidence goes into the shelf, per slug, under `_nonrenewal` (and in
   `_rights_checked` for an archive.org item, which the fetch gate needs), then
   `fetch_shelf.py <shelf>` and `--verify --record`.

## Batch 1 (2026-11-03): Lane D's holds, released

Lane D's renewal search of 2026-11-03 (Stanford) found 45 held storyteller
books unrenewed and left them held for Adam's word. Re-checked with
`renewal_check.py` (second, independent source) plus PG 43677, which that
search had skipped. All 46 fetched, identity and rights gates passed, `_checks`
recorded. 12 shelves: burroughs-works (8), roy-j-snell (22), madeline-brandeis
(4), percy-keese-fitzhugh (3), arthur-train, jackson-gregory, nell-speed,
wodehouse-works (Right Ho, Jeeves: first published in the US), and the
storytellers-tail shelves 29, 32, 38, 50 (Fauley, Edwin Green, McIntosh,
Gadsby).

Still held, and why: Lost on Venus (book renewed, R305497); Watson's Mark of
the Beast (renewed, R271289); Buchan's Days to Remember (British, possible
URAA); Pinkerton (1989 reprint text); Anstey (1986 reprint text); the 1966
Kindergarten book (automatic renewal era).

### URAA review of batches 1-2 (2026-11-03, coordinator's request)

Every book was re-read for foreign origin. All but one are by American
authors and were first published in the US (New York, Boston, Chicago
imprints read in the fetched texts or scan records; Emerton and Taylor are
American scholars published by Columbia University Press). The one foreign
author is Wodehouse: *Right Ho, Jeeves* ran first in *The Saturday Evening
Post* (Dec. 1933 - Jan. 1934), and the book came out in London (5 Oct. 1934)
and Boston as *Brinkley Manor* (15 Oct. 1934) within 30 days of each other,
so it was never a restorable work. Kept. Every title was also searched
without the surname (a misspelt name, e.g. "WODEHODSE", can hide a renewal);
the only full-title hits were other works (Sgroi's 1954 Tarzan, a 1950 comic
strip, Phillpotts's *A Shadow Passes*, MacDonald's *Galloping Ghost*).

## Batch 2 (2026-11-03): theology

On the shelves now:

| shelf | book | why it is free |
|---|---|---|
| boniface-of-mainz | Emerton, *The Letters of Saint Boniface* (Columbia, 1940) | no renewal; American translator, US first edition |
| hugh-of-saint-victor | Taylor, *The Didascalicon* (Columbia, 1961) | no renewal; the scan's library (UF) reviewed it out of copyright |
| a-t-robertson | *Word Pictures in the NT* vols. I-III (1930) | 1930 books are PD since 2026 (the old shelf note said "after 1929") |
| a-w-tozer (new) | Tozer, *The Pursuit of God* (1948), PG 25141 | no renewal, while his five later books all show theirs |

Unrenewed, waiting for a scan (`_pending`): Robertson's Word Pictures vol. IV
(1931); Deferrari's Hugh *On the Sacraments* (1951).

Checked and **renewed** (do not chase): Machen's *Christian Faith in the
Modern World* (1936) and *Christian View of Man* (1937); Chafer's Systematic
Theology (1947-48); Vos's Biblical Theology (1948); Lenski's commentaries
(1934-); Warfield's Oxford volumes of 1931-32 (Calvin and Calvinism,
Perfectionism I-II, Westminster Assembly); Berkhof's Reformed Dogmatics
(1932); Robertson's Word Pictures V-VI; McGiffert's History of Christian
Thought (1932-33); Ryan and Ripperger's Golden Legend (1941); Hersholt's
Andersen (1942, 1949); Hendriksen's More than Conquerors (1939); Tozer's books
of 1950-61; Ironside's Expository Notes (1948-52); the Fathers of the Church
volumes of 1947-58 that were searched.

Unrenewed but NOT taken, and why: Berkhof's *Systematic Theology* (1938/41) is
a revision of the renewed *Reformed Dogmatics* (1932), so only its new matter
is free until 2028; his *History of Christian Doctrines* (1937), *Summary*
(1938) and *Principles of Biblical Interpretation* (1950) show no renewal but
no open scan was found. Warfield's *Critical Reviews* and *Studies in
Theology* (1932) show no renewal; no open scan found.

## Batch 3 (2026-11-03): other shelves' "after 1930" exclusions

On the shelves now (all American, first published in the US, no renewal):

| shelf | book |
|---|---|
| philip-schaff | *The Creeds of Christendom* vols. I-II, sixth edition rev. David S. Schaff (Harper, 1931), CCEL |
| martin-luther | Luther on Galatians, Theodore Graebner's abridgment (Zondervan, 1939), CCEL |
| paul-rader | *Round the World* (Revell, 1932) |
| singles-nonfiction-2 | Nicole's *Essay on True and Apparent Beauty*, tr. J. V. Cunningham (Augustan Reprint Society, 1950), PG 28921 |

Renewed: Lofting's *Gub Gub's Book* (1932, R248269).

Left alone, and why: British translators of the 1930s (Atherton's Bondage of
the Will, Evans's Eckhart II, Sutro's Maeterlinck, Rawson's Strindberg,
Duff's Silius II) are foreign works the URAA likely restored; Kipling and
Ransome likewise. Lowrie's four Oxford (London) Kierkegaard volumes are held
for Adam's ruling already written on the swenson-lowrie shelf (an American
translator, first published abroad: a URAA question, not a renewal one).

For Lane B (Loebs, Harvard and London at once): no renewal of Shorey's
*Republic* vol. II (1935) or Nixon's *Plautus* vols. IV-V (1932, 1938); both
are American translators. Lane B owns those shelves.

## Resume point

Next, in order:
1. Scans for the `_pending` items above (HathiTrust full view, or a DLI copy).
2. Batch 3 read every `_excluded`/`_pending`/`_held` note naming a year
   1931-1963 (dumped by a one-off script); what remains is reprint questions
   ("later printing"), not new works. Next source of candidates: Gutenberg's
   1931-63 books by shelved US authors that no shelf lists yet.
3. Ironside's and Pink's 1931-1950 books one by one (Loizeaux renewed some,
   not all).
4. Loeb volumes of 1931-1963 published in Cambridge, Mass. at the same time as
   London (a simultaneous US publication is not restorable): Lanes B and C
   own those shelves; send them the list, do not shelve directly.
5. Bloom-list candidates go to Lane B's staging area only (Adam, 10/27).
