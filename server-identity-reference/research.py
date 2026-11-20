"""Public documentation/license retrieval only; no identity inputs or SDK execution."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,re,urllib.request,urllib.error
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
D.mkdir(exist_ok=True);(D/'sources').mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if not (D/'HISTORY_BEFORE.json').exists():
    paths={p.relative_to(R).as_posix():sha(p) for p in R.iterdir() if p.is_file() and re.match(r'^\d\d_',p.name)}
    for rel in ['engineering76/ARTIFACT_MANIFEST.json','official-samples-audit/ARTIFACT_MANIFEST.json','adjust-mechanisms/ARTIFACT_MANIFEST.json']:
        for x in load(R/rel):
            if x['path'] in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']:continue
            p=R/x['path'];assert sha(p)==x['sha256'],p
            paths[x['path']]=x['sha256']
        paths[rel]=sha(R/rel)
    save(D/'HISTORY_BEFORE.json',paths)
    (D/'EVIDENCE_INDEX.before.md').write_bytes((R/'EVIDENCE_INDEX.md').read_bytes())
    (D/'EVIDENCE_GRAPH.before.json').write_bytes((R/'prediction-system/EVIDENCE_GRAPH.json').read_bytes())
    save(D/'BASELINE_HASHES.json',{p:sha(R/p) for p in ['EVIDENCE_INDEX.md','prediction-system/EVIDENCE_GRAPH.json']})

manifest=load(D/'FETCH_MANIFEST.json') if (D/'FETCH_MANIFEST.json').exists() else []
def fetch(item):
    sid,url,kind=item
    existing=next((x for x in manifest if x['id']==sid and x['url']==url),None)
    if existing:return existing
    row=dict(id=sid,url=url,kind=kind,collected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    req=urllib.request.Request(url,headers={'User-Agent':'GrowthResearch-public-doc-review/1.0','Accept':'application/json' if 'api.github.com' in url else '*/*'})
    try:
        with urllib.request.urlopen(req,timeout=30) as response:
            body=response.read(2_000_001)
            if len(body)>2_000_000:raise ValueError('Body limit exceeded; not stored')
            row.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'),last_modified=response.headers.get('Last-Modified'))
    except urllib.error.HTTPError as e:
        body=e.read(200000);row.update(status=e.code,final_url=e.url,error=str(e))
    except Exception as e:
        row.update(status='FETCH_FAILED',error=str(e));return row
    p=D/'sources'/(sid+'.raw');p.write_bytes(body)
    row.update(path=p.relative_to(R).as_posix(),bytes=len(body),sha256=sha(p))
    return row
def batch(items):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(fetch,items))
    for row in results:
        prev=next((x for x in manifest if x['id']==row['id']),None)
        if prev:assert prev==row
        else:manifest.append(row)
        print(json.dumps({k:row.get(k) for k in ['id','status','bytes','error']},ensure_ascii=False))
    save(D/'FETCH_MANIFEST.json',manifest)
    return results

if __name__=='__main__':
    repos={'splink':'moj-analytical-services/splink','dedupe':'dedupeio/dedupe','recordlinkage':'J535D165/recordlinkage','feast':'feast-dev/feast'}
    heads=batch([(k+'-head','https://api.github.com/repos/'+repo+'/commits?per_page=1','Official repository commit metadata') for k,repo in repos.items()])
    pins=[]
    for h in heads:
        if h.get('status')!=200:continue
        data=load(R/h['path'])[0];k=h['id'].removesuffix('-head');repo=repos[k]
        pins.append(dict(component=k,repository=repo,commit=data['sha'],commit_date=data['commit']['committer']['date'],
                         commit_url=data['html_url'],pin_source=h['id'],scope='Pinned snapshot; not latest release claim'))
    save(D/'COMPONENT_PINS.json',pins)
    items=[]
    for p in pins:
        k=p['component'];base='https://raw.githubusercontent.com/'+p['repository']+'/'+p['commit']+'/'
        for label,path in [('readme','README.md'),('license','LICENSE')]:items.append((k+'-'+label,base+path,'Pinned official source documentation/license'))
        items.append((k+'-tree','https://api.github.com/repos/'+p['repository']+'/git/trees/'+p['commit']+'?recursive=1','Official repository file-tree metadata; no private data'))
    batch(items)
