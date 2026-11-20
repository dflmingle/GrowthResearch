"""Register new evidence without rewriting prior studies; offline integrity checks."""
from pathlib import Path
import json,hashlib,datetime,re,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'prediction-system'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
g=json.loads((R/'EVIDENCE_GRAPH.json').read_text(encoding='utf-8'))
errors=[]

# Explicitly distinguish failed discovery, indirect clues and primary-use documents.
fetches=[x for p in R.glob('fetches-*.json') for x in json.loads(p.read_text(encoding='utf-8'))]
for x in fetches:
 id=x['id']
 if id.startswith('search-'):reason='HTTP200 but only redirect/help page; not a useful search result'
 elif id.startswith('bing-'):reason='RSS content not relevant to query; not used as research evidence'
 elif id.startswith('patents-'):reason='Discovery only; verify selected patent original; Unity results contain unrelated rendering/animation'
 elif x.get('status')!=200:reason='HTTP failure; retained as access/gap evidence only'
 elif 'job' in id:reason='Public job record; indirect, never production-model proof'
 else:reason='Public page inspected; exact claims use registered excerpts only'
 x['evidence_use']=reason
(R/'SEARCH_LEDGER.json').write_text(json.dumps(fetches,ensure_ascii=False,indent=2),encoding='utf-8')

# Validate graph references and original excerpt content.
nodes={n['id'] for n in g['nodes']};sources={s['id']:s for s in g['sources']}
for s in g['sources']:
 p=ROOT/s['path']
 if not p.is_file():errors.append('missing source '+s['path']);continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:errors.append('source hash '+s['id'])
 lines=p.read_text(encoding='utf-8').splitlines()
 expected='\n'.join(f'{i+1}: {lines[i]}' for i in range(s['start_line']-1,s['end_line']))
 if s['excerpt']!=expected:errors.append('excerpt content '+s['id'])
for e in g['edges']:
 if e['source'] not in nodes or e['target'] not in nodes:errors.append('invalid endpoint '+e['id'])
 if not e['source_ids'] or any(x not in sources for x in e['source_ids']):errors.append('missing edge source '+e['id'])
 if e['production_actual_proven']:errors.append('unsupported observed production '+e['id'])
 if e['observed_target_game_delivery']:errors.append('unsupported game delivery '+e['id'])
 if not e['permission_conditions'] or not e['missing_evidence']:errors.append('missing conditions/gap '+e['id'])
 if e['status'] in ['unknown','inference','indirect'] and e['diagram_style']!='dashed':errors.append('promoted uncertain edge '+e['id'])
 if e['status']=='excluded' and e['diagram_style']!='barred':errors.append('excluded edge not barred')

# Existing synthetic experiment is auxiliary. No retraining or new vendor comparisons.
res=json.loads((ROOT/'ltv/model/output/results.json').read_text())
assert res['synthetic_only'] and res['not_vendor_comparison']
assert len(res['rows'])==81
for shape in res['shapes']:
 for seed in res['seeds']:
  rs=[x for x in res['rows'] if x['shape']==shape and x['seed']==seed]
  if len(set(x['inventory_digest'] for x in rs))!=1:errors.append('noncommon inventory')
  for x in rs:
   if not 0<=x['spend_usd']<=x['budget_usd']+1e-6:errors.append('budget error')
   if abs(x['realized_D28_ROAS']-x['realized_D28_revenue_usd']/x['spend_usd'])>1e-8:errors.append('ROAS arithmetic')

# Register primary snapshots, raw job JSON and scripts/reports with provenance.
mf=ROOT/'EVIDENCE_MANIFEST.json';m=json.loads(mf.read_text(encoding='utf-8'))
seen={}
for e in m['entries']:
 if e.get('id','').startswith('PS'):continue
 for s in e.get('sources',[]):
  if s.get('path') and s.get('sha256'):seen.setdefault(s['path'],s['sha256'])
for s in g['sources']:
 if s['path'] in seen and seen[s['path']]!=s['sha256']:errors.append('prior original changed '+s['path'])

reports=[next(ROOT.glob(str(n)+'_*.md')) for n in range(41,47)]
def file_source(p):
 return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
