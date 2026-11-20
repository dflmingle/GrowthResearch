from pathlib import Path
import json, hashlib, datetime, csv

R=Path(__file__).resolve().parent.parent; D=R/'lineage71'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):(R/p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
fetch=[]
for p in sorted(D.glob('FETCH_*.json')):
    if p.name!='FETCH_MANIFEST.json':fetch+=json.loads(p.read_text(encoding='utf-8-sig'))
save('lineage71/FETCH_MANIFEST.json',fetch)
docspec=[
('L71S01','max-mmp-api','lineage71/sources/max-mmp-api.txt',13,67,'MMP communicator contract names id unique internal ID for serve;subscription required;not a production receipt'),
('L71S02','max-s2s-impression','lineage71/sources/max-s2s-impression.txt',20,204,'Separate account-enabled S2S impression API:EVENT_ID UUID,EVENT_TOKEN,TS,PRECISION;5s timeout,no retries;no equality to SDK id promised'),
('L71S03','adjust-max-integration','lineage71/sources/adjust-max-integration.article.txt',5,66,'Explicit MaxAd revenue/network/unit/placement -> AdjustAdRevenue -> trackAdRevenue official example;no serve ID/precision in example'),
('L71S04','adjust-ad-revenue','lineage71/sources/adjust-ad-revenue.article.txt',421,520,'Callback parameters versus configured/enabled external partner parameters;not automatic platform consumption'),
('L71S05','adjust-event','lineage71/sources/adjust-event.article.txt',507,570,'AdjustEvent deduplication API and finite ID cache;not an AdjustAdRevenue exactly-once contract'),
('L71S06','af-ad-revenue-v6','lineage71/sources/af-ad-revenue-v6.article.txt',6,66,'SDK6.15+ logAdRevenue and optional additional map;remove old connector;revenue attributed to original UA source at product-contract level'),
('L71S07','af-dedup','lineage71/sources/af-dedup.article.txt',235,251,'ROI360 warning:manual af_revenue plus connectors/API can duplicate revenue;not evidence of automatic reconciliation'),
('L71S08','unity-post-events-canonical','lineage71/sources/unity-post-events-canonical.raw',12,59,'Official event types -> campaigns -> models;misconfigured postbacks cannot retroactively send lost events;not physical training columns'),
('L71S09','max-user-api','lineage71/sources/max-user-api.txt',107,163,'Daily export sample:impression time,USD revenue at6 decimals;no mandatory event ID in shown schema'),
('L71S10','adjust-s2s-revenue','lineage71/sources/adjust-s2s-revenue.article.txt',17,127,'S2S ad revenue product contract:28-day arrival limit,created_at,amount,currency,app/allowed device fields;not a public dataset'),
('L71S11','max-ilrd','lineage71/sources/max-ilrd.txt',124,200,'Client ILRD accessible in lifecycle callbacks;precision levels;current undefined description differs from cached13.6.4 API comments')]
docs=[]
for sid,key,path,a,b,claim in docspec:
    f=next(x for x in fetch if x['id']==key);assert f['status']==200
    p=R/path;lines=p.read_text(encoding='utf-8-sig').splitlines();assert b<=len(lines),(sid,b,len(lines))
    docs.append(dict(id=sid,url=f['url'],final_url=f['final_url'],path=f['path'],sha256=f['sha256'],acquired_utc=f['acquired_utc'],source_date='2026-11-18' if sid=='L71S08' else 'not stated;2026-11-20 snapshot',excerpt_path=path,excerpt_sha256=sha(p),start_line=a,end_line=b,excerpt='\n'.join(f'{i+1}: {t}' for i,t in enumerate(lines) if a<=i+1<=b),claim=claim,evidence_level='官方公开证实的接口/产品契约',production_actual_proven=False,server_received=False,server_model_training=False,permission_conditions='Public document GET only;account activation,partner mapping,consent and data rights separately required'))
save('lineage71/SOURCE_EVIDENCE.json',docs)
prior=read('lineage71/EVIDENCE_GRAPH.before.json')
origin=next(x for x in prior['sources'] if x['id']=='CGS50')
p=R/origin['path'];ls=p.read_text(encoding='utf-8').splitlines()
docs.append(dict(id='L71D01',url=origin['url'],path=origin['path'],sha256=sha(p),excerpt_path=origin['path'],excerpt_sha256=sha(p),start_line=165,end_line=249,excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(ls) if 165<=i+1<=249),claim='Adjust->Axon partner parameter mapping and explicit outgoing placeholders including revenue_usd,is_organic,match_type,partner_parameters;not training schema',source_date='not stated;prior verified snapshot reused',reviewed_utc=now,origin_source_id='CGS50',evidence_level='官方伙伴字段契约',server_received=False,server_model_training=False))
save('lineage71/SOURCE_EVIDENCE.json',docs)
A='ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/'
U='ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/'
M='ThirdPartySDKs/AppLovin/MAX/13.6.4/sources/com/applovin/mediation/'
specs=[
('L71C01','lineage71/java/com/applovin/impl/sdk/k.java',284,317,'AppLovin/MAX','13.6.4','k.a(c3)','Initial bundle id=c3.T and ad metadata;later ad_values.putAll may override same keys','Same MaxAd object;subscriber/config gating;server values unknown'),
('L71C02','lineage71/java/com/applovin/impl/sdk/k.java',177,183,'AppLovin/MAX','13.6.4','k.b(c3)','Base bundle + revenue_parameters overlay + country -> max_revenue_events','revenue_parameters may override id/revenue;do not promise final id equals c3.T without collision check'),
('L71C03','auction/sdk/MAX-13.6.4/java/com/applovin/impl/c3.java',172,198,'AppLovin/MAX','13.6.4','c3.y/S/R/T','ad_values/revenue_parameters are per-ad JSON;T reads full-response event_id','Response-selected suffix;not economic ledger uniqueness'),
('L71C04','lineage71/java/com/applovin/impl/sdk/k.java',274,277,'AppLovin/MAX','13.6.4','k.a(Bundle,String)','Communicator publish;message sticky policy selected by config','Local pubsub;not an HTTP send or MMP subscription observation'),
('L71C05',M+'MaxAd.java',63,80,'AppLovin/MAX','13.6.4','MaxAd.getRevenue/getRevenuePrecision','Amount may be0 when unavailable;precision exact/estimated/publisher_defined/undefined','API contract13.6.4;not final bank settlement;current online undefined wording differs'),
('L71C06',M+'MaxAdWaterfallInfo.java',10,35,'AppLovin/MAX','13.6.4','MaxAdWaterfallInfo interface','Public interface has no getEventId;implementation getter exists in70','Does not exclude arbitrary getAdValue or other configured integrations'),
('L71C07',A+'AdjustAdRevenue.java',6,76,'Adjust/Android','5.8.1','AdjustAdRevenue fields,setters,addPartnerParameter','Amount,currency,network,unit,placement,callback/partner maps;no dedicated deduplicationId member','Optional metadata only when caller supplies;not automatically populated with MAX ID'),
('L71C08',A+'PackageBuilder.java',180,191,'Adjust/Android','5.8.1','buildAdRevenuePackage','AdjustAdRevenue -> AD_REVENUE package /ad_revenue;metadata carried','Build path only;no observed request or receipt'),
('L71C09',A+'PackageBuilder.java',880,946,'Adjust/Android','5.8.1','getAdRevenueParameters','Maps serialized as callback_params/partner_params;source,revenue,currency,network,unit,placement;created_at from SDK processing time','Allowed identifiers/config only;not original impression timestamp;no dedicated precision/serve-id serialization in this range'),
('L71C10',A+'ActivityHandler.java',3161,3176,'Adjust/Android','5.8.1','trackAdRevenueI','enabled,valid,not GDPR-forgotten -> package queue -> sendFirstPackage call','Invocation is not actual delivery;no shouldProcessEventI here'),
('L71C11',A+'ActivityHandler.java',2066,2075,'Adjust/Android','5.8.1','trackEventI','Generic AdjustEvent calls shouldProcessEventI(deduplicationId)','Do not transfer generic-event guard to dedicated ad revenue path'),
('L71C12',A+'ActivityHandler.java',3503,3516,'Adjust/Android','5.8.1','shouldProcessEventI','Missing ID accepted;duplicate cached ID rejected;new ID stored','Local cache scope;not universal server deduplication'),
('L71C13',A+'ActivityState.java',185,210,'Adjust/Android','5.8.1','addDeduplicationId/eventDeduplicationIdExists','Bounded list eviction;0 disables remembering;max size configurable','Not permanent ledger;server behavior unknown'),
('L71C14',A+'AdjustEvent.java',6,75,'Adjust/Android','5.8.1','AdjustEvent.setDeduplicationId','Explicit caller-supplied generic event dedup key','Not generated from MAX event_id by this API'),
('L71C15',U+'core/data/model/AdObject.kt',23,43,'Unity/Ads','4.17.0','AdObject','opportunityId val;trackingToken var','Object-lifetime stability not global economic uniqueness'),
('L71C16',U+'core/domain/events/GetOperativeEventRequest.kt',21,42,'Unity/Ads','4.17.0','GetOperativeEventRequest.invoke','New eventId;opportunity and current token copied into built request;context also serialized','Opaque additionalData;not proven money or IAP label'),
('L71C17',U+'core/data/repository/OperativeEventRepository.kt',11,21,'Unity/Ads','4.17.0','addOperativeEvent','Built request emitted to SharedFlow with DROP_OLDEST','Not lossless;not server ACK'),
('L71C18',U+'core/domain/events/OperativeEventObserver.kt',37,55,'Unity/Ads','4.17.0','OperativeEventObserver.invoke','Payload -> full request -> serialized bytes under separate random workId;fallback sender','Enveloping time differs from operative creation;no history token rewrite shown'),
('L71C19',U+'core/domain/work/UniversalRequestJob.kt',25,43,'Unity/Ads','4.17.0','UniversalRequestJob.doWork','Read persisted bytes -> parse request -> sender;retry on failure;remove on sender return','Same persisted event identity on retry in this path;success not equal to server ingestion'),
('L71C20',U+'core/data/model/ShowEvent.kt',5,12,'Unity/Ads','4.17.0','ShowEvent','Started/Clicked/ReceivedReward/Completed are separate SDK lifecycle event variants','Not a proven one-to-one wire enum or income event'),
('L71C21',U+'core/domain/events/GetOperativeEventApi.kt',14,46,'Unity/Ads','4.17.0','GetOperativeEventApi.invoke','Current AdObject token passed by value to event builder before event queued','Refresh changes later events,not a shown rewrite of persisted earlier payloads')]
specs.append(('L71C22','lineage71/java/com/applovin/impl/sdk/k.java',206,210,'AppLovin/MAX','13.6.4','k.b(String)','Communicator enable flag and sticky-topic list OR active subscriber gate','Publish configuration is not proof an MMP actually subscribes'))
matrix=read('cross-sdk/SDK_MATRIX.json');code=[]
for sid,path,a,b,sdk,ver,method,claim,limit in specs:
    p=R/path;lines=p.read_text(encoding='utf-8-sig').splitlines();assert b<=len(lines),(sid,b,len(lines))
    packages=[z for x in matrix if x['sdk']==sdk and x['version']==ver for z in x.get('artifacts',[]) if z['path'].endswith('.aar')]
    assert packages,(sid,sdk,ver)
    for z in packages:assert sha(R/z['path'])==z['sha256']
    code.append(dict(id=sid,path=path,sha256=sha(p),start_line=a,end_line=b,sdk=sdk,version=ver,class_or_method=method,claim=claim,trigger_privacy_and_limits=limit,excerpt='\n'.join(f'{i+1}: {t}' for i,t in enumerate(lines) if a<=i+1<=b),original_packages=packages,reviewed_utc=now,evidence_level='SDK代码证实',six_layers=dict(sdk_capability=True,actual_game_business_callsite=False,request_construction_code=sid in ['L71C08','L71C09','L71C16','L71C18'],production_successful_send=False,server_received=False,server_model_training=False)))
