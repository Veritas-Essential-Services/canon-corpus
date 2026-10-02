# Lane B — Classical (English translations)

slug: `classical` · queue: `overnight/divines/QUEUE-B.json` · map section: `docs/divines-map/B-classical.md`

## Notes for this lane's authors

- **Jowett's Plato** (classical grouping): Benjamin Jowett's complete English translation of the dialogues (3rd ed., 1892), public domain, clean on Gutenberg and Internet Archive. One translator's whole Plato — prefer his collected set over scattered single dialogues. English only; no Greek.
- **Aristotle** (classical grouping): the target is the **W.D. Ross Oxford translation**, *The Works of Aristotle Translated into English* (12 vols., early 1900s, public domain) on Internet Archive — the coordinated English corpus. Perseus's English Aristotle is thin and is a GAP-FILL fallback only; do not pull Perseus Greek. Record the translator per volume.
- **Hesiod** (classical): English only — the Hugh Evelyn-White prose translation (Theogony, Works and Days, the fragments, Homeric Hymns), public domain, one volume.
- **Ovid** (classical): English only, and NO single public-domain translator covers all of him. Metamorphoses, Heroides, Amores, Ars Amatoria, Fasti, Tristia come from different translators — record the translator per work. Dryden-Garth Metamorphoses lives on the DRYDEN shelf (below); the Ovid section cross-references that uid rather than re-fetching it.
- **TRANSLATOR SHELVES — `dryden` and `garnett`** are their own grouping, NOT author sections. Each translated title is a first-class work with its own uid, built exactly like an author's book (its own shelf entry, its own unit ids). An author section (Ovid, Virgil, a Russian novelist later) cross-references the SAME uid — never mint a second uid for the same passage, never duplicate the text. This is the repo's rule 3/3b (a citation says where to look, a uid says what you find). Dryden shelf: all his translations — Virgil (Aeneid/Georgics/Eclogues), Ovid (Dryden-Garth Metamorphoses), Homer, Juvenal, Persius, Lucretius, Theocritus, Fables Ancient and Modern. Garnett shelf: her Russians — Dostoevsky, Tolstoy, Chekhov, Turgenev, Gogol (all public-domain Garnett translations; her later revisions may not be PD — record the edition/year per title and exclude anything post-1930 you cannot date).
- **Virgil** (classical): standalone author section (Aeneid, Georgics, Eclogues). Dryden's Virgil lives on the DRYDEN shelf; this section cross-references those uids.

## Cross-lane rules

**Cross-lane references (B ↔ C).** Lane C builds the Dryden and Garnett shelves; Lane B's Ovid and Virgil sections point at Dryden's titles. Whichever lane you are: never fetch or shelve another lane's titles. Lane B: if a Dryden slug does not exist yet, list it in your map section as `cross-ref → Dryden shelf (lane C), pending` and move on — do not wait, do not fetch Dryden. Lane C: name Dryden's slugs predictably (`dryden-aeneid`, `dryden-georgics`, `dryden-eclogues`, `dryden-metamorphoses`) so Lane B's pointers resolve, and never shelve a non-Dryden translation of Ovid or Virgil.
