"""Append exact contract/boundary evidence, never upgrade production observations."""
from pathlib import Path
import copy,datetime,hashlib,json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
g=load(R/'prediction-system/EVIDENCE_GRAPH.json');old=load(O/'EVIDENCE_GRAPH.before.json')
assert g==old,'Concurrent graph change; reconcile instead of overwriting.'
ss=load(O/'SOURCE_EVIDENCE.json');smap={s['id']:s for s in g['sources']+ss}
assert len(smap)==len(g['sources'])+len(ss)
g['sources'].extend(copy.deepcopy(ss))
nodes=[('RV_U_budget','Unity UA budget controls: billing-specific automated bids, 7-day pacing, country groups','Unity'),
 ('RV_A_budget_guidance','AppLovin global-budget and target-conversion operating recommendations','AppLovin'),
 ('RV_A_site_dedup','AppLovin website Pixel/site-to-site/SDK dedupe contract; not MMP IAA','AppLovin'),
 ('RV_Adjust_amount_guard','Adjust5.8.1 checkRevenue local negative-amount assignment guard','Adjust')]
for ident,label,company in nodes:
    g['nodes'].append(dict(id=ident,label=label,company=company,stage='revenue_bid_contract'))
edges=[]
def add(n,a,b,claim,refs,status,scope,missing,supp=(),chain='',conditions='Applicable partner setup, consent, identity availability and product/billing scope; no production test'):
    lev={'official':'【官方公开证实】','sdk':'【SDK代码证实】','unknown':'【无法确认】'}[status]
    rs=[smap[x] for x in refs]
    edges.append(dict(id=f'RV61E{n:02d}',source=a,target=b,claim=claim,status=status,evidence_level=lev,
      source_ids=refs,data_provider=a,data_receiver=b,applies_to=scope,
      explicit_call_chain=chain or 'Public product/integration contract only; no production server call chain recovered',
      permission_conditions=conditions,missing_evidence=missing,supplements_original_edges=list(supp),
      diagram_style='dashed' if status=='unknown' else 'solid',reviewed_utc=NOW,
      modality='documented operating recommendation' if n==7 else ('SDK-local validation' if status=='sdk' else 'documented contract or stated unknown'),
      class_method_lines=[dict(path=s['path'],start_line=s['start_line'],end_line=s['end_line'],url=s.get('url'),
        method=s.get('class_or_method',s.get('product'))) for s in rs],
      sha256=[dict(path=s['path'],sha256=s['sha256'],official_packages=s.get('official_packages',[])) for s in rs],
      six_layers=dict(sdk_capability=status=='sdk',actual_game_business_callsite=False,request_construction_code=False,
        production_successful_send=False,server_received=False,server_model_training=False),
      production_actual_proven=False,observed_target_game_delivery=False,independent_production_audit=False,
      production_evidence='No production requests/events or real identifiers; source statement not independent delivery/training observation'))

add(1,'U_revenue','CG_U_receiver',
 'Unity formal post-install contract separately defines purchase, ad_revenue, session and level_complete and describes their model/goal uses',
 ['RV61S01'],'official','Unity Ads UA MMP contract; raw behavior is not real revenue',
 'Actual delivery, canonical label generation and field-specific feature/label consumption unknown',('U05','U07'))
add(2,'M_af','CG_U_receiver',
 'Unity explicitly requires dedicated IAA mapping except the documented Singular combined-event configuration; wrong purchase mapping can break optimization',
 ['RV61S03','RV61S04'],'official','Partner-specific mapping; Singular exception not generalized',
 'Target-game switches and server label schema still unknown',('CGE09','CGE10'))
add(3,'CG_U_receiver','U_labels',
 'Public data-loss/no-retroactive-send warning constrains backfill claims, but zero labels/refunds/dedup/late-watermark construction remains undisclosed',
 ['RV61S02','MA60S15'],'unknown','Missing-event limitation is not a training-data or maturity implementation',
 'Canonical install universe, complete/zero versus missing, revenue revision/FX/refund/watermarks and sampled negatives',('CGE20','U07'))
