from pathlib import Path
import datetime,hashlib,json

R=Path(__file__).resolve().parent.parent;D=R/'blackbox75'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();files=sorted(R.glob('75_*'));assert len(files)==8
readiness=dict(reviewed_utc=now,current_external_authorization=False,current_real_ad_execution=False,
 L0=dict(status='GO_ARCHIVED_DOCS_AND_OFFLINE_SYNTHETIC',executed=True),
 L1=dict(status='LOCAL_MOCK_FEASIBLE_DEVICE_APP_PILOT_NOT_EXECUTED',external_platform_experiment='STOP'),
 L2=dict(status='STOP_EXPLICIT_PLATFORM_SCOPE_NOT_OBTAINED',required=['written scoped sandbox','synthetic approved test subjects','purpose/consent gates','event receipt and availability timing','candidate/cap/model/aggregate versions','anonymous source/receiver/route lineage','actual nonnull feature-read audit']),
 same_device_primary='Paired device-block source-history randomization;all eligible opportunities incl no-fill',
 cross_device_primary='Source-history by account-link interaction;account not natural person',
 main_nonpersonal_null='D0 with frozen aggregates/model and no alternative source->current-context path;includes H0/H3',
 unknown=['Real platform same-device routing','Cross-device person entity','Axon/Vector C_graph','Independent value prediction gain','Relative vendor advantage'],
 next_minimal='A0/A1 local mock observability pilot;platform same-device canary replay only after L2 scope',
 real_value_experiment='STOP_NO_REAL_AUTHORIZED_MATURE_LABELS',
 live_identity_queries=False,real_training=False)
save(D/'EXPERIMENT_READINESS.json',readiness)
g=read(D/'EVIDENCE_GRAPH.before.json');sources=[]
specs=[
 ('BB75S01',D/'HYPOTHESES.json','Researcher operational training-source and online-link definitions;not vendor architecture'),
 ('BB75S02',R/'75_黑盒可识别性矩阵.csv','56 prospective observability rows;conditional identification not actual observations'),
 ('BB75S03',D/'PREREGISTRATION.md','Frozen before synthetic simulation;no real test preregistration claimed'),
 ('BB75S04',D/'CONFIG.json','Complete fixed synthetic parameters and seed'),
 ('BB75S05',D/'simulate.py','Offline statistical design generator;no model fitting or network'),
 ('BB75S06',D/'results/REPLICATE_RESULTS.csv','5700 synthetic repeated-design results;not vendor effects'),
 ('BB75S07',D/'results/DESIGN_SUMMARY.csv','19 synthetic scenario summaries with Monte Carlo rejection uncertainty'),
 ('BB75S08',D/'results/OBSERVATIONS/EQUIVALENT_WORLDS.csv','Three exact observable-equivalence constructions;not empirical real-device data'),
 ('BB75S09',D/'results/TRUTH/EQUIVALENT_WORLDS.json','Synthetic latent explanations kept separate from external observation'),
 ('BB75S10',D/'results/VALUE_SCALE_COUNTEREXAMPLE.json','Identical winners do not identify absolute hidden score scale'),
 ('BB75S11',D/'ADMISSION_AND_INTERPRETATION_CHECKS.json','12 hypothetical admission/interpretation fixtures;L2 not held'),
 ('BB75S12',D/'EXPERIMENT_READINESS.json','Current real platform experiment STOP;no identity queries or mature-value experiment'),
 ('BB75S13',R/'75_同设备跨App关联实验.md','Prospective same-device causal design and privacy/lifecycle boundaries'),
 ('BB75S14',R/'75_跨设备同人关联实验.md','Prospective account-history factorial;person identity not assumed'),
 ('BB75S15',R/'75_实验授权与数据边界.md','L0/L1/L2 scope and proposed anonymous audit fields,not vendor schema'),
 ('BB75S16',R/'75_混杂因素与反证实验.md','Competing paths and five inherited LiveRamp/provider safeguards')]
for sid,p,claim in specs:
 sources.append(dict(id=sid,path=p.relative_to(R).as_posix(),sha256=sha(p),source_date=now,claim=claim,
  evidence_kind='independent synthetic design artifact' if 'results/' in p.as_posix() else 'prospective design or independent protocol',
  evidence_stages=[],permission_conditions='Offline or future scoped sandbox only;no actual platform permission inferred',
  production_match_proven=False,prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False))
