#!/bin/bash
# runall.sh PLAN.json : apply, fetch, verify, commit each planned shelf; failures left uncommitted and logged.
B=/tmp/claude-0/-home-user-canon-corpus/e2b3c735-11ff-534b-9d5b-21a3d720dd05/scratchpad/bloom
PLAN=$1
cd /home/user/canon-corpus
for s in $(python3 -c "import json;print(' '.join(p['shelf'] for p in json.load(open('$PLAN'))))"); do
  if grep -qx "$s" $B/done.txt 2>/dev/null; then continue; fi
  if [ -n "$(git status --porcelain pipeline/${s}_shelf.json)" ]; then echo "SKIP-DIRTY $s"; continue; fi
  au=$(python3 -c "import json;print([p['author'] for p in json.load(open('$PLAN')) if p['shelf']=='$s'][0])")
  python3 $B/apply.py $PLAN $s || { echo "APPLY-FAIL $s"; continue; }
  timeout 600 python3 pipeline/fetch_shelf.py $s > $B/logs/$s.fetch 2>&1
  timeout 300 python3 pipeline/fetch_shelf.py $s --verify --record > $B/logs/$s.verify 2>&1
  fails=$(grep -E "items, [1-9][0-9]* failed" $B/logs/$s.fetch)
  mism=$(grep -E "verify: [1-9][0-9]* mismatched|rights flags: \[.+\]" $B/logs/$s.verify)
  if [ -z "$fails$mism" ] && grep -q "verify: 0 mismatched" $B/logs/$s.verify; then
    n=$(git diff --numstat pipeline/${s}_shelf.json | wc -l)
    git add pipeline/${s}_shelf.json && git commit -q -m "Bloom: ${au} (${s})

Works on Bloom's Western Canon list, US public domain, verified by
fetch_shelf.py --verify --record. Evidence per row under _bloom.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019py4L13uTQm4WKARXE6hs6" && echo "$s" >> $B/done.txt && echo "OK $s"
  else
    echo "NEEDS-REVIEW $s :: $fails :: $mism"
  fi
done
echo ALLDONE
