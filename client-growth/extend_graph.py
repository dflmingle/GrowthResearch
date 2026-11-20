"""Append evidence without promoting static capabilities to production facts."""
from pathlib import Path
import copy, datetime, hashlib, json

R = Path(__file__).resolve().parent.parent
O = R / 'client-growth'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

path = R / 'prediction-system/EVIDENCE_GRAPH.json'
before = load(O/'EVIDENCE_GRAPH.before_client56.json')
g = load(path)
assert g == before, 'Concurrent or previous extension detected; review instead of overwriting.'
ss = load(O/'SOURCE_EVIDENCE.json')

# Add only two reused official public documents. No downloads or SDK execution.
extra = [
 ('CGS54','axon/gaming-apps.txt',18,80,'AppLovin gaming ROAS and MAX prerequisites',
  'https://www.applovin.com/en/gaming-apps'),
 ('CGS55','axon/doc-tracking-url-macros.txt',14,106,'AppLovin click/impression device and request tracking macros',
  'https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/tracking-url-macros'),
]
for ident, rel, start, end, title, url in extra:
    p = R/rel; lines = p.read_text(encoding='utf-8-sig').splitlines()
    ss.append(dict(id=ident,product=title,path=rel,sha256=sha(p),start_line=start,
      end_line=min(end,len(lines)),url=url,source_date='publication date not stated; local official snapshot reused 2026-11-19',
      reviewed_utc=NOW,evidence_level='【官方公开证实】',evidence_priority='A',
      excerpt='\n'.join(f'{i}: {lines[i-1]}' for i in range(start,min(end,len(lines))+1)),
      scope='public integration contract, not target-game activation or observed delivery',
      production_delivery=False,server_received=False,model_training_proven=False))

source_map = {s['id']:s for s in g['sources']+ss}
assert len(source_map)==len(g['sources'])+len(ss)
g['sources'].extend(copy.deepcopy(ss))
save(O/'SOURCE_EVIDENCE.complete.json',ss)

catalog = (O/'SOURCE_CATALOG.md').read_text(encoding='utf-8')
catalog = catalog.split('\n<a id="cgs54"></a>')[0]
for s in ss[-2:]:
    catalog += f'\n<a id="{s["id"].lower()}"></a>\n## {s["id"]} · {s["product"]}\n\n'
    catalog += f'[{s["path"]}:L{s["start_line"]}](../{s["path"]})\n\n'
    catalog += f'{s["evidence_level"]}；文件SHA256 `{s["sha256"]}`。\n\n[官方原文]({s["url"]})；{s["source_date"]}。\n'
(O/'SOURCE_CATALOG.md').write_text(catalog,encoding='utf-8')

nodes = [
 ('CG_U_history','Unity Ads process/session ad history','Unity'),
 ('CG_U_token','Unity Ads visible HeaderBiddingToken protobuf','Unity'),
 ('CG_U_pii','Unity Ads gated Pii including Analytics App Instance ID','Unity'),
 ('CG_U_gateway_config','Unity Ads gateway-returned AllowedPii and session state','Unity'),
 ('CG_MAX_collect','MAX per-provider signal collection and cache','AppLovin'),
 ('CG_MAX_request','MAX mediated POST request builder','AppLovin'),
 ('CG_MAX_history','MAX previous request/network and gated request counters','AppLovin'),
 ('CG_LP_collect','LevelPlay9.5 concurrent provider bidding data collector','Unity'),
 ('CG_LP_map','LevelPlay provider-instance bidding map','Unity'),
 ('CG_Allsource','Advertiser-authorized same-app all-source MMP data','both'),
 ('CG_U_receiver','Unity partner postback receiving contract','Unity'),
 ('CG_A_receiver','AppLovin partner postback receiving contract','AppLovin'),
 ('CG_MAX_queue','MAX EventService dispatch/postback queue','AppLovin'),
 ('CG_Game_value','Target-game specific behavior and proxy value','target games'),
]
for ident,label,company in nodes:
    assert not any(n['id']==ident for n in g['nodes'])
    g['nodes'].append(dict(id=ident,label=label,company=company,stage='client_growth_lineage'))

