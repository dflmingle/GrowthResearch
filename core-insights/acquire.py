"""Public official artifacts/docs only. No SDK/native initialization or production events."""
from pathlib import Path
import requests,json,hashlib,datetime,tarfile,io,concurrent.futures
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'core-insights';R.mkdir(exist_ok=True)
snapshot=R/'EVIDENCE_GRAPH.before53.json'
if not snapshot.exists():snapshot.write_bytes((ROOT/'prediction-system/EVIDENCE_GRAPH.json').read_bytes())
log=[]
def get(id,url):
 row=dict(id=id,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='public GET; SDK not initialized')
 try:
  a=requests.get(url,timeout=(8,25));row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),sha256=hashlib.sha256(a.content).hexdigest(),last_modified=a.headers.get('Last-Modified'))
  (R/(id+'.raw')).write_bytes(a.content)
  if a.status_code==200:
   if url.endswith('.md'):(R/(id+'.txt')).write_text(a.text,encoding='utf-8')
   elif 'text/html' in a.headers.get('Content-Type',''):
    s=BeautifulSoup(a.content,'html.parser');[n.decompose() for n in s(['script','style','nav','footer'])]
    (R/(id+'.txt')).write_text(s.get_text('\n',strip=True),encoding='utf-8')
  log.append(row);return a
 except Exception as e:row['error']=str(e);log.append(row);return None
def core():
 a=get('core-registry','https://packages.unity.com/com.unity.services.core')
 if a is None or a.status_code!=200:return
 d=a.json();m=d['versions']['1.19.0'];url=m['dist']['tarball'];dest=R/'sdk/core/1.19.0';dest.mkdir(parents=True,exist_ok=True)
 archive=dest/'com.unity.services.core-1.19.0.tgz'
 if not archive.exists():
  a=get('core-1.19.0',url)
  if a is None or a.status_code!=200:return
  archive.write_bytes(a.content)
 data=archive.read_bytes();assert hashlib.sha1(data).hexdigest()==m['dist']['shasum']
 out=dest/'extracted';out.mkdir(exist_ok=True)
 with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as t:
  for item in t.getmembers():
   p=(out/item.name).resolve()
   if not p.is_relative_to(out.resolve()) or item.issym() or item.islnk():raise ValueError('unsafe archive')
   if item.isfile():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.extractfile(item).read())
 (dest/'provenance.json').write_text(json.dumps(dict(sdk='Unity Services Core',version='1.19.0',url=url,sha256=hashlib.sha256(data).hexdigest(),registry_sha1=m['dist']['shasum'],registry_time=d.get('time',{}).get('1.19.0'),metadata=m,scope='official public UPM package, not installed into any game project'),ensure_ascii=False,indent=2),encoding='utf-8')
 print('Core 1.19.0 acquired and registry hash verified',flush=True)
if __name__=='__main__':
 urls={
  'unity-runtime-tree':'https://api.github.com/repos/Unity-Technologies/UnityCsReference/git/trees/master?recursive=1',
  'iap-data-collection':'https://docs.unity.com/en-us/iap/privacy-and-consent/data-collection.md',
  'iap-privacy-overview':'https://docs.unity.com/en-us/iap/privacy-and-consent/overview.md',
  'runtime-identifiers-api':'https://docs.unity3d.com/6000.7/Documentation/ScriptReference/UnityConsent.Identifiers.html',
 }
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  fs=[ex.submit(core)]+[ex.submit(get,k,u) for k,u in urls.items()]
  for f in fs:f.result()
 (R/'ACQUISITION.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
 print([(x['id'],x.get('status')) for x in log],flush=True)
