"""Offline source/citation/incremental-graph verification. No network or SDK execution."""
from pathlib import Path
import json,hashlib,re,datetime
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];checks=[]
def check(name,ok):
 checks.append(dict(check=name,pass_=bool(ok)))
 if not ok:errors.append(name)
before=json.loads((R/'EVIDENCE_GRAPH.before47.json').read_text(encoding='utf-8'))
g=json.loads((ROOT/'prediction-system/EVIDENCE_GRAPH.json').read_text(encoding='utf-8'))
for k in ['nodes','edges','sources']:check('all original graph '+k+' preserved',g[k][:len(before[k])]==before[k])
check('fixed final graph equals current graph',sha(R/'EVIDENCE_GRAPH.after52.json')==sha(ROOT/'prediction-system/EVIDENCE_GRAPH.json'))
ss=json.loads((R/'CODE_EVIDENCE.json').read_text(encoding='utf-8'));sourceids={s['id'] for s in g['sources']};nodeids={n['id'] for n in g['nodes']}
count=0
for s in ss:
 p=ROOT/s['path'];check('file hash '+s['id'],p.is_file() and sha(p)==s['sha256'])
 lines=p.read_text(encoding='utf-8').splitlines();expected='\n'.join(f'{i+1}: {lines[i]}' for i in range(s['start_line']-1,s['end_line']))
 check('exact excerpt '+s['id'],expected==s['excerpt']);a=s['official_package'];check('archive hash '+s['id'],sha(ROOT/a['path'])==a['sha256']);count+=1
for e in g['edges'][len(before['edges']):]:
 check('edge references '+e['id'],e['source'] in nodeids and e['target'] in nodeids and all(s in sourceids for s in e['source_ids']))
 check('no production/training promotion '+e['id'],not any(e['six_layers'][k] for k in ['production_successful_send','server_received','server_model_training']) and not e['production_actual_proven'])
 check('original edge targets valid '+e['id'],all(k in {x['id'] for x in before['edges']} for k in e['supplements_original_edges']))

# Check the high-value negative/version evidence, not merely file existence.
P=R/'packages/purchasing';old=(P/'5.4.0/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs').read_text(encoding='utf-8')
new=(P/'5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs').read_text(encoding='utf-8')
check('old writer lacks Firebase session serialization', 'WriteOptionalString(s, 4, e.FirebaseSessionId)' not in old)
check('new writer serializes Firebase session', 'WriteOptionalString(s, 4, e.FirebaseSessionId)' in new)
data=(P/'5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs').read_text(encoding='utf-8')
check('Firebase bridge requires consent and allowlist', 'ConsentState.AdsIntent == ConsentStatus.Granted' in data and 'enabledAttributes.Contains(ConnectionsSettingsClient.AppInstanceIdKey)' in data)
olddata=(P/'5.4.0/extracted/package/Runtime/Stores/Data/PlayerData.cs').read_text(encoding='utf-8')
check('old Firebase read commented, not active', '//appInstanceId = m_CachedAppInstanceId' in olddata)
cfg=(P/'5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs').read_text(encoding='utf-8')
check('remote allowlist defaults empty and only true', 'return s_Cached ?? k_Empty;' in cfg and 'entry.Value is bool collect && collect' in cfg)
check('release note confirms Firebase session serialization fix','left out of the event sent to Unity' in (P/'5.5.1/extracted/package/CHANGELOG.md').read_text(encoding='utf-8'))
dispatcher=(R/'packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/Dispatcher.cs').read_text(encoding='utf-8')
check('4xx cache clearing not mislabeled delivery','if (success || badRequest)' in dispatcher and 'else if (intermittentError)' in dispatcher)
matrix=json.loads((R/'SDK_MATRIX.json').read_text(encoding='utf-8'));artcount=0
for m in matrix:
 for a in m['artifacts']:
  check('matrix artifact '+a['path'],sha(ROOT/a['path'])==a['sha256']);artcount+=1

# Preserve prior evidence-manifest graph proof under its original byte-exact snapshot.
mf=ROOT/'EVIDENCE_MANIFEST.json';m=json.loads(mf.read_text(encoding='utf-8'))
for group in m['entries']:
 if group.get('id','').startswith('CS'):continue
 for s in group.get('sources',[]):
  if s.get('path')=='prediction-system/EVIDENCE_GRAPH.json':
   check('prior graph manifest preserved',s.get('sha256')==sha(R/'EVIDENCE_GRAPH.before47.json'))
   s['superseded_logical_path']='prediction-system/EVIDENCE_GRAPH.json';s['path']='cross-sdk/EVIDENCE_GRAPH.before47.json'