edges=[]
def edge(num,source,target,claim,status,ids,chain,conditions,missing,supplements=(),construction=False,business=False):
    refs=[source_map[i] for i in ids]
    levels={'sdk':'【SDK代码证实】','official':'【官方公开证实】','unknown':'【无法确认】','inference':'【合理推断】'}
    row=dict(id=f'CGE{num:02d}',source=source,target=target,claim=claim,status=status,evidence_level=levels[status],
      source_ids=ids,data_provider=source,data_receiver=target,explicit_call_chain=chain,
      permission_conditions=conditions,missing_evidence=missing,
      supplements_original_edges=list(supplements),diagram_style='dashed' if status in ['unknown','inference'] else 'solid',
      reviewed_utc=NOW,applies_to='specific standalone SDK code or official product contract; not observed target-game production',
      production_actual_proven=False,observed_target_game_delivery=False,
      production_evidence='No production endpoint tests, SDK initialization, real identifiers or event transmission.',
      six_layers=dict(sdk_capability=status=='sdk',actual_game_business_callsite=business,
        request_construction_code=construction,production_successful_send=False,server_received=False,server_model_training=False),
      versions=sorted(set(str(s.get('version',s.get('product',s.get('sdk','official documented contract')))) for s in refs)),
      class_method_lines=[dict(path=s['path'],method=s.get('class_or_method',s.get('product','document contract')),
        start_line=s.get('start_line'),end_line=s.get('end_line')) for s in refs],
      sha256=[dict(path=s['path'],sha256=s['sha256'],official_packages=s.get('official_packages',s.get('official_package'))) for s in refs])
    edges.append(row)

edge(1,'CG_U_history','CG_U_token','Prior counters and loaded/shown campaign state are explicitly written into visible token outer protobuf','sdk',
 ['CGS01','CGS02','CGS03','CGS04','CGS05','CGS06','CGS07','CGS08','CGS22'],
 'viewer win/start/reset and campaign update -> repositories; build token snapshots state -> protobuf -> base64 version2',
 'prior callbacks and initialization branch; campaign data opaque; server may update session counters',
 'No per-target-game token capture, bid-time freshness or model feature mapping',('U01','U04'),construction=True)
edge(2,'U_firebase_ids','CG_U_pii','Unity Ads fid is populated from FirebaseAnalytics.getAppInstanceId via cached reflection bridge','sdk',
 ['CGS10','CGS11','CGS12','CGS13','CGS14','CGS15'],
 'ServiceProvider -> CachedFIdDataSource(AndroidFIdDataSource) -> FIdBridge -> FirebaseAnalytics.getAppInstanceId -> Pii.fid',
 'allowed.fid gates field population; cache constructor prewarms getter; Firebase/OS and applicable consent restrictions separate',
 'No cross-app ID equality, successful matching or target-game production value',('U02','U04'),construction=True)
edge(3,'CG_U_gateway_config','CG_U_pii','Gateway response can update AllowedPii controlling token PII fields','sdk',
 ['CGS09','CGS10','CGS16'],
 'UniversalResponse mutableData.allowedPii -> SessionRepository -> DeviceInfoRepository -> privacyDataSource.fetch',
 'AllowedPii initially default-empty; ad provider init can occur before field gate; OS and purpose consent separate',
 'Actual deployed allowlists, complete underlying getter collection gates and production use',('U02',),construction=True)
edge(4,'CG_U_token','CG_MAX_collect','MAX Unity adapter requests format-specific token and returns it through signal callback','sdk',
 ['CGS23','CGS24','CGS27'],
 'UnityAdsMediationAdapter.collectSignal -> updatePrivacyConsent -> UnityAds.getToken(TokenConfiguration(format)) -> callback -> MAX collector',
 'MAX consent/doNotSell only when supplied; provider initialization/callback conditions; no decoding token',
 'Which target-game opportunity invoked adapter and whether token arrived at downstream DSP',('U01',))
edge(5,'CG_MAX_collect','CG_MAX_request','Collected provider signal_data is serialized into MAX POST request construction','sdk',
 ['CGS25','CGS26','CGS27','CGS28','CGS29','CGS30','CGS31','CGS32','CGS33'],
 'Unity/Google provider signal -> cache or collect callback -> signal array -> a6.i puts signal_data -> a6.run POST scheduled',
 'network-specific conditions; signal TTL only caches if >0; format/unit/all scope; timeout; Google QueryInfo opaque',
 'Actual HTTP success, server reception, OpenRTB mapping and Axon bidder features',('A01','U01'),construction=True)
edge(6,'CG_MAX_history','CG_MAX_request','MAX request includes prior request/network context and optionally request-count statistics','sdk',
 ['CGS32','CGS34','CGS35','CGS36','CGS37','CGS38'],
 'ad-unit previous request/load/winner -> a6 ad_info.extra_parameters; w3.ar +1 counts -> gated mediation_stats',
 'umsm default false; production override unknown; previous data may not exist; user_data separate object/flag',
 'Not monetary LTV; SDK M reference time unproven; not evidence of competitor bids/users in model',('A01','A18'),construction=True)