add(4,'RV_U_budget','U_bid',
 'Official Unity docs state CPI-billed ROAS campaigns automatically use Automated bidding with day adjustments and week-level budget control',
 ['RV61S07','RV61S09'],'official','Unity ROAS+CPI billing; not an independently observed Vector model implementation',
 'Per-bid pacing factors/controller coefficients and all other billing-mode behavior unknown',('MA60E12','U10','U11'))
add(5,'RV_U_budget','U_exchange',
 'Unity budget contract exposes real-time spend allocation within country groups and Daily/Geo Capped delivery states',
 ['RV61S05','RV61S06','RV61S09'],'official','UA delivery/budget product behavior, not server exchange prediction source',
 'Exact eligibility gating, per-opportunity prices and marginal allocation algorithm unknown',('MA60E12',))
add(6,'RV_U_budget','U_bid',
 'Unity publicly acknowledges campaign/creative exploration and recommends exploration funding; ROAS goals configured by country',
 ['RV61S08','RV61S10'],'official','Operating recommendations/setup; 5x budget not a training threshold',
 'Exploration algorithm/rate, uncertainty use, new-game/no-ID fallback unknown',('MA60E09','MA60E12'))
add(7,'RV_A_budget_guidance','A_bid',
 'AppLovin recommends meaningful conversion volume (15-20 daily), realistic profitability goals and single global budget across countries',
 ['RV61S12'],'official','Operational recommendation, not disclosed Axon pacing or training minimum',
 'Actual pacing/constraint implementation, risk adjustment and target-game settings unknown',('MA60E02','A17'))
add(8,'A_web','RV_A_site_dedup',
 'AppLovin website cross-Pixel/site-to-site/SDK same-event dedupe_id contract merges within30s and drops later duplicate after5min',
 ['RV61S13'],'official','Website multi-route conversion contract only; not generalized to IAA or MMP',
 '30sec-5min behavior, event-time versus arrival-time nuance, refunds and model training dedup remain unknown',('A15','A16'))
add(9,'M_adjust','RV_Adjust_amount_guard',
 'Adjust5.8.1 checkRevenue rejects assignment of negative revenue and requires currency; zero is not rejected by this comparison',
 ['RV61S14'],'sdk','Official standalone API; no assertion target games use5.8.1',
 'Not proof whole event dropped, refund unsupported globally, zero-revenue labels ingested, or receipt/training',('CGE19','CGE20'),
 chain='AdjustEvent.setRevenue -> checkRevenue -> if false return without revenue/currency assignment',
 conditions='Developer must invoke API; local validation only; official source archive hash/member verified, never SDK executed')
add(10,'MA_A_value_distribution','A_bid',
 'Axon multi-day value distribution wording does not establish per-user conditional distribution/quantile or variance/risk-sensitive bid consumption',
 ['MA60S01','MA60S02','RV61S12'],'unknown','Scalar/multistage/distribution/risk hypotheses may coexist',
 'Serving output random-variable/condition/window schema, loss/calibration and policy consumption/ablation',('MA60E01','MA60E02'))
add(11,'U_predict','U_bid',
 'Official CVR-CPI-eCPM relation and revenue dynamic bidding do not establish separate pInstall and conditional-LTV heads or actual bid formula',
 ['RV61S11','MA60S13','MA60S16'],'unknown','Public decision relationship versus internal parameterization kept separate',
 'Per-opportunity score schema, conversion conditions, uncertainty, fees, policy and production latency mapping',('MA60E08','MA60E11'))
add(12,'A_bid','A_exchange',
 'MAX public unified first-price auction consumes valid bids, merges waterfall and bills after render; this is not Axon valuation/shading implementation',
 ['RV61S15'],'official','Supply-side protocol only; not all Axon traffic guaranteed same route',
 'Axon private value-to-quote function, shading/pacing, fee/net adjustments and risk use unknown',('A17',))
