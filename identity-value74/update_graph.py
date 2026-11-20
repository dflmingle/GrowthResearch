from pathlib import Path
import datetime, hashlib, json

R=Path(__file__).resolve().parent.parent;D=R/'identity-value74'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
protocol=next(p for p in R.glob('74_*.md') if p.name.startswith('74_') and 'M4减M3' in p.read_text('utf-8'))
readiness=dict(design_version='74-v1-design-only',reviewed_utc=now,real_training_performed=False,
 goal='Incremental personal-history feature value beyond aggregate/shared-parameter learning',
 primary_contrast='M4-M3',primary_endpoint='D28 total-revenue MAE paired difference;ranking/calibration also reported',
 all_target_training_samples_fixed=True,M2_M3_M4_source_supervised_pool_fixed=True,
 M3_M4_effective_supervised_samples_fixed=True,
 all_five_effective_source_data_equal=False,
 source_data_caveat='M0/M1 do not consume cross-game supervision;their total difference is not identity-only lift',
 model_capacity='Fixed predictor dimension/regularization/compute;zero slots do not guarantee equal effective rank;source-stage budget separately counted',
 models=[dict(model=f'M{i}',status='STOP_REAL_DATA_NOT_ADMITTED',result=None) for i in range(5)],
 gates=['Owner/purpose-authorized real revenue and complete cohort','Observed zero vs missing distinction','Mature labels and available_at <= bid_time',
 'Training labels mature before next phase','Time/entity-isolated target and source supervised splits','M4 accurate legal relationship and graph snapshot at prediction'],
 no_personal_cross_app_id_required_for=['M2 aggregate cohort prior','M3 shared parameters'],
 fixed_decision_policy=True,real_ROAS_allowed=False,
 further_ROAS_gate='Authorized opportunity/cost/randomization and mature net outcomes;prediction metrics alone insufficient',
 protocol_path=protocol.name,protocol_sha256=sha(protocol))
save(D/'EXPERIMENT_READINESS.json',readiness)

g=read(D/'EVIDENCE_GRAPH.before.json');sources=read(D/'SOURCE_EVIDENCE.json')
for sid,p,claim in [('IV74R01',protocol,'Prospective real-data design only;primary M4-M3,not executed'),
 ('IV74R02',R/'74_身份关联商业价值证据矩阵.csv','18 bounded A/B/C_id/C_graph/D claims;not effect estimates'),
 ('IV74R03',D/'EXPERIMENT_READINESS.json','All real experiments STOP;no training or real ROAS')]:
 sources.append(dict(id=sid,path=p.relative_to(R).as_posix(),sha256=sha(p),claim=claim,
  evidence_stages=[],source_date=now,production_match_proven=False,prediction_model_consumption_proven=False,independent_identity_lift_proven=False))
labels={
 'al_categories':'Axon officially disclosed identifier/history decision categories (C_id)',
 'al_cross':'AppLovin official cross-app/device collection and combination scope',
 'al_graph':'Unknown AppLovin resolved person graph output',
 'al_model':'Unknown resolved graph -> Axon value feature consumption (C_graph)',
 'upa':'Unity organization account/project link contracts',
 'lr_match':'LiveRamp match/derived return and quality metadata contracts',
 'lr_namespace':'Person/household partner encoding and direction-specific translation',
 'lr_lifecycle':'Envelope expiration,opt-out and subnetwork failure rules',
 'exchange':'Unity Exchange official US/Canada RampID availability',
 'vector_graph':'Unknown resolved identity -> Vector feature consumption',
 'vector_cohort':'Vector officially disclosed cross-game/cohort decision use',
 'causal_lift':'Unknown identity-only real prediction/acquisition/profit increment (D)',
 'aggregate':'Aggregate/shared-parameter alternative not ruled out',
 'trial':'M4 vs M3 real-data experiment design;all STOP',
 'privacy':'Purpose/identifier-scoped privacy rights;not verified model deletion',
 'correction':'Old navigation citations and unreliable search coverage explicitly bounded',
}
nodes=[dict(id='IV74N_'+k,label=v,stage='unknown' if k in ['al_graph','al_model','vector_graph','causal_lift'] else 'public_contract_or_design',contains_personal_values=False) for k,v in labels.items()]
edges=[]
def edge(a,b,claim,ids,status='official_contract_or_disclosure',grades=(),missing=''):
 edges.append(dict(id=f'IV74E{len(edges)+1:02}',source='IV74N_'+a,target='IV74N_'+b,claim=claim,source_ids=ids,
  status=status,evidence_stages=list(grades),evidence_level='UNKNOWN' if status=='unknown' else 'Official claim/contract or independent design;not observed production',
  reviewed_utc=now,permission_conditions='Source-specific consent,purpose,namespace and receiver authorization;no real identity data obtained',
  production_match_proven=False,prediction_model_consumption_proven=False,independent_identity_lift_proven=False,
  target_platform_actual_receipt_proven=False,missing_evidence=missing or 'Authorized platform-specific receipts,feature lineage and controlled identity-only effect',
  six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,production_successful_send=False,server_received=False,server_model_training=False)))