edge(7,'CG_LP_collect','CG_LP_map','LevelPlay9.5 gathers concurrent provider responses with deadline and instance-keyed bidding maps','sdk',
 ['CGS39','CGS40','CGS41'],
 'provider callables -> workerManager deadline -> success/error/timeout -> provider instance bidding map',
 'provider initialization, availability and timeout; provider data opaque',
 'Complete cloud wire format, full TTL lifecycle, target-game invocation and Vector feature use',('U01',))
edge(8,'CG_Allsource','U_predict','Unity explicitly recommends prelaunch unattributed postbacks plus SDK data to train models; not counted toward learning threshold','official',
 ['CGS42','CGS43','CGS53'],
 'same advertiser app all-source install/session/purchase/ad revenue -> authorized MMP sharing -> Unity product-level learning statement',
 'at least two weeks recommended; lifetime/max window; purpose/privacy authorization and partner setup',
 'Per-field training lineage, actual target-game sharing, historical backfill and measured lift',('U07',))
edge(9,'M_af','CG_U_receiver','Unity AppsFlyer contract supports organic/non-organic installs and mapped sessions/purchase/ad revenue with sharing permissions','official',
 ['CGS44','CGS45'],
 'Activate Partner -> correct advertiser Game ID -> all-source default installs and in-app postbacks -> purchase/ad_revenue mapping',
 'background partner activation; event/revenue sharing scope and product permissions; privacy restrictions',
 'Target-game configuration, successful delivery, receipt and use',('U05','U06'))
edge(10,'M_adjust','CG_U_receiver','Unity Adjust requires all-source selection, event maps and dedicated ad_revenue path/account capability','official',
 ['CGS46','CGS48'],
 'Unity Ads partner + advertiser Game ID -> data source selection -> sessions/revenue sharing and event mapping -> Unity postback',
 'partner/account permissions; ad revenue dedicated path; valid privacy and source scope',
 'Target-game switches and production ad revenue postback ACK',('U05','U06'))
edge(11,'CG_U_receiver','U_predict','Unity ROAS product specifies post-install learning and mature cohort thresholds; D28 learning threshold uses D7 data','official',
 ['CGS47','CGS53'],
 'post-install revenue/installs -> learning threshold by optimization objective and cohort window',
 'IAA/IAP/Hybrid objective; D7 maturity; separate learning thresholds, not entire training sample count',
 'Actual labels, feature construction, model weights and target-game production training',('U07',))
edge(12,'U_mmp','CG_U_receiver','Unity S2S contract carries permitted identifiers, campaign/game/install/event time, attribution flag and revenue','official',
 ['CGS43','CGS48'],
 'MMP-authorized secondary postback -> gamer_id/aid/ifa + advertiser game_id/campaign + install_ts/time + attributed flag/value',
 'valid applicable privacy controls; identifier availability; correct advertiser rather than publisher Game ID',
 'Successful join, match rates, deduplication, delayed feedback and target-game receipt',('U06',))
edge(13,'A_context','A_predict','Axon explicitly discloses device/network, engagement, own MAX win/loss and advertiser-shared data for continual models and advertiser-value bidding','official',
 ['CGS51'],
 'official described collected/partner-shared data -> model continual learning -> impression value for advertiser -> bidding',
 'advertiser voluntary data; excludes sensitive/protected/children and other bidder bid/user data',
 'Per-field features, model structure, target-game calls, production delivery and measured contribution',('A01','A06','A13','A18'))
edge(14,'M_af','CG_A_receiver','AppLovin AppsFlyer partner mapping supports all media sources including organic; checkout excludes IAA/predicted LTV','official',
 ['CGS49','CGS52'],
 'AF configured event -> landing/checkout/postinstall; source scope and value/revenue choice -> AppLovin partner contract',
 'partner enabled and authorized; checkout only direct actual user payments; correct event window',
 'Game-specific event mapping/receipt; no IAA via checkout; no implicit MAX EventService routing',('A08',))
edge(15,'M_adjust','CG_A_receiver','Adjust Axon partner offers all-sources versus Axon-only, revenue sharing and explicit mapped events','official',
 ['CGS50','CGS52'],
 'partner data sharing activation -> source scope -> optional sessions/revenue + mapping; unmapped events not shared',
 'actual partner configuration; session callback high-volume opt-in; in-app revenue semantics',
 'Target-game enablement, server receipt and selected optimization objective',('A08',))
