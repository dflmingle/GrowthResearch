"""Append only: license/sample findings,never vendor identity-model claims."""
from pathlib import Path
import datetime,hashlib,json

R=Path(__file__).resolve().parent.parent
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
h=load(D/'HISTORY_BEFORE.json')
for p,s in h.items():assert sha(R/p)==s,p
g=load(D/'EVIDENCE_GRAPH.before.json')
sources=[]
for i,x in enumerate(load(D/'LICENSE_EVIDENCE.json'),1):
    sources.append(dict(id=f'OSAS{i:02}',path=x['raw_path'],sha256=x['raw_sha256'],url=x['url'],final_url=x['final_url'],
      text_path=x['readable_path'],text_sha256=x['readable_sha256'],excerpt=x['quote'],start_line=x['quote_line'],
      source_date='License version/tag or current terms;not SDK deployment date',acquired_utc=x['acquired_utc'],
      evidence_kind='Official license/terms evidence ONLY;not identity matching or model use',claim=x['conclusion'],
      evidence_stages=[],production_actual_proven=False,production_match_proven=False,prediction_model_consumption_proven=False,
      independent_real_identity_lift_proven=False,permission_conditions='Only license/metadata inspected;future analysis requires stated per-file scope'))
for i,path in enumerate(['official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv',
 'official-samples-audit/IDENTITY_FIELD_REUSE_MATRIX.csv','official-samples-audit/MECHANISM_TEST_DESIGN.csv'],11):
    sources.append(dict(id=f'OSAS{i:02}',path=path,sha256=sha(R/path),url=None,source_date=now,
      evidence_kind='Local inventory/historical reuse/design;NOT new SDK functional analysis or production evidence',
      evidence_stages=[],production_actual_proven=False,production_match_proven=False,
      prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False))
nodes=[dict(id='OSAN_'+key,label=label,stage='license_inventory_phase_only',contains_real_personal_data=False) for key,label in [
 ('samples','30 versions/47 existing packages hash-checked;no new SDK downloads'),
 ('open','3 Adjust MIT source candidates;Google Apache repo needs pinned source;analysis not started'),
 ('hold','MAX EULA/Unity terms and other scope gates;no new restricted analysis'),
 ('reuse','30 identity fields/10 call mappings reused within historical proof scope'),
 ('unknown','Axon/Vector C_graph and D UNKNOWN;production forensics STOP')]]
edges=[]
for i,(a,b,sids,claim,status) in enumerate([
 ('samples','open',['OSAS01','OSAS02','OSAS03','OSAS04','OSAS11'],'Licenses identify next-phase source candidates,not completed analysis','official_license_scope_only'),
 ('samples','hold',['OSAS05','OSAS06','OSAS07','OSAS08','OSAS09','OSAS10'],'Core and adapter permissions are not inherited from public availability;new analysis held','license_gate_only'),
 ('reuse','unknown',['OSAS12'],'Historical identifier and interface capability does not prove production receipt,matching or model use','unknown'),
 ('open','unknown',['OSAS13'],'Independent future design/test cannot substitute for vendor C_graph or real D evidence','unknown'),
 ('hold','unknown',['EC78S01','EC78S04'],'Preserve round78 authorization/production evidence gates;no platform requests or76 changes','unknown')],1):
    edges.append(dict(id=f'OSAE{i:02}',source='OSAN_'+a,target='OSAN_'+b,source_ids=sids,claim=claim,status=status,
      evidence_level='License/historical capability or design only;NOT E5/E6',reviewed_utc=now,evidence_stages=[],
      production_actual_proven=False,production_match_proven=False,prediction_model_consumption_proven=False,
      independent_real_identity_lift_proven=False,six_layers={k:False for k in ['sdk_capability','actual_game_business_callsite',
       'request_construction_code','production_successful_send','server_received','server_model_training']}))
g['nodes'].extend(nodes);g['edges'].extend(edges);g['sources'].extend(sources)
g['official_sample_license_inventory']=dict(reviewed_utc=now,scope='First-round sample inventory and license verification only',
 reports='official-samples-audit/REPORT_PATHS.json',catalog='official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv',
 acquired_existing_artifacts=47,versions=30,new_SDK_downloads=0,new_functional_static_analyses=0,public_metadata_gets=22,
 new_node_ids=[n['id'] for n in nodes],new_edge_ids=[e['id'] for e in edges],new_source_ids=[s['id'] for s in sources],
 C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',engineering76_modified=False)
target=R/'prediction-system/EVIDENCE_GRAPH.json'
assert sha(target)==h['prediction-system/EVIDENCE_GRAPH.json']
target.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
append='''

## 官方技术样本与许可核验：未编号首轮专项（2026-11-20）

首轮已盘点30个版本、47份既有AAR/source jar/UPM包并核对哈希；未下载新SDK，未新增功能静态分析。22次公开请求只取官方许可/仓库/发布元数据。3份Adjust MIT源码包可列下一阶段优先，Google官方适配器Apache许可需固定源码commit；MAX/Unity核心/其他范围未自动放行。

交付：[样本与许可](official-samples-audit/官方样本清单与许可核验.md)、[47行版本/哈希/URL](official-samples-audit/ACQUIRED_SAMPLE_CATALOG.csv)、[静态分析可行性](official-samples-audit/静态分析可行性报告.md)、[身份字段与调用关系图](official-samples-audit/身份字段及调用关系图.md)、[五项机制](official-samples-audit/五项优先机制与反证测试.md)、[下一轮条件](official-samples-audit/下一轮授权与测试条件.md)。

[来源与SHA256](official-samples-audit/SOURCE_CATALOG.md)、[勘误](official-samples-audit/CORRECTIONS.md)、[当前状态](official-samples-audit/STATUS.json)、[核验](official-samples-audit/VALIDATION.json)。旧AppLovin适配器license.txt实际为404，不能当许可证据；当前条款不追溯替代历史许可。30字段/10映射仅复用旧证据，不是新代码分析。

00—78共153份编号文件保留，76审计器不改、不运行；C_graph.Axon/Vector与D仍UNKNOWN，原生产取证STOP。主图只追加5节点/5边/13份许可或本地盘点/设计来源，旧298/353/644对象及元数据保持；未创建79号任务或自主实现生产消费。
'''
idx=R/'EVIDENCE_INDEX.md'
assert sha(idx)==h['EVIDENCE_INDEX.md']
idx.write_bytes((D/'EVIDENCE_INDEX.before.md').read_bytes()+append.encode('utf-8'))
save(D/'ADDED_GRAPH_OBJECTS.json',dict(nodes=nodes,edges=edges,sources=sources))
print(json.dumps(dict(new_nodes=len(nodes),new_edges=len(edges),new_sources=len(sources),production_upgrades=0)))