labels={
 'definitions':'Operational training-source T0/T1 and online link D0/D1/D2 axes',
 'h0':'H0 target/context training with no individual source-app query',
 'h3':'H3 aggregate/shared training without individual source-app query',
 'h1':'H1 same-device source-app route;real platform status unknown',
 'h2account':'H2 cross-device account history;not person',
 'h2person':'H2 person-level claim requires independent authorized entity truth',
 'household':'Household/network alternative;shared IP is not person truth',
 'ads':'Ads/creative/frequency/category response only',
 'audience':'Authorized recipient-specific audience/match status needed;not held',
 'feature':'Authorized actual nonnull matched-history feature-read trace needed;not held',
 'vendor_use':'Unknown real Axon/Vector matched-history value-model consumption',
 'gain':'Unknown independent real opportunity-value prediction benefit',
 'same_design':'Same-device randomized history design;real execution STOP',
 'cross_design':'Cross-device history x link factorial design;real execution STOP',
 'simulation':'5700 independent synthetic repeated-design results;no real value labels',
 'equivalence':'Three exact observational-equivalence constructions',
 'confounds':'Inventory/caps/context/aggregation can mimic identity response',
 'admission':'L0 GO;L1 local mock only;L2 explicit permission not held'}
nodes=[dict(id='BB75N_'+k,label=v,stage='design_synthetic_or_unknown',contains_real_personal_data=False) for k,v in labels.items()]
edges=[]
def edge(a,b,claim,ids,status):
 edges.append(dict(id=f'BB75E{len(edges)+1:02}',source='BB75N_'+a,target='BB75N_'+b,claim=claim,source_ids=ids,status=status,
  evidence_level='Independent design/synthetic or unknown;not E5/E6',evidence_stages=[],reviewed_utc=now,
  permission_conditions='Public archived evidence/local synthetic only;future product-specific permission required',
  production_match_proven=False,prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
  missing_evidence='Authorized recipient-specific route/entity/time/actual-consumption audit and independent real label test',
  six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,production_successful_send=False,server_received=False,server_model_training=False)))
edge('definitions','h0','Researcher mutually bounded source-training null,not classification recovered from ads',['BB75S01'],'definition')
edge('definitions','h3','H3 differs by training provenance,not necessarily visible frozen mapping',['BB75S01'],'definition')
edge('h0','equivalence','Can produce the same externally observed mapping as H3',['BB75S08','BB75S09'],'synthetic_exact_counterexample')
edge('h3','equivalence','Frozen outputs do not reveal training knowledge source',['BB75S08','BB75S09'],'synthetic_exact_counterexample')
edge('same_design','h1','Random source-history effect identifies a same-device data path only with audited exclusion/receiver provenance',['BB75S13','BB75S02'],'conditional_design_not_executed')
edge('cross_design','h2account','History-by-link interaction alone does not exclude context or audience rule;audits needed',['BB75S14','BB75S08'],'conditional_design_not_executed')
edge('h2account','h2person','Same controlled account across devices is insufficient for person entity truth',['BB75S14','IG72S02','IG72S03'],'unknown')
edge('household','h2person','Shared network or household co-response cannot prove same natural person',['BB75S14','IV74S02'],'unknown')
edge('ads','h1','Creative/frequency shifts alone do not identify cross-app linkage',['BB75S02','BB75S16'],'nonidentifiable_without_extra_audit')
edge('ads','h2account','Account main effect or unaudited interaction is not unique cross-device history evidence',['BB75S06','BB75S08','BB75S14'],'nonidentifiable_without_extra_audit')
edge('confounds','ads','Stock/caps/context can generate responses without history lookup',['BB75S06','BB75S07','BB75S16'],'synthetic_design_failure_examples')
edge('simulation','same_design','Cluster vs IID,privacy gate,route errors,drift and low stock stress design;not real power',['BB75S03','BB75S04','BB75S05','BB75S06'],'synthetic_only')
edge('simulation','cross_design','Factorial separates login main effect under assumptions but can be fooled by target-context mediation',['BB75S06','BB75S07'],'synthetic_only')
edge('simulation','equivalence','Different internals share row-identical observable output;not merely non-significant test',['BB75S08','BB75S09'],'synthetic_exact_counterexample')
edge('audience','vendor_use','Match/activation state does not prove Axon/Vector actual feature consumption',['IV74S01','IV74S05','IG72S05','BB75S15'],'unknown')
edge('feature','vendor_use','Future specified-model read trace with source/time/permission would support C_graph;none obtained',['BB75S15','IV74S09','MA60S17'],'unknown')
edge('vendor_use','gain','Actual reading still needs fixed-data/capacity independent mature real-label identity-only comparison',['IV74R01','BB75S12'],'unknown')
edge('ads','gain','Identical selected winner can hide different score/value scales;no real prediction-gain inference',['BB75S10'],'nonidentifiable_from_winner')
edge('admission','same_design','Owned devices permit local mock checks,not automatic platform experiments',['BB75S11','BB75S12','BB75S15'],'execution_scope_guard')
edge('admission','cross_design','No real person linkage/identity queries or platform calls authorized',['BB75S11','BB75S12','BB75S15'],'execution_scope_guard')
edge('audience','h2person','Maintained/derived,cascade-confidence,namespace and entity scope are separate checks',['IV74S01','IV74S02','IV74S04','IV74S05','BB75S16'],'contract_limits_not_observation')
for k,added in [('nodes',nodes),('edges',edges),('sources',sources)]:
 prior={x['id'] for x in g[k]};assert not prior&{x['id'] for x in added};g[k]+=added