add(13,'U_bid','U_exchange',
 'Unity Exchange public tmax depends on waterfall seat or mediation with processing deduction; no derived Vector model serving SLA',
 ['RV61S16','MA60S18','MA60S20'],'official','Exchange deadline actual contract, model-engineering links remain indirect',
 'Vector feature-fetch/inference P99, per-stage timeout/fallback and deployed shading algorithm unknown',('MA60E11','MA60E12'))

nodeids={n['id'] for n in g['nodes']};oldedges={e['id'] for e in g['edges']}
for e in edges:
    assert e['source'] in nodeids and e['target'] in nodeids,e['id']
    assert all(x in oldedges for x in e['supplements_original_edges']),e['id']
g['edges'].extend(edges);g['reviewed_utc']=NOW
g['revenue_bid_round61_63']=dict(reviewed_utc=NOW,new_sources=len(ss),new_nodes=len(nodes),new_edges=len(edges),
  scope='61/63 revenue distribution and budget contracts, not production model architecture recovery',
  before='model-architecture/round61-63/EVIDENCE_GRAPH.before.json',
  hypothesis_rule='A1-A4 and V1-V4 may coexist; distribution words and recruitment do not uniquely identify architecture',
  actual_game_delivery_or_training_proven=False)
save(R/'prediction-system/EVIDENCE_GRAPH.json',g);save(O/'EVIDENCE_GRAPH.after.json',g);save(O/'NEW_EDGES.json',edges)

idx=R/'EVIDENCE_INDEX.md'
assert idx.read_bytes()==(O/'EVIDENCE_INDEX.before.md').read_bytes()
with idx.open('a',encoding='utf-8') as f:
    f.write('\n\n<a id="rv61"></a>\n\n## RV61 · 61＋63收入分布与价值出价专项\n\n')
    f.write('- [61号收入标签与价值分布预测](61_收入标签与价值分布预测.md)\n')
    f.write('- [63号预测价值到实时竞价与预算约束](63_预测价值到实时竞价与预算约束.md)\n')
    for name in ['SOURCE_CATALOG.md','SOURCE_EVIDENCE.json','COMPETING_HYPOTHESES.md','ACQUISITION_LEDGER.json','NEW_EDGES.json','MATH_EXAMPLES.json','VALIDATION.json']:
        f.write(f'- [{name}](model-architecture/round61-63/{name})\n')
    f.write('- [更新后CLAIM_MATRIX](model-architecture/CLAIM_MATRIX.csv) / [原28行快照](model-architecture/round61-63/CLAIM_MATRIX.before.csv)\n')
    f.write('- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [更新前快照](model-architecture/round61-63/EVIDENCE_GRAPH.before.json)\n\n')
    f.write('新增正式数据/预算约束，不是新增生产网络结构：Unity CPI计费ROAS自动竞价、7日滚动预算/国家组分配和探索；Unity丢失事件不追溯补发警告；AppLovin网站去重时段与手游MMP边界。Axon条件分布/风险出价、Vector标签与共享表示仍未知。\n\n')
    for s in ss:
        f.write(f'<a id="{s["id"].lower()}"></a>\n\n- **{s["id"]}** [{s["company"]}/{s["product"]}](model-architecture/round61-63/SOURCE_CATALOG.md#{s["id"].lower()})；{s["evidence_level"]}；{s["path"]}:L{s["start_line"]}。\n\n')

manifest=R/'EVIDENCE_MANIFEST.json';m=load(manifest)
assert m==load(O/'EVIDENCE_MANIFEST.before.json')
paths=[R/'61_收入标签与价值分布预测.md',R/'63_预测价值到实时竞价与预算约束.md',R/'model-architecture/CLAIM_MATRIX.csv']
paths += [p for p in O.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
m['entries'].append(dict(id='RV61',title='61＋63真实收入/价值分布/动态竞价预算约束',
  notes='16 exact claims, 13 graph edges; no recovered production model, no target-game delivery/training or causal performance proof',
  sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sorted(paths)]))
m['revenue_bid_round61_63_utc']=NOW;save(manifest,m)
print('Preserved old graph, appended',len(nodes),'nodes,',len(edges),'edges,',len(ss),'sources; index updated.')