edge(16,'A_max','CG_MAX_queue','MAX EventService has event-name gated structured/legacy envelope and scheduled postback implementation','sdk',
 ['XS31','XS32','XS33'],
 'trackEvent -> axon_events choice -> structured or legacy payload -> scheduled postback',
 '13.7 standalone evidence; prior20-22 cover actual target versions; optional user_data and dedupe inputs not automatic',
 'Specific game business caller, successful send, reception and training',('A01',),construction=True)
edge(17,'CG_MAX_request','U_exchange','No complete mapping established from private SDK signals to server-side Unity/OpenRTB fields or final bidder inputs','unknown',
 ['CGS01','CGS21','CGS32','CGS33'],
 'Known private protobuf/JSON builders stop before documented exchange/DSP mapping',
 'Do not initialize SDK or probe production bidding; inspect authorized server traces only',
 'Server serializer/field lineage and authorized request trace; opaque token fields stay unknown',('A03','U04'))
edge(18,'CG_U_token','U_features','Session/ad history serialization does not prove each field becomes a Vector pre-install feature or useful LTV signal','unknown',
 ['CGS01','CGS04','CGS16','CGS53'],
 'Token serialization known; exact feature ingestion and bid-time as-of unknown',
 'Install-before time separation, purpose authorization and per-field availability required',
 'Feature schema, as-of joins, training provenance and controlled ablation',('U04',))
edge(19,'CG_A_receiver','A_labels','AppLovin target-game receipt, canonical revenue rows and field-level LTV label generation remain unproven','unknown',
 ['CGS49','CGS50','CGS51','CGS52'],
 'Public postback contract -> unknown receipt/join/dedup/maturity/training dataset',
 'actual authorized sharing; IAA distinct from IAP checkout; field-level privacy and time scope',
 'Partner export/ACK, canonical revenue ledger, training-data lineage and dataset version',('A08','A10'))
edge(20,'CG_U_receiver','U_labels','Unity public learning contract is not event-by-event proof of receipt, joins, mature canonical label rows or model ingestion','unknown',
 ['CGS42','CGS47','CGS48'],
 'Product-level learning established; specific postback -> canonical label transformation not visible',
 'attributed/unattributed separated; real revenue vs proxy; consent, cohort maturity and bid-time isolation',
 'Authorized delivery logs, joins, dedup/refund/FX/delay handling and model data lineage',('U06','U07'))
edge(21,'GAME_rotate','M_af','Rotate original wrapper sends the same double revenue into AFAdRevenueData plus separate ad_revenue2/4 paths','sdk',
 ['XS43'],
 'g8.a original revenue wrapper -> AFAdRevenueData(network,APPLOVIN_MAX,USD,d); eventTracking ad_revenue2; ad_revenue4 callback',
 'actual original game method reached; original runtime rules, privacy and API conditions',
 'Successful MMP delivery; downstream partner sharing and dedup of alternative events',('XM01',),business=True)
edge(22,'CG_Game_value','CG_MAX_queue','No complete target-game specific value rule -> MAX EventService chain established; generic capability is insufficient','unknown',
 ['XS31','XS32','CGS34'],
 'Public generic event and optional user-data capabilities; four-game original call scan separately preserved in report20/XD01-XD02',
 'Car generic Unity/Metica bridge not proven concrete caller; no absence claim for native/reflection/hotfix/server paths',
 'Concrete business callsite/arguments plus production postback and reception; cannot infer from default event names',('A10',))
edge(23,'A_max','A_predict','AppLovin gaming product links MAX monetization with IAA/Blended ROAS and MMP-based UA; internal label schema is not disclosed','official',
 ['CGS54','CGS51'],
 'official Ad ROAS/Blended products + MAX integration/MMP prerequisites -> advertised acquisition optimization',
 'product eligibility, advertiser activation and authorized data use; no specific target-game campaign observation',
 'Exact MAX income rows -> Axon labels/features, receipt and incremental effect',('A09',))
edge(24,'A_feedback','A_mmp','AppLovin tracking macros expose ad-response event ID shared by impression/click and permitted device/campaign context','official',
 ['CGS55'],
 'ad response tracking template -> EVENT_ID shared by click/impression + device/campaign macros -> MMP tracking contract',
 'advertiser tracking template; privacy/identifier availability; not raw target user data',
 'Actual configured URL, install mapping, privacy fallback and successful server matching',('A02','A08'))

