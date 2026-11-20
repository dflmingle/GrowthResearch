"""Collect every usable adapter version constant found in existing game evidence, then its direct SDK dependencies."""
from collect_sdk import acquire,R
import json,concurrent.futures,re
ROOT=R.parent;M='https://repo.maven.apache.org/maven2';G='https://dl.google.com/dl/android/maven2'
aliases={'amazonadmarketplace':'amazon-tam','fresh':'bigo','bigoads':'bigo','inneractive':'fyber','googleadmanager':'google-ad-manager'}
version_rows=json.loads((ROOT/'SDK_VERSION_EVIDENCE.json').read_text(encoding='utf-8'))
specs={};origins={}
for x in version_rows:
 if '/applovin/mediation/adapters/' not in x['class'] or 'BuildConfig;' not in x['class'] or x['field'] not in ['VERSION_NAME','ADAPTER_VERSION']:continue
 network=x['class'].split('/')[-2];artifact=aliases.get(network,network)+'-adapter';version=str(x['value']);key=(artifact,version)
 specs[key]=('AppLovin','Adapter-'+artifact,'com.applovin.mediation',artifact,version,M,'adapter')
 origins.setdefault(artifact+'@'+version,[]).append({k:x[k] for k in ['slug','dex','class','field','value']})
todo=[s for s in specs.values() if not (R/s[0]/s[1]/s[4]/'provenance.json').exists()]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(acquire,todo))
(R/'DETECTED_ADAPTER_MANIFEST.json').write_text(json.dumps({'origins':origins,'attempts':out},ensure_ascii=False,indent=2),encoding='utf-8')
deps={}
for p in (R/'AppLovin').glob('Adapter-*/*/provenance.json'):
 a=json.loads(p.read_text(encoding='utf-8'))
 for d in a.get('dependencies',[]):
  group,artifact,v=d['group'],d['artifact'],d['version']
  if not v or not re.fullmatch(r'\d[\w.-]*',v) or group.startswith(('androidx','org.jetbrains','com.applovin')):continue
  repo=G if group.startswith(('com.google.','com.android.')) else M
  if group.startswith('com.mbridge'):repo='https://dl-maven-android.mintegral.com/repository/mbridge_android_sdk_oversea'
  if group.startswith('com.pangle'):repo='https://artifact.bytedance.com/repository/pangle'
  # Different vendor namespaces are explicit rather than falsely called AppLovin core.
  vendor={'com.facebook.android':'Meta','com.unity3d.ads-mediation':'Unity','com.unity3d.ads':'Unity','com.inmobi.monetization':'InMobi','com.vungle':'Liftoff','com.moloco.sdk':'Moloco','com.pangle.global':'Pangle','com.mbridge.msdk.oversea':'Mintegral'}.get(group,group.split('.')[1] if '.' in group else group)
  deps[(group,artifact,v)]=(vendor,'Dependency-'+artifact,group,artifact,v,repo,'core-dependency')
existing=set()
for p in R.glob('*/*/*/provenance.json'):
 a=json.loads(p.read_text(encoding='utf-8'))
 if any(z['path'].endswith('.aar') for z in a.get('artifacts',[])):existing.add((a['group'],a['artifact'],a['version']))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(acquire,[s for k,s in deps.items() if k not in existing]))
(R/'DETECTED_DEPENDENCY_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
