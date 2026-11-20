from collect_sdk import R,acquire
from pathlib import Path
import json,re,concurrent.futures,datetime
M='https://repo.maven.apache.org/maven2';G='https://dl.google.com/dl/android/maven2'
existing=set();deps={}
for p in R.glob('*/*/*/provenance.json'):
 x=json.loads(p.read_text(encoding='utf-8'))
 if any(a['path'].endswith('.aar') or (a['path'].endswith('.jar') and not a['path'].endswith('-sources.jar')) for a in x.get('artifacts',[])):existing.add((x['group'],x['artifact'],x['version']))
 if x.get('kind')!='adapter':continue
 for d in x.get('dependencies',[]):
  g,a,v=d['group'],d['artifact'],d['version']
  if not v or not re.fullmatch(r'\d[\w.-]*',v) or g.startswith(('androidx','org.jetbrains','com.applovin')):continue
  repo=G if g.startswith(('com.google.','com.android.')) else M
  if g.startswith('com.mbridge'):repo='https://dl-maven-android.mintegral.com/repository/mbridge_android_sdk_oversea'
  if g.startswith('com.pangle'):repo='https://artifact.bytedance.com/repository/pangle'
  vendor={'com.facebook.android':'Meta','com.unity3d.ads-mediation':'Unity','com.unity3d.ads':'Unity','com.inmobi.monetization':'InMobi','com.vungle':'Liftoff','com.moloco.sdk':'Moloco','com.pangle.global':'Pangle','com.mbridge.msdk.oversea':'Mintegral'}.get(g,g.split('.')[1] if '.' in g else g)
  deps[(g,a,v)]=(vendor,'Dependency-'+a,g,a,v,repo,'core-dependency')
todo=[s for k,s in deps.items() if k not in existing]
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for x in ex.map(acquire,todo):
  rows.append(x);(R/'DETECTED_DEPENDENCY_MANIFEST.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'resume bounded downloads after stalled request; successful earlier artifacts retained in provenance','attempts':rows},indent=2),encoding='utf-8')
print('completed bounded dependency attempts',len(rows),flush=True)
