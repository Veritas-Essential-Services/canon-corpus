# The Wall Gallery

Paintings for a wall-mounted TV used as a picture frame: the greatest works of the Louvre, the Palace of Versailles and the Nelson-Atkins in Kansas City, and the masters of the Romantic age wherever they hang. Chosen as the good, the true and the beautiful for a Christian family, to shape a child's moral imagination. Built 2026-10-17 for the Word Hoard's Pinacotheca.

## What was left out, and why

No nudity (classical nudes included), no sensual or amorous subjects, no horror or gore. The infant Christ, putti, and the Passion stay in. Every famous work left out is listed in `left_out` with the reason, so any of them can be restored by hand.

## `collection.json`

Top level: `title`, `built`, `about`, `screen` (3840x2160), `rights`, `rooms` (each with `name`, `terms`, `terms_url`: what that museum says about using its own images), `works`, `left_out`.

Each work:

- `qid`, `wikidata`: the Wikidata record; `room` (`louvre`, `versailles`, `nelson-atkins`, `romantic`) and `order` within the room, by year.
- `title`, `title_fr`, `artist`, `artist_died`, `year`, `holding` (the museum), `inventory`, `louvre_ark` (collections.louvre.fr/ark:/53355/<ark>).
- `image`: the best Wikimedia Commons file found: `file`, `page`, `original`, `width`, `height`, `mime`, `bytes`, and `chosen` (`wikidata` = the image on the Wikidata record; `commons-search` = a larger photograph of the same painting found on Commons).
- `orientation`; `tv`: `ready_4k` (the original is at least 3840 wide or 2160 high once fitted to the screen), `scale_to_fit` (under 1 means it is shrunk to fit; over 1 means the TV must enlarge it), `screen_fill` (share of the screen the painting covers when fitted).
- `featured` and `note`: a one-line "what to look for" on about forty works.
- `pd_us`, `pd_reason`.

## Rights

US law only. Every work is a painting made before 1931 by a painter who died before 1956, so it is US public domain, and a faithful photograph of a 2D public-domain work adds no new US copyright (Bridgeman v. Corel, 1999). Images are linked from Wikimedia Commons, never rehosted full size here (Adam's decision, 2026-10-07).

The museums' own image sites are more restrictive, and their terms are recorded per room. In short: the Louvre allows free private use of its site images; Versailles reserves its media library for tourism professionals; the Nelson-Atkins leaves reuse to the user. This collection does not draw on any of them.

## Putting it on the TV

    pip install pillow
    python pipeline/download_wall_art.py E:\WallArt              # every work, fitted to 3840x2160 on a dark mat
    python pipeline/download_wall_art.py E:\WallArt --caption    # with title, painter and year on the mat
    python pipeline/download_wall_art.py E:\WallArt --featured   # the featured works only
    python pipeline/download_wall_art.py E:\WallArt --size 1920x1080   # a 1080p TV

Copy the folder to a USB stick and open it in the TV's photo or gallery app as a slideshow. The mat keeps the TV from cropping tall portraits. Resumable; `--dry-run` shows the plan.

## Known gaps

- Works not `ready_4k` will look softer when the TV enlarges them. `chosen: commons-search` marks those where a larger Commons photograph replaced the Wikidata image; each was matched by painter, title words and aspect ratio, and copies, prints and details were excluded by filename.
- Nelson-Atkins coverage depends on Wikidata and Commons; the museum's own site offers only about 1,280 px.

## Memory-work videos

`pipeline/memory_video.py` makes a video for YouTube: one poem learned by heart over one painting from this collection. The painting drifts slowly behind the words, which sit in the calmest patch of the picture so a face, a sun or a ship is left clear. The poem runs through four rounds: all the words, every other word cut to its first letter, first letters only, and blank lines to recite alone. Then the whole poem is shown once more, followed by a credit card. Only poems with hosted text in `data/poetry/texts.jsonl` and paintings marked `pd_us` are accepted.

    python pipeline/memory_video.py --poem "Crossing the Bar" --painting Q257580 --out crossing-the-bar.mp4
    python pipeline/memory_video.py --poem "Crossing the Bar" --painting Q257580 --still 40 --out check.png   # one frame, to check the layout

It needs Pillow and ffmpeg. The fonts are EB Garamond and Cinzel (SIL Open Font Licence, from github.com/google/fonts), placed in `fonts/` or given with `--fonts`; without them it falls back to DejaVu. A 6-minute 1080p video takes about 15 minutes to render. `--size 3840x2160` makes a 4K version, and `--place right-top` and similar override where the words go. Videos are not committed.
