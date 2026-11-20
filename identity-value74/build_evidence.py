from pathlib import Path
import csv, datetime, hashlib, json

R=Path(__file__).resolve().parent.parent;D=R/'identity-value74'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
fetch=[]
for p in sorted(D.glob('FETCH_*.json')):
 if p.name!='FETCH_MANIFEST.json':fetch+=read(p)
save(D/'FETCH_MANIFEST.json',fetch)
spec=[
 ('IV74S01','lr-match-guide',1,25,'E4','LiveRamp','Resolution can return maintained match or derived RampID;returning an ID is not proof of existing entity match'),
 ('IV74S02','lr-translation',1,59,'E4','LiveRamp','Partner-specific encoding and direction-specific consent/revocable translation;not a globally interchangeable identifier'),
 ('IV74S03','lr-envelope',1,33,'E4','LiveRamp','Person envelope -> partner-space anonymousConsumerLink;credentials required;not direct cookie/mobile-ID decryption'),
 ('IV74S04','lr-envelope',74,123,'E4','LiveRamp','30-day envelope expiry,opted-out/deleted entity and subnetwork failures;not full RampID or model retention TTL'),
 ('IV74S05','lr-match-metadata',1,43,'E4','LiveRamp','matchComponents/distinctMatch/matchConfidence contract;confidence is cascade step,not calibrated probability'),
 ('IV74S06','lr-match-schema',1,86,'E4','LiveRamp','Documented fuzzy-normalization match request and output semantics;API is not executed'),
 ('IV74S07','al-privacy',82,136,'E3','AppLovin','Official cross-app/device collection,combination and other-app personalization scope;no resolved graph output schema'),
 ('IV74S08','al-privacy',161,178,'E3','AppLovin','ID-linked access/deletion paths and typical up-to-two-year retention with exceptions;no training purge proof'),
 ('IV74S09','al-ads-public',1,45,'E3','AppLovin/Axon','Official Axon ad decision factors include advertising IDs,engagement/purchase histories and conditional ecommerce contacts;not specific graph-column consumption'),
 ('IV74S10','al-ads-public',49,81,'E3','AppLovin/Axon','Opt-out may need repeating after ad-ID change;public template messages are not this researcher opting out'),
 ('IV74S11','al-partners',66,240,'E3','AppLovin','Demand and measurement partner listing and roles;co-listing Unity/Adjust/Branch is not identity translation or model sharing contract'),
 ('IV74S12','unity-privacy',874,886,'E3','Unity','Identifier-scoped privacy requests and Ads historical-data deletion/opt-out;security IP logs excepted'),
 ('IV74S13','unity-privacy',948,963,'E3','Unity','Purpose/legal-based retention and security/accounting exceptions;no uniform identity-feature TTL disclosed'),
 ('IV74S14','unity-privacy',979,988,'E3','Unity','Opted-out profiling serves contextual ads;partner ad requests do not establish Vector graph feature ingestion'),
]
sources=[]
for sid,key,a,b,grade,company,claim in spec:
 f=next(x for x in fetch if x['id']==key);assert f['status']==200
 p=R/f['path'];t=R/f['text_path'];ls=t.read_text('utf-8').splitlines();assert b<=len(ls)
 assert sha(p)==f['sha256'] and sha(t)==f['text_sha256']
 sources.append(dict(id=sid,company=company,url=f['url'],final_url=f['final_url'],path=f['path'],sha256=f['sha256'],
  text_path=f['text_path'],text_sha256=f['text_sha256'],start_line=a,end_line=b,
  excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if a<=i+1<=b),claim=claim,evidence_stages=[grade],
  source_date='2026-08-06 effective' if key=='al-privacy' else '2026-06-30 review;2025-07-24 updated' if key=='unity-privacy' else 'page says 8 months ago;exact date UNKNOWN' if key.startswith('lr-') else 'publication date UNKNOWN;collection timestamp retained',
  acquired_utc=f['acquired_utc'],reviewed_utc=now,permission_conditions='Public static documentation only;runtime matching needs provider authorization,consent and namespace permissions',
  production_match_proven=False,prediction_model_consumption_proven=False,independent_identity_lift_proven=False))
