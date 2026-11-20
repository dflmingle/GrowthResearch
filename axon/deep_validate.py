from pathlib import Path
import json,re,hashlib,datetime,collections,zipfile,io
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];issues=[];rows=[]
versions={'car-race':'13.6.4','meowdoku':'13.2.0','rotate-rings':'13.6.2','jewel-coloring':'13.6.3'}
for slug,v in versions.items():
 x=json.loads((R/'games'/slug/'calls.json').read_text(encoding='utf-8'));methods=[m for m in x['methods'] if m['class']=='Lcom/applovin/impl/sdk/EventServiceImpl;'];paths=[m['file'] for m in x['methods']]
 for f,n in collections.Counter(paths).items():
  if n>1:issues.append({'game':slug,'error':'method export path collision','file':f})
 s='\n'.join((R/m['file']).read_text(encoding='utf-8') for m in methods);matches={}
 # Androguard prints const-string with quotes, but const-string/jumbo without them.
 # Parse both instruction forms; never change the expected protocol features.
 strings=set()
 for line in s.splitlines():
  m=re.match(r'^\S+:\s+const-string(?:/jumbo)?\s+\S+,\s+(.*)$',line)
  if m:strings.add(m[1].strip().strip('"'))
 expected={'v1/app':v!='13.2.0','dedupe_id':v!='13.2.0','visitInfo':v!='13.2.0','user_data':v=='13.6.4'}
 for t,wanted in expected.items():
  found=t in strings;matches[t]=found
  if found!=wanted:issues.append({'game':slug,'literal':t,'actual':found,'expected':wanted})
 for m in x['methods']:
  p=R/m['file']
  if not p.exists():issues.append({'game':slug,'error':'missing export','file':m['file']})
 rows.append({'game':slug,'version':v,'original_dex_EventService_literals':matches,'eventservice_methods':len(methods)})
# Verify original native inputs against archive again; do not modify either.
native=[];base=Path('C:/Users/89trillion/game/car-race/source')
with zipfile.ZipFile(base/'CarRace-1.348.2.xapk') as outer:
 for n in outer.namelist():
  if not n.endswith('.apk'):continue
  with zipfile.ZipFile(io.BytesIO(outer.read(n))) as z:
   for key in ['lib/armeabi-v7a/libil2cpp.so','assets/bin/Data/Managed/Metadata/global-metadata.dat']:
    if key not in z.namelist():continue
    h=hashlib.sha256(z.read(key)).hexdigest();local=hashlib.sha256((base/'extracted'/key).read_bytes()).hexdigest();native.append({'split':n,'entry':key,'archive_sha256':h,'local_sha256':local,'equal':h==local})
    if h!=local:issues.append({'error':'native original mismatch','entry':key})
val={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protocol_checks':rows,'native_original_integrity':native,'issues':issues,'status':'PASS' if not issues else 'FAIL','scope':'static evidence identity and protocol literal cross-check only; not runtime reachability, successful HTTP delivery, production attribution, or Axon training proof'}
(R/'VALIDATION.json').write_text(json.dumps(val,indent=2),encoding='utf-8');print(json.dumps(val,indent=2));raise SystemExit(bool(issues))
