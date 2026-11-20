"""Maintain distinct A/B/C/D and train/bid roles, with historical objects intact."""
from pathlib import Path
import copy,datetime,hashlib,json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
g=load(R/'prediction-system/EVIDENCE_GRAPH.json');old=load(O/'EVIDENCE_GRAPH.before.json')
assert g==old,'Concurrent graph changes; reconcile instead of overwriting.'
ss=load(O/'SOURCE_EVIDENCE.json');smap={s['id']:s for s in g['sources']+ss}
assert len(smap)==len(g['sources'])+len(ss)
g['sources'].extend(copy.deepcopy(ss))
nodes=[]
for co,prefix in [('AppLovin','A'),('Unity','U')]:
    for m,lab in [('A','same advertiser-app organic/cross-channel history'),('B','cross-game aggregate cohort/prior hypothesis'),
                  ('C','non-personal shared parameters/representations hypothesis'),('D','permitted personal cross-game history hypothesis')]:
        node=dict(id=f'CT_{prefix}_{m}',company=co,label=lab,stage='cold_start_'+m,
          hypothesis_only=m in ['B','C','D'],mechanism=m)
        if prefix=='U' and m=='B':node['hypothesis_only']=False;node['scope']='aggregate-insight purpose officially stated; exact implementation unknown'
        nodes.append(node)
g['nodes'].extend(nodes)
edges=[]
def add(n,a,b,claim,ids,status,mechanism,stage,missing,supp=(),negative=False):
    levels={'official':'【官方公开证实】','unknown':'【无法确认】','inference':'【合理推断】'}
    refs=[smap[i] for i in ids]
    edges.append(dict(id=f'CT62E{n:02d}',source=a,target=b,claim=claim,source_ids=ids,status=status,evidence_level=levels[status],
      mechanism=mechanism,training_or_bidding_stage=stage,edge_type='exclusion_or_gating' if negative else 'scoped_data_or_purpose',
      data_provider=a,data_receiver=b,diagram_style='solid' if status=='official' else 'dashed',
      explicit_call_chain='Public disclosure or documented interface scope only; no recovered production train/serve call chain',
      permission_conditions='Valid source/purpose authorization and platform privacy gating; event/available/aggregate/model deployment must predate bid',
      applies_to='standalone public product/data-use contract or explicitly bounded hypothesis; not target-game enablement',
      missing_evidence=missing,supplements_original_edges=list(supp),reviewed_utc=NOW,
      class_method_lines=[dict(path=s['path'],start_line=s['start_line'],end_line=s['end_line'],url=s.get('url')) for s in refs],
      sha256=[dict(path=s['path'],sha256=s['sha256']) for s in refs],
      six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,
        production_successful_send=False,server_received=False,server_model_training=False),
      production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
      production_evidence='No identifiers/SDK execution/production advertising requests; official assertions separated from independently observed implementation'))

add(1,'A_mmp','CT_A_A','Axon partner all-source option admits same advertiser-app data from other attribution sources; does not imply cross-game identity',
 ['CT62S08','MA60S03'],'official','A','authorized data supply',
 'Actual advertiser switches/mapping, delivery, canonical samples and learning gain unknown',('CGE14','CGE15'))
add(2,'CT_A_A','A_predict','Axon data categories permit voluntary advertiser data, but target-app sample-to-training consumption and cold-start effect remain unproven',
 ['CT62S07','CT62S08'],'unknown','A','training sample consumption',
 'Need authorized source-to-dataset/label lineage and new-campaign experiment',('CGE19','A10'))
add(3,'U_mmp','CT_U_A','Unity unattributed includes other-network and organic installs for the same target app',
 ['CT62S06','CT62S04'],'official','A','data source scope',
 'Do not equate the MMP source category with cross-game personal history; real switches and delivery unknown',('CGE09','CGE10'))
add(4,'CT_U_A','U_predict','Unity explicitly recommends prelaunch SDK/corresponding unattributed data for training, distinct from exit learning thresholds',
 ['CT62S04','CT62S05'],'official','A','training purpose',
 'Per-field dataset, source weights, deployed model and incremental effect unknown; not zero-data guarantee',('MA60E09','CGE08'))
add(5,'CT_U_B','U_bid','Vector product article explicitly claims cross-game patterns and aggregate cohort insights distinguish player types at bid decision',
 ['CT62S02'],'official','B','bid-time aggregate purpose',
 'Formation/aggregation/similar-game schema, time freshness, parameter-sharing or personal-history contributions unknown',('MA60E07','MA60E10'))
