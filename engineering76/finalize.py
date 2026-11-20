from pathlib import Path
import datetime,hashlib,json

R=Path(__file__).resolve().parent.parent;D=R/'engineering76';O=D/'results/acceptance-v3'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
summary=read(O/'SUMMARY.json');assert summary['status']=='PASS'
for rel,digest in read(O/'CODE_AT_RUN.json').items():assert sha(D/rel)==digest,'Code changed since final acceptance: '+rel
manifest=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
save(O/'MANIFEST.json',manifest)
save(D/'VALIDATION.json',dict(status='PENDING_FINAL_INTEGRITY_VERIFICATION'))
g=read(D/'EVIDENCE_GRAPH.before.json')
specs=[
 ('EN76S01',D/'mock76/app_source.py','Independent offline source App process,strict mock-event schema'),
 ('EN76S02',D/'mock76/app_target.py','Independent offline target App with fixed context and explicit leak bridge'),
 ('EN76S03',D/'mock76/service.py','Local D0/D1/LEAK event/time/purpose/epoch and read-decision chain;not production'),
 ('EN76S04',D/'mock76/auditor.py','Evidence-only local auditor;no service or hidden-route truth dependency'),
 ('EN76S05',D/'mock76/safety.py','Python-level socket/child guard;not OS sandbox assurance'),
 ('EN76S06',D/'acceptance/CASES.json','56 original round75 rows mapped to positive/bounded/unknown/STOP engineering fixtures'),
 ('EN76S07',O/'MATRIX_RESULTS.csv','56/56 matrix acceptance;21 unknown,14 local-chain,7 audience,7 status,7 STOP'),
 ('EN76S08',O/'REGRESSION_RESULTS.json','13 finite engineering regressions;no new Monte Carlo experiment'),
 ('EN76S09',O/'UNITTEST.json','40 successful standard-library engine/auditor unit tests'),
 ('EN76S10',O/'SUMMARY.json','Final v3 runtime/seed/scope summary;not vendor performance'),
 ('EN76S11',O/'MANIFEST.json','All final acceptance IPC/transcript/ledger/state/case/log hashes'),
 ('EN76S12',D/'TEST_REPORT.md','Engineering evidence report and non-production/identifiability boundaries')]
sources=[]
for sid,p,claim in specs:
 sources.append(dict(id=sid,path=p.relative_to(R).as_posix(),sha256=sha(p),source_date=now,claim=claim,
  evidence_kind='executed offline mock engineering verification',evidence_stages=[],
  mock_execution_proven=True,production_match_proven=False,prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
  permission_conditions='Self-contained local mock;no authority for actual advertising or identity services'))
labels={
 'source':'Source App S independent Python CLI process;generated events only',
 'target':'Target App T independent Python CLI process;fixed context or explicit bridge',
 'gates':'Local receipt/available_at/purpose/epoch checks;no real identifiers',
 'D0':'Executed local D0:no individual source lookup in this run;H0/H3 unresolved',
 'D1':'Executed local D1:same-device source history read',
 'leak':'Executed local explicit source-to-current-context leakage',
 'ledger':'Time-ordered source/read/feature/decision hash chain;trusted fixture producer',
 'auditor':'Separate evidence-only auditor;no private route state input',
 'unknown':'External responses or incomplete evidence remain non-identifiable',
 'acceptance':'56 matrix rows +13 process regressions +40 unit tests passed',
 'platform':'Axon/Vector real graph,model use and independent value gain still UNKNOWN'}
nodes=[dict(id='EN76N_'+k,label=v,stage='offline_engineering_mock_only',contains_real_personal_data=False) for k,v in labels.items()]
edges=[]
def edge(a,b,claim,ids,status='mock_executed'):
 edges.append(dict(id=f'EN76E{len(edges)+1:02}',source='EN76N_'+a,target='EN76N_'+b,claim=claim,source_ids=ids,status=status,
  evidence_level='Executed local mock or explicit unknown;not platform E5/E6',evidence_stages=[],reviewed_utc=now,
  mock_execution_proven=status=='mock_executed',production_match_proven=False,prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
  six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,production_successful_send=False,server_received=False,server_model_training=False),
  permission_conditions='Offline fixtures only;no platform deployment or access authorization',
  missing_evidence='Product-specific authorized receipt,entity/feature lineage and real independent mature-value evaluation'))
