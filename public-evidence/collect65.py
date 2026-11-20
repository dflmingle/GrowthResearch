from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import requests, hashlib, json, re
from bs4 import BeautifulSoup

ROOT=Path(r'D:\GrowthResearch')
BASE=ROOT/'public-evidence'
(BASE/'raw').mkdir(parents=True,exist_ok=True)
(ROOT/'public-experiments'/'audit').mkdir(parents=True,exist_ok=True)
history={}
for p in ROOT.glob('*.md'):
    if re.match(r'\d\d_',p.name) and int(p.name[:2])<=64: history[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
snapshot=BASE/'HISTORY.before65.json'
if not snapshot.exists():
    snapshot.write_text(json.dumps(history,ensure_ascii=False,indent=2),encoding='utf-8')
    for rel,dest in [('prediction-system/EVIDENCE_GRAPH.json','EVIDENCE_GRAPH.before65.json'),('EVIDENCE_INDEX.md','EVIDENCE_INDEX.before65.md')]:
        (BASE/dest).write_bytes((ROOT/rel).read_bytes())

PACKAGES={'car':'com.dino.race.master','meow':'com.oakever.meowdoku','rotate':'com.nebula.rotaterings','jewel':'color.number.paint.pixle.art.sort.jigsaw'}
targets=[]
for slug,pkg in PACKAGES.items():
    targets.extend([(slug+'-play',f'https://play.google.com/store/apps/details?id={pkg}&hl=en&gl=US'),
                    (slug+'-appbrain',f'https://www.appbrain.com/app/{pkg}'),
                    (slug+'-aptoide',f'https://ws75.aptoide.com/api/7/app/get/package_name={pkg}')])
targets += [
 ('criteo-attribution','https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/'),
 ('criteo-uplift','https://ailab.criteo.com/criteo-uplift-prediction-dataset/'),
 ('ipinyou-repo','https://raw.githubusercontent.com/wnzhang/make-ipinyou-data/master/README.md'),
 ('ipinyou-license','https://raw.githubusercontent.com/wnzhang/make-ipinyou-data/master/LICENSE'),
 ('openbandit-repo','https://raw.githubusercontent.com/st-tech/zr-obp/master/README.md'),
 ('openbandit-data','https://research.zozo.com/data.html'),
 ('uci-retail','https://archive.ics.uci.edu/dataset/352/online+retail'),
 ('uci-retail-api','https://archive.ics.uci.edu/api/dataset?id=352'),
 ('uci-retailii','https://archive.ics.uci.edu/dataset/502/online+retail+ii'),
 ('kuairand','https://raw.githubusercontent.com/chongminggao/KuaiRand/main/README.md'),
 ('kuairand-license','https://raw.githubusercontent.com/chongminggao/KuaiRand/main/LICENSE'),
 ('game-search-github','https://api.github.com/search/repositories?q=game+ltv+dataset&per_page=8'),
 ('game-search-zenodo','https://zenodo.org/api/records?q=game%20lifetime%20value&size=8'),
 ('game-search-datacite','https://api.datacite.org/dois?query=titles.title:%22game%22%20AND%20%22revenue%22&page[size]=8'),
 ('criteo-search','https://www.bing.com/search?q=Criteo+attribution+modeling+bidding+dataset+license'),
 ('game-search-web','https://www.bing.com/search?q=public+mobile+game+lifetime+value+dataset+license+multiple+games'),
]

def fetch(item):
    ident,url=item;path=BASE/'raw'/ident
    started=datetime.now(timezone.utc).isoformat()
    if path.with_suffix('.json').exists():return json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
    try:
        response=requests.get(url,headers={'User-Agent':'GrowthResearch-public-evidence-audit/65 (read-only academic research)'},timeout=(12,25))
        data=response.content
        if len(data)>6_000_000: raise ValueError('Page exceeds bounded public metadata size')
        path.with_suffix('.raw').write_bytes(data)
        txt=response.text
        if '<html' in txt[:1000].lower() or '<!doctype html' in txt[:1000].lower():
            soup=BeautifulSoup(txt,'html.parser')
            for tag in soup(['script','style','noscript']):tag.decompose()
            txt=soup.get_text('\n',strip=True)
        path.with_suffix('.txt').write_text(txt,encoding='utf-8')
        record={'id':ident,'url':url,'final_url':response.url,'status':response.status_code,'observed_utc':started,
          'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'path':path.with_suffix('.raw').relative_to(ROOT).as_posix(),
          'text_path':path.with_suffix('.txt').relative_to(ROOT).as_posix(),'content_type':response.headers.get('Content-Type'),
          'last_modified':response.headers.get('Last-Modified'),'access':'public single request; no login, bypass, cookies supplied or retries'}
    except Exception as e: record={'id':ident,'url':url,'observed_utc':started,'error':type(e).__name__+': '+str(e)}
    path.with_suffix('.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return record

if __name__=='__main__':
    records=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for f in as_completed([pool.submit(fetch,t) for t in targets]):
            rec=f.result();records.append(rec);print(json.dumps({k:rec.get(k) for k in ['id','status','bytes','error']},ensure_ascii=True),flush=True)
    (BASE/'FETCH_LEDGER.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
