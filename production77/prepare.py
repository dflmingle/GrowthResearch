from pathlib import Path
import datetime,hashlib,json,shutil
from urllib.parse import urlsplit,urlunsplit

R=Path(__file__).resolve().parent.parent;D=R/'production77';(D/'sources').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (D/'HISTORY_BEFORE.json').exists(),'Do not replace frozen history'
h={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name[:2].isdigit() and int(p.name[:2])<=76}
for rel in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:h[rel]=sha(R/rel)
save(D/'HISTORY_BEFORE.json',h)
shutil.copyfile(R/'EVIDENCE_INDEX.md',D/'EVIDENCE_INDEX.before.md');shutil.copyfile(R/'prediction-system/EVIDENCE_GRAPH.json',D/'EVIDENCE_GRAPH.before.json')
g=json.loads((D/'EVIDENCE_GRAPH.before.json').read_text('utf-8'))
catalog=[]
for s in g['sources']:
 if s.get('url'):catalog.append(dict(id=s['id'],url=s['url'],path=s['path'],sha256=s['sha256']))
save(D/'PRIOR_URL_CATALOG.json',catalog)
reuseids=['S25','S26','S27','S31','MA60S06','MA60S07','MA60S11','MA60S12','MA60S17','IG72S05','IV74S09','EN76S04']
reuse=[next(s for s in g['sources'] if s['id']==sid) for sid in reuseids]
for x in reuse:assert sha(R/x['path'])==x['sha256']
save(D/'REUSED_EVIDENCE.json',reuse)
shutil.copyfile(R/'identity-value74/fetch.py',D/'fetch.py')
save(D/'discovery.json',[
 ['al-job-list','https://boards-api.greenhouse.io/v1/boards/applovin/jobs'],
 ['unity-job-list','https://boards-api.greenhouse.io/v1/boards/unity3d/jobs'],
 ['al-patent-search','https://patents.google.com/xhr/query?url=q%3D%2522identity%2Bgraph%2522%26assignee%3DApplovin%26num%3D20&exp='],
 ['unity-patent-search','https://patents.google.com/xhr/query?url=q%3D%2522cross-device%2522%26assignee%3DUnity%2BTechnologies%26num%3D20&exp='],
 ['al-paper-search','https://api.openalex.org/works?search=AppLovin%20user%20representation&per-page=10'],
 ['unity-paper-search','https://api.openalex.org/works?search=Unity%20Vector%20identity%20advertising&per-page=10']])
save(D/'SEARCH_PLAN.json',dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),allowed_categories=['Official jobs/team duties','Patents','Official talks/blogs/papers','Acquisition/integration/partner architecture'],
 exclusion='No SDK scan,privacy-policy survey,partner lists,simulation,mock development or re-fetch of archived evidence URLs',
 bridge='identity component -> actual receiving product -> value-model feature consumption',
 stopping='One bounded index batch;follow only previously unseen original primary candidates with identity/representation/product content. Stop if no bridge,report zero C_graph upgrades. Search failures not absence evidence.'))
print(json.dumps(dict(history=len(h)-2,existing_urls=len(catalog),reused=len(reuse))))
