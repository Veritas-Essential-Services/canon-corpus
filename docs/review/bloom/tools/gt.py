import json,sys,re
h=json.load(open('held2.json'));core=json.load(open('core.json'))
def cls(br):
    return 'main' if 'main' in br else 'relay' if 'claude/armarium-divines' in br else 'pr38' if br==['claude/project-thread-yu0x73'] else 'branch:'+br[0]
for pat in sys.argv[1:]:
    r=re.compile(pat,re.I);print('##',pat)
    for s,e in h.items():
        for slug,(sec,i,t) in e['rows'].items():
            if r.search(t) or r.search(slug): print('  ',cls(e['branches']),s,'|',t[:110])
    for k,e in core.items():
        if r.search(e['title']) or r.search(k): print('   ',cls(e['branches']),'core:'+k,'|',e['author'][:30],e['title'][:80])
