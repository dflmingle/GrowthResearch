"""Append architecture disclosure evidence; preserve all prior evidence objects."""
from pathlib import Path
import copy,datetime,hashlib,json
R=Path(__file__).resolve().parent.parent;O=R/'model-architecture'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
old=load(O/'EVIDENCE_GRAPH.before60.json');g=load(R/'prediction-system/EVIDENCE_GRAPH.json')
assert old==g,'Graph changed since baseline; reconcile instead of overwrite.'
ss=load(O/'SOURCE_EVIDENCE.json');sm={s['id']:s for s in ss}
assert not ({s['id'] for s in g['sources']} & set(sm))
g['sources'].extend(copy.deepcopy(ss))
newnodes=[
 ('MA_A_value_distribution','Axon2 official predicted multi-day expected-value distributions','AppLovin'),
 ('MA_A_advertiser_diversity','Additional advertiser-category data: forward-looking gaming benefit','AppLovin'),
 ('MA_U_crossgame_patterns','Vector claimed cross-game patterns and aggregate cohort insights at bid time','Unity'),
]
for ident,label,company in newnodes:g['nodes'].append(dict(id=ident,label=label,company=company,stage='architecture_disclosure'))
edges=[]
def edge(n,source,target,claim,ids,status,scope,modality,missing,supp=()):
    refs=[sm[i] for i in ids]
    level={'official':'【官方公开证实】','indirect':'【间接技术线索】','unknown':'【无法确认】'}[status]
    edges.append(dict(id=f'MA60E{n:02d}',source=source,target=target,claim=claim,source_ids=ids,
      status=status,evidence_level=level,applies_to=scope,modality=modality,
      data_provider=source,data_receiver=target,
      explicit_call_chain='Official disclosure/engineering clue only; no recovered production server call chain',
      permission_conditions='Applicable consent, advertiser sharing permission, identifier availability and product scope; no expanded authorization inferred',
      diagram_style='solid' if status=='official' and modality!='forward-looking' else 'dashed',
      missing_evidence=missing,supplements_original_edges=list(supp),reviewed_utc=NOW,
      class_method_lines=[dict(path=s['path'],start_line=s['start_line'],end_line=s['end_line'],url=s.get('url')) for s in refs],
      sha256=[dict(path=s['path'],sha256=s['sha256']) for s in refs],
      six_layers=dict(sdk_capability=False,actual_game_business_callsite=False,request_construction_code=False,
        production_successful_send=False,server_received=False,server_model_training=False),
      production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
      production_evidence='Vendor assertion or indirect public clue, NOT independently observed target-game delivery/training'))

edge(1,'A_predict','MA_A_value_distribution',
 'Axon2 official CEO article states current models predict expected value distributions many days into the future',
 ['MA60S01'],'official','Axon2; paragraph emphasizes valuation of non-game offers shown to game players',
 'vendor present-tense deployment assertion',
 'Distribution family, model heads/loss, window, calibration and per-game implementation unknown',('A04','A13'))
edge(2,'MA_A_value_distribution','A_bid',
 'Official multi-day value prediction described as supporting real-time capital allocation; each impression bidding uses advertiser return goals',
 ['MA60S01','MA60S04'],'official','Axon/AppLovin Ads product-level prediction-to-bidding purpose',
 'vendor present-tense product assertion',
 'No recovered pInstall/LTV decomposition, price equation, pacing, shading or uncertainty policy',('A13','A17'))
edge(3,'A_context','A_predict',
 'Axon official disclosure explicitly connects permitted device/network/engagement, own win-loss and advertiser-shared data to continual model training',
 ['MA60S02'],'official','Data categories only, excludes competitor bid/user data and sensitive/protected/children data',
 'vendor present-tense data-use assertion',
 'Per-feature lineage, joins, data cutoffs, training jobs and target-game implementation unknown',('A01','A06'))
