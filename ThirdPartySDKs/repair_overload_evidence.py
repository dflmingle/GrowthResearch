"""Export each selected method under a descriptor-qualified name; avoid overloaded-method filename collisions."""
from embedded_scan import R,dexes,redact
from androguard.core.dex import DEX
import json,hashlib,re,gc,sys
sys.stdout.reconfigure(encoding='utf-8')
traces=json.loads((R/'BUSINESS_TRACES.json').read_text(encoding='utf-8'))
for slug in ['car-race','meowdoku','rotate-rings','jewel-coloring']:
 p=R/'Embedded'/slug/'audit.json';audit=json.loads(p.read_text(encoding='utf-8'))
 rows=[(x,False) for x in audit['selected_methods'] if 'file' in x]+[(x,True) for x in traces if x['slug']==slug]
 by={}
 for row,trace in rows:by.setdefault(row['dex'],{}).setdefault((row['class'],row['method'],row['descriptor']),[]).append((row,trace))
 fixed=0
 for apk,dn,data in dexes(slug):
  if dn not in by:continue
  d=DEX(data);wanted=by[dn]
  for c in d.get_classes():
   for m in c.get_methods():
    key=(c.get_name(),m.get_name(),m.get_descriptor())
    if key not in wanted or not m.get_code():continue
    body=[];off=0
    for ins in m.get_code().get_bc().get_instructions():
     body.append(f'{off:04x}: '+redact(ins.get_name()+' '+ins.get_output()));off+=ins.get_length()
    for row,trace in wanted[key]:
     label=re.sub(r'[^\w.-]','_',c.get_name()+'__'+m.get_name())[:125]+'-'+hashlib.sha256(m.get_descriptor().encode()).hexdigest()[:10]+'.txt'
     dest=R/'Embedded'/slug/('business-trace' if trace else 'method-bodies')/dn/label;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(body),encoding='utf-8');row['file']=str(dest.relative_to(R)).replace('\\','/');fixed+=1
  del d;gc.collect()
 p.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8');print(slug,'descriptor-qualified exports',fixed,flush=True)
(R/'BUSINESS_TRACES.json').write_text(json.dumps(traces,ensure_ascii=False,indent=2),encoding='utf-8')
