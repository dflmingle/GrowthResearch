from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent.parent;D=R/'game-industry69'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
base=read(D/'EVIDENCE_GRAPH.before.json')
current=read(R/'prediction-system/EVIDENCE_GRAPH.json')
if 'game_industry_round69' not in current:assert current==base,'Graph changed outside this synthesis; reconcile first'
else:
    for k in ['nodes','edges','sources']:assert current[k][:len(base[k])]==base[k]
g=json.loads(json.dumps(base,ensure_ascii=False))
new_sources=read(D/'SOURCE_EVIDENCE.json')+read(D/'CODE_EVIDENCE.json')
for x in new_sources:
    assert sha(R/x['path'])==x['sha256']
    x['evidence_priority']=('B' if x['id'].startswith('GI69C') else ('A' if x['id'] in ['GI69S_apple_aa','GI69S_apple_sk'] else ('C' if x['id'].startswith('GI69S_unity_') and x['id']!='GI69S_unity_research_route' or x['id']=='GI69S_ageishtaria' else 'D')))
    x['priority_note']='A=official protocol, B=static code, C=original research material, D=historical participant/discovery/self-description;none proves target production training'
g['sources'].extend(new_sources)
node_specs=[('uken_restricted','Uken2015 participant-described data;current permission/window unresolved','data_source'),('unity_private_iap','Unity real private iOS IAP study;payer-only,game-local keys','data_source'),('synthetic_reproduction','Published synthesis code/demo uses synthetic placeholder data','counterevidence'),('mag_unresolved','MAG five-game source identity/license unresolved','unknown'),('admission','No newly admitted real game-value training dataset','admission'),('pre_ad','Client pre-ad request context and limited prior-ad history','prebid_input'),('post_ad','Ad lifecycle and revenue metadata/callback/MMP package','feedback'),('partner_ingress','Configured platform postback/Insights ingress contracts','receiver'),('training_unknown','Per-field production join/mature label/model consumption unknown','unknown')]
new_nodes=[dict(id='GI69_'+k,label=label,stage=stage) for k,label,stage in node_specs]
g['nodes'].extend(new_nodes)
def edge(n,a,b,claim,ids,known=False,sdk=False,request=False,missing='',vendor=False):
    return dict(id='GI69E'+str(n),source='GI69_'+a,target='GI69_'+b,claim=claim,source_ids=ids,status='proven' if known else 'unknown',diagram_style='solid' if known else 'dashed',evidence_level='【SDK代码证实】' if sdk else ('【原始材料证实】' if known else '【无法确认】'),reviewed_utc=now,permission_conditions='Public source/static SDK only;restricted datasets require new explicit permission;app consent/partner mapping independently required',production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False,vendor_disclosed_product_model_use=vendor,missing_evidence=missing,six_layers=dict(sdk_capability=sdk,actual_game_business_callsite=False,request_construction_code=request,production_successful_send=False,server_received=False,server_model_training=False))
