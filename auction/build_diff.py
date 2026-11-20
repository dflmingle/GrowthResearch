from pathlib import Path
import json,re
R=Path(__file__).resolve().parent
rows=json.loads((R/'PROTOCOL_FIELDS.json').read_text())
prefix={
 'AppLovin':{'Bid request object':'','App object':'app','Device object':'device','Geo object':'device.geo',
             'Impression object':'imp[]','Metric object':'imp[].metric[]','Video object':'imp[].video','Banner object':'imp[].banner','Native object':'imp[].native',
             'Bid response object':'','Seatbid object':'seatbid[]','Bid object':'seatbid[].bid[]'},
 'Unity':{'request objects':'','app objects':'app','publisher objects':'app.publisher','device objects':'device',
          'imp objects':'imp[]','banner objects':'imp[].banner','video objects':'imp[].video','source objects':'source',
          'schain objects':'source.schain','nodes objects':'source.schain.nodes[]','pmp objects':'pmp','deal objects':'pmp.deals[]',
          'regs object and extensions':'','user object extension':'','response objects':'','seatbid objects':'seatbid[]','bid objects':'seatbid[].bid[]','bid.ext objects':'seatbid[].bid[].ext'}
}
mapped=[]
for x in rows:
 if x['kind'] not in ['request','response','privacy']:continue
 if x['section'] not in prefix[x['vendor']]:continue
 f=re.sub(r'\s*\([^)]*\)$','',x['field'])
 # SKAN nested abbreviated path normalization is explicit, not silently guessed.
 if f.startswith('….fidelities'):f='ext.skadn'+f[1:]
 if f.startswith('….skoverlay'):f='ext.skadn'+f[1:]
 if x['vendor']=='Unity' and x['section']=='bid.ext objects' and f.startswith('ext.'):f=f[4:]
 p=prefix[x['vendor']][x['section']]
 # Unity's source table repeats absolute paths for some extension fields.
 path=f if p=='source' and f.startswith('source.') else (p+'.'+f if p else f)
 mapped.append({**x,'canonical_path':path,'direction':'request' if x['kind']=='privacy' else x['kind']})
out=[]
for direction in ['request','response']:
 for path in sorted(set(x['canonical_path'] for x in mapped if x['direction']==direction)):
  al=[x for x in mapped if x['direction']==direction and x['canonical_path']==path and x['vendor']=='AppLovin']
  un=[x for x in mapped if x['direction']==direction and x['canonical_path']==path and x['vendor']=='Unity']
  out.append(dict(direction=direction,path=path,status='both_documented' if al and un else ('only_AppLovin_documented' if al else 'only_Unity_documented'),AppLovin=al,Unity=un))
(R/'FIELD_DIFF.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
md='# 规范化字段全量差分\n\n只表示本轮取得文档是否列出，不代表平台独有或生产启用。字段同名不代表条件、类型和语义相同；原始描述、章节及哈希在PROTOCOL_FIELDS.json。Unity pmp/source.schain严格保留取得文档的路径，不静默改成通用标准位置。SKAN专页、loss及宏表另见原始目录。\n'
for direction in ['request','response']:
 md+=f'\n## {direction}\n\n| 路径 | 文档覆盖 | AppLovin原始章节 | Unity原始章节 |\n|---|---|---|---|\n'
 for x in out:
  if x['direction']!=direction:continue
  md+=f'| `{x["path"]}` | {x["status"]} | {", ".join(t["section"] for t in x["AppLovin"])} | {", ".join(t["section"] for t in x["Unity"])} |\n'
(R/'FIELD_DIFF.md').write_text(md,encoding='utf-8')
print('normalized entries',len(out),'both',sum(x['status']=='both_documented' for x in out))

# Parse complete JSON examples only; malformed documentation examples remain errors, not repaired captures.
examples=[]
for p in [R.parent/'identity-graph/unity-exchange-identity.raw',R/'unity-response.raw']:
 for i,m in enumerate(re.finditer(r'```json[^\n]*\n(.*?)\n```',p.read_text(),re.S)):
  try:obj=json.loads(m[1])
  except json.JSONDecodeError as e:
   examples.append(dict(source=p.relative_to(R.parent).as_posix(),example=i,status='invalid_document_example',error=str(e)));continue
  paths=[]
  def walk(o,path=''):
   if isinstance(o,dict):
    for k,v in o.items():walk(v,path+'.'+k if path else k)
   elif isinstance(o,list):
    for v in o:walk(v,path+'[]')
   else:paths.append(path)
  walk(obj)
  examples.append(dict(source=p.relative_to(R.parent).as_posix(),example=i,status='parsed_document_example',paths=sorted(set(paths))))
(R/'DOCUMENT_EXAMPLES.json').write_text(json.dumps(examples,indent=2),encoding='utf-8')
print('JSON examples',len(examples),'parsed',sum(x['status']=='parsed_document_example' for x in examples))