add(6,'U_context','CT_U_B','No production mapping recovered from source-game data to exact cohort/prior tables or features',
 ['CT62S01','CT62S02'],'unknown','B','training/aggregation',
 'Need official aggregation schema, provenance, access/purpose and temporal versioning',('U04','MA60E10'))
add(7,'CT_U_C','U_predict','Vector shared non-personal parameters/transfer learning remain a viable but unproven implementation',
 ['CT62S02','MA60S19','MA60S21'],'unknown','C','training parameter sharing and deployment',
 'Need production model shared layers/conditions and leave-game-out ablation; recruitment not deployment proof',('MA60E10','U04'))
add(8,'CT_U_D','U_bid','Vector legal personal cross-game history consumption at bid time is not established by co-packaged IDs or broad cross-game claims',
 ['CT62S02','CT62S10'],'unknown','D','bid-time personal feature join',
 'Need authorized identity scope/join/time/feature-consumption and gated fallback, not raw personal IDs',('U04','U17'))
add(9,'CT_A_B','A_predict','Axon system-level additional advertiser data/improvement statement does not identify cross-game aggregate-prior implementation',
 ['CT62S07','CT62S09'],'unknown','B','aggregate transfer',
 'Need exact cohort/prior production contract, source scope and cold-start ablation',('MA60E05','A03'))
add(10,'CT_A_C','A_predict','Axon cross-game parameter sharing is not proven by continuous learning, user-representation jobs or future cross-category benefit',
 ['CT62S07','CT62S09','MA60S06','MA60S07'],'unknown','C','training parameter sharing and deployment',
 'Need named production shared model/layers and source-target mapping or controlled transfer experiment',('MA60E06','A04'))
add(11,'CT_A_D','A_bid','Axon personal cross-game history as a specific bid-time feature remains unknown despite allowed general engagement-data descriptions',
 ['CT62S07','MA60S02'],'unknown','D','bid-time personal feature join',
 'Need authorized field-level join, valid purpose and as-of snapshot, actual consumption and no-ID policy',('A03','A10'))
add(12,'CT_U_A','U_predict','Direct ROAS onboarding removes prerequisite Install campaign, not data readiness or Learning requirements',
 ['CT62S03','CT62S05'],'official','A','onboarding/learning boundary',
 'Cannot infer zero-history new app receives accurate LTV model immediately; initial model and B/C/D contributions unknown',('MA60E09','RV61E06'))
add(13,'A_context','A_predict','Cached Axon official statement describes allowed engagement/voluntary data and improvement with additional advertiser data; exact transfer type unspecified',
 ['CT62S07'],'official','A/B/C/D not uniquely identified','general training purpose',
 'Fresh public GET403; cached statement does not distinguish aggregate statistics, shared parameters, personal history or independent models',('MA60E03','MA60E05'))
add(14,'A_review','CT_A_D','Official Ad Review exclusion rules out treating its other-network user outputs as Axon personal-history training source',
 ['CT62S11','MA60S02'],'official','D source exclusion','source/purpose exclusion',
 'Excludes this source/path only, not every permitted B/C/D implementation',('MA60E14','A18'),negative=True)
add(15,'U_runtime','CT_U_D','Unity Developer Data ads intent gating prevents assuming unrestricted default use of personal advertising histories',
 ['CT62S10'],'official','D gating','data use authorization',
 'Framework-specific gate; not proof all SDKs share same collection gate, no alternate legal linkage, or all D absent',('XU07','C53E13'),negative=True)
add(16,'CT_U_B','CT_U_C','Aggregate statistics and non-personal parameter transfer need not use cross-app individual lookup; theoretical independence, not deployed Unity path',
 ['CT62S02','CT62S10'],'inference','B/C without D','conceptual independence only',
 'No implementation edge asserted; both may work without D but actual production weights/benefit unknown',('MA60E10',))

nodeids={n['id'] for n in g['nodes']};edgeids={e['id'] for e in g['edges']}
for e in edges:
    assert e['source'] in nodeids and e['target'] in nodeids,e['id']
    assert set(e['supplements_original_edges'])<=edgeids,e['id']