edge('al_cross','al_categories','Official cross-property collection/personalization scope and explicit Axon ID/history factors;C_id supported at disclosure level',['IV74S07','IV74S09','CGS51'],grades=['E3'])
edge('al_cross','al_graph','Collection and combination do not reveal person/device/household entity resolution contract',['IV74S07'],status='unknown')
edge('al_graph','al_model','No resolved key -> timed physical Axon feature/model-version consumption trace',['IV74S09','CGS51'],status='unknown')
edge('al_categories','al_model','Identifier category use cannot establish specific graph-derived feature use',['IV74S09'],status='unknown')
edge('upa','vector_graph','First-party account link does not establish UPA -> Ads/Vector mapping',['IG72S02','IG72S03'],status='unknown')
edge('lr_match','lr_namespace','Public return status and partner translation contracts;not a Unity-specific invocation path',['IV74S01','IV74S02','IV74S05','IV74S06'],grades=['E4'])
edge('lr_namespace','lr_lifecycle','Envelope decryption has permission/expiration/opt-out limits;30 days applies to envelope,not every identity',['IV74S03','IV74S04'],grades=['E4'])
edge('lr_namespace','exchange','Unity officially supports RampID activation;generic API details do not establish which Unity interfaces or granularity are used',['IG72S05','IV74S02'],grades=['E3','E4'])
edge('exchange','vector_graph','Exchange receiver availability is not Vector-specific actual receipt or model input proof',['IG72S05'],status='unknown')
edge('vector_cohort','vector_graph','Cross-game/cohort data-use categories cannot identify personal resolved-history representation',['MA60S17'],status='unknown')
edge('al_model','causal_lift','No real fixed-data identity feature ablation or causal acquisition outcome',['IV74R01','IV74R02'],status='unknown')
edge('vector_graph','causal_lift','No real graph-vs-aggregate/shared-parameter effect measurement',['IV74R01','IV74R02'],status='unknown')
edge('aggregate','vector_cohort','Official cross-game/cohort disclosure remains compatible with aggregate/shared parameters',['MA60S17'],grades=['E3'])
edge('aggregate','al_categories','Personal history is not identified as necessary by current official model categories',['CGS51','IV74S09'],status='architectural_alternative_not_ruled_out')
edge('trial','causal_lift','M4-M3 proposed with same effective supervised data,feature time,capacity budget and decision policy;not run',['IV74R01','IV74R03'],status='design_only_STOP')
edge('lr_match','trial','Derived return and cascade confidence cannot be treated as accurate personal-link ground truth',['IV74S01','IV74S05','IV74R01'],status='contract_constrains_design',grades=['E4'])
edge('privacy','al_graph','Identifier-linked rights/typical retention do not prove graph or feature deletion propagation',['IV74S08','IV74S10'],status='unknown')
edge('privacy','vector_graph','Unity contextual fallback and retention exceptions do not reveal Vector feature lifecycle',['IV74S12','IV74S13','IV74S14'],status='unknown')
edge('correction','al_cross','Correct legal-domain body supplements old navigation-only privacy citation;original old objects preserved',['IV74S07','IV74S08'],status='semantic_citation_correction',grades=['E3'])
for k,added in [('nodes',nodes),('edges',edges),('sources',sources)]:
 oldids={x['id'] for x in g[k]};assert not oldids&{x['id'] for x in added};g[k]+=added
g['identity_value_causality_round74']=dict(reviewed_utc=now,new_node_ids=[x['id'] for x in nodes],new_edge_ids=[x['id'] for x in edges],new_source_ids=[x['id'] for x in sources],
 baseline=dict(nodes=243,edges=293,sources=590),
 C_id='Official identifier/history category evidence exists;do not conflate with resolved graph',C_graph='UNKNOWN',D_identity_only_gain='UNKNOWN',
 actual_platform_graph_receipt='UNKNOWN',real_model_training=False,
 independent_73_results='Synthetic only;not real lift or vendor implementation',
 corrections_path='identity-value74/CORRECTIONS.md',search_coverage_path='identity-value74/SEARCH_COVERAGE.json',validation_path='identity-value74/VALIDATION.json')
ids={x['id'] for x in g['nodes']};sids={x['id'] for x in g['sources']}
assert all(e['source'] in ids and e['target'] in ids and set(e['source_ids'])<=sids for e in edges)
save(R/'prediction-system/EVIDENCE_GRAPH.json',g)
files=sorted(R.glob('74_*'));assert len(files)==5
section=['','','## 74号：身份图谱是否驱动买量优势（2026-11-20）','',
 '结论：第三方解析/命名空间/失败契约有新增补证；Unity账号/Exchange合作与AppLovin跨App用途和C_id类别披露有证。特定解析结果入Axon/Vector的C_graph和独立增益D仍UNKNOWN。没有新训练或真实收益。','',
 '| 交付 | 内容 |','|---|---|']
for p in files:section.append(f'| [{p.name}]({p.name}) | '+('18项A/B/C_id/C_graph/D证据矩阵' if p.suffix=='.csv' else '本轮结论、方法或停止条件')+' |')
section+=['','[一手来源及SHA256](identity-value74/SOURCE_CATALOG.md)；[覆盖与失败](identity-value74/SEARCH_COVERAGE.json)；[补充勘误](identity-value74/CORRECTIONS.md)；[准入STOP](identity-value74/EXPERIMENT_READINESS.json)；[验证](identity-value74/VALIDATION.json)。','',
 f'仅追加{len(nodes)}节点/{len(edges)}边/{len(sources)}来源，原243/293/590对象及旧元数据保留。00—73共129份编号文件保持原字节。未重扫SDK、重试数据下载、采集身份或调用生产匹配/广告服务。','']
(R/'EVIDENCE_INDEX.md').write_bytes((D/'EVIDENCE_INDEX.before.md').read_bytes()+'\n'.join(section).encode('utf-8'))
print(json.dumps(dict(deliverables=len(files),nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources'])),indent=2))
