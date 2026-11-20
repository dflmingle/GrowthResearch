from pathlib import Path
import json,re,hashlib,collections,datetime,zipfile,sys
from loguru import logger
from androguard.core.dex import DEX
logger.remove()
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def hfile(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
catalog=[]
for slug in ['car-race','meowdoku','rotate-rings','amaze-go','jewel-coloring','rotate-rings-1.2.2']:
 p=R/slug/'static/sample-identity.json'
 if p.exists():
  a=read(p);row={k:a.get(k) for k in ['package','versionName','versionCode','sha256','bytes','certificate_sha256','abis','unity_versions','engine','audited_utc']}
  row['sample_path']=a['sample'];row['original_release_date']='not established; catalog/page timestamps are not release dates';row['slug']=slug
  row['properties']={k:v.splitlines()[0] for s in a.get('splits',[]) for k,v in s.get('sdk_properties',{}).items() if re.search(r'^(firebase-(analytics|config)|billing|play-services-measurement-api)\.properties$',k)}
  d=read(R/slug/'static/dex-audit.json');c=collections.Counter()
  for x in d['dex_inventory']:c.update(x['families'])
  row['sdk_class_counts']=dict(c);row['dex_count']=len(d['dex_inventory'])
 elif slug=='car-race':
  a=read(R/slug/'reused-evidence/AcquisitionMonetization-20261117/original-identity.json')
  sp=R/slug/'signature.txt';raw=sp.read_bytes();sig=raw.decode('utf-16' if raw[:2]==b'\xff\xfe' else 'utf-8');sp.write_text(sig,encoding='utf-8')
  row={'slug':slug,'package':a['package'],'versionName':a['version'],'versionCode':a['code'],'sha256':a['archive_sha256'],'sample_path':'C:/Users/89trillion/game/car-race/source/CarRace-1.348.2.xapk','certificate_sha256':re.findall(r'^Signer #1 certificate SHA-256 digest: (\w+)',sig,re.M),'abis':['armeabi-v7a'],'engine':'Unity IL2CPP','unity_versions':['6000.3.21f1'],'original_release_date':'not established'}
 else:row={'slug':slug,'package':'com.oakever.arrows','status':'MISSING_SAMPLE','original_release_date':'unknown'}
 if row.get('sample_path'):
  p=Path(row['sample_path']);row['verified_sha256']=hfile(p);row['hash_matches']=row['sha256']==row['verified_sha256']
 catalog.append(row)
write(R/'SAMPLE_CATALOG.json',catalog)
# Exact package-linked version fields, not arbitrary version-looking strings.
versions=[]
targets=['Lcom/adjust/sdk/','Lcom/appsflyer/','Lcom/tiktok/','Lcom/applovin/','Lio/appmetrica/','Lcom/learnings/']
for slug in ['meowdoku','rotate-rings','jewel-coloring']:
 out=R/slug/'static';apk=next(a for a in (out/'splits').glob('*.apk') if 'classes.dex' in zipfile.ZipFile(a).namelist());z=zipfile.ZipFile(apk)
 for dex in sorted(x for x in z.namelist() if re.fullmatch(r'classes\d*\.dex',x)):
  d=DEX(z.read(dex))
  for c in d.get_classes():
   n=c.get_name()
   if not any(n.startswith(x) for x in targets):continue
   for f in c.get_fields():
    if not re.search(r'version|sdk.*name',f.get_name(),re.I):continue
    v=f.get_init_value()
    if not v:continue
    val=v.get_value()
    if isinstance(val,(str,int)) and len(str(val))<110:
     versions.append({'slug':slug,'dex':dex,'class':n,'field':f.get_name(),'value':val})
 print('versions',slug,len(versions),flush=True)
write(R/'SDK_VERSION_EVIDENCE.json',versions)
# Full packaged game event schemas, separate from proven runtime event delivery.
rows=[]
for x in read(R/'meowdoku/static/business-configs-redacted.json'):
 if x['entry'].endswith('analyze_config.json'):
  for ev in x['data'].get('eventList',[]):rows.append({'game':'meowdoku','evidence':'packaged event schema, not delivery trace','source':x['entry'],**ev})
for x in read(R/'car-race/reused-evidence/monetization-20261117/event-schema-catalog.json'):rows.append({'game':'car-race','evidence':'ARM ToParameters method','source':x['file'],**x})
write(R/'EVENT_SCHEMA_CATALOG.json',rows)
print('DONE sample hashes',all(x.get('hash_matches',True) for x in catalog),'event schemas',len(rows),flush=True)