g['edges'].extend(edges);g['reviewed_utc']=NOW
g['cross_game_cold_start_round62']=dict(reviewed_utc=NOW,new_sources=len(ss),new_nodes=len(nodes),new_edges=len(edges),
  rule='A same-app cross-source; B aggregate prior; C non-personal shared parameters; D personal cross-game history. No substitutions.',
  temporal_rule='training/aggregation/model deployment/feature availability and use authorization must precede the evaluated bid',
  public_search_stop='Linked primary sources did not distinguish B/C/D production implementations; stop repeated broad searches pending concrete new material',
  before='model-architecture/round62/EVIDENCE_GRAPH.before.json',production_impl_or_causal_gain_proven=False)
save(R/'prediction-system/EVIDENCE_GRAPH.json',g);save(O/'EVIDENCE_GRAPH.after.json',g);save(O/'NEW_EDGES.json',edges)

trace=load(O/'AUTHOR_TRACE.json');trace['new_followups']=load(O/'FETCHES.json')
trace['followup_assessment']=[
 dict(source='original D7/D28 article',result='Daniel Godley, content marketing; no author profile/research/GDC/model reference observed',role='official product assertion, not implementation paper'),
 dict(source='linked uads-march-updates',result='Danielle Shevchuk, product marketing; direct ROAS + data enablement + Learning gates; no B/C/D structure',role='new cold-start boundary evidence'),
 dict(source='Vector product',result='ecosystem/matching and MMP best practices; no specific shared layers/cohort schema/personal join',role='scope confirmation only'),
 dict(source='Unity attribution docs',result='unattributed scope explicitly same target App outside Unity acquisition',role='source classification contra identity conflation'),
 dict(source='Axon official legal refresh',result='HTTP403; no retry/bypass; prior hashed cached official copy reused',role='retrieval limitation, not negative model evidence')]
trace['stop_decision']='Stop repeated public-architecture broad searches; resume only with a specific vendor production paper/talk/schema/authorized ablation.'
trace['not_searched_or_claimed']='No exhaustive claim that talks/papers do not exist; no private backend/identity/production-ad access.'
save(O/'TRACE_LEDGER.json',trace)

idx=R/'EVIDENCE_INDEX.md';assert idx.read_bytes()==(O/'EVIDENCE_INDEX.before.md').read_bytes()
with idx.open('a',encoding='utf-8') as f:
    f.write('\n\n<a id="ct62"></a>\n\n## CT62 · 跨游戏知识迁移与冷启动（62号）\n\n')
    f.write('- [62号报告与四机制矩阵/训练竞价分离图](62_跨游戏知识迁移与冷启动机制.md)\n')
    for name in ['SOURCE_CATALOG.md','SOURCE_EVIDENCE.json','AUTHOR_TRACE.json','TRACE_LEDGER.json','FOUR_MECHANISMS.csv','FOUR_MECHANISMS.json','NEW_EDGES.json','VALIDATION.json']:
        f.write(f'- [{name}](model-architecture/round62/{name})\n')
    f.write('- [CLAIM_MATRIX](model-architecture/CLAIM_MATRIX.csv) / [原44行快照](model-architecture/round62/CLAIM_MATRIX.before.csv)\n')
    f.write('- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [更新前快照](model-architecture/round62/EVIDENCE_GRAPH.before.json)\n\n')
    f.write('最强路径：两家A（同目标App全来源样本），Vector另有B聚合cohort的bid-time用途披露。C共享参数与D个人历史未唯一识别；A/B/C理论上不必D，但训练用途/隐私条件仍需满足。沿原文作者和相关链接未得新生产模型材料，建议停止重复广搜。\n\n')
    for s in ss:
        f.write(f'<a id="{s["id"].lower()}"></a>\n\n- **{s["id"]}** [{s["company"]}/{s["product"]}](model-architecture/round62/SOURCE_CATALOG.md#{s["id"].lower()})；{s["evidence_level"]}；{s["path"]}:L{s["start_line"]}；范围及反证见目录。\n\n')

manifest=R/'EVIDENCE_MANIFEST.json';m=load(manifest);assert m==load(O/'EVIDENCE_MANIFEST.before.json')
paths=[R/'62_跨游戏知识迁移与冷启动机制.md',R/'model-architecture/CLAIM_MATRIX.csv']+[p for p in O.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
m['entries'].append(dict(id='CT62',title='62号跨游戏知识迁移与冷启动机制',
  notes='A/B/C/D and train/bid phases distinguished; no specific C/D deployment or causal cold-start advantage claimed',
  sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sorted(paths)]))
m['cross_game_round62_utc']=NOW;save(manifest,m)
print('Graph/index extended:',len(nodes),'nodes,',len(edges),'edges,',len(ss),'sources. No historical objects changed.')