g['blackbox_identifiability_round75']=dict(reviewed_utc=now,new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in sources],
 baseline=dict(nodes=259,edges=312,sources=607),real_platform_experiments=False,real_identity_queries=False,
 positive_new_vendor_production_evidence=False,C_graph='UNKNOWN',D_independent_real_gain='UNKNOWN',
 identifiability_matrix_rows=56,synthetic_replicates_rows=5700,synthetic_scenarios=19,
 exact_equivalence_pairs=3,validation_path='blackbox75/VALIDATION.json')
nids={x['id'] for x in g['nodes']};sids={x['id'] for x in g['sources']}
assert all(x['source'] in nids and x['target'] in nids and set(x['source_ids'])<=sids for x in edges)
save(R/'prediction-system/EVIDENCE_GRAPH.json',g)
section=['','','## 75号：身份图谱黑盒验证与可识别性（2026-11-20）','',
 '先完成设计与可行性审计，无真实投放、身份查询、外部请求、旧SDK扫描或真人数据。H0/H3按训练来源与在线依赖两轴定义；广告响应不能直接恢复个人图谱或价值优势。','',
 '| 交付 | 范围 |','|---|---|']
for p in files:section.append(f'| [{p.name}]({p.name}) | '+('56行条件可识别性' if p.suffix=='.csv' else '研究设计、边界或本地合成结果')+' |')
section+=['','[本地来源/复现](blackbox75/README.md)；[冻结协议](blackbox75/PREREGISTRATION.md)；[5700重复结果](blackbox75/results/REPLICATE_RESULTS.csv)；[19场景摘要](blackbox75/results/DESIGN_SUMMARY.csv)；[当前准入](blackbox75/EXPERIMENT_READINESS.json)；[VALIDATION](blackbox75/VALIDATION.json)。','',
 '合成给出三组不同内部机制、逐行相同外部输出的反例；统计响应显著也可能来自库存/频控/目标上下文。未新增Axon/Vector实际入模或独立收益证据。下一步先做自有本地mock可观测性先导，平台固定回放需L2明确授权。','',
 f'主图仅追加{len(nodes)}节点/{len(edges)}边/{len(sources)}来源；旧259/312/607对象和元数据保留，00—74共134份编号文件保持原字节。','']
(R/'EVIDENCE_INDEX.md').write_bytes((D/'EVIDENCE_INDEX.before.md').read_bytes()+'\n'.join(section).encode('utf-8'))
print(json.dumps(dict(deliverables=len(files),nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources'])),indent=2))
