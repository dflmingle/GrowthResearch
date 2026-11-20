from pathlib import Path
import json,re,csv,collections,zipfile,hashlib,sys
from loguru import logger
from androguard.core.dex import DEX
logger.remove();R=Path(__file__).resolve().parent;J=R/'jewel-coloring/deep';sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
c=load(J/'resources/ad_worth_event.json.redacted.json');models=c['extras']['condition_config']['weightWorth'];events=c['events'];rows=[];used=set();platforms=collections.Counter()
for k,e in events.items():
 def weights(o):
  if isinstance(o,dict):
   if 'weightWorth' in o:used.update(o['weightWorth'].get('type',{}))
   for x in o.values():weights(x)
  elif isinstance(o,list):
   for x in o:weights(x)
 weights(e);platforms.update(e.get('sendPlatform',{}).keys())
 rows.append({'event_id':k,'event_name':e.get('eventName',''),'init':e.get('init',{}),'conditions':e.get('conditions',{}),'platforms':e.get('sendPlatform',{}),'status':'packaged definition, not observed runtime firing'})
save(J/'rule-catalog.json',rows)
with (J/'rule-catalog.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,dict) else v for k,v in x.items()} for x in rows)
symbols=load(J/'symbol-index.json');awe=[x for x in symbols if re.search(r'ad::event::|AdWorth',x['name'])];unique={x['rva']:x for x in awe}
with (J/'adworth-method-inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['rva','size','name','mangled']);w.writeheader();w.writerows(sorted(unique.values(),key=lambda x:int(x['rva'],16)))
conditions=sorted({re.match(r'ad::event::(\w+)::',x['name'])[1] for x in awe if re.match(r'ad::event::(AWE\w+)::',x['name'])})
summary={'sample':'1.24.1 code24','config_version_fields':{k:c[k] for k in ['version','version_name','project_template_version']},'events':len(events),'weight_tables':len(models),'referenced_weight_tables':sorted(used),'unreferenced_weight_tables':sorted(set(models)-used),'platform_definition_counts':dict(platforms),'default_has_source_weight_reference':any('subChannel' in json.dumps(e) for e in events.values()),'default_has_country_condition':any(re.search(r'"(?:country|costRecovery|userGroup|channelName|subChannelName)"',json.dumps(e)) for e in events.values()),'native_adworth_unique_functions':len(unique),'native_condition_and_send_classes':conditions,'source_weight_table':models['subChannelWeight1_fb_purchase'],'guard':'All are original package defaults; production hot updates and initialized-condition subset unknown'}
save(J/'rule-analysis.json',summary)
# Export narrow raw DEX methods to corroborate Java decompilation including unusual permission branch.
exports={'jewel-coloring':('classes6.dex',{'Lcommon/platform;':['getLocalSharedDeviceId','_getLocalSharedDeviceIdSaveID','EventUserAdWorthEventAllIn1','sendAdjustAdRevenue']}),'meowdoku':('classes4.dex',{'Lcom/learnings/analyze/UUIDManager;':['getUUID'],'Lcom/learnings/analyze/LearningsIdManager;':['getLearningsIdInfo'],'Lcom/learnings/auth/LxAuth;':['syncAccountId']})}
for slug,(dex,targets) in exports.items():
 base=R/slug/'static/splits';apk=next(p for p in base.glob('*.apk') if dex in zipfile.ZipFile(p).namelist());d=DEX(zipfile.ZipFile(apk).read(dex));out=R/'identity-deep/raw-methods'/slug;out.mkdir(parents=True,exist_ok=True)
 for c1 in d.get_classes():
  if c1.get_name() not in targets:continue
  for m in c1.get_methods():
   if m.get_name() not in targets[c1.get_name()] or not m.get_code():continue
   lines=[f'// {apk.name} {dex} class={c1.get_name()} method={m.get_name()} {m.get_descriptor()}'];off=0
   for ins in m.get_code().get_bc().get_instructions():
    t=ins.get_name()+' '+ins.get_output()
    if re.search('(?i)secret|devkey|sdkkey|access_token',t):t='[credential-related instruction omitted]'
    lines.append(f'{off:04x}: {t}');off+=ins.get_length()
   (out/(re.sub('[^A-Za-z0-9_.-]','_',c1.get_name()+'__'+m.get_name())+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
print('defaults',summary['events'],'weight tables',len(models),'unused',len(set(models)-used),'native unique',len(unique),flush=True)
