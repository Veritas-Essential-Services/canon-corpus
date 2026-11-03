# overnight/divines — the Armarium relay

Unattended cloud routines that build the Armarium collection in bursts. Four lanes (A Divines · B Classical · C Translator shelves · D Storytellers), one branch (`claude/armarium-divines`), one switch (`RUN-CONTROL.json`).

- `RULES.md`: what every worker does. `lanes/<L>.md`: each lane's notes.
- `QUEUE-<L>.json`, `LOCK-<L>.json`, `REPORT-<L>.md`, `DIGEST-<L>.md`: each lane's own state; no lane touches another's.
- `RUN-CONTROL.json`: Adam's on/off switch and stop time. `RESTART.md`: how to start the next burn. `ROUTINES.md`: the four routine prompts.
- The master checklist is `docs/DIVINES-MASTER-MAP.md`, generated from `docs/divines-map/*.md`.

After a burn, read the four DIGEST files first.
