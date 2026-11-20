"""Package round78 local specifications. No network, SDK import, or experiment."""
from pathlib import Path
import csv, datetime, hashlib, json

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):
    assert not p.exists(),f'Refuse overwrite: {p}'
    p.write_text(s.rstrip()+'\n',encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2))
def table(p,rows):
    assert rows and not p.exists()
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

h=load(D/'HISTORY_BEFORE.json')
for path,digest in h.items():assert sha(R/path)==digest,path
for path,digest in load(D/'LEGACY_ARTIFACTS_BEFORE.json').items():assert sha(R/path)==digest,path
g=load(D/'EVIDENCE_GRAPH.before.json')
assert [len(g[k]) for k in ['nodes','edges','sources']]==[293,349,639]
inputs=load(D/'INPUT_CATALOG.json')
for x in inputs:assert sha(R/x['path'])==x['sha256'],x['path']

groups=[
 ('F01','provenance/component','evidence_package_ref;resolver_owner;component_ref/version;schema_version;original_locator'),
 ('F02','entity/namespace','source_app_alias;target_app_alias;entity_granularity;source/target_namespace;relation_span;alias_attestation'),
 ('F03','resolution/purpose','resolution_receipt_ref;result_type;match_status;relation_method/quality_scope;purpose;policy_version;legal_basis_or_permission_ref'),
 ('F04','actual receiver','receiver_owner/product/service/version;environment;receiver_receipt_ref;resolution_receipt_ref;received_at;receipt_status'),
 ('F05','source event/time','source_event_ref;event_at;source_received_at;source_available_at;audit_written_at;clock_uncertainty;history_window/watermark'),
 ('F06','feature/model','feature_group/version;graph_or_mapping_version;lineage_ref;materialized_at;receiver_available_at;model_owner/family/version/task'),
 ('F07','actual model input','feature_read_ref;inference_ref;read_at;actual_input_consumed;lineage_present;input_valid;default_fallback;nonnull;runtime_path_attestation'),
 ('F08','opportunity/decision','opportunity_audit_ref;decision_ref;inference_ref;feature_read_ref;decision_at;model_version;decision_use'),
 ('F09','lifecycle','permission_intervals;coverage_attestation;revoked_at;expires_at;reset_epoch;deletion_requested/effective_at;cache_invalidation_watermark;invalid_after'),
 ('F10','authenticity/integrity/rights','issuer_authority;original_hash;transformation_manifest;authenticity_method;coverage/gaps;independent_reviewer/conflicts;inspection/export/quotation_permission')]
table(D/'CONTRACT_GROUPS.csv',[dict(group_id=i,group=n,proposed_fields=f,origin='RESEARCHER_PROPOSED_NOT_VENDOR_SCHEMA',real_values_received=False) for i,n,f in groups])

gate_names=[
 ('G00','permission and lawful handling','STOP_AUTHORIZATION'),('G01','source authenticity and independent review','PROVENANCE_UNVERIFIED'),
 ('G02','specific product/model/task/environment','SCOPE_UNRESOLVED'),('G03','relation semantics and entity scope','RELATION_UNRESOLVED'),
 ('G04','actual receiver evidence','RECEIPT_UNRESOLVED'),('G05','time and lifecycle','TIME_OR_LIFECYCLE_UNRESOLVED'),
 ('G06','actual valid non-default model input','READ_UNRESOLVED'),('G07','opportunity and active decision references','DECISION_LINK_UNRESOLVED'),
 ('G08','scoped integrity,coverage and limitations','COVERAGE_UNRESOLVED')]
save(D/'ADAPTER_SPEC.json',dict(specification_version='78.1',status='DESIGN_ONLY_NOT_IMPLEMENTED',
 current_engine='engineering76/mock76/auditor.py',current_engine_environment='offline-mock only',
 production_adapter_connected=False,production_adapter_implemented=False,real_packets_received=0,
 proposed_input='Authorized export or independently reviewable scoped report;no live API',
 input_restrictions=['No raw personal identifiers or their direct hashes','Owner retains mapping;limited audit aliases only after rights review',
   'Do not convert production records into offline-mock fixtures','Do not query for missing fields'],
 required_groups=[i for i,_,_ in groups],
 gates=[dict(id=i,check=n,missing_result=s,executed=False) for i,n,s in gate_names],
 output_fields=['claim_ref','predicate','environment','product/model/task/version','entity_scope','evidence_refs',
  'provenance_verification','independence_scope','gate_results','missing_fields','contradictions','permission_scope',
  'supported_subclaims','not_identified','reviewer/decision_date'],
 result_classes=['STOP_AUTHORIZATION','INVALID_EVIDENCE','UNIDENTIFIABLE','A_COMPONENT_ONLY','B_RECEIVED_SCOPED',
  'C_TEST_ONLY','C_SHADOW_ONLY','C_TRAINING_ONLY','C_GRAPH_REPORTED','C_GRAPH_CONFIRMED_SCOPED',
  'NO_READ_OBSERVED_SCOPED','D_SCOPED_REAL_INCREMENT'],
 independence='Verified original provenance plus explicitly scoped independent inspection of actual emission/consumption path;signature alone not factual truth',
 time_rule='Per-dependency DAG with clock uncertainty;no fabricated global ordering across systems',
 c_graph_vs_D='Confirmed actual consumption does not establish independent predictive gain;effect does not identify architecture'))

