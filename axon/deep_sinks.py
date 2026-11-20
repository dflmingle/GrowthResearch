from pathlib import Path
import sys,json,re,hashlib,gc
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ThirdPartySDKs'))
from embedded_scan import dexes,redact
from androguard.core.dex import DEX
R=Path(__file__).resolve().parent/'deep';sys.stdout.reconfigure(encoding='utf-8')
configs={'car-race':('13.6.4','t7','c5','e5'),'meowdoku':('13.2.0','y6','l4','n4'),'rotate-rings':('13.6.2','p7','z4','b5'),'jewel-coloring':('13.6.3','s7','c5','e5')}
for slug,(v,mgr,conf,pref) in configs.items():
 wanted={f'Lcom/applovin/impl/{x};' for x in [mgr,conf,pref]}
 wanted.update({'Lcom/applovin/impl/sdk/'+x+';' for x in ['j','k'] if v=='13.2.0'} or {'Lcom/applovin/impl/sdk/m;'})
 wanted.update('Lcom/applovin/impl/sdk/network/'+x+';' for x in ['b','c','d','PostbackServiceImpl'])
 rows=[]
 for apk,dn,data in dexes(slug):
  # Skip parsing DEX that has none of the target definitions based on existing class origins when known.
  existing=json.loads((R/'games'/slug/'calls.json').read_text(encoding='utf-8'))
  # Keep complete scan of matching namespace files, not class-string exclusions for small obfuscated names.
  if b'com/applovin' not in data:continue
  d=DEX(data)
  for c in d.get_classes():
   if c.get_name() not in wanted:continue
   for m in c.get_methods():
    if not m.get_code():continue
    body=[];off=0
    for ins in m.get_code().get_bc().get_instructions():
     body.append(f'{off:04x}: '+redact(ins.get_name()+' '+ins.get_output()));off+=ins.get_length()
    label=re.sub(r'[^\w.-]','_',c.get_name()+'__'+m.get_name())[:125]+'-'+hashlib.sha256(m.get_descriptor().encode()).hexdigest()[:10]
    p=R/'games'/slug/'sinks'/dn/(label+'.txt');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(body),encoding='utf-8')
    rows.append({'dex':dn,'class':c.get_name(),'method':m.get_name(),'descriptor':m.get_descriptor(),'file':str(p.relative_to(R)).replace('\\','/')})
  del d;gc.collect()
 (R/'games'/slug/'sinks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(slug,len(rows),flush=True)
