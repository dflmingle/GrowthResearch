"""Public distribution acquisition only. Never loads/initializes an SDK."""
from pathlib import Path
import requests,json,hashlib,datetime,concurrent.futures,xml.etree.ElementTree as ET,zipfile,re,sys,time
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
SPECS=[
 ('AppLovin','MAX','com.applovin','applovin-sdk',None,'https://repo.maven.apache.org/maven2','core'),
 ('Adjust','Android','com.adjust.sdk','adjust-android',None,'https://repo.maven.apache.org/maven2','core'),
 ('AppsFlyer','Android','com.appsflyer','af-android-sdk','6.14.2','https://repo.maven.apache.org/maven2','core'),
 ('AppsFlyer','Android','com.appsflyer','af-android-sdk','6.17.5','https://repo.maven.apache.org/maven2','core'),
 ('Meta','FacebookCore','com.facebook.android','facebook-core','18.0.3','https://repo.maven.apache.org/maven2','core'),
 ('Meta','AudienceNetwork','com.facebook.android','audience-network-sdk','6.22.0','https://repo.maven.apache.org/maven2','core'),
 ('TikTok','Business','com.tiktok','tiktok-business-android-sdk','1.6.1','https://repo.maven.apache.org/maven2','core'),
 ('TikTok','Business','com.tiktok','tiktok-business-android-sdk','1.7.1','https://repo.maven.apache.org/maven2','core'),
 ('Google','MobileAds','com.google.android.gms','play-services-ads','25.1.0','https://dl.google.com/dl/android/maven2','core'),
 ('Google','MobileAds','com.google.android.gms','play-services-ads','25.2.0','https://dl.google.com/dl/android/maven2','core'),
 ('Google','FirebaseAnalytics','com.google.firebase','firebase-analytics','22.1.2','https://dl.google.com/dl/android/maven2','core'),
 ('Google','FirebaseAnalytics','com.google.firebase','firebase-analytics','22.4.0','https://dl.google.com/dl/android/maven2','core'),
 ('Google','FirebaseAnalytics','com.google.firebase','firebase-analytics','23.2.0','https://dl.google.com/dl/android/maven2','core'),
 ('Google','InstallReferrer','com.android.installreferrer','installreferrer','2.2','https://dl.google.com/dl/android/maven2','core'),
 ('Unity','Ads','com.unity3d.ads','unity-ads','4.17.0','https://repo.maven.apache.org/maven2','core'),
 ('Unity','Ads','com.unity3d.ads','unity-ads','4.18.1','https://repo.maven.apache.org/maven2','core'),
 ('Moloco','Android','com.moloco.sdk','moloco-sdk','4.4.0','https://repo.maven.apache.org/maven2','core'),
 ('InMobi','Android','com.inmobi.monetization','inmobi-ads-kotlin','11.1.1','https://repo.maven.apache.org/maven2','core'),
 ('Liftoff','Vungle','com.vungle','vungle-ads','7.6.3','https://repo.maven.apache.org/maven2','core'),
 ('Liftoff','Vungle','com.vungle','vungle-ads','7.7.1','https://repo.maven.apache.org/maven2','core'),
 ('AppMetrica','Android','io.appmetrica.analytics','analytics','7.14.2','https://repo.maven.apache.org/maven2','core'),
 ('AppMetrica','Android','io.appmetrica.analytics','analytics','8.3.0','https://repo.maven.apache.org/maven2','core'),
]
for a,v in [('facebook-adapter','6.22.0.0'),('google-adapter','25.1.0.0'),('unityads-adapter','4.17.0.0'),('ironsource-adapter','9.3.0.0.0'),('mintegral-adapter','16.9.91.0'),('bytedance-adapter','7.8.5.2.0'),('moloco-adapter','4.4.0.0'),('inmobi-adapter','11.1.1.0'),('vungle-adapter','7.6.3.0')]:
 SPECS.append(('AppLovin','Adapter-'+a,'com.applovin.mediation',a,v,'https://repo.maven.apache.org/maven2','adapter'))

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def bounded_get(url,timeout=None):
 started=time.monotonic()
 a=requests.get(url,timeout=(8,12),stream=True)
 data=bytearray()
 try:
  for chunk in a.iter_content(65536):
   data.extend(chunk)
   if time.monotonic()-started>45:raise TimeoutError('bounded public download exceeded 45 seconds')
   if len(data)>90*1024*1024:raise ValueError('bounded public download exceeded 90 MiB')
 finally:a.close()
 a._content=bytes(data);a._content_consumed=True
 return a