known_node_ids={n['id'] for n in g['nodes']}
known_edge_ids={e['id'] for e in g['edges']}
for e in edges:
    assert e['source'] in known_node_ids and e['target'] in known_node_ids
    assert all(i in known_edge_ids for i in e['supplements_original_edges']),e['id']
g['edges'].extend(edges)
g['reviewed_utc']=NOW
g['client_growth_extension']=dict(reviewed_utc=NOW,snapshot_before='client-growth/EVIDENCE_GRAPH.before_client56.json',
 source_count=len(ss),new_nodes=len(nodes),new_edges=len(edges),
 scope='56-59 client traces; original historical edges not modified; no production observations',
 six_layer_rule='SDK capability / game callsite / request construction / successful send / server receipt / model training kept distinct')

save(path,g);save(O/'EVIDENCE_GRAPH.after59.json',g)
save(O/'NEW_EDGES.json',edges)
lines=['# 本轮关系边目录','','实线仅表示给定静态代码或官方契约范围已证；不表示实际生产送达。旧图对象全部保留。','']
for e in edges:
    lines += [f'## {e["id"]} · {e["claim"]}','',f'{e["source"]} → {e["target"]}；{e["evidence_level"]}。','',
      '来源：'+', '.join(f'[{i}](SOURCE_CATALOG.md#{i.lower()})' if i.startswith('CGS') else f'[{i}](../EVIDENCE_INDEX.md#{i.lower()})' for i in e['source_ids']),
      '',f'调用链：{e["explicit_call_chain"]}',f'条件：{e["permission_conditions"]}',f'未证：{e["missing_evidence"]}','']
(O/'EDGE_CATALOG.md').write_text('\n'.join(lines),encoding='utf-8')

index=R/'EVIDENCE_INDEX.md'
(O/'EVIDENCE_INDEX.before59.md').write_bytes(index.read_bytes())
with index.open('a',encoding='utf-8') as f:
    f.write('\n\n<a id="cg56"></a>\n\n## CG56 · 56—59客户端买量机制痕迹专项\n\n')
    for pattern in ['56_*Token*.md','57_*.md','58_*.md','59_*.md']:
        for p in R.glob(pattern):f.write(f'- [{p.name}]({p.name})\n')
    f.write('\n旧56号数据资产审计与prediction-validation保持原样，本轮不是其真实模型实验。\n\n')
    f.write('- [逐字段安装前血缘](client-growth/PREBID_FIELD_LINEAGE.json) / [原包来源及哈希](client-growth/PACKAGE_PROVENANCE.json)\n')
    f.write('- [原始片段及行号](client-growth/SOURCE_EVIDENCE.complete.json) / [来源目录](client-growth/SOURCE_CATALOG.md)\n')
    f.write('- [本轮24条边及条件](client-growth/EDGE_CATALOG.md) / [完整关系图](prediction-system/EVIDENCE_GRAPH.json) / [旧图快照](client-growth/EVIDENCE_GRAPH.before_client56.json)\n')
    f.write('- [完整性及证据引用核验](client-growth/VALIDATION.json)\n\n')
    for s in ss:
        f.write(f'<a id="{s["id"].lower()}"></a>\n\n- **{s["id"]}** [{s.get("class_or_method",s["product"])}](client-growth/SOURCE_CATALOG.md#{s["id"].lower()})：{s["path"]}:L{s["start_line"]}；{s["evidence_level"]}，版本/原包哈希与限定见原始目录。\n\n')
    f.write('新证据补齐广告历史→Token外层、允许条件下Firebase Analytics App Instance ID→Unity Pii、SDK signal→MAX构包，以及全来源/自然量postback的官方学习契约。未补齐目标游戏生产回传、身份join成功、逐字段训练与因果ROAS。\n')

manifest=R/'EVIDENCE_MANIFEST.json'
(O/'EVIDENCE_MANIFEST.before59.json').write_bytes(manifest.read_bytes())
m=load(manifest)
m['entries'].append(dict(id='CG56',title='56-59客户端买量机制及24条新增关系边',
 notes='No production traffic, real IDs or model performance claims; historical graph objects preserved',
 sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sorted(O.rglob('*'))
   if p.is_file() and '__pycache__' not in str(p) and p.name not in ['EVIDENCE_MANIFEST.before59.json']]))
m['client_growth_audit_utc']=NOW;save(manifest,m)
print('Graph and index extended:',len(nodes),'nodes,',len(edges),'edges,',len(ss),'sources.')
