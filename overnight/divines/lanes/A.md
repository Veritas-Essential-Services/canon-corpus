# Lane A — Divines

slug: `divines` · queue: `overnight/divines/QUEUE-A.json` · map section: `docs/divines-map/A-divines.md`

## Notes for this lane's authors

- **Horatius Bonar** and **Andrew Bonar** are two separate items and two separate map sections.
- Horatius Bonar's **hymns** belong to Adam's separate hymn manifest. List his hymn collections in the map as `see hymn manifest`; do not ingest them here.
- **Adolph Saphir** (1831–1891), Hebrew Christian expositor — not any other Saphir.
- **John Flavel**: the complete Works (1820, six volumes) is on Internet Archive; `flavel-fountain` is already in `fetch_sources.py` from CCEL — list it in the shelf as already held, do not refetch it.
- **John Bunyan**: `bunyan-pilgrim` and `bunyan-holy_war` are already held; the target is the collected Works.
- **J.C. Ryle** died 1900; works published in his lifetime are public domain. Later abridgements and modern reprints are not.
- **Edwards** is largely done (`pipeline/edwards_shelf.json`: all of CCEL, 2 Gutenberg, 31 Internet Archive). His item is a GAP AUDIT: what public-domain Edwards exists that the shelf lacks? Add only verified gaps. Do not rebuild what is there.

## Cross-lane rules

**Cross-lane references (B ↔ C).** Lane C builds the Dryden and Garnett shelves; Lane B's Ovid and Virgil sections point at Dryden's titles. Whichever lane you are: never fetch or shelve another lane's titles. Lane B: if a Dryden slug does not exist yet, list it in your map section as `cross-ref → Dryden shelf (lane C), pending` and move on — do not wait, do not fetch Dryden. Lane C: name Dryden's slugs predictably (`dryden-aeneid`, `dryden-georgics`, `dryden-eclogues`, `dryden-metamorphoses`) so Lane B's pointers resolve, and never shelve a non-Dryden translation of Ovid or Virgil.