groups=[]
groups.append(dict(id='PS01',title='模型来源逐条摘录与公开技术线索',claim='A官方用途 B接口 D招聘/专利；不混为生产证明',utc=now,
 sources=[{**file_source(ROOT/s['path']),**{k:v for k,v in s.items() if k not in ['excerpt','text']}} for s in g['sources']]))
groups.append(dict(id='PS02',title='证据关系图及新一轮公开获取原始材料',claim='31节点38边；未知连接保持虚线；搜索失败保留',utc=now,
 sources=[file_source(p) for p in sorted(R.iterdir()) if p.is_file() and p.name!='VALIDATION.json']))
groups.append(dict(id='PS03',title='41—46核心系统研究报告',claim='官方数据用途和接口证据拼图，不宣称恢复闭源模型',utc=now,sources=[file_source(p) for p in reports]))
aux=[ROOT/'ltv/model/experiment.py',ROOT/'ltv/model/summarize.py',ROOT/'ltv/model/test_experiment.py']
aux += [p for p in (ROOT/'ltv/model/output').iterdir() if p.is_file()]
groups.append(dict(id='PS04',title='辅助合成特征消融实验',claim='81组人为数据；不构成Axon/Vector效果或身份图谱证明',utc=now,sources=[file_source(p) for p in aux]))
m['entries']=[e for e in m['entries'] if not e.get('id','').startswith('PS')]+groups
m['prediction_system_audit_utc']=now
mf.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

idx=ROOT/'EVIDENCE_INDEX.md';txt=idx.read_text(encoding='utf-8');marker='<!-- PREDICTION_SYSTEM_2026_11_19 -->'
txt=txt.split(marker)[0].rstrip()+'\n\n'+marker+'\n'
for group in groups:
 txt+=f'\n<a id="{group["id"].lower()}"></a>\n\n## {group["id"]} · {group["title"]}\n\n{group["claim"]}。\n\n'
 if group['id']=='PS01':
  txt+='完整来源、产品、日期、URL、行号及SHA256见[SOURCE_CATALOG](prediction-system/SOURCE_CATALOG.md)和[SOURCE_EXCERPTS](prediction-system/SOURCE_EXCERPTS.json)。\n\n'
  for s in g['sources']:
   txt+=f'- {s["id"]} [{s["path"]}]({s["path"]}):L{s["start_line"]}；级别{s["evidence_priority"]}'
   if s.get('url'):txt+=f'；[原始URL]({s["url"]})'
   txt+='\n'
 else:
  important={'EVIDENCE_GRAPH.json','SEARCH_LEDGER.json','REPORT_REUSE_INDEX.json','SOURCE_CATALOG.md','build_system.py','finalize.py','results.json','summary.json','SUMMARY.md','experiment.py','recall_ablation.png','roas_ablation.png'}
  for s in group['sources']:
   if group['id']=='PS03' or Path(s['path']).name in important:txt+=f'- [{s["path"]}]({s["path"]})\n'
 txt+='\n原文件哈希及获取时间见EVIDENCE_MANIFEST.json；实际生产运行、服务器训练与目标游戏启用没有独立日志证明。\n'
idx.write_text(txt,encoding='utf-8')

links=0
for p in reports+[R/'SOURCE_CATALOG.md']:
 text=p.read_text(encoding='utf-8')
 if '\ufffd' in text:errors.append('encoding replacement '+p.name)
 for _,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',text):
  if target.startswith(('http:','https:','mailto:')):continue
  fn,_,anchor=target.partition('#');q=p.parent/fn if fn else p;links+=1
  if not q.is_file():errors.append('missing report link '+p.name+' '+target)
for group in groups:
 for s in group['sources']:
  if hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()!=s['sha256']:errors.append('registered hash '+s['path'])
validation=dict(status='PASS' if not errors else 'FAIL',utc=now,reports=[file_source(p) for p in reports],
 nodes=len(g['nodes']),edges=len(g['edges']),original_excerpts=len(g['sources']),local_links_checked=links,
 source_hashes_checked=sum(len(x['sources']) for x in groups),synthetic_arms=81,
 production_observation=False,scope='Offline source/graph/citation integrity; not model truth or production compliance certification',errors=errors)
(R/'VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
