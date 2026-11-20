from pathlib import Path
import json,datetime
R=Path(__file__).resolve().parent.parent;D=R/'closure70'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
base=read(D/'EVIDENCE_GRAPH.before.json');current=read(R/'prediction-system/EVIDENCE_GRAPH.json')
if 'closed_loop_round70' not in current:assert current==base,'External graph edit;reconcile before mutation'
else:
    for k in ['nodes','edges','sources']:assert current[k][:len(base[k])]==base[k]
g=json.loads(json.dumps(base,ensure_ascii=False))
sources=read(D/'SOURCE_EVIDENCE.json')+read(D/'CODE_EVIDENCE.json')
for x in sources:
    x['evidence_priority']='B' if x['id'].startswith('CL70C') else 'A'
    x['priority_note']='Static code or official contact/metadata;not raw dataset permission or observed production training'
    x['production_actual_proven']=False;x['observed_target_game_delivery']=False;x['server_model_training']=False
g['sources'].extend(sources)
specs=[('max_response','MAX full-response event_id stored in each selected ad context','response'),('max_tracker','MAX winner tracker event_id by adUnit','client_history'),('max_next','Next MAX previous_loaded_request_id','request'),('max_revenue','Same MaxAd configurable impression/click revenue callback;load internal branch separate','feedback'),('unity_load_uuid','Adapter fresh load-time UUID shared by load/show options','identity_of_ad_not_person'),('unity_adobject','Unity opportunityId + current mutable trackingToken in AdObject','ad_lifecycle'),('unity_events','Operative eventId + opportunityId + trackingToken -> queue/sender','feedback'),('mmp_ingress','Revenue MMP entry and configured partner-ingress contract','receiver_contract'),('model_unknown','Event-level server join/labels/training/bid effect unresolved','unknown'),('uken_route','Verified current SFU/Uken liaison contacts;drafts not sent','access_routing'),('data_admission','No new licensed real-player dataset;training STOP','admission')]
nodes=[dict(id='CL70_'+key,label=label,stage=stage) for key,label,stage in specs]
g['nodes'].extend(nodes)
edges=[]
def add(key,a,b,claim,ids,known,sdk=False,request=False,missing='',game=False):
    edges.append(dict(id='CL70E'+key,source='CL70_'+a,target='CL70_'+b,claim=claim,source_ids=ids,status='proven' if known else 'unknown',diagram_style='solid' if known else 'dashed',evidence_level='【SDK代码证实】' if sdk else ('【官方公开证实】' if known else '【无法确认】'),reviewed_utc=now,permission_conditions='Static authorized/public release analysis;privacy gates,partner config and dataset permission independently required;no production test',production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False,missing_evidence=missing,six_layers=dict(sdk_capability=sdk,actual_game_business_callsite=game,request_construction_code=request,production_successful_send=False,server_received=False,server_model_training=False)))
