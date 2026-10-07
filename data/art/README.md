# Illustration catalog

The golden age of illustration, published before 1931 and so public domain in the US: the Brandywine school (Pyle, N. C. Wyeth, Jessie Willcox Smith and others), Americana (Rockwell's Saturday Evening Post covers 1916–1930, Leyendecker, Parrish, Remington, Russell) and the storybook masters (Rackham, Dulac, Nielsen, Crane, Caldecott, Greenaway, Tenniel, Doré, Denslow). Built 2026-10-07 for the art-appreciation module (the Word Hoard's Pinacotheca room).

`catalog.json`: 39 artists, 599 works (585 marked `pd_us: true`). Each work has `published`, `pd_us` (true, false, or "check"), and `sources` best first, each with `host`, `url`, `iiif` (manifest or image service, when one exists) and `verified`:

- `fetched`: the page or API record was opened and checked.
- `search-result`: found by search, not opened.
- `unverified`: built from the host's usual address pattern, not checked.

A source can also carry:

- `iiif_check`: what `pipeline/verify_illustrations.py` found when it opened the IIIF link: `status` (`ok`, `no-files`, `http-4xx`, `unreachable`), the date, the page count (`canvases`) and the largest pixel size. For the Library of Congress it also records `iiif_service` (the first page's IIIF image server) and `largest_file` (usually the master TIFF), read through loc.gov's JSON API because its `manifest.json` sits behind a bot wall.
- `image` and `display`: for Wikimedia Commons, the original file and a 1280px copy (Commons is not a IIIF server).
- `plate`: the caption of a single plate, where a source is one picture rather than the whole book.

Display is by IIIF (or Commons) from the holding library's own servers (Adam's decision, 2026-10-07); nothing full-size is hosted here.

## State of the links (2026-10-07)

| Host | IIIF links | Checked |
|---|---|---|
| NYPL Digital Collections | 47 | all open; plates 2,000–4,000 px on the long side |
| Library of Congress | 50 | 42 open; 7 are catalog records with no scan; 1 timed out |
| Metropolitan Museum, Smithsonian | 3 | all open |
| Internet Archive | 98 | **not checked**: archive.org answered 503 from the sandbox all day |

Wikimedia Commons: 95 Rockwell Post cover dates matched to their catalog entries, 183 Leyendecker and 6 Wyeth Post covers added as new works (`pipeline/commons_covers.py`). Most Commons cover scans are about 600×800; the Google Art Project photographs of Rockwell originals are 2,400–3,800 px.

## Known gaps

- **Internet Archive** IIIF links are unchecked (above). Rerun `python3 pipeline/verify_illustrations.py --host iiif.archive.org` from a machine that can reach it.
- **Wyeth's *Deerslayer* (1925) and *Drums* (1928)**: no open hi-res scan on NYPL, LoC or Commons. Both are reported readable at archive.org; their identifiers are not yet recorded.
- **Rockwell Post covers**: the open copies are small. The Post's own archive has them large but is members-only. Rockwell's name is a trademark of his estate: show the pictures, never imply endorsement.
- **Leyendecker covers** added from Commons carry the date only; their subject titles are not yet recorded.
- **NYPL search** needs an API token (free from NYPL); without one, plates were found by web search, so many more Rackham, Dulac and Nielsen plates are there than are listed.

## Scripts

    python3 pipeline/verify_illustrations.py            # open every IIIF link not yet ok, record what it found
    python3 pipeline/verify_illustrations.py --report   # the tally only
    python3 pipeline/commons_covers.py --add            # match Commons Post covers; add the unlisted ones

**Offline backup:** `python pipeline/download_illustrations.py <folder on your drive>` saves the largest copy of every `pd_us: true` work: IIIF at full size, the Library of Congress master files, and Commons originals. Internet Archive manifests are whole books, so expect many gigabytes. Resumable; `--artist Rackham` for one artist, `--dry-run` to see the plan.