channels=[]
for company,prefix in [('AppLovin Axon','A'),('Unity Vector','V')]:
    for i,(route,owner,rights,proof,alternative) in enumerate([
      ('Formal research/technical cooperation','Platform rights holder for designated data/model;actual contact UNKNOWN',
       'Research purpose;inspection/export/quotation separately','Potential full chain if scoped actual audit is supplied','Owner-controlled review instead of raw export;still permission required'),
      ('Explicitly authorized test environment','Platform environment/model owner and test app/account owner',
       'Environment,allowed actions,data scope,quotation','Only actual test/shadow scope;not production from parity alone','Stop at sandbox scope if production audit refused'),
      ('Citable anonymous independent engineering audit','Platform authorizes records/production scope;auditor authorized to inspect and report',
       'Inspection and report release;third-party source rights where relevant','Potential actual product receipt and model-read chain','Retain originals at owner;report and limited references only'),
      ('Product-specific partner lineage','Each source rights holder;consumer scope needs platform authority',
       'Publication of own records plus explicit consumer bridge authorization','Only owned segment unless explicit consumer audit provided','Keep sender/Exchange scoped facts;C_graph stays UNKNOWN'),
      ('New already-public first-party architecture','Authorized publisher;no concrete new URL currently known',
       'Lawful public access/citation;not private access','Official production disclosure if exact mapping is stated;not automatically independent verification','Wait for concrete new input;do not repeat searches')],1):
        channels.append(dict(channel_id=f'{prefix}{i}',company=company,route=route,rights_holder_role=owner,
          permission_needed=rights,minimum_fields='F01-F10 as relevant;missing stages remain explicit',
          can_prove=proof,not_needed='Raw IDs/contact hashes,personal graph rows,weights,bid prices',
          independent_verification='Owner-controlled original inspection and citable scoped audit;not self-created hashes',
          refusal_alternative=alternative,verified_specific_contact=False,current_feasibility='UNKNOWN',
          new_public_URL='NONE',authorization_received=False,outreach_sent=False))
table(D/'CHANNEL_MATRIX.csv',channels)

old75=list(csv.DictReader((R/'75_黑盒可识别性矩阵.csv').open(encoding='utf-8-sig',newline='')))
mapping={
 'O1_creative':('UNIDENTIFIABLE','Response does not locate data route;require G00-G08 for any C_graph claim'),
 'O2_frequency':('UNIDENTIFIABLE','Caps,stock and context may explain response;require actual feature consumption'),
 'O3_advertiser_category':('UNIDENTIFIABLE','Ad/category changes do not distinguish graph vs cohort/shared parameters'),
 'O4_audience':('BOUNDED_AUDIENCE_ONLY','Attested receiver audience state;not model input'),
 'O5_match':('BOUNDED_COMPONENT_OR_RECEIVER_ONLY','Scope/result_type/namespace,maintained vs derived;not actual model use'),
 'O6_feature':('CONDITIONAL_SCOPED_C_GRAPH_ONLY','G00-G08 plus original entity boundary;real production scope required'),
 'O7_score':('UNIDENTIFIABLE_FROM_DIFFERENCE_ALONE','Score/bid difference needs independent actual-read lineage;not architecture proof'),
 'O8_increment':('STOP_REAL_EXPERIMENT_REQUIRED','Separate D with authorized real labels,independent test and fixed controls')}
crosswalk=[]
for row in old75:
    boundary,needed=mapping[row['observation_id']]
    crosswalk.append(dict(**row,round78_design_boundary=boundary,required_evidence=needed,
       required_gates='G00-G08 for full opportunity-level C_graph;O8 requires separate D admission',
       training_origin_claim='H0/H3 training source remains separately unidentifiable from online response/read alone',
       real_evidence_received=False,round78_execution='NOT_EXECUTED_DESIGN_CROSSWALK_ONLY'))
