# reads.py: load the hand readings for a scan from the committed fix list, data/ocr-fixes/<id>.json
import json,os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','..'))
def path(i): return os.path.join(REPO,'data','ocr-fixes',i+'.json')
def meta(i): return json.load(open(path(i))) if os.path.exists(path(i)) else {}
def load(i): return meta(i).get('reads',[])
