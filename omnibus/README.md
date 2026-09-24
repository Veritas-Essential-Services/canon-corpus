# Omnibus

A six-volume great-books curriculum built entirely from public-domain texts,
in the tradition of the Veritas Press *Omnibus* (general editors Douglas
Wilson and G. Tyler Fischer). It follows the same structure: three eras
(Ancient, Fathers to the Reformation, Modern), run twice. Volumes I–III
carry the primary books and volumes IV–VI the secondary ones. The
selections, essays and questions are our own, and so is the voice
(`VOICE.md`).

## How it relates to canon-corpus

canon-corpus is the library. It holds the texts, cut into citable unit ids.
The Omnibus is the teacher. It holds none of the text itself: every
reading assignment is a unit-id range into canon-corpus, and the anthology
build pulls the text from there. When a book is missing, it gets acquired
in canon-corpus (manifest + fetcher, one commit per acquisition wave) and
never pasted in here.

## Layout

    plan/omnibus.csv      THE PLAN: every volume and chapter, edition, rights, corpus slug
    plan/GAPS.md          generated: what's built, on the shelf, to acquire, not PD
    plan/reference-junior-great-books.md   Junior Great Books author lists (a model for a younger track)
    tools/gap_check.py    regenerates GAPS.md; fails if a slug names nothing
    VOICE.md              the house voice
    CHAPTER_ANATOMY.md    the shape of every chapter
    RIGHTS.md             what may be printed, and where

## Commands

    python3 tools/gap_check.py --corpus ../canon-corpus

## Status

The plan is done. Sample chapter drafted: `volumes/1/05-iliad.md` (with teacher key).