assert len(crosswalk)==56
table(D/'MATRIX75_CROSSWALK.csv',crosswalk)
save(D/'READINESS.json',dict(reviewed_utc=NOW,preparation='COMPLETE_SPECIFICATION_ONLY',execution='STOP',
 Axon_C_graph='UNKNOWN',Vector_C_graph='UNKNOWN',D_independent_gain='UNKNOWN',
 direct_production_evidence_packages=0,new_vendor_sources=0,authorized_test_environments=0,
 verified_new_acquisition_opportunities=0,actual_contact_or_program_confirmed=False,
 external_actions_authorized=False,outreach_sent=False,platform_interfaces_called=0,
 public_gets=0,SDK_scans=0,job_patent_privacy_partner_searches=0,mock_runs=0,synthetic_experiments=0,model_training_runs=0,
 engineering76_code_modified=False,production_adapter_implemented=False,
 selected_conditional_path='Rights-holder-controlled review of existing production records,with citable independent anonymous report;feasibility UNKNOWN',
 current_legal_local_action='Preparation and preservation only;cannot itself create new C_graph facts',
 possible_breakthrough_requires='Owner-authorized evidence release/audit OR a new concrete already-public first-party mapping',
 next_task_created=False,restart_inputs=[
 'Citable scoped production audit with F01-F10 and explicit consumer lineage',
 'Explicit rights-holder test/inspection authorization with product,environment,fields and quotation scope',
 'Concrete new first-party original URL showing deployed component -> actual product -> value model use'],
 current_decision='STOP;do not manufacture round79'))

auditor=(R/'engineering76/mock76/auditor.py').read_text(encoding='utf-8').splitlines()
markers=['def _audit','complete_local_audit','NO_REAL_PLATFORM_ATTESTATION','HASH_CHAIN_OR_SEQUENCE_INVALID',
 'FEATURE_DECISION_LINK_MISSING','NO_ACTUAL_NON_NULL_READ','MODEL_OR_AVAILABILITY_MISMATCH',
 'SOURCE_RECEIPT_MISSING','UNAUTHORIZED_PROVENANCE_READ','def assess_observable','def hypothesis_verdict']
locators=[dict(path='engineering76/mock76/auditor.py',line=i,exact_line=line.strip())
 for i,line in enumerate(auditor,1) if any(m in line for m in markers)]
save(D/'CODE_LOCATORS.json',locators)
cat=['# 78号输入与规范来源目录','',
 '本轮没有新增外部材料或生产证据。12份已有输入全文在本地读取并哈希；这里只建立取证规范。既有官方披露的证明边界不变。','',
 '| 原始文件 | SHA256 | 既有证据编号 |','|---|---|---|']
for s in inputs:
    cat.append(f"| [{s['path']}](../{s['path']}) | `{s['sha256']}` | {', '.join(s['existing_source_ids']) or '历史报告/矩阵；路径为原件定位'} |")
cat+=['','## 76号审计器精确定位','',
 '| 文件 | 行 | 原文 |','|---|---|---|']
for x in locators:cat.append(f"| {x['path']} | {x['line']} | `{x['exact_line'].replace('|','&#124;')}` |")
cat+=['','以上代码位置支持“76号只能证明本地fixture”的方法边界，不支持真实平台图谱存在。78号拟议来源真实性、授权、跨系统产品/模型及生命周期检查尚未实现为生产适配器。','',
 '保全：00—77共148份编号文件；76/77旧manifest覆盖的1217项文件与两个共享索引/主图的冻结基线分别验证。共享文件按要求追加，不拿新哈希与旧版本混比。',
 '新增主图来源EC78S01—05均为研究者设计文件，URL为空、生产标记为false。不能把规范或文档校验PASS升级为C_graph或D。']
write(D/'SOURCE_CATALOG.md','\n'.join(cat))

reports=[
 '78_身份图谱最小生产证据契约.md','78_Axon证据获取路径.md','78_Vector证据获取路径.md',
 '78_证据验收与升级规则.md','78_最小行动方案与停止条件.md']
sources=[]
for i,path in enumerate(reports,1):
    assert (R/path).is_file()
    sources.append(dict(id=f'EC78S{i:02}',path=path,sha256=sha(R/path),url=None,source_date=NOW,
       evidence_kind='researcher_acquisition_and_acceptance_specification_NOT_vendor_production_evidence',
       original_inputs='acquisition78/INPUT_CATALOG.json',claim='Proposed evidence/authorization gates only;current C_graph and D UNKNOWN,execution STOP',
       evidence_stages=[],production_actual_proven=False,production_match_proven=False,
       prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
       permission_conditions='Public local specification only;no authority to contact platforms,access private data or run tests'))
save(D/'SPECIFICATION_SOURCES.json',sources)
nodes=[dict(id='EC78N_'+k,label=label,stage='researcher_specification_only',contains_real_personal_data=False)
 for k,label in [('contract','Minimum scoped anonymous production evidence contract F01-F10'),
 ('channels','Axon/Vector candidate channels unconfirmed;no current authorized acquisition route'),
 ('adapter','Proposed independent evidence adapter;existing76 remains offline-mock only'),
 ('gates','Separate component,receipt,actual value-model use and independent lift gates'),
 ('stop','C_graph and D remain UNKNOWN;execution STOP until concrete new authorized/public input')]]
