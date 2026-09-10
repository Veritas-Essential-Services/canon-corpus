# Scripture echo detection

    python3 build_kjv.py                 # -> kjv.tsv, kjv.norm.tsv, kjv.jsonl (needs pythonbible-kjv)
    python3 echoes2.py  KJV.json TARGET.json out.jsonl BG1.txt,BG2.txt [min_hits] [min_run]
    python3 names2.py   KJV.json TARGET.json out.jsonl BG1.txt,BG2.txt

Two channels, deliberately separate:

* `echoes2.py` — shared rare 4-grams. Finds quotation. Low recall (~1%);
  everything it reports still needs an eye on it.
* `names2.py`  — biblical proper nouns, gazetteer built from the data by the
  "never seen lowercase" test. High precision, narrow.

**The background corpus is part of the instrument.** Use period-matched prose
(Gibbon, Burke, Federalist) for `echoes2.py`. Do NOT use them for `names2.py` —
Gibbon is a history of Christianity and will delete Adam, Eve and Satan from the
gazetteer. Milton scored lower than Homer because of exactly this. Names need a
background with no religious content.

See `SCRIPTURE ECHO — Greppable KJV and the Two-Channel Detector (2026-09-10).md`
in the vault under `9 - Projects/Canon OS/`.
