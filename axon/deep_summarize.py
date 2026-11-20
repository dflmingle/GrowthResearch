from pathlib import Path
import json,re,hashlib,csv,sys,collections
R=Path(__file__).resolve().parent/'deep';ROOT=R.parents[1];sys.stdout.reconfigure(encoding='utf-8')
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
games=[];events=[];ids=[]
for p in sorted((R/'games').glob('*/calls.json')):
 x=json.loads(p.read_text(encoding='utf-8'));count=0
 for m in x['methods']:
  for h in m['hits']:
   if 'event' in h['kinds'] and re.search(r'->(?:trackEvent|trackCheckout|trackInAppPurchase|maybeTrackAppOpenEvent)',h['instruction']):
    cn=m['class'];category='sdk-internal'
    if '/metica/' in cn or '/mediation/unity/' in cn:category='generic-bridge-not-gameplay-trigger'
    if cn.endswith('/EventServiceImpl;'):category='event-service-overload-or-automatic-open'
    events.append({'game':x['slug'],'class':cn,'method':m['method'],'descriptor':m['descriptor'],'dex':m['dex'],'offset':hex(h['offset']),'category':category,'instruction':h['instruction'],'file':m['file']});count+=1
   if 'identity' in h['kinds'] and re.search(r'->(?:setUserIdentifier|setUserData|getUUID)|AppLovinUserData;',h['instruction']):
    ids.append({'game':x['slug'],'class':m['class'],'method':m['method'],'dex':m['dex'],'offset':hex(h['offset']),'instruction':h['instruction'],'file':m['file']})
 games.append({'game':x['slug'],'dexes':len(x['dex_inventory']),'classes':sum(d['class_count'] for d in x['dex_inventory']),'exported_methods':len(x['methods']),'event_invocation_candidates':count,'scope':x['scope']})
write(R/'game-scan-summary.json',games);write(R/'event-callsite-catalog.json',events);write(R/'identity-callsite-catalog.json',ids)
with (R/'event-callsite-catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(events[0]));w.writeheader();w.writerows(events)
versions=[]
for v,config,manager in [('13.2.0','l4','y6'),('13.6.2','z4','p7'),('13.6.3','c5','s7'),('13.6.4','c5','t7')]:
 root=R/'versions'/v;event=root/'java/com/applovin/impl/sdk/EventServiceImpl.java';conf=root/'selected/com/applovin/impl'/(config+'.java');s=event.read_text(encoding='utf-8');c=conf.read_text(encoding='utf-8');defs={}
 for line in c.splitlines():
  m=re.match(r'\s*(\w+) = a\("([^"]+)", (.*)\);',line)
  if m and m[2] in ['axon_events','top_level_events','eete','eetbe','send_user_data','qq3','pui','max_postback_attempts','max_persisted_postbacks','spp','sossp','event_tracking_endpoint_v2','event_tracking_backup_endpoint_v2']:defs[m[2]]={'symbol':m[1],'default_expression':m[3],'line':c[:c.find(line)].count('\n')+1}
 row={'version':v,'manager_class':'com.applovin.impl.'+manager,'structured_axon_branch':'"v1/app"' in s,'optional_user_data':'"user_data"' in s,'dedupe_id':'"dedupe_id"' in s,'visitInfo':'"visitInfo"' in s,'event_service_path':str(event.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(event.read_bytes()).hexdigest(),'config_path':str(conf.relative_to(ROOT)).replace('\\','/'),'config_defaults':defs}
 versions.append(row)
write(R/'protocol-matrix.json',versions)
# Numbered excerpts link implementation and raw code, with file hashes.
excerpts=[]
needles=['trackEvent(', 'maybeTrackAppOpenEvent(', '"cuid"', '"user_data"', '"dedupe_id"', '"visitInfo"', '"axon_events"', '"pui"', '"qq3"', 'persistent_postback_cache.json', 'dispatchPostbackRequest', 'setUserIdentifier(', 'void a(String str)', '"com.applovin.sdk.user_id"', '"adrevenue_sdk"']
for p in (R/'versions').rglob('*.java'):
 if p.name in ['class-index.txt']:continue
 lines=p.read_text(encoding='utf-8').splitlines()
 for n in needles:
  found=[i for i,l in enumerate(lines) if n in l]
  for i in found[:3]:excerpts.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'needle':n,'start_line':max(0,i-3)+1,'end_line':min(len(lines),i+8),'text':'\n'.join(lines[max(0,i-3):i+8])})
write(R/'numbered-excerpts.json',excerpts);print('games',games,'events',len(events),'version matrix',len(versions),'excerpts',len(excerpts))