add('01','max_response','max_tracker','Full response event_id -> c3.T -> q.e[adUnit] at successful waterfall load',['CL70C18','CL70C19','CL70C20','CL70C21','CL70C22','CL70C23'],True,True,missing='Selected V2 path;ID may be reused across candidates;no impression uniqueness')
add('02','max_tracker','max_next','q.a(adUnit) getter -> next a6.previous_loaded_request_id,explicit value propagation',['CL70C23','CL70C24'],True,True,True,missing='No production request;does not prove Axon training inclusion')
add('03','max_response','max_revenue','Same c3 -> configured mimp/vimp/cimp/click public callback;load branch internal only',['CL70C19','CL70C28','CL70C29','CL70C37','CL70C38'],True,True,missing='Actual game trigger config/delivery,precision/settlement,dedup')
add('04','unity_load_uuid','unity_adobject','Matching adapter4.17/source4.17 objectId -> opportunity UUID -> request/config -> AdObject;selected4.18 counterparts verified',['CL70C01','CL70C02','CL70C03','CL70C04','CL70C05','CL70C06','CL70C07','CL70C08','CL70C09','CL70C34','CL70C35'],True,True,True,missing='Load UUID occurs after original token collection;server token->markup/auction mapping opaque')
add('05','unity_adobject','unity_events','Same ad used in show and viewer operative event;current token read;new eventId;timestamp/queue policies distinct',['CL70C10','CL70C11','CL70C12','CL70C13','CL70C14','CL70C15','CL70C16','CL70C17','GI69C01','GI69C02','CL70C36'],True,True,True,missing='Opaque additionalData subtype,money;no event delivery/model use proven')
add('06','max_revenue','mmp_ingress','Game revenue API call exists but economic ID propagation to MMP not proven;Rotate forwards amount/network and extra event copies',['XS43','CGS44','CGS46','CGS49','CGS50'],False,True,False,missing='No explicit MAX event_id/Unity opportunityId -> MMP revenue dedup/partner join contract',game=True)
add('07','mmp_ingress','model_unknown','Official partner product learning uses disclosed;event-specific received/training columns and bid effects unresolved',['CGS42','CGS48','CGS49','CGS50','CGS51','MA60S17'],False,missing='Authorized receipt,dedup,install/revenue identity,mature labels,feature/label columns and model version')
add('08','unity_events','model_unknown','Client event transport association does not establish Vector source->label/feature use',['CL70C13','CL70C14','CL70C17','MA60S17'],False,True,True,missing='Production ingestion and field-level training lineage;token can refresh')
add('09','max_next','model_unknown','Proven request-history identifier does not prove natural-person graph or Axon training use',['CL70C23','CL70C24','CGS51'],False,True,True,missing='Actual feature inclusion and privacy/advertiser scope contract')
add('10','uken_route','data_admission','Current official liaison paths verified;no dedicated rights-granting data channel or NDA obtained;drafts unsent',['CL70S01','CL70S02','CL70S03','CL70S04','CL70S05','GI69S_uken_participant'],False,missing='2015 organizer/custodian,current license/NDA,raw files/scaling/windows/zero coverage')
add('11','data_admission','model_unknown','Public paper/code access not raw game-data permission;no legal mature-player training set acquired',['GI69S_unity_paper','GI69S_unity_osf','GI69S_unity_code','GI69S_ageishtaria','CL70S06'],False,missing='Legally admitted actual game cohort;no new model experiment possible')
g['edges'].extend(edges)
g['unknown_breakpoints'].extend(['CL70: original header-bidding tokenId/MAX response event_id/Unity load opportunity mapping','CL70: unique economic impression ID and ILRD-MMP duplicate reconciliation','CL70: client event received->identity attribution->training feature/label columns->subsequent bid/model version','CL70: Uken2015 current license/custodian/NDA and observation/scaling contract'])
g['excluded_claims'].extend(['CL70: biddingAdId/load opportunity is not established identical to prebid tokenId or MAX event_id','CL70: trackingToken is mutable,not a guaranteed immutable ad identity','CL70: MAX full-response event_id not proven unique per candidate/economic impression','CL70: load internal revenue_event processing is not proof of early developer onAdRevenuePaid','CL70: all onAdRevenuePaid callbacks cannot be assigned one universal impression timestamp;click branch exists','CL70: current SFU/Uken contact is not a confirmed authorized raw-data access grant'])
reports=['70_Uken数据授权与申请准备.md','70_真实游戏数据新增来源审计.md','70_Axon竞价数据闭环.md','70_Vector竞价数据闭环.md','70_预测输入与收入反馈时间线.csv','70_下一阶段突破建议.md']
g['closed_loop_round70']=dict(reviewed_utc=now,reports=reports,source_catalog='closure70/SOURCE_CATALOG.md',code_evidence='closure70/CODE_EVIDENCE.json',event_associations='closure70/EVENT_ASSOCIATIONS.json',contact_registry='closure70/CONTACT_REGISTRY.json',application_drafts='closure70/application',new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in sources],substantive_delta=['MAX response event_id -> winner/adUnit state -> next request identifier','adapter-generated load/show objectId -> Unity opportunity -> AdObject -> operative event association','MAX callback phase refinement and mutable Unity tracking-token counterevidence'],new_licensed_real_player_datasets=0,applications_sent=0,models_trained=0,production_requests=0)
for field in ['nodes','edges','sources']:assert len({x['id'] for x in g[field]})==len(g[field])
all_nodes={x['id'] for x in g['nodes']};all_sources={x['id'] for x in g['sources']}
for x in edges:
    assert x['source'] in all_nodes and x['target'] in all_nodes
    assert set(x['source_ids'])<=all_sources,(x['id'],set(x['source_ids'])-all_sources)
(R/'prediction-system/EVIDENCE_GRAPH.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'EVIDENCE_GRAPH.after.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
index0=(D/'EVIDENCE_INDEX.before.md').read_text(encoding='utf-8-sig');currentidx=(R/'EVIDENCE_INDEX.md').read_text(encoding='utf-8-sig')
assert currentidx==index0 or '\n## CL70：' in currentidx,'External index edit;reconcile before mutation'
append='''

## CL70：真实游戏授权准备与竞价/事件关联补证（2026-11-20）

本轮有新的客户端赋值链，未取得新原始玩家数据/许可、未训练、未发送申请或生产测试。

- [Uken授权与申请准备](70_Uken数据授权与申请准备.md)：由SFU官方目录找到现行统计系管理/咨询转介及Uken公开入口；不是已证实数据许可渠道。[四份未发送草稿](closure70/application/RESEARCH_BRIEF_AND_DATA_REQUEST.md)。
- [真实游戏新增来源审计](70_真实游戏数据新增来源审计.md)：Unity补充材料复用验哈希；Age原作者记录核验；MAG仍无法准确匹配原研究；数据训练STOP。
- [Axon/MAX闭环](70_Axon竞价数据闭环.md)：完整响应event_id→赢家map→下一请求previous_loaded_request_id；同广告对象收入回调；click/load与impression分支边界补齐。
- [Vector/Unity Ads闭环](70_Vector竞价数据闭环.md)：适配器新load UUID→load/show objectId→Unity机会→广告对象→operative关联；Token ID不可自动等同，trackingToken可刷新。
- [22项预测输入/反馈时间线](70_预测输入与收入反馈时间线.csv)：逐项共同ID/显式赋值、时间、触发、接收方与生产/训练未知。
- [下一阶段建议](70_下一阶段突破建议.md)：优先授权成熟游戏cohort与经济事件/MMP/训练列关联契约，不再重复SDK清单。

新增38段静态代码证据+6份官方联系/元数据，复用27条既核验材料；片段数量不等于独立发现数量。[SOURCE_CATALOG](closure70/SOURCE_CATALOG.md)、[原包/源码哈希及片段](closure70/CODE_EVIDENCE.json)、[关联机器表](closure70/EVENT_ASSOCIATIONS.json)、[字节码核验记录](closure70/BYTECODE_CHECK.json)。

关系图追加CL70节点/边/来源，所有00—69报告及旧图对象保留。真实生产发送、接收和字段级模型训练均未新增证明。[完整性核验](closure70/VALIDATION.json)。
'''
(R/'EVIDENCE_INDEX.md').write_text(index0+append,encoding='utf-8')
print(json.dumps({x:len(g[x]) for x in ['nodes','edges','sources']}))
