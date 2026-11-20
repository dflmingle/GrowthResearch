"""Static SDK views and public documentation only; no production requests."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, requests

ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'client-growth';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n','utf-8')
snapshot=OUT/'EVIDENCE_GRAPH.before_client56.json'
if not snapshot.exists():snapshot.write_bytes((ROOT/'prediction-system/EVIDENCE_GRAPH.json').read_bytes())
baseline=OUT/'HISTORY.before.json'
if not baseline.exists():
    files=list(ROOT.glob('[0-9][0-9]_*.md'))
    files += [ROOT/'prediction-system/EVIDENCE_GRAPH.json']
    files += [p for p in (ROOT/'prediction-validation').rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    save(baseline,[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in files])

JADX=Path('C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar')
tasks=[
 ('max-1364','AppLovin/MAX/13.6.4',r'^com\.applovin\.impl\.(?:a6|i5|v3)$',5),
 ('unity-4181','Unity/Ads/4.18.1',r'^com\.unity3d\.ads\.core\.(?:domain\.(?:AndroidBuildHeaderBiddingToken|CommonInitAwaitingGetHeaderBiddingToken|AndroidGetLimitedSessionToken)|data\.repository\.(?:AndroidCampaignRepository|AndroidDeviceInfoRepository)|data\.datasource\.(?:AndroidPrivacyDeviceInfoDataSource|AndroidFIdDataSource|AndroidStaticDeviceInfoDataSource))$',12),
 ('levelplay-950','Unity/LevelPlay/9.5.0',r'^com\.ironsource\.(?:Q1|g2|N2|C|U1|mediationsdk\.r|mediationsdk\.adapter\.AbstractRewardedVideoAdapter)$',10),
]
def decompile(task):
 name,rel,pattern,maximum=task;jar=ROOT/'ThirdPartySDKs'/rel/'classes.jar';dest=OUT/'java'/name;dest.mkdir(parents=True,exist_ok=True)
 command=['java','-Xmx800m','-cp',str(JADX)+';'+str(ROOT),'SelectJadx',str(jar),str(dest),pattern,str(maximum)]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (dest/'jadx.log').open('wb') as f:
  run=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,timeout=160)
 return dict(name=name,sdk=rel,classes_jar_sha256=sha(jar),decompiler_jar_sha256=sha(JADX),
     static_only=True,started_utc=started,exit_code=run.returncode,pattern=pattern,
     source_files=[p.relative_to(ROOT).as_posix() for p in dest.rglob('*.java')])

def fetch(item):
 name,url=item;raw=OUT/(name+'.md')
 if raw.exists():return dict(id=name,url=url,scope='existing local official-doc copy reused',sha256=sha(raw),path=raw.relative_to(ROOT).as_posix())
 row=dict(id=name,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='public documentation GET only')
 try:
  a=requests.get(url,timeout=(8,30));raw.write_bytes(a.content)
  row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),sha256=sha(raw),path=raw.relative_to(ROOT).as_posix())
 except requests.RequestException as e:row['error']=type(e).__name__
 return row

if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  decomp=list(ex.map(decompile,tasks))
 save(OUT/'DECOMPILE.json',decomp)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  docs=list(ex.map(fetch,[('unity-post-install-data','https://docs.unity.com/en-us/grow/acquire/partner-integration/post-install-event-data.md'),
      ('unity-attribution-types','https://docs.unity.com/en-us/grow/acquire/partner-integration/attribution/introduction.md')]))
 save(OUT/'PUBLIC_FETCHES.json',docs)
 print('Static decompile',[(r['name'],r['exit_code'],len(r['source_files'])) for r in decomp])
 print('Docs',[(r['id'],r.get('status',r.get('error','reused'))) for r in docs])