def acquire(s):
 vendor,sdk,group,artifact,v,repo,kind=s
 base=repo+'/'+group.replace('.','/')+'/'+artifact
 rec=dict(vendor=vendor,sdk=sdk,group=group,artifact=artifact,requested_version=v,kind=kind,utc=now(),requests=[])
 root=R/vendor/sdk;root.mkdir(parents=True,exist_ok=True)
 try:
  mr=bounded_get(base+'/maven-metadata.xml')
  rec['requests'].append({'url':mr.url,'status':mr.status_code})
  if mr.ok:
   (root/'maven-metadata.xml').write_bytes(mr.content)
   mt=ET.fromstring(mr.content);versions=[x.text for x in mt.findall('.//version')]
   rec['metadata_versions']=versions;rec['metadata_updated']=mt.findtext('./versioning/lastUpdated')
   if v is None:v=mt.findtext('./versioning/release') or versions[-1]
  if not v:raise ValueError('no version resolved')
  rec['version']=v;dest=root/v;dest.mkdir(exist_ok=True);prefix=f'{base}/{v}/{artifact}-{v}'
  artifacts=[];rec['artifacts']=artifacts
  for suffix in ['.pom','.aar','-sources.jar','.jar']:
   if suffix=='.jar' and any(x['path'].endswith('.aar') for x in artifacts):continue
   url=prefix+suffix;resp=bounded_get(url)
   q={'url':url,'status':resp.status_code,'final_url':resp.url,'last_modified':resp.headers.get('Last-Modified')};rec['requests'].append(q)
   if not resp.ok:continue
   if len(resp.content)>90*1024*1024:q['error']='bounded collection: artifact over 90 MB';continue
   if suffix!='.pom' and not resp.content.startswith(b'PK'):q['error']='not ZIP';continue
   p=dest/(artifact+'-'+v+suffix);p.write_bytes(resp.content)
   item={'path':str(p.relative_to(R)),'sha256':hashlib.sha256(resp.content).hexdigest(),'bytes':len(resp.content),'url':url,'http_last_modified':q['last_modified']};artifacts.append(item)
   if suffix=='.pom':
    ns={'m':'http://maven.apache.org/POM/4.0.0'};tree=ET.fromstring(resp.content)
    rec['licenses']=[{'name':x.findtext('m:name',namespaces=ns),'url':x.findtext('m:url',namespaces=ns)} for x in tree.findall('.//m:license',ns)]
    rec['dependencies']=[{'group':x.findtext('m:groupId',namespaces=ns),'artifact':x.findtext('m:artifactId',namespaces=ns),'version':x.findtext('m:version',namespaces=ns)} for x in tree.findall('.//m:dependencies/m:dependency',ns)]
   elif suffix=='.aar':
    with zipfile.ZipFile(p) as z:
     (dest/'archive-index.json').write_text(json.dumps(z.namelist(),indent=2),encoding='utf-8')
     for n in ['classes.jar','AndroidManifest.xml','R.txt','proguard.txt']:
      if n in z.namelist():(dest/n).write_bytes(z.read(n))
  rec['artifacts']=artifacts;rec['status']='acquired' if any(x['path'].endswith('.aar') or (x['path'].endswith('.jar') and not x['path'].endswith('-sources.jar')) for x in artifacts) else 'no-binary'
  rec['match_note']='Version match requires embedded bytecode comparison; adapter version is not core version. Latest resolved when requested_version=null.'
  (dest/'provenance.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
 except Exception as e:
  rec['status']='error';rec['error']=str(e)
  if v:
   dest=root/v;dest.mkdir(exist_ok=True)
   (dest/'provenance.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
 print(vendor,sdk,v,rec['status'],flush=True)
 return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(acquire,SPECS))
 (R/'COLLECTION_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