reports=[next(ROOT.glob(f'{n}_*.md')) for n in range(47,53)]
def file(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
files=[p for p in sorted(R.rglob('*')) if p.is_file() and p.suffix not in ['.pyc'] and '__pycache__' not in p.parts and p.name not in ['VALIDATION.json']]
groups=[dict(id='CS01',title='跨SDK关键调用、源码与原包',claim='明确赋值、条件和请求代码；未证明生产送达/训练',utc=now,sources=[file(p) for p in files]),
 dict(id='CS02',title='47—52报告与增量关系图',claim='原图逐对象保留；六层证据不跳级',utc=now,sources=[file(p) for p in reports]+[file(ROOT/'prediction-system/EVIDENCE_GRAPH.json')])]
m['entries']=[e for e in m['entries'] if not e.get('id','').startswith('CS')]+groups;m['cross_sdk_audit_utc']=now
mf.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

index=ROOT/'EVIDENCE_INDEX.md';t=index.read_text(encoding='utf-8');marker='<!-- CROSS_SDK_47_52 -->'
t=t.split(marker)[0].rstrip()
t=t.replace('[prediction-system/EVIDENCE_GRAPH.json](prediction-system/EVIDENCE_GRAPH.json)','[00—46阶段证据图快照](cross-sdk/EVIDENCE_GRAPH.before47.json)')
t+='\n\n'+marker+'\n\n<a id="cs01"></a>\n\n## CS01 · 跨SDK源码、原包与调用链\n\n'
t+='本轮44段代码定位；49项选定版本矩阵。所有新SDK仅静态分析，未初始化，未发送生产事件。\n\n'
for path in ['cross-sdk/SDK_MATRIX.json','cross-sdk/CODE_CATALOG.md','cross-sdk/CODE_EVIDENCE.json','cross-sdk/IDENTITY_MAPPINGS.json','cross-sdk/API_DELTAS.json','cross-sdk/ACQUISITION.json','cross-sdk/DECOMPILE.json','cross-sdk/packages/singular/12.17.0/provenance.json']:
 t+=f'- [{path}]({path})\n'
for s in ss:t+=f'- {s["id"]} [{s["class_or_method"]}]({s["path"]}):L{s["start_line"]}；{s["sdk"]} {s["version"]}，原包/文件SHA256见代码目录。\n'
t+='\n<a id="cs02"></a>\n\n## CS02 · 47—52报告与关系图更新\n\n'
for p in reports:t+=f'- [{p.name}]({p.name})\n'
for path in ['prediction-system/EVIDENCE_GRAPH.json','cross-sdk/EVIDENCE_GRAPH.before47.json','cross-sdk/EVIDENCE_GRAPH.after52.json','cross-sdk/VALIDATION.json']:
 t+=f'- [{path}]({path})\n'
t+='\n原图31节点/38边/40来源保存在before47；当前48节点/53边/84来源。旧未知训练边保留，客户端关联不升级为实际训练。完整文件哈希在EVIDENCE_MANIFEST.json的CS01/CS02。\n'
index.write_text(t,encoding='utf-8')

links=0
for p in reports+[R/'CODE_CATALOG.md']:
 text=p.read_text(encoding='utf-8');check('valid UTF8 '+p.name,'\ufffd' not in text)
 for _,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',text):
  if target.startswith(('http:','https:','mailto:')):continue
  fn,_,anchor=target.partition('#');q=p.parent/fn if fn else p;links+=1
  if not q.is_file():errors.append('missing link '+p.name+' '+target)
result=dict(status='PASS' if not errors else 'FAIL',utc=now,reports=[file(p) for p in reports],
 checks=len(checks),sdk_versions=len(matrix),archive_records_verified=artcount,exact_excerpts=len(ss),
 graph_before=dict(nodes=len(before['nodes']),edges=len(before['edges']),sources=len(before['sources'])),
 graph_after=dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources'])),
 local_links_checked=links,production_events_sent=False,scope='Static citation/identity assignment/serialization/version/incremental-graph checks; not production SDK or model certification',errors=errors)
(R/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
