#!/bin/bash
# usage: fetch.sh id...
A=/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth
for id in "$@"; do
  [ -s $A/texts/$id.txt ] && { echo "$id cached"; continue; }
  repo=$(tr -d "\r" < $A/repo_list.tsv | awk -F'\t' -v i=$id '$1==i{print $2; exit}')
  [ -z "$repo" ] && { echo "$id NOREPO"; continue; }
  ok=0
  for f in $id.txt $id-0.txt $id-8.txt; do
    code=$(curl -sS -o $A/texts/$id.tmp -w '%{http_code}' "https://raw.githubusercontent.com/GITenberg/$repo/master/$f")
    if [ "$code" = 200 ]; then mv $A/texts/$id.tmp $A/texts/$id.txt; echo "$id OK $f $(wc -c <$A/texts/$id.txt)"; ok=1; break; fi
  done
  rm -f $A/texts/$id.tmp
  [ $ok = 0 ] && echo "$id FAIL $repo"
done