save(D/'SOURCE_EVIDENCE.json',sources)
g=read(D/'EVIDENCE_GRAPH.before.json')
reuse_ids=['IG72S01','IG72S02','IG72S03','IG72S04','IG72S05','IG72S06','IG72S09','IG72C04','IG72C05','IG72C14','IG72C25','IG72C27','CGS51','MA60S01','MA60S17','EX73R04','EX73R06','EX73R07','EX73R08','EX73R09']
reuse=[next(x for x in g['sources'] if x['id']==sid) for sid in reuse_ids]
for x in reuse:assert sha(R/x['path'])==x['sha256'],x['id']
save(D/'REUSED_EVIDENCE.json',reuse)
assessment=[]
for x in fetch:
 key=x['id'];quality='substantive primary page' if key in {z[1] for z in spec} else 'discovery only;not used as claim proof'
 if key.startswith('search-'):quality='unreliable/off-topic results' if 'google' not in key else 'search rendering shell;no readable results'
 if key in ['lr-api','lr-resolution','lr-privacy-guide','al-audiences']:quality='redirect to documentation/product landing;not requested contract'
 if key in ['lr-sidecar','wurl-behavior','wurl-mobile']:quality='empty or navigation-only extracted content;no substantive assertion admitted'
 if x.get('status')!=200:quality='HTTP failure;not evidence of product absence'
 assessment.append(dict(id=key,url=x['url'],final_url=x.get('final_url'),status=x.get('status'),quality=quality,claim_proof_used=key in {z[1] for z in spec},sha256=x.get('sha256'),coverage='snapshot only;not exhaustive historical/production coverage'))
save(D/'SEARCH_COVERAGE.json',dict(reviewed_utc=now,requests=len(fetch),search_pages=sum(x['id'].startswith('search-') for x in fetch),assessments=assessment,
 stopping='No SDK rescans or failed-dataset retries. Search engines did not provide reliable coverage;only directly read primary contracts admitted. No claim that all global publications were searched.'))
save(D/'RUN_SCOPE.json',dict(new_sdk_downloads=0,old_sdk_rescans=0,production_matching_calls=0,production_ad_events=0,real_identifier_collection=0,real_identity_resolution=0,new_model_training=0,TalkingData_download_retries=0,Criteo_download_retries=0,emails_sent=0,agreements_signed=0,
 evidence_boundary='Official declarations and third-party contracts;no authorized production receipts,feature traces or real identity-only lift'))
rows=[]
def row(company,product,mechanism,a,b,cid,cgraph,d,unit,grade,ids,limit,next_evidence):
 rows.append(dict(claim_id=f'IV74C{len(rows)+1:02}',company=company,product=product,mechanism=mechanism,
  A_capability_or_contract=a,B_receiver_disclosure=b,B_actual_target_receipt='UNKNOWN',C_identifier_category_use=cid,
  C_resolved_identity_model_use=cgraph,D_identity_only_incremental_gain=d,unit=unit,evidence_grade=grade,
  source_ids=';'.join(ids),source_files=';'.join(x['path'] for sid in ids for x in sources+reuse if x['id']==sid),
  source_sha256=';'.join(x['sha256'] for sid in ids for x in sources+reuse if x['id']==sid),
  limitations=limit,next_discriminating_material=next_evidence))
