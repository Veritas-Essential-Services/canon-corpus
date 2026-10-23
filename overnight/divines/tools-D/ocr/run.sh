#!/bin/bash
# run.sh <ia_id> [workdir] : rebuild the corrected witness of one Internet Archive scan.
# Reads data/ocr-fixes/<ia_id>.json (the scans it is collated with, where its index starts,
# and the hand readings), works in [workdir] (default /tmp/ocr-<ia_id>), and writes
# data/corpus/<shelf>/<witness>.corrected.txt (gitignored).
set -e
I=$1; T=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$T/../../../.." && pwd)
W=${2:-/tmp/ocr-$I}; mkdir -p "$W"; cd "$W"
F=$REPO/data/ocr-fixes/$I.json
read -r OTHERS IDX SHELF WIT < <(python3 -c "import json;m=json.load(open('$F'));print(','.join(m['collated_with']),m.get('index_from_page',0),m['shelf'],m['witness'])")
for x in $I ${OTHERS//,/ }; do
  [ -f ${x}_djvu.xml ] || curl -sSfL -o ${x}_djvu.xml https://archive.org/download/$x/${x}_djvu.xml
  [ -f $x.pages.json ] || python3 "$T/pages.py" $x >/dev/null
done
python3 "$T/collate.py" $I ${OTHERS//,/ } | tail -1
python3 "$T/reocr.py" $I | tail -1
python3 "$T/replay.py" $I; python3 "$T/pass2.py" $I
[ "$IDX" -gt 0 ] && python3 "$T/idxrules.py" $I $IDX
python3 "$T/final.py" $I
python3 -c "import json;c=json.load(open('$I.collated.json'));open('$REPO/data/corpus/$SHELF/$WIT.corrected.txt','w').write('\n\n\n'.join(c['pages']))"
echo "wrote data/corpus/$SHELF/$WIT.corrected.txt"
