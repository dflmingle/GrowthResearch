from pathlib import Path
import json,re,subprocess,hashlib,csv,sys,datetime,collections
R=Path(__file__).resolve().parent;ROOT=R.parent;sys.stdout.reconfigure(encoding='utf-8')
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
entries=[]
for p in sorted(R.glob('*/*/*/provenance.json')):
 x=json.loads(p.read_text(encoding='utf-8'));x['provenance']=str(p.relative_to(R)).replace('\\','/');x['files_verified']=all(hashlib.sha256((R/a['path']).read_bytes()).hexdigest()==a['sha256'] for a in x.get('artifacts',[]));entries.append(x)
dump(R/'CATALOG.json',entries)
mapped={'car-race':('13.6.4','5.5.0',None),'meowdoku':('13.2.0',None,'6.14.2'),'rotate-rings':('13.6.2',None,'6.17.5'),'jewel-coloring':('13.6.3','5.7.0',None)}
rows=[];versions=[]
for slug,(al,adj,af) in mapped.items():
 p=R/'Embedded'/slug/'audit.json';x=json.loads(p.read_text(encoding='utf-8'))
 versions.append({'game':slug,'AppLovin':al,'Adjust':adj,'AppsFlyer':af,'evidence':str(p.relative_to(R)).replace('\\','/')})
 paths={'Lcom/applovin/':R/'AppLovin/MAX'/al,'Lcom/adjust/':R/'Adjust/Android'/str(adj),'Lcom/appsflyer/':R/'AppsFlyer/Android'/str(af)}
 byclass=collections.defaultdict(list)
 for m in x['selected_methods']:byclass[m['class']].append(m)
 for cls,methods in byclass.items():
  root=next((d for pre,d in paths.items() if cls.startswith(pre)),None)
  if not root or not (root/'classes.jar').exists():continue
  cn=cls[1:-1].replace('/','.');a=subprocess.run(['javap','-p','-s','-classpath',str(root/'classes.jar'),cn],capture_output=True,encoding='utf-8',errors='replace')
  dest=root/'api-comparison';dest.mkdir(exist_ok=True);f=dest/(cn+'.javap.txt');f.write_text(a.stdout,encoding='utf-8')
  sm={};prev=''
  for line in a.stdout.splitlines():
   if 'descriptor:' in line:
    if '(' in prev:
     name=prev.split('(')[0].strip().split()[-1];name='<init>' if name==cn else name
     sm[(name,line.split('descriptor:')[1].strip())]=prev.strip()
   elif line.strip():prev=line
  for m in methods:
   name=m['method'];desc=m['descriptor'].replace(' ','')
   if name=='<clinit>':continue
   rows.append({'game':slug,'class':cls,'method':name,'descriptor':desc,'official_version':root.name,'official_declaration_present':(name,desc) in sm,'embedded_method':m.get('file'),'official_api':str(f.relative_to(R)).replace('\\','/'),'scope':'declaration/signature only; no claim of bytecode or semantic identity; R8 may remove members'})
dump(R/'VERSION_MATCHES.json',versions);dump(R/'API_COMPARISON.json',rows)
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'distribution_versions':len(entries),'aar_count':sum(a['path'].endswith('.aar') for x in entries for a in x.get('artifacts',[])),'source_jar_count':sum(a['path'].endswith('-sources.jar') for x in entries for a in x.get('artifacts',[])),'raw_artifact_bytes':sum(a['bytes'] for x in entries for a in x.get('artifacts',[])),'all_raw_artifact_hashes_pass':all(x['files_verified'] for x in entries),'selected_method_declarations':len(rows),'selected_declarations_present':sum(x['official_declaration_present'] for x in rows),'scope':'bounded public SDK collection, not every transitive dependency; exact embedded match only for documented core versions; HTTP Last-Modified is repository time, not proven first release date'}
dump(R/'COLLECTION_VALIDATION.json',summary);print(json.dumps(summary,indent=2))