row('AppLovin','MAX/Axon','Multiple identifiers in explicit request construction','CODE_CONFIRMED','REQUEST_CONSTRUCTION_ONLY','OFFICIAL_CATEGORIES','UNKNOWN','UNKNOWN','device/request','E1/E2/E3',['IG72C04','IG72C05','IV74S09'],'Same payload is not resolved person,cross-device graph or receipt','Authorized namespace/mapping receipt then physical model column lineage')
row('AppLovin','Advertising Services','Cross-app/device information combination and previous other-app personalization','OFFICIAL_DISCLOSURE','OFFICIAL_COLLECTION_SCOPE','OFFICIAL_AD_PERSONALIZATION','UNKNOWN','UNKNOWN','scope not quantified','E3',['IV74S07','IV74S09'],'Supports cross-property use disclosure,not a recoverable personal graph contract','Resolved entity granularity,matching rules and activation schema')
row('AppLovin','Axon','Identifier and history categories disclosed as decision factors','OFFICIAL_DISCLOSURE','OFFICIAL_GENERAL_USE','OFFICIAL_AXON_FACTORS','UNKNOWN','UNKNOWN','device/behavior categories','E3',['IV74S09','CGS51'],'C_id exists;C_graph is not proven;cannot claim no identifiers used','Matched-feature-group version and bid-time feature lineage')
row('AppLovin','CAPI/Pixel','Merchant user/contact/click conversion fields','CONTRACT_CONFIRMED','OFFICIAL_RECEIVER_CONTRACT','CONDITIONAL_ECOMMERCE','UNKNOWN','UNKNOWN','merchant/event','E3',['IG72S06','IV74S07'],'No merchant account success,game GAID join or ecommerce-to-game model proof','Anonymized mapping contract and purpose-bound model consumption record')
row('AppLovin','Demand/MMP partnerships','Listed Unity,Adjust,Branch roles','LISTING_CONFIRMED','POTENTIAL_ROLE_SCOPE','UNKNOWN','UNKNOWN','UNKNOWN','organization/data direction','E3',['IV74S11','CGS51'],'Names and general sharing do not prove identity graph partnership;competitor-user-data exclusion retained','Bilateral identity-specific scope/direction/namespace agreement')
row('AppLovin','Privacy lifecycle','Ad-ID/contact linked deletion and typical retention','OFFICIAL_RIGHTS_RULE','NOT_RECEIPT_EVIDENCE','NOT_A_MODEL_CLAIM','UNKNOWN','UNKNOWN','identifier/purpose','E3',['IV74S08','IV74S10'],'ID reset can require renewed opt-out;no graph merge/split or historical-feature purge audit','Deletion propagation schema and authorized completion trace')
row('Unity','Player Accounts/Authentication','Explicit organization account and project provider linking','ACCOUNT_CONTRACT_CONFIRMED','AUTHENTICATION_CONTRACT','NOT_VECTOR_FEATURE_PROOF','UNKNOWN','UNKNOWN','logged-in organization account','E1/E2/E3/E4',['IG72S02','IG72S03','IG72C14'],'First-party cross-game/devices possible;requires login and scope;not all Unity players','UPA -> Ads/Vector purpose-authorized mapping contract')
row('Unity','Exchange/LiveRamp','RampID identity audience activation in US/Canada','PARTNERSHIP_CONFIRMED','OFFICIAL_EXCHANGE_AVAILABILITY','NOT_VECTOR_FEATURE_PROOF','UNKNOWN','UNKNOWN','partner person/household granularity unresolved for Unity','E3/E4',['IG72S05'],'Vendor availability and partner support condition,not measured match count or Vector receipt','Unity-specific RampID field/granularity and receiver schema')
row('LiveRamp','Match/Retrieval','Fuzzy matching returns maintained or derived identifier','API_CONTRACT_CONFIRMED','PROVIDER_RETURN_SCHEMA','NOT_AXON_VECTOR','UNKNOWN','UNKNOWN','individual;raw PII not collected','E4',['IV74S01','IV74S06'],'A derived return does not prove an existing identity match','Authorized maintained/derived status distribution and quality truth,without raw PII')
row('LiveRamp','Translation','Partner-specific encoding and person/household namespaces','API_CONTRACT_CONFIRMED','AUTHORIZED_TRANSLATION_CONTRACT','NOT_AXON_VECTOR','UNKNOWN','UNKNOWN','individual vs household','E4',['IV74S02'],'Each direction separately permissioned;do not assume universal string equality or Unity encoding','Receiver-specific agreement and namespace metadata')
row('LiveRamp','Envelope decryption','Person envelope -> partner-space pseudonymous result','API_CONTRACT_CONFIRMED','PUBLIC_RESPONSE_SCHEMA','NOT_AXON_VECTOR','UNKNOWN','UNKNOWN','person envelope','E4',['IV74S03'],'No direct mobile/cookie-ID input support in this endpoint;not executed','Authorized actual receiver contract;no live identity query')
row('LiveRamp','Envelope errors','Expired/opted-out/deleted/subnetwork restriction','FAILURE_CONTRACT_CONFIRMED','NOT_RECEIPT_EVIDENCE','NOT_A_MODEL_CLAIM','UNKNOWN','UNKNOWN','envelope lifecycle','E4',['IV74S04'],'30 days is this envelope expiry,not universal identity TTL or model purge SLA','Receiver-specific TTL/revocation/deletion propagation contract')
row('LiveRamp','matchMetadata','Component,cascade-confidence and distinct-match flags','METADATA_CONTRACT_CONFIRMED','PUBLIC_RESPONSE_SCHEMA','NOT_AXON_VECTOR','UNKNOWN','UNKNOWN','candidate match metadata','E4',['IV74S05'],'matchConfidence is not calibrated probability;distinctMatch not guaranteed real person truth','Authorized independent match quality/calibration evaluation')
row('Unity','Ads privacy','Opt-out contextual fallback,identifier-scoped deletion/retention','OFFICIAL_RIGHTS_RULE','OFFICIAL_AD_SCOPE','NOT_VECTOR_GRAPH_PROOF','UNKNOWN','UNKNOWN','app/device/purpose','E3',['IV74S12','IV74S13','IV74S14'],'Fallback permits contextual ads;does not disclose fallback model or equivalence','Gating implementation and feature-removal audit')
row('Unity','Vector','Cross-game behavioral patterns and aggregate cohort insights','OFFICIAL_DATA_USE','OFFICIAL_BID_TIME_USE','OFFICIAL_CATEGORIES','UNKNOWN','UNKNOWN','granularity not uniquely disclosed','E3',['MA60S17'],'Compatible with shared parameters,aggregates or legal personal history;not identity ablation','Feature groups with timestamps/versions and identity-off paired ablation')
row('AppLovin','Axon','Future value distribution and continued training','OFFICIAL_MODEL_PURPOSE','OFFICIAL_MODEL_PURPOSE','OFFICIAL_CATEGORIES','UNKNOWN','UNKNOWN','architecture unresolved','E3',['MA60S01','CGS51'],'No graph vs aggregate fixed-data ablation','Fixed-data/capacity identity ablation and authorized model lineage')
row('Independent','BPID','Six synthetic matching methods and stress tests','SYNTHETIC_BENCHMARK','NOT_PLATFORM_RECEIPT','NOT_VENDOR_MODEL','NOT_VENDOR_MODEL','SYNTHETIC_ONLY','synthetic pair','NOT_E5_E6',['EX73R04','EX73R06'],'F1-max RF has ~39.7% false merge;isolated pairs do not test multi-hop;no real people','Consented ground-truth linking and cost-sensitive tests')
row('Independent','Generated D','Identity/group/shared-rule comparisons with drift','SYNTHETIC_MECHANISM','NOT_PLATFORM_RECEIPT','NOT_VENDOR_MODEL','NOT_VENDOR_MODEL','SYNTHETIC_ONLY','generated users/values','NOT_E5_E6',['EX73R07','EX73R08','EX73R09'],'Extra source rows and assumed DGP;not vendor or game profit proof','Real authorized M4 vs M3 fixed-data/feature-time comparison')
with (R/'74_身份关联商业价值证据矩阵.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
save(D/'CLAIMS.json',rows)
catalog=['# 74号一手来源与检索边界','',f'UTC: {now}。只读公开文档；无真实匹配或模型训练。','', '| ID | 原始URL | 原件SHA256 | 行号/等级 |','|---|---|---|---|']
for x in sources:catalog.append(f"| {x['id']} | {x['url']} | `{x['sha256']}` | {x['start_line']}—{x['end_line']} / {','.join(x['evidence_stages'])} |")
catalog+=['','每条精确摘录、采集日期与最终URL见SOURCE_EVIDENCE.json；旧图20条对象逐哈希复用见REUSED_EVIDENCE.json，不改历史来源。', '',
 'SEARCH_COVERAGE.json记录全部请求及失败/导航/重定向。Bing定向查询结果离题，Google只有渲染壳，不能把它们作为“未有论文”的全面检索证据。Wurl/Sidecar正文未成功取得，不从首页导航推断合作不存在。', '',
 'LiveRamp公开接口文档包含生产服务URL和示例；本轮仅保存文档，没有请求任何匹配、令牌、转码、解密或删除接口。官方示例不是本项目真实返回值。', '',
 'AppLovin合法新隐私原文和公开广告说明补充旧72导航页面不足，旧报告不改，勘误见CORRECTIONS.md。没有新C_graph/D生产证据；停止继续旧版本逆向。','']
(D/'SOURCE_CATALOG.md').write_text('\n'.join(catalog),encoding='utf-8')
print(json.dumps(dict(primary_excerpt_records=len(sources),reused=len(reuse),matrix_rows=len(rows),requests=len(fetch)),indent=2))