edges=[
edge(1,'uken_restricted','admission','Participant reports300k rows but explicitly cannot upload;source documentation does not grant data access',['GI69S_uken_participant','GI69S_uken_tree','GI69S_uken_code'],True,missing='Rights-holder license/NDA,original files,amount scaling,fixed input/label windows,observation coverage'),
edge(2,'unity_private_iap','admission','Paper explicitly restricts raw data to Unity warehouse;authors cannot share/facilitate access;payer-only sample',['GI69S_unity_paper','GI69S_unity_osf'],True,missing='New Unity permission,actual tables,all-install population and monetary/observation contract'),
edge(3,'synthetic_reproduction','admission','Public reproduction R and Uken-inspired310K demo cannot count as real game economic samples',['GI69S_unity_code','GI69S_uken_synthetic'],True),
edge(4,'mag_unresolved','admission','Company page does not establish specific five-game dataset identity,files or permission',['GI69S_mag_site'],missing='Exact original paper/DOI,supplement,license and real file audit'),
edge(5,'pre_ad','post_ad','Unity operative event separately assigns eventId,opportunityId and trackingToken then persists a UniversalRequest job',['CGS21','GI69C01','GI69C02'],True,True,True,missing='Selected event caller/type decoding and actual production receipt;not every event is impression revenue'),
edge(6,'post_ad','partner_ingress','AF/Adjust have explicit revenue field/package contracts;platform postbacks require independent configuration',['GI69C03','GI69C04','GI69C05','CGS44','CGS46','CGS49','CGS50'],True,True,True,missing='Four-game partner activation,delivery,dedup and exact money reconciliation'),
edge(7,'partner_ingress','training_unknown','Product-level learning use disclosed;actual source,event/identity joins,as-of times and training columns unresolved',['CGS42','CGS48','CGS51','MA60S17'],missing='Authorized ingestion to feature/label dataset lineage and model inclusion audit',vendor=True),
edge(8,'pre_ad','partner_ingress','Apple signed attributable-ad context precedes conversion;privacy-tiered postbacks follow install/reengagement',['GI69S_apple_aa','GI69S_apple_sk'],True,missing='No target iOS game adoption,postback receipt or raw per-user income proven'),
edge(9,'unity_private_iap','training_unknown','Historical research game-local pseudonyms do not prove current Vector personal cross-game join or training consumption',['GI69S_unity_paper','MA60S17'],missing='Current authorized product-specific training-data contract'),
edge(10,'admission','training_unknown','Without lawful raw rows and mature true-value labels no new empirical model advantage claim can be made',['GI69S_uken_participant','GI69S_unity_paper','GI69S_unity_code'],True,missing='Qualified game cohort,actual future revenue,licensed second game for transfer'),
]
g['edges'].extend(edges)
g['unknown_breakpoints'].extend(['GI69: Uken original NDA/amount scaling/as-of windows and per-user coverage','GI69: MAG five-game original paper/source identity and license','GI69: no lawful full-install denominator paired with IAA impression ledger and IAP refunds','GI69: configured platform ingress to actual training dataset column/identity join'])
g['excluded_claims'].extend(['GI69: Uken-inspired310K synthetic demo is not Uken real player release','GI69: Many Faces public R sample is not real69m-payer transactional dataset','GI69: historical Unity research use is not proof that its table trained Vector','GI69: returned bid price,win notice,realized impression revenue,and attribution did-win are not interchangeable'])
g['game_industry_round69']=dict(reviewed_utc=now,report_paths=['69_真实游戏数据来源与获取可行性.md','69_Uken数据获取与准入审计.md','69_Unity交易数据来源审计.md','69_MAG游戏经营数据审计.md','69_广告请求与收入反馈字段时间线.md','69_Axon_Vector训练与竞价数据连接证据.md','69_NEXT_RESEARCH_PRIORITY.md'],source_catalog='game-industry69/SOURCE_CATALOG.md',source_evidence='game-industry69/SOURCE_EVIDENCE.json',field_timeline='game-industry69/SDK_FIELD_TIMELINE.json',dataset_admission='game-industry69/DATASET_ADMISSION.csv',new_node_ids=[x['id'] for x in new_nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in new_sources],new_real_training_datasets=0,models_trained=0,applications_sent=0,production_requests=0,scope_note='Parallel game-industry69;all original retail69 objects remain intact')
node_ids={x['id'] for x in g['nodes']};source_ids={x['id'] for x in g['sources']}
for x in edges:
    assert x['source'] in node_ids and x['target'] in node_ids
    assert set(x['source_ids'])<=source_ids,(x['id'],set(x['source_ids'])-source_ids)
for k in ['nodes','edges','sources']:assert len({x['id'] for x in g[k]})==len(g[k])
(R/'prediction-system/EVIDENCE_GRAPH.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'EVIDENCE_GRAPH.after.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
index=(D/'EVIDENCE_INDEX.before.md').read_text(encoding='utf-8-sig')
current_index=(R/'EVIDENCE_INDEX.md').read_text(encoding='utf-8-sig')
assert current_index==index or '\n## GI69：真实游戏数据' in current_index
append='''

## GI69：真实游戏数据、广告请求与价值反馈专项（2026-11-20）

与原零售69号并行保留。没有新增可直接训练的真实游戏玩家文件；没有发送申请、签约、训练或生产测试。

- [69总览](69_真实游戏数据来源与获取可行性.md)：6候选准入卡，真实训练均STOP或排除。
- [Uken](69_Uken数据获取与准入审计.md)：SFU2015参与者30万行/44字段说明，明确无上传数据权限；缩放、观察窗口和完整NDA未知。
- [Unity交易研究](69_Unity交易数据来源审计.md)：真实IAP论文、OSF两份补充文件已下载验哈希；原数据内部受控、作者不能共享、仅付费者、跨游戏ID不关联；R样本为合成。
- [MAG](69_MAG游戏经营数据审计.md)：五游戏原论文/数据包身份尚未匹配，UNKNOWN/STOP，不以无检索结果否定其存在。
- [字段时间线](69_广告请求与收入反馈字段时间线.md)：24条广告前/响应/展示/收入/MMP/Apple归因字段链；复用220条哈希核验材料。
- [Axon/Vector连接](69_Axon_Vector训练与竞价数据连接证据.md)：官方产品用途与客户端字段级消费保持分开，没有新增生产训练血缘。
- [70号建议](69_NEXT_RESEARCH_PRIORITY.md)：优先数据授权、成熟cohort与接收→训练列契约；没有合格数据不训练。

原始URL、位置、日期、SHA256：[SOURCE_CATALOG](game-industry69/SOURCE_CATALOG.md)、[来源对象](game-industry69/SOURCE_EVIDENCE.json)、[代码片段](game-industry69/CODE_EVIDENCE.json)、[获取记录](game-industry69/FETCH_MANIFEST.json)。[字段CSV](game-industry69/SDK_FIELD_TIMELINE.csv)、[准入CSV](game-industry69/DATASET_ADMISSION.csv)。

图追加GI69节点/边/来源，保留全部历史对象；六层不跳级，所有本轮生产送达/接收/训练状态未证。[核验结果](game-industry69/VALIDATION.json)。
'''
(R/'EVIDENCE_INDEX.md').write_text(index+append,encoding='utf-8')
print(json.dumps({k:len(g[k]) for k in ['nodes','edges','sources']}))
