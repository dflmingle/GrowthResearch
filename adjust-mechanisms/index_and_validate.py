"""Append local scoped research to index/graph. No prior graph object is changed."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
R=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
base=load(D/'EVIDENCE_GRAPH.before.json');g=load(R/'prediction-system/EVIDENCE_GRAPH.json')
extension='adjust_mit_source_mechanism_review'
assert len({x['id'] for x in g['sources']})==len(g['sources'])
if extension not in g:
    assert g==base,'Unexpected graph changes; do not overwrite'
    add_sources=[]
    def src(sid,path,kind,url=None):
        add_sources.append(dict(id=sid,path=path,sha256=sha(R/path),url=url,source_date=now,evidence_kind=kind,
            evidence_stages=['client_static'] if kind=='Adjust MIT source archive' else [],
            production_actual_proven=False,production_match_proven=False,prediction_model_consumption_proven=False,
            independent_real_identity_lift_proven=False))
    for i,s in enumerate(load(D/'SAMPLES.json'),1):src(f'AMSS{i:02d}',s['path'],'Adjust MIT source archive',s['official_download_url'])
    paths=['EXTRACTED_FILES.json','CODE_EVIDENCE.json','FINDINGS.json','DIFF_INDEX.final.json',
       'Adjust身份与归因机制图.md','三版本源码差分.md','身份标识生命周期表.md','已证实机制与服务端未知清单.md',
       '自主IdentityResolver最小设计建议.md','下一阶段授权和测试条件.md','license-review/版本许可复核.md',
       'license-review/FETCH_MANIFEST.json','STATUS.json']
    for i,p in enumerate(paths,4):src(f'AMSS{i:02d}','adjust-mechanisms/'+p,'Local scoped static analysis/license review/design; not production')
    for i,s in enumerate(load(D/'license-review/FETCH_MANIFEST.json'),1):src(f'AMSL{i:02d}',s['path'],'Official legal-only HTTP response; not implementation permission inference',s['url'])
    nodes=[
       dict(id='AMN_source',label='3 Adjust MIT source archives / scoped client review',stage='client_static',contains_real_personal_data=False),
       dict(id='AMN_client',label='App-private UUID / external ID transport / attribution response / bounded queues',stage='client_static',contains_real_personal_data=False),
       dict(id='AMN_design',label='Independent scoped identity resolver design only',stage='reference_design',contains_real_personal_data=False),
       dict(id='AMN_license',label='MAX/LevelPlay core/adapters permission HOLD; legal-only review',stage='license_gate',contains_real_personal_data=False),
       dict(id='AMN_unknown',label='Axon/Vector C_graph and D UNKNOWN; production forensics STOP',stage='unproven',contains_real_personal_data=False)]
    edges=[]
    configs=[('AME01','AMN_source','AMN_client',['AMSS01','AMSS02','AMSS03','AMSS05','AMSS06'],
       'Scoped static proof of listed client calls only; no observed sends/receipt/graph/model','client_static'),
      ('AME02','AMN_client','AMN_design',['AMSS12','AMSS13'],
       'Reference mechanisms for independent design; not a vendor architecture reproduction','design'),
      ('AME03','AMN_license','AMN_unknown',['AMSS14','AMSS15'],
       'Custom version-specific licenses remain HOLD; no MAX/LevelPlay functional analysis','unknown'),
      ('AME04','AMN_client','AMN_unknown',['AMSS11','AMSS13'],
       'Adjust client transport does not prove Axon/Vector receipt or identity-feature consumption','unknown')]
    for eid,a,b,sids,claim,status in configs:
        edges.append(dict(id=eid,source=a,target=b,source_ids=sids,claim=claim,status=status,
          evidence_level='B: client static only' if status=='client_static' else 'Design/license/unknown; no production upgrade',reviewed_utc=now,
          evidence_stages=['client_static'] if status=='client_static' else [],production_actual_proven=False,
          production_match_proven=False,prediction_model_consumption_proven=False,independent_real_identity_lift_proven=False,
          six_layers=dict(sdk_capability=status=='client_static',actual_game_business_callsite=False,
            request_construction_code=status=='client_static',production_successful_send=False,server_received=False,server_model_training=False)))
    g['nodes'].extend(nodes);g['edges'].extend(edges);g['sources'].extend(add_sources)
    g[extension]=dict(reviewed_utc=now,samples=['OSM034','OSM036','OSM038'],scope='111 selected Adjust MIT Java entries; no SDK execution',
       findings=22,changed_selected_pairs=24,new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],
       new_source_ids=[x['id'] for x in add_sources],C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP',
       SDK_executions=0,production_requests=0,engineering76_modified=False,before='adjust-mechanisms/EVIDENCE_GRAPH.before.json')
    save(D/'ADDED_GRAPH_OBJECTS.json',dict(nodes=nodes,edges=edges,sources=add_sources,extension=g[extension]))
    save(R/'prediction-system/EVIDENCE_GRAPH.json',g)
else:
    oldadded=load(D/'ADDED_GRAPH_OBJECTS.json')
    assert all(sha(R/s['path'])==s['sha256'] for s in oldadded['sources']),'New artifacts changed after append; review before refresh'
index=R/'EVIDENCE_INDEX.md';marker='## Adjust MIT源码机制验证：未编号限定专项'
if marker not in index.read_text(encoding='utf-8-sig'):
    assert index.read_bytes()==(D/'EVIDENCE_INDEX.before.md').read_bytes()
    addition='''

## Adjust MIT源码机制验证：未编号限定专项（2026-11-20）

仅分析OSM034/036/038（5.5.0/5.7.0/5.8.1）MIT源码：111个选定条目、22项发现/61行逐版本记录、76个配对比较中的24项变化/新增。区分应用私有UUID、OS标识、external_device_id输入与服务器adid；有限去重/出队不等于经济事件唯一或远端成功。5.7类白名单/FB开关/TPS回调，5.8细分读取开关及重试恢复差分有明确代码位置。

交付：[总览](adjust-mechanisms/README.md)、[身份/归因机制图](adjust-mechanisms/Adjust身份与归因机制图.md)、[三版本差分](adjust-mechanisms/三版本源码差分.md)、[标识生命周期](adjust-mechanisms/身份标识生命周期表.md)、[客户端已证实与服务端未知](adjust-mechanisms/已证实机制与服务端未知清单.md)、[独立Resolver设计](adjust-mechanisms/自主IdentityResolver最小设计建议.md)、[下一阶段条件](adjust-mechanisms/下一阶段授权和测试条件.md)。

[源码证据/完整方法/哈希](adjust-mechanisms/CODE_EVIDENCE.json)、[61行矩阵](adjust-mechanisms/FINDINGS.csv)、[MAX/LevelPlay逐版本许可复核](adjust-mechanisms/license-review/版本许可复核.md)、[静态保全核验](adjust-mechanisms/VALIDATION.json)。5次新请求仅为法律文件；未下载新SDK、未分析MAX/LevelPlay功能、未启动SDK/生产请求或真实身份查询。

00—78共153份编号文件保留；76程序不改、不重跑；不创建79。Adjust机制不归属于Axon/Vector。C_graph.Axon=UNKNOWN、C_graph.Vector=UNKNOWN、D=UNKNOWN，原生产取证STOP。主图只追加5节点/4边/21来源；旧303/358/657对象及旧元数据保留。核验PASS仅说明静态引用、版本差分和保全，不是实际匹配/删除/接收/模型测试。
'''
    with index.open('ab') as f:f.write(addition.encode('utf-8'))
print(json.dumps(dict(graph_counts={k:len(g[k]) for k in ['nodes','edges','sources']},extension=extension)))