edge(4,'A_web','A_predict',
 'Discovery product explicitly uses same historical purchase data as Prospecting to pursue new-visitor purchaser goal',
 ['MA60S05'],'official','Ecommerce Discovery/Prospecting ONLY; not a target-game IAA training connection',
 'official product launch/setup assertion',
 'Whether input is exclusion/feature/label or combination, matching details and gaming reuse unknown',('A15','A16'))
edge(5,'MA_A_advertiser_diversity','A_predict',
 'CEO says incremental data from broader advertiser set will improve outcomes for gaming partners',
 ['MA60S04'],'official','Cross-category benefit direction, NOT deployed per-row ecommerce-to-gaming training',
 'forward-looking',
 'Actual cross-business dataset use, consent/purpose, shared weights, label schema and measured effect not established',('A16',))
edge(6,'A_features','A_predict',
 'AppLovin ML job duties discuss user representations, ranking/retrieval and multitask research; data engineering job discusses training and feature serving',
 ['MA60S06','MA60S07'],'indirect','AppLovin advertising-platform research/infrastructure; not identified Axon model/version',
 'job research duties and skill requirements',
 'No named architecture, production graph, feature store implementation or target-game linkage',('A03','A04'))
edge(7,'MA_U_crossgame_patterns','U_bid',
 'Unity official IAP product article explicitly says cross-game behavioral patterns and aggregate cohort insights distinguish player types at moment of bid decision',
 ['MA60S17'],'official','Vector D7/D28 IAP product disclosure; not an individual identity-graph or embedding architecture claim',
 'vendor present-tense data-use assertion',
 'Exact features/time windows, aggregation, consent and identity dependency, model structure and incremental gain unknown',('U04','U13'))
edge(8,'U_labels','U_predict',
 'Unity official D28 release describes per-user 28-day ad revenue prediction and combined 28-day Hybrid revenue objective',
 ['MA60S13','MA60S16'],'official','IAA/IAP/Hybrid product targets/windows; label assembly remains unknown',
 'official product launch and present-tense prediction purpose',
 'Canonical labels, zero/negative cases, loss function, refunds, delay handling and target-game delivery unknown',('U07',))
edge(9,'CG_Allsource','U_predict',
 'Unity best practices explicitly say prelaunch SDK data and corresponding unattributed postbacks help train models, outside learning exit thresholds',
 ['MA60S14','MA60S15'],'official','Same advertiser app all-source data contract; not arbitrary cross-advertiser personal sharing',
 'explicit official training-purpose contract',
 'Actual game activation, history backfill, sampling weights, row-level label/feature use and ablation unknown',('CGE08','CGE11'))
edge(10,'U_context','MA_U_crossgame_patterns',
 'Vector product publicly claims holistic player/game intelligence and IAP/ad-behavior correlations; mechanism producing cross-game patterns is undisclosed',
 ['MA60S17','MA60S21'],'unknown','Public purposes cannot recover raw-data-to-representation mapping',
 'implementation breakpoint',
 'Shared parameters versus aggregate statistics versus person-level history and their actual upstream data sources',('U04',))
edge(11,'U_predict','U_bid',
 'Vector Gamer AI job describes online model inference powering ranking/bidding; model details not disclosed',
 ['MA60S18','MA60S19'],'indirect','Named Vector team duties; not independently verified system deployment',
 'job statement about engineering/production responsibility',
 'Actual deployed serving/model stack, feature joins, latency budget and SLA unknown; Triton only optional experience',('U10','U11'))
edge(12,'U_bid','U_exchange',
 'Vector Bidding Science job duties concern bidding/pacing and bid-landscape forecasting with offline and online experiments',
 ['MA60S20'],'indirect','Research/next-generation engineering scope, not proof RL or survival model is deployed',
 'job research duties and skills',
 'Production pacing, shading, exploration, market-price/uncertainty logic and economic experiments unknown',('U10','U11'))
edge(13,'U_purchase','U_predict',
 'Official keynote says IAP/D2C purchase data can enrich Vector; visible IAP gateway/native forwarding does not establish per-row training lineage',
 ['MA60S22','MA60S23','MA60S24'],'official','Product-purpose possibility bounded by consent and closed native/server interface',
 'can-help-enrich product statement, not per-event deployment',
 'Insights rows to training features/labels, runtime transport ACK, joins and purpose control remain unproven',('U09','C53E13'))