edge('source','gates','Separate source process emits strict local event,receipt/dedupe/time and consent checked',['EN76S01','EN76S03'])
edge('target','gates','Target process supplies local request;bridge requires current fixture scope/time',['EN76S02','EN76S03'])
edge('gates','D0','Executed contextual baseline with no source lookup;not training-origin identification',['EN76S03','EN76S08'])
edge('gates','D1','Future/denied/reset history cannot enter valid same-device lookup;valid history consumed',['EN76S03','EN76S09'])
edge('gates','leak','Explicit authorized mock bridge introduces current-context source data;not hidden identity proof',['EN76S02','EN76S03','EN76S09'])
for k in ['D0','D1','leak']:edge(k,'ledger','Local instrumented run preserves request,actual read and decision provenance',['EN76S03','EN76S11'])
edge('ledger','auditor','Auditor checks public packet only;temporal/gating/scope contradictions rejected',['EN76S04','EN76S08','EN76S09'])
edge('auditor','unknown','Identical D1/LEAK response remains unidentifiable when provenance unavailable',['EN76S04','EN76S08'])
edge('auditor','acceptance','56 row-specific primary expectations plus weakened/derived evidence regressions executed',['BB75S02','EN76S06','EN76S07','EN76S08','EN76S09'])
edge('acceptance','platform','Local engineering PASS cannot establish actual vendor identity matching,use or value advantage',['EN76S10','EN76S12','IV74S09','IG72S05'],status='unknown')
for k,added in [('nodes',nodes),('edges',edges),('sources',sources)]:
 assert not {x['id'] for x in g[k]}&{x['id'] for x in added};g[k]+=added
g['identity_chain_engineering_round76']=dict(reviewed_utc=now,new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in sources],
 baseline=dict(nodes=277,edges=333,sources=623),apps='Two Python CLI mock processes,not mobile APKs',
 actual_platform_experiment=False,real_identity_query=False,new_statistical_simulation=False,
 final_acceptance='engineering76/results/acceptance-v3',matrix_cases_passed=56,process_regressions_passed=13,unit_tests_passed=40,
 C_graph='UNKNOWN',D_real_value_gain='UNKNOWN',validation_path='engineering76/VALIDATION.json')
ni={x['id'] for x in g['nodes']};si={x['id'] for x in g['sources']}
assert all(x['source'] in ni and x['target'] in ni and set(x['source_ids'])<=si for x in edges)
save(R/'prediction-system/EVIDENCE_GRAPH.json',g)
report=next(R.glob('76_*.md'))
section=['','','## 76号：身份图谱证据链工程验证（2026-11-20）','',
 f'交付：[{report.name}]({report.name})；[可运行代码/README](engineering76/README.md)；[测试报告](engineering76/TEST_REPORT.md)；[最终v3摘要](engineering76/results/acceptance-v3/SUMMARY.json)；[矩阵逐行结果](engineering76/results/acceptance-v3/MATRIX_RESULTS.csv)；[完整性验证](engineering76/VALIDATION.json)。','',
 '双App为独立Python CLI进程，以本地文件IPC实现D0/D1/上下文泄漏三路由。独立审计不读隐藏route真值，时间/用途/epoch门控和不可识别判定已落地。56行矩阵、13进程回归、40单元通过；不把本地fixture升级为真实平台匹配/入模/价值收益。','',
 '无外部请求、真实身份查询、生产SDK、文献搜索、SDK扫描或新增统计模拟；00—75共142份编号文件保留。旧结果保留但正式验证只引用当前代码对应acceptance-v3。', '',
 f'主图仅追加{len(nodes)}节点/{len(edges)}边/{len(sources)}来源，原277/333/623数组和元数据保持原样。','']
(R/'EVIDENCE_INDEX.md').write_bytes((D/'EVIDENCE_INDEX.before.md').read_bytes()+'\n'.join(section).encode('utf-8'))
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources']),acceptance=summary['status']),indent=2))
