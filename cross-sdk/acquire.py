"""Public official packages only; content-addressed reuse, never initialize SDKs."""
from pathlib import Path
import json,hashlib,datetime,requests,concurrent.futures,tarfile,io,re,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk';R.mkdir(exist_ok=True)
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
baseline=ROOT/'prediction-system/EVIDENCE_GRAPH.json'
snapshot=R/'EVIDENCE_GRAPH.before47.json'
if not snapshot.exists():snapshot.write_bytes(baseline.read_bytes())
log=[]
def get(name,url):
 row=dict(id=name,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  a=requests.get(url,timeout=(8,25));row.update(status=a.status_code,final_url=a.url,bytes=len(a.content),sha256=hashlib.sha256(a.content).hexdigest(),last_modified=a.headers.get('Last-Modified'))
  (R/(name+'.raw')).write_bytes(a.content)
  log.append(row)
  return a
 except Exception as e:row['error']=str(e);log.append(row);return None

def upm(name):
 a=get(name+'-registry','https://packages.unity.com/com.unity.'+name)
 if a is None or a.status_code!=200:return
 d=a.json();versions=d.get('versions',{});latest=d.get('dist-tags',{}).get('latest')
 choices=[latest]
 # IAP 5.4 is the product evidence referenced in report 43; latest separately identified.
 if name=='purchasing':choices+=['5.4.0']
 for v in dict.fromkeys(choices):
  if v not in versions:continue
  m=versions[v];url=m.get('dist',{}).get('tarball')
  if not url:continue
  dest=R/'packages'/name/v;dest.mkdir(parents=True,exist_ok=True)
  archive=dest/(name+'-'+v+'.tgz')
  if archive.exists():content=archive.read_bytes();print('reuse',archive,flush=True)
  else:
   t=get(name+'-'+v,url)
   if t is None or t.status_code!=200:continue
   content=t.content;archive.write_bytes(content)
  sha1=hashlib.sha1(content).hexdigest();expected=m.get('dist',{}).get('shasum')
  if expected and sha1!=expected:raise ValueError('UPM hash mismatch')
  out=dest/'extracted';out.mkdir(exist_ok=True)
  with tarfile.open(fileobj=io.BytesIO(content),mode='r:gz') as t:
   for member in t.getmembers():
    target=(out/member.name).resolve()
    if not target.is_relative_to(out.resolve()) or member.issym() or member.islnk():raise ValueError('unsafe member')
    if member.isfile():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(t.extractfile(member).read())
  (dest/'provenance.json').write_text(json.dumps(dict(sdk='com.unity.'+name,version=v,url=url,sha256=hashlib.sha256(content).hexdigest(),sha1=sha1,registry_sha1=expected,registry_time=d.get('time',{}).get(v),package_metadata=m,acquired_utc=NOW,scope='official UPM standalone, not target-game version'),ensure_ascii=False,indent=2),encoding='utf-8')
  print('acquired',name,v,flush=True)

if __name__=='__main__':
 # New packages only; pre-existing Maven SDKs are not downloaded again.
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(upm,['services.analytics','purchasing']))
 singular=get('singular-metadata','https://repo.maven.apache.org/maven2/com/singular/sdk/singular_sdk/maven-metadata.xml')
 if singular is not None and singular.status_code==200:
  t=ET.fromstring(singular.content);v=t.findtext('./versioning/release');dest=R/'packages/singular'/v;dest.mkdir(parents=True,exist_ok=True);art=[]
  for suffix in ['.pom','.aar','-sources.jar']:
   url=f'https://repo.maven.apache.org/maven2/com/singular/sdk/singular_sdk/{v}/singular_sdk-{v}{suffix}'
   p=dest/('singular_sdk-'+v+suffix)
   if p.exists():continue
   a=get('singular-'+v+suffix.replace('.','-'),url)
   if a is None or a.status_code!=200:continue
   p.write_bytes(a.content);art.append(dict(path=p.relative_to(ROOT).as_posix(),url=url,sha256=hashlib.sha256(a.content).hexdigest(),last_modified=a.headers.get('Last-Modified')))
   if suffix=='.aar':
    with zipfile.ZipFile(p) as z:(dest/'classes.jar').write_bytes(z.read('classes.jar'))
  (dest/'provenance.json').write_text(json.dumps(dict(sdk='Singular Android',version=v,artifacts=art,acquired_utc=NOW,scope='standalone official Maven artifact; not target-game integration'),indent=2),encoding='utf-8')
 get('adjust-changelog','https://raw.githubusercontent.com/adjust/android_sdk/master/CHANGELOG.md')
 get('max-changelog','https://raw.githubusercontent.com/AppLovin/AppLovin-MAX-Unity-Plugin/master/CHANGELOG.md')
 get('unity-ads-changelog','https://raw.githubusercontent.com/Unity-Technologies/unity-ads-android/master/CHANGELOG.md')
 (R/'ACQUISITION.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
