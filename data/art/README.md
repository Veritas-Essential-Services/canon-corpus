# Illustration catalog

The golden age of illustration, published before 1931 and so public domain in the US: the Brandywine school (Pyle, N. C. Wyeth, Jessie Willcox Smith and others), Americana (Rockwell's Saturday Evening Post covers 1916–1930, Leyendecker, Parrish, Remington, Russell) and the storybook masters (Rackham, Dulac, Nielsen, Crane, Caldecott, Greenaway, Tenniel, Doré, Denslow). Built 2026-10-07 for the art-appreciation module.

`catalog.json`: 39 artists, 410 works. Each work has `published`, `pd_us` (true, false, or "check"), and `sources` best first, each with `host`, `url`, `iiif` (manifest or image service, when one exists) and `verified`:

- `fetched`: the page was opened and checked.
- `search-result`: found by search, not opened.
- `unverified`: built from the host's usual address pattern, not checked.

Display is by IIIF from the holding library's own servers (Adam's decision, 2026-10-07); nothing full-size is hosted here.

**Known gaps:** most IIIF links are unchecked, because the cloud sandbox could not reach loc.gov, archive.org or Wikimedia. Rockwell cover titles are partly matched from the Rockwell Museum's print-shop order (each cover's notes say which). Rockwell's name is a trademark of his estate: show the pictures, never imply endorsement.

**Offline backup:** `python pipeline/download_illustrations.py <folder on your drive>` saves the largest copy of every `pd_us: true` work. Internet Archive manifests are whole books, so expect many gigabytes.
