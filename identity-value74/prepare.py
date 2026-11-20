from pathlib import Path
import datetime, hashlib, json, shutil
from urllib.parse import quote_plus

R=Path(__file__).resolve().parent.parent
D=R/'identity-value74';D.mkdir(exist_ok=True);(D/'sources').mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (D/'HISTORY_BEFORE.json').exists(),'Do not replace baseline'
history={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=73}
for rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:
 history[rel]=sha(R/rel)
save(D/'HISTORY_BEFORE.json',history)
shutil.copyfile(R/'EVIDENCE_INDEX.md',D/'EVIDENCE_INDEX.before.md')
shutil.copyfile(R/'prediction-system/EVIDENCE_GRAPH.json',D/'EVIDENCE_GRAPH.before.json')
shutil.copyfile(R/'identity72-experiments73/fetch.py',D/'fetch.py')
queries=[
 ('search-al-partner','site:applovin.com identity matching LiveRamp device graph'),
 ('search-wurl-partner','site:wurl.com UID2 identity Experian household'),
 ('search-unity-partner','site:unity.com RampID Vector identity matching'),
 ('search-unity-contract','site:docs.unity.com exchange identity eids RampID'),
 ('search-ramp-partner','site:liveramp.com Unity AppLovin identity'),
 ('search-model-ablation','Axon Vector identity features ablation cross app user representation')]
save(D/'search.json',[(k,'https://www.bing.com/search?q='+quote_plus(q)) for k,q in queries])
save(D/'SEARCH_PLAN.json',dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),queries=queries,
 scope='Targeted primary identity partner/feature-ablation evidence;no SDK scanning,dataset retries or production API calls',
 stopping='One initial search batch plus primary contract links;if no new C/D evidence retain UNKNOWN and stop public reverse engineering'))
print(json.dumps(dict(frozen_files=len(history)-2,queries=len(queries))))
