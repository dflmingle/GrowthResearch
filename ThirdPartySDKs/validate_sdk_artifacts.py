from pathlib import Path
import json,zipfile,hashlib,datetime,collections
R=Path(__file__).resolve().parent;issues=[];aars=0;methods=0
def h(b):return hashlib.sha256(b).hexdigest()
for p in R.glob('*/*/*/provenance.json'):
 x=json.loads(p.read_text(encoding='utf-8'))
 for a in x.get('artifacts',[]):
  q=R/a['path']
  if h(q.read_bytes())!=a['sha256']:issues.append({'path':a['path'],'error':'raw hash mismatch'})
  if not q.name.endswith('.aar'):continue
  aars+=1
  with zipfile.ZipFile(q) as z:
   if z.testzip():issues.append({'path':a['path'],'error':'ZIP CRC'})
   cp=q.parent/'classes.jar'
   if 'classes.jar' in z.namelist() and (not cp.exists() or h(z.read('classes.jar'))!=h(cp.read_bytes())):issues.append({'path':a['path'],'error':'extracted classes.jar mismatch'})
for p in R.glob('Embedded/*/audit.json'):
 x=json.loads(p.read_text(encoding='utf-8'));files=[]
 for m in x['selected_methods']:
  if 'file' not in m:continue
  files.append(m['file']);methods+=1
  if not (R/m['file']).exists():issues.append({'path':m['file'],'error':'missing selected method'})
 for f,n in collections.Counter(files).items():
  if n>1:issues.append({'path':f,'error':'method overload path collision'})
traces=json.loads((R/'BUSINESS_TRACES.json').read_text(encoding='utf-8'))
for f,n in collections.Counter(x['file'] for x in traces).items():
 if n>1:issues.append({'path':f,'error':'business trace path collision'})
v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'aars_crc_and_extracted_jar_checked':aars,'selected_method_files_checked':methods,'business_trace_files':len(traces),'issues':issues,'status':'PASS' if not issues else 'FAIL','scope':'offline artifact identity and export integrity; no production delivery, game SDK full semantic equivalence, or ad performance claim'}
(R/'ARTIFACT_VALIDATION.json').write_text(json.dumps(v,indent=2),encoding='utf-8');print(json.dumps(v,indent=2));raise SystemExit(bool(issues))