edges=[]
for i,(a,b,sids,claim) in enumerate([
 ('contract','adapter',['EC78S01','EC78S04','EN76S04'],'Reuse local audit principles as design only;add authority,scope and cross-system verification'),
 ('channels','contract',['EC78S02','EC78S03'],'Potential owner-controlled anonymous audit requires unconfirmed rights and opportunity;not an available cooperation claim'),
 ('adapter','gates',['EC78S04'],'Defined acceptance gates are not executed production evidence and cannot promote mock results'),
 ('gates','stop',['EC78S05','EC78S04'],'No new C_graph or D evidence;no authorized executable breakthrough route currently confirmed')],1):
    edges.append(dict(id=f'EC78E{i:02}',source='EC78N_'+a,target='EC78N_'+b,source_ids=sids,claim=claim,
      status='proposed_specification_only' if i<4 else 'unknown',evidence_level='Researcher normative design;NOT E5/E6',
      reviewed_utc=NOW,evidence_stages=[],production_actual_proven=False,production_match_proven=False,
      prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
      six_layers={k:False for k in ['sdk_capability','actual_game_business_callsite','request_construction_code','production_successful_send','server_received','server_model_training']},
      missing_evidence='Rights-holder-authorized,citable actual product receipt and designated model input/decision lineage;D needs separate real controlled experiment'))
g['nodes'].extend(nodes);g['edges'].extend(edges);g['sources'].extend(sources)
g['identity_evidence_acquisition_round78']=dict(reviewed_utc=NOW,reports=reports,new_node_ids=[n['id'] for n in nodes],
 new_edge_ids=[e['id'] for e in edges],new_local_specification_sources=[s['id'] for s in sources],
 new_vendor_sources=0,new_production_evidence=0,c_graph_upgrades=0,Axon_C_graph='UNKNOWN',Vector_C_graph='UNKNOWN',D='UNKNOWN',
 preparation='SPECIFICATION_COMPLETE',execution='STOP',readiness='acquisition78/READINESS.json',
 adapter_implemented=False,real_experiments_executed=0,next_task_created=False)
graph_path=R/'prediction-system/EVIDENCE_GRAPH.json'
assert sha(graph_path)==h['prediction-system/EVIDENCE_GRAPH.json']
graph_path.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
addition='''

## 78号：身份图谱关键证据突破方案（2026-11-20）

结论：**契约与获取/验收门槛已完成；C_graph与D仍UNKNOWN。当前无已确认可执行的新证据渠道，执行STOP，不创建79号任务。** 未搜索、联网、联系平台、接收真实日志、训练、模拟或重跑76号mock。所有候选渠道可行性UNKNOWN，不代表平台已开放合作。

| 交付 | 内容 |
|---|---|
| [78_身份图谱最小生产证据契约.md](78_身份图谱最小生产证据契约.md) | F01—F10，实体/产品/模型/时间/权限/原件与引用权 |
| [78_Axon证据获取路径.md](78_Axon证据获取路径.md) | 5类候选渠道、权利角色、最小匿名审计询问草稿；未发送 |
| [78_Vector证据获取路径.md](78_Vector证据获取路径.md) | 5类渠道及Exchange/Vector、设备/账号/人的反误判 |
| [78_证据验收与升级规则.md](78_证据验收与升级规则.md) | 76原则的设计适配；G00—G08；C_graph与D分开 |
| [78_最小行动方案与停止条件.md](78_最小行动方案与停止条件.md) | 7项回答、最小受控审计方案及具体恢复输入 |

[输入原件与SHA256](acquisition78/SOURCE_CATALOG.md)、[75号56行逐行门槛对照](acquisition78/MATRIX75_CROSSWALK.csv)、[拟议适配契约](acquisition78/ADAPTER_SPEC.json)、[当前准入](acquisition78/READINESS.json)、[保全核验](acquisition78/VALIDATION.json)。56行对照仅设计，未执行实验；76号代码只认offline-mock，未改动。00—77共148份编号文件及1217项旧产物保留。主图只追加5节点/4边/5份本地规范来源；旧293/349/639对象与旧元数据保留，不升级生产匹配/消费。
'''
index=R/'EVIDENCE_INDEX.md'
assert sha(index)==h['EVIDENCE_INDEX.md']
index.write_bytes((D/'EVIDENCE_INDEX.before.md').read_bytes()+addition.encode('utf-8'))
print(json.dumps(dict(reports=5,contract_groups=10,gates=9,channels=10,crosswalk_rows=56,new_vendor_sources=0,execution='STOP',new_graph_objects=[5,4,5])))
