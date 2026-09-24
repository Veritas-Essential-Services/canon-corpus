# Anatomy of a chapter

Every chapter is one Markdown file, `volumes/<vol>/<ch>-<slug>.md`, with front
matter the export tools read. The same file feeds both outputs:

- **the guide**: the teaching layer, with the readings given as citations
- **the anthology**: the teaching layer plus the assigned text, pulled from
  canon-corpus by unit id at build time, never pasted into the chapter

## Front matter

```yaml
vol: 1
ch: 5
work: The Iliad
author: Homer
edition: tr. Samuel Butler (1898)
corpus: iliad-butler            # canon-corpus book slug
rights: pd
sessions:                       # the readings are unit-id ranges, not page numbers.
                                # Illustrative: Butler's Iliad is cut into line-block
                                # cards, so real endpoints must be actual card anchors.
  - range: iliad-butler:1.1-1.611
  - range: iliad-butler:6.1-6.529
memory: iliad-butler:6.146-6.149   # the recitation passage
status: plan                    # plan → draft → revised → final
```

## Sections, in order

1. **Opening.** About 300 words: the hook. Why a Christian should read
   this pagan, or this heretic, or this saint.
2. **General information**
   - *Author and context*: who, when, where, and what was happening
   - *Significance*: why it's on the list and what it gave the West
   - *Main characters / the argument*: a map of the book, not a summary
     that replaces it
3. **Worldview essay.** 1,500 to 3,000 words in the house voice
   (`VOICE.md`). This is the heart of the chapter.
4. **Sessions**, one per reading range, each with:
   - *Before you read*: two or three things to watch for
   - *Comprehension*: what happens, what is argued
   - *Interpretive*: a question with more than one defensible answer from
     the text. This is the shared-inquiry discussion method of the Great
     Books Foundation: the leader asks, the students have to answer from
     the page.
   - *Cultural analysis*: how the book's world thinks, and where our world
     thinks the same way without noticing
   - *Biblical analysis*: questions tied to real `kjv:` unit ids
   - *Application*: what the reader should love, hate or do differently
   - *Summa*: the one question that gathers the whole session
5. **Recitation.** The memory passage, by unit id.
6. **Writing.** One essay prompt, one creative prompt, one Socratic
   debate prompt (argue the other side at full strength).
7. **Evaluation.** Test questions, plus a teacher's key kept in a separate
   file so the anthology can leave it out.
8. **Threads.** Links forward and back to other chapters (Achilles to Aeneas
   to Beowulf to Roland), so the six volumes read as one conversation.