save('lineage71/CODE_EVIDENCE.json',code)
g=read('lineage71/EVIDENCE_GRAPH.before.json')
reuseids=[f'CL70C{i:02}' for i in range(1,39)]+['CL70S01','CL70S02','CL70S03','CL70S04','CL70S05','GI69S_uken_participant','GI69S_uken_poster','GI69S_uken_code','CGS42','CGS43','CGS44','CGS45','CGS46','CGS47','CGS48','CGS49','CGS50','CGS51','CGS52','XS43','MA60S17']
reuse=[]
for sid in reuseids:
    x=next(z for z in g['sources'] if z['id']==sid);assert sha(R/x['path'])==x['sha256'],sid
    reuse.append(x)
save('lineage71/REUSED_EVIDENCE.json',reuse)
catalog=['# 71号原始证据目录','',f'核验UTC：{now}。新增材料仅公开文档GET与定点源码核验；未提交事件、未访问报表或生产API。','', '## 新的一手文档','', '| ID | 原始URL | 原件SHA256 | 证据位置 | 支持与限制 |','|---|---|---|---|---|']
for x in docs:catalog.append(f"| {x['id']} | {x['url']} | `{x['sha256']}` | {x['excerpt_path']}:{x['start_line']} | {x['claim']} |")
catalog+=['','## 定点代码核验','', '| ID | SDK/版本 | 类/方法 | 原始位置 | 结论与边界 |','|---|---|---|---|---|']
for x in code:catalog.append(f"| {x['id']} | {x['sdk']} {x['version']} | {x['class_or_method']} | {x['path']}:{x['start_line']} | {x['claim']}; {x['trigger_privacy_and_limits']} |")
catalog+=['','全部精确片段、源文件和原包SHA256/官方URL见CODE_EVIDENCE.json；复用证据逐哈希确认，见REUSED_EVIDENCE.json。sdk.k为本轮新定位的单类，不重复扫描SDK版本。TARGETED_ANALYSIS.json记录原JAR、单类反编译及javap结果。','', '所有官方示例中的标识仅为文档示例，未采集真实用户值、未生成生产请求。FETCH_MANIFEST保留404和失效重定向记录；其内容不算有效接口证据。Unity旧路径重定向到0.0.0.0失败，随后仅读取官网canonical文档路径。','', '没有新增数据集许可；SFU/Uken联系路径复用70号官方原件，不以当前岗位证明2015保管权。']
(D/'SOURCE_CATALOG.md').write_text('\n'.join(catalog)+'\n',encoding='utf-8')
print(json.dumps(dict(docs=len(docs),code=len(code),reused=len(reuse),fetch=len(fetch)),indent=2))
