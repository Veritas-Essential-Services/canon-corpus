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

## Batch 4 (2026-11-15): Gutenberg books by shelved authors

Method: every English Gutenberg text (PG's `pg_catalog.csv`, fetched
2026-11-15) whose author is named on a shelf, whose number no shelf lists
anywhere, and whose author died 1955 or later (so could have published in
1931-1963). About 30 shelves match; most hits are pre-1931 books (PD by date,
and not this sweep's business) or British authors (URAA).

On the shelves now:

| shelf | book | renewal |
|---|---|---|
| ca-manning | *Ukrainian Literature* (Ukrainian National Association, 1944), PG 77771 | none |
| ca-manning | *Taras Shevchenko, the Poet of Ukraine* (UNA, 1945), PG 78316 (was `_excluded` on the old "after 1930" rule) | none |
| ca-manning | *The Story of the Ukraine* (Philosophical Library, 1947), PG 78161 | none |
| ca-manning | *Ukraine under the Soviets* (Bookman Associates, 1953), PG 79579 | none |
| ca-manning | *A History of Slavic Studies in the United States* (Marquette, 1957), PG 75446 | none |

Manning was American and every imprint is American. His *Marko, the King's
Son* (1932, R261912) and *Forgotten Republics* (1952, RE64670) were renewed:
not taken.

Seen and left: Frederic Arnold Kummer **Jr.** (1913-1990) has four 1940s-50s
pulp stories on Gutenberg (61781, 61869, 61958, 62085); the
frederic-arnold-kummer shelf is his father's, so these would need a shelf of
their own (Lane D's call). Checked and pre-1931 (PD by date, so not this
sweep's; left to each shelf's owner): Underwood's *The Taste of Honey*
(Mosher, 1930, PG 71882), *Garden of Desire* (1913), *Book of Dear Dead Women*
(1909); Howard's *Deems Taylor* (1927); Munro's *Social Civics* (1922).

## Batch 5 (2026-11-15): Gutenberg religion-subject books no shelf lists

Method: PG catalog rows with a religion subject or LoCC, number 20000+, an
author dying 1958 or later, and no shelf listing the number (115 texts); each
one's "Original publication" header line read, kept if 1931-1963. Older
releases lack that line (83 of 115), so they still need reading by hand.

On the shelves now:

| shelf | book | renewal |
|---|---|---|
| gore-vidal (new) | Vidal, *Messiah* (Dutton, 1954), PG 73527 | none, while every other Vidal book of 1948-60 shows its renewal |

Also shelved (new weston-la-barre shelf): La Barre, *The Peyote
Cult* (Yale Publications in Anthropology 19, 1938; Shoe String reprint 1959,
PG 77791): no renewal of either printing, while his *Human Animal* (1954,
RE135555) shows one. American author, US imprints. The 1950s pulp stories in
the same hit list (PG 67455, 67497, 68529, 72614, 78935) are Lane D's.

## Batch 6 (2026-11-15): Gutenberg's recent releases, non-fiction and books

Method: every English Gutenberg text numbered 60000 or above, by an author
dying 1955 or later (born 1870 or later), that no shelf lists (3,069 texts).
Each one's "Original publication" header line was read (2,049 have one) and
kept if it gives 1931-1963: about 1,450. Most are pulp magazine stories (science
fiction, westerns, horror), put aside below. The 152 left are books; this batch
took the ones that suit the Word Hoard and checked each with
`renewal_check.py` (author plus title words, the title's key words under any
name, and every renewal under the surname).

On the shelves now (new `nonrenewal-singles` shelf unless named):

| book | year | note |
|---|---|---|
| Weaver, *The Ethics of Rhetoric* | 1953 | |
| Brinton, *The Anatomy of Revolution* | 1938 | the 1952 revision was renewed; the 1938 text was not |
| Pearl S. Buck, *The Mother* | 1934 | her 1933 and 1935 books were renewed |
| L'Engle, *And Both Were Young* | 1949 | |
| Enright, *Return to Gone-Away* | 1961 | her *Gone-Away Lake* (1957) was renewed |
| Marguerite Henry, *Stormy, Misty's Foal* and *Gaudenzia* | 1963, 1960 | |
| Russell Kirk, *Old House of Fear* | 1961 | |
| Neihardt, *When the Tree Flowered* | 1951 | |
| Styron, *The Long March* | 1952 | |
| Muste, *Of Holy Disobedience* | 1952 | |
| Fred C. Kelly, *The Wright Brothers* | 1943 | |
| Kalashnikoff, *The Defender* (Newbery Honor) | 1951 | US first edition |
| Wilhelmsen, *Hilaire Belloc: No Alienated Man* | 1953 | |
| Kallen, *College Prolongs Infancy* | 1932 | |
| Goldwater, *The Conscience of a Conservative* | 1960 | |
| Stefansson, *Adventures in Error* | 1936 | |
| C. S. Baldwin, *Renaissance Literary Theory and Practice* | 1939 | |
| Hazlitt, *The Free Man's Library* | 1956 | |
| Vidal, *Williwaw* (gore-vidal shelf) | 1946 | RE492396 renews only the 1962 omnibus |

**Renewed, though Gutenberg released them** (not taken; worth telling PG):
Ellsberg, *Hell on Ice* (1938, R355571); Shirley Graham, *There Was Once a
Slave* (1947, R574012).

## Batch 7 (2026-11-15): 64 more from the same 152

Same method and checks as batch 6, onto `nonrenewal-singles` (83 titles now;
each slug's evidence under `_nonrenewal`). Among them: Howe's *Salt Mines and
Castles* (1946), Berkeley's *Giant Brains* (1949), Blotner's *The Political
Novel* (1955), Menzel's *World of Flying Saucers* (1963), Sterling Brown's *The
Negro in American Fiction* (1937), Dobie's *Stories of Christmas and the Bowie
Knife* (1953), John Hay's three Cape Cod books, *The Letters of Hart Crane*
(1952), Chubb's *The Byzantines* (1959), Mirsky's *Thirty-One Brothers and
Sisters* (1952), Bester's *Who He?* (1953), J. Edgar Hoover's *Masters of
Deceit* (1958), Hurok's memoir (1953), and Helen Hull's three novels.

Found unrenewed but left for Adam (content, not rights): *The Price of Salt*
(Highsmith as Claire Morgan, 1952), *Women's Barracks* (1950), *The Scorpion*
(Weirauch tr., 1932: a German work, also a URAA question), two Nightstand
paperbacks (1960-61), Foster's and Garde's literature bibliographies (1956,
1959), Putnam's *Race and Reason* (1961). Also left: the US government
publications in the list (PD anyway as federal works, not by non-renewal).

## Batch 8 (2026-11-15): older Gutenberg releases (20000-59999)

Method: every English text numbered 20000-59999 by an author dying 1955 or
later (born 1870 or later) that no shelf lists (3,345 texts). The first 40 KB
of each was read for a 1931-63 copyright line or PG's note that "research did
not uncover any evidence that the U.S. copyright on this publication was
renewed" (478 hits). Leaving out science fiction, westerns, horror and
mystery magazine stories left 201. Thirteen were dropped before checking: old
books with renewal lines, Canadian and British-law works, later editions,
two atheist tracts and a bibliography. Four pulp texts had no readable date.
The other 184 were each checked with `renewal_check.py`, and all 184 were
clear.

New author shelves (three or more titles each): mildred-wirt (29; she wrote
the first Nancy Drews as "Carolyn Keene"), robert-sidney-bowen (15, Dave
Dawson), paul-hutchens (6, the Sugar Creek Gang), robert-leckie (6, Sandy
Steele), t-j-wertenbaker (5, colonial Virginia), rutherford-g-montgomery,
jim-kjelgaard, paul-linebarger, graham-m-dean (4 each), ethel-c-brill,
natt-n-dodge, mary-elting, francis-lynde-kroll (3 each). The rest went onto
nonrenewal-singles (178 titles now). Among them: Neville's *It's Like This,
Cat* (1963, Newbery Medal), Messenger's *Christian Hymns of the First Three
Centuries* (1942) and *The Medieval Latin Hymn* (1953), Aaberg's *Hymns and
Hymnwriters of Denmark* (1945), Reuel Howe's *Herein Is Love* (1961), Toomer's
*An Interpretation of Friends Worship* (1947), Pfeiffer's *Tell el Amarna and
the Bible* (1963), MacKendrick's *The Mute Stones Speak* (1960), Haight's
*Essays on the Greek Romances* (1943), Peattie's *Trees You Want to Know*
(1934), and Andre Norton's *Ride Proud, Rebel!* (1961).

Two Wirt titles of 1940 have renewals, but those renew 1958 re-registrations
of revised editions; the 1940 texts were never renewed (noted per slug).

## Resume point

Next, in order:
1. Scans for the `_pending` items above (HathiTrust full view, or a DLI copy).
2. Batch 3 read every `_excluded`/`_pending`/`_held` note naming a year
   1931-1963 (dumped by a one-off script); what remains is reprint questions
   ("later printing"), not new works. Batch 4 began the next source,
   Gutenberg's books by shelved authors: Manning done. Next in that list,
   read each hit's "Original publication" line (PG's header) and keep only
   1931-1963 US imprints. Recreate the list with the script described under
   Batch 4 (catalog x shelf `_surname`, author died >= 1955); then widen to
   authors with no shelf yet (PG's 1931-63 US books are cleared the same way).
3. Ironside's and Pink's 1931-1950 books one by one (Loizeaux renewed some,
   not all).
4. Loeb volumes of 1931-1963 published in Cambridge, Mass. at the same time as
   London (a simultaneous US publication is not restorable): Lanes B and C
   own those shelves; send them the list, do not shelve directly.
5. Bloom-list candidates go to Lane B's staging area only (Adam, 10/27).
