"""Append only this documentary design to main index/evidence graph."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=load(D/'EVIDENCE_GRAPH.before.json');g=load(R/'prediction-system/EVIDENCE_GRAPH.json')
key='server_identity_reference_design';now=datetime.now(timezone.utc).isoformat()
if key not in g:
    assert g==old,'Unexpected intervening graph change; no overwrite permitted'
    sources=[]
    for x in load(D/'SOURCE_EVIDENCE.json'):
        sources.append(dict(id=x['id'],path=x['source_path'],sha256=x['source_sha256'],url=x['url'],source_date=x['collected_utc'],
            text_path=x['text_path'],text_sha256=x['text_sha256'],start_line=x['start_line'],end_line=x['end_line'],
            evidence_kind=x['evidence_level'],scope=x['scope'],license_scope=x['license_scope'],
            evidence_stages=['reference_technical_document_or_code'],production_actual_proven=False,production_match_proven=False,
            prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False))
    local=load(D/'REPORT_PATHS.json')+['server-identity-reference/'+p for p in ['REFERENCE_CONTRACTS.json','OPEN_SOURCE_COMPONENTS.csv',
        'ACCEPTANCE_TEST_DESIGN.csv','AXON_VECTOR_GAP_MATRIX.csv','STATUS.json','SOURCE_CATALOG.md']]
    for i,p in enumerate(local,1):sources.append(dict(id=f'SIRL{i:02d}',path=p,sha256=sha(R/p),url=None,source_date=now,
        evidence_kind='Independent reference design/license audit; no production deployment or experiment',evidence_stages=[],
        production_actual_proven=False,production_match_proven=False,prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False))
    specs=[('namespace','Scoped namespaces: tenant/issuer/app/partner and typed entities'),('resolver','Authorized deterministic relations and optional scored candidates'),
      ('graph','Confidence-aware temporal relationship graph reference design'),('event','Temporal event and economic ledger linkage reference design'),
      ('feature','As-of feature service and independent consumer receipts'),('consent','Consent/revocation/deletion design, not a compliance certificate'),
      ('audit','Provenance and anonymous evidence acceptance design'),('boundary','Axon/Vector C_graph and D UNKNOWN; production forensics STOP')]
    nodes=[dict(id='SIRN_'+k,label=label,stage='reference_design' if k!='boundary' else 'unproven',contains_real_personal_data=False) for k,label in specs]
    links=[('namespace','resolver',['SIR14','SIR15','SIR16','SIRL07'],'Issuer/client scope and authentication references; not verified person identity'),
      ('resolver','graph',['SIR01','SIR02','SIR03','SIR05','SIR06','SIRL07'],'Candidate and typed account relations must pass independent graph/policy constraints'),
      ('graph','feature',['SIR04','SIR07','SIR08','SIR18','SIR19','SIRL07'],'Reference clustering and uncertainty concepts; no vendor graph inference'),
      ('event','feature',['AMSS05','AMSS06','SIRL07'],'Separate identity relation, economic idempotence and event/available time'),
      ('consent','feature',['SIR17','EC78S01','SIRL04','SIRL07'],'Revocation and derived feature invalidation are independent proposed rules'),
      ('feature','audit',['SIR11','SIR12','SIR13','SIRL05','SIRL07'],'Feature materialization/retrieval differ from nonempty model consumption and active decision'),
      ('audit','boundary',['EC78S01','EC78S04','SIRL10'],'No new vendor receipt or model-read evidence; production status unchanged'),
      ('namespace','boundary',['IV74S02','IG72S05','SIRL10'],'Partner encoding/Exchange contract does not map to Axon/Vector production model')]
    edges=[]
    for i,(a,b,sids,claim) in enumerate(links,1):edges.append(dict(id=f'SIRE{i:02d}',source='SIRN_'+a,target='SIRN_'+b,source_ids=sids,
      claim=claim,status='reference_design' if b!='boundary' else 'unknown',evidence_level='E: independent design with scoped original reference sources',
      reviewed_utc=now,evidence_stages=[],production_actual_proven=False,production_match_proven=False,prediction_model_consumption_proven=False,
      independent_real_identity_lift_proven=False,six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,
      production_successful_send=False,server_received=False,server_model_training=False)))
    allsrc={s['id'] for s in g['sources']}|{s['id'] for s in sources}
    assert all(s in allsrc for e in edges for s in e['source_ids'])
    assert not any(s['id'] in {z['id'] for z in g['sources']} for s in sources)
    extension=dict(reviewed_utc=now,scope='Public original technical research and independent reference architecture; no resolver/SDK/model execution',
       reports=load(D/'REPORT_PATHS.json'),new_node_ids=[n['id'] for n in nodes],new_edge_ids=[e['id'] for e in edges],new_source_ids=[s['id'] for s in sources],
       before='server-identity-reference/EVIDENCE_GRAPH.before.json',pinned_open_source_components=4,new_vendor_production_evidence=0,
       unexecuted_test_designs=20,C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',engineering76_modified=False)
    save(D/'ADDED_GRAPH_OBJECTS.json',dict(nodes=nodes,edges=edges,sources=sources,extension=extension))
    g['nodes'].extend(nodes);g['edges'].extend(edges);g['sources'].extend(sources);g[key]=extension
    save(R/'prediction-system/EVIDENCE_GRAPH.json',g)
else:
    added=load(D/'ADDED_GRAPH_OBJECTS.json');assert all(sha(R/s['path'])==s['sha256'] for s in added['sources']),'Artifacts changed; review before refresh'
index=R/'EVIDENCE_INDEX.md';marker='## 服务端身份解析机制与参考架构：未编号专项'
if marker not in index.read_text(encoding='utf-8-sig'):
    assert index.read_bytes()==(D/'EVIDENCE_INDEX.before.md').read_bytes(),'Unexpected index change'
    addition='''

## 服务端身份解析机制与参考架构：未编号专项（2026-11-20）

完成4个固定commit的开源许可/文档核验（Splink MIT、dedupe MIT、RecordLinkage BSD-3、Feast Apache-2），并引用OIDC、PROV-DM与原作者图式记录关联论文。42次GET仅公开技术/法律材料，19项逐行原文证据；没有真实身份接口、SDK或模型运行。

六项交付：[路线比较](server-identity-reference/服务端身份解析技术路线对比.md)、[组件与许可](server-identity-reference/开源组件与许可清单.md)、[七组件架构](server-identity-reference/身份关系图谱参考架构.md)、[14条关系/冲突/删除规则](server-identity-reference/关系建立冲突撤销与删除规则.md)、[图谱/LTV接口](server-identity-reference/图谱特征与LTV预测接口设计.md)、[Axon/Vector差距](server-identity-reference/与Axon_Vector已证证据的差距矩阵.md)。

[来源/哈希/版本](server-identity-reference/SOURCE_CATALOG.md)、[拟议契约](server-identity-reference/REFERENCE_CONTRACTS.json)、[20项未执行验收设计](server-identity-reference/ACCEPTANCE_TEST_DESIGN.csv)、[数据准入](server-identity-reference/DATA_READINESS.csv)、[静态核验](server-identity-reference/VALIDATION.json)。当前Feast文档区分事件时间与created过滤，但后端/真实available_at仍需单独验证；配对分数、簇一致性、认证账号与自然人真值明确分开。

本轮只研究与设计，没有新增合格真实跨设备/游戏收入数据，没有新的厂商生产证据或可升级C_graph材料。历史153份编号文件、76代码、官方样本审计及Adjust专项保留；主图只追加8节点/8边/31来源，旧308/362/678对象及旧元数据不变。C_graph.Axon=UNKNOWN、C_graph.Vector=UNKNOWN、D=UNKNOWN，原生产取证STOP，不创建79号；第三方参考技术不归属于厂商。
'''
    with index.open('ab') as f:f.write(addition.encode('utf-8'))
print(json.dumps(dict(graph_counts={k:len(g[k]) for k in ['nodes','edges','sources']},added_sources=len(load(D/'ADDED_GRAPH_OBJECTS.json')['sources']))))
