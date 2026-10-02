# Starting another burn

The relay lives in this folder and survives between burns: queues, shelves, map and logs persist. Restarting is flipping switches, not rebuilding.

**The one-line way:** open a Claude Code session on canon-corpus and say:
> Start a usage burn of the Armarium relay until <day, date> <time> Missouri time. Follow overnight/divines/RESTART.md.

**What that session (or you, by hand) does:**

1. Check out `claude/armarium-divines`. If the branch was merged and deleted, recreate it from `main`; these files will be there.
2. Edit `overnight/divines/RUN-CONTROL.json`: `"mode": "on"`; `"stop_after"` = the new stop as an ISO time with the right Central offset (`-05:00` during daylight time, mid-March to early November; `-06:00` otherwise); any lane you don't want → `"off"`; update `note`. Commit and push.
3. Re-enable the four routines at claude.ai/code/routines, or recreate them from `ROUTINES.md` if deleted: Cloud, Opus, repo canon-corpus, the full-network environment, hourly, **no connectors**.
4. Press **Run now** on Lane A, then the others.
5. To add authors: append items to the right lane's `QUEUE-<L>.json` (status `todo`, a clear `scope`) and notes to `lanes/<L>.md`. A new grouping gets a new lane: `lanes/E.md`, `QUEUE-E.json`, `LOCK-E.json`, `REPORT-E.md`, `docs/divines-map/E-<slug>.md`, `"E": "on"` in RUN-CONTROL, and a fifth routine.
6. Items marked `done` stay done. A lane with nothing left spends its time on RULES.md §5 (verification and measurement); add new items first if you want acquisition.

**Ending a burn early:** set `"mode": "off"` and push. Running workers stop at their next item boundary; idle fires log at most once a day. Disable (don't delete) the routines to silence them fully.
