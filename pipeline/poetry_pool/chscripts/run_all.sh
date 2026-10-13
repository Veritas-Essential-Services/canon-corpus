set -e
cd /tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/chscripts
P="python3 -I"
$P lyra.py; $P burt.py; $P wiggin.py 22922 INDEX; $P wiggin.py 34237 "INDEX BY"; $P blue.py; $P cambridge.py
$P generic_toc.py 67522 CONTENTS ILLUSTRATIONS
$P patch.py 67522 "Canterbury" first_line "An ancient story I’ll tell you anon"
$P patch.py 67522 "Canterbury" title "King John and the Abbot of Canterbury"
$P generic_toc.py 63858 CONTENTS "SUGGESTIONS FOR TEACHERS"
$P hyett.py
$P patch.py 72625 "To His Saviour, A Child; A Present from a Child" first_line "Go pretty child, and bear this flower"
$P patch.py 72625 "An Ode of the Birth of Our Saviour" first_line "In numbers, and but these few,"
$P patch.py 72625 "The Bells" first_line "Ring out, wild bells, to the wild sky,"
$P patch.py 72625 "Noël" first_line "On a winter’s night long time ago"
timeout 100 $P garland.py; $P gems.py; $P narr.py; timeout 100 $P hither.py
$P greenaway.py; timeout 110 $P firstidx.py 26197 "Index of First Lines\]" "Illustration: Preface"
$P halliwell.py; $P summerly2.py; $P knife.py
$P capsheads.py 44835 "^ *CHILDREN\.$" 8 14
$P keepsake.py; $P battle.py; $P lamb.py
$P generic_toc.py 42850 CONTENTS. "LIST OF ILLUSTRATIONS"
$P -c "
import json
p='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth/rows/42850.jsonl'
r=[json.loads(l) for l in open(p)]
for x in r: x['author']='Robert Browning'
open(p,'w').write(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in r))"
$P smiles_ewing.py
$P patch.py 16686 "Master Fritz" first_line "Fritz and I are not brother and sister, but we're next-door"
$P patch.py 27441 "Verses, supposed to be written by Alexander Selkirk" first_line "I am monarch of all I survey,"
$P patch.py 62119 "Two Nut Trees" first_line "I had a little nut tree,"
