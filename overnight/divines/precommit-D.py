#!/usr/bin/env python3
"""Lane D pre-commit guard: refuse a commit that changes a shelf another lane owns.

Added 2026-10-03 after Lane D overwrote Lane A's pipeline/perkins_shelf.json
(William Perkins) with a new shelf of the same name. A shelf belongs to the
lane whose commit created it. For every staged pipeline/*_shelf.json that
already exists in HEAD, every earlier commit touching it must be a Lane D
commit (subject starting "Lane D" or "relay D"); otherwise the commit is
refused. A staged deletion of such a file is refused the same way. The one
exception is a restore: staged content identical to the file as the owning
lane last committed it.

Install in a clone with:
    cp overnight/divines/precommit-D.py .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
Lane D's commit helper also runs it before each commit.
"""
import re, subprocess, sys

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout

OURS = re.compile(r"^(Lane D|relay D)\b")
bad = []
for line in git("diff", "--cached", "--name-status").splitlines():
    status, *paths = line.split("\t")
    for path in paths:
        if not re.fullmatch(r"pipeline/[^/]+_shelf\.json", path):
            continue
        if not git("cat-file", "-t", f"HEAD:{path}").strip():
            continue  # new file: nobody owns it yet
        others = [s for s in git("log", "--format=%h %s", "HEAD", "--", path).splitlines()
                  if not OURS.match(s.split(" ", 1)[1])]
        staged = git("rev-parse", f":{path}").strip()
        last_theirs = git("rev-parse", f"{others[0].split()[0]}:{path}").strip() if others else ""
        if others and staged != last_theirs:
            bad.append(f"{path}: owned by another lane ({others[-1]})")
if bad:
    print("precommit-D: refused, this commit changes a shelf Lane D does not own:", *bad, sep="\n  ")
    print("Pick a different shelf name, or ask the owning lane.")
    sys.exit(1)