edge(14,'A_review','A_predict',
 'Official Ad Review statement excludes using Ad Review outputs to build profiles or feed Axon/other models',
 ['MA60S08','MA60S02'],'official','Explicit negative boundary; does not exclude authorized advertiser own revenue feedback',
 'official explicit data-use exclusion',
 'No license to infer other bidder data from mediation visibility; no target-game production audit',('A18','A19'))

nodeids={n['id'] for n in g['nodes']};edgeids={e['id'] for e in g['edges']}
for e in edges:
    assert e['source'] in nodeids and e['target'] in nodeids
    assert all(i in edgeids for i in e['supplements_original_edges']),e['id']
g['edges'].extend(edges);g['reviewed_utc']=NOW
g['model_architecture_round60']=dict(reviewed_utc=NOW,new_source_count=len(ss),new_edges=len(edges),new_nodes=len(newnodes),
  scope='First round60 only. Public disclosures vs indirect clues; no reports61-64 or production model experiments.',
  before='model-architecture/EVIDENCE_GRAPH.before60.json',
  priority=['61 canonical revenue labels','63 value to bid constraints','62 cross-game representation mechanism','64 target-game attribution and causal effects'],
  observation_rule='Vendor statements recorded separately from six production observation layers; all new production flags false')
save(R/'prediction-system/EVIDENCE_GRAPH.json',g);save(O/'EVIDENCE_GRAPH.after60.json',g);save(O/'NEW_EDGES.json',edges)

idx=R/'EVIDENCE_INDEX.md'
with idx.open('a',encoding='utf-8') as f:
    f.write('\n\n<a id="ma60"></a>\n\n## MA60 · 模型架构公开证据第一轮（60）\n\n')
    f.write('- [60号主报告](60_Axon_Vector模型架构公开证据.md)：两家各五组证据、生产架构边界及61—64调查优先级。\n')
    for name in ['SOURCE_CATALOG.md','CLAIM_MATRIX.csv','ARCHITECTURE_HYPOTHESES.md','CONTRADICTIONS.md','EVIDENCE_GAPS.md','SOURCE_EVIDENCE.json','PATENT_RECORDS.json','ACQUISITION_LEDGER.json','VALIDATION.json']:
        f.write(f'- [{name}](model-architecture/{name})\n')
    f.write('- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [旧图快照](model-architecture/EVIDENCE_GRAPH.before60.json) / [新增边](model-architecture/NEW_EDGES.json)\n\n')
    f.write('新增重点：Axon2未来多日价值分布与实时资本配置的官方陈述；Vector跨游戏行为模式/聚合cohort用于bid decision的官方陈述。两者均非生产网络/损失函数恢复；跨业务受益的前瞻声明不升级为部署。61—64本轮未制作。\n\n')
    for s in ss:
        f.write(f'<a id="{s["id"].lower()}"></a>\n\n- **{s["id"]}** [{s["company"]} / {s["product"]}](model-architecture/SOURCE_CATALOG.md#{s["id"].lower()})；{s["evidence_level"]}；{s["path"]}:L{s["start_line"]}；日期/原文/哈希/部署措辞见目录。\n\n')

manifest=load(R/'EVIDENCE_MANIFEST.json')
paths=[R/'60_Axon_Vector模型架构公开证据.md']+[p for p in O.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
manifest['entries'].append(dict(id='MA60',title='Axon/Vector模型架构公开证据第一轮',
  notes='28 claims, explicit vendor deployment wording separated from observed production; no61-64 final conclusions',
  sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sorted(paths)]))
manifest['model_architecture_round60_utc']=NOW;save(R/'EVIDENCE_MANIFEST.json',manifest)
print('Appended graph:',len(newnodes),'nodes,',len(edges),'edges,',len(ss),'sources. Historical objects retained.')
