"""Read-only evidence synthesis. Never executes SDKs, sample R, or training."""
from pathlib import Path
import json, hashlib, csv, datetime, re
R=Path(__file__).resolve().parent.parent
D=R/'game-industry69'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def write(p,x):
    (R/p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name,rows):
    with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
fetches=[]
for p in sorted(D.glob('FETCH_*.json')):
    if p.name=='FETCH_MANIFEST.json':continue
    fetches.extend(json.loads(p.read_text(encoding='utf-8')))
for x in fetches:
    # Errors may occur while interpreting a successfully saved non-object JSON response.
    if not x.get('path'):
        p=D/'sources'/(x['id']+'.html')
        if p.exists():
            x.update(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size)
    if x.get('path'):
        p=R/x['path'];x['sha256_verified']=sha(p)==x.get('sha256')
        x['filesystem_last_write_utc']=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()
    # Public OSF download redirects have expiring signed URLs; permanent origin is sufficient.
    if x.get('final_url','').find('X-Amz-')>=0:x['final_url']=x['final_url'].split('?')[0]
    x.pop('text_preview',None);x.pop('works',None);x.pop('links',None)
write('game-industry69/FETCH_MANIFEST.json',fetches)
selected=[
 ('GI69S_unity_paper','unity-full-paper','paper','2023; accepted author manuscript','Sections 2.1/2.2/2.4/2.5; extracted lines 815-825,979-1066,1548-1563','Real iOS IAP research; data not public; within-game keys only'),
 ('GI69S_unity_osf','unity-osf-files','official author repository API','file dates 2022-12-09','data[].attributes/name,extra.hashes; links.next=null','Two public supplement files, neither a raw transaction dataset'),
 ('GI69S_unity_code','unity-analysis-code','author reproduction code','2022-12-09 (OSF metadata)','raw lines containing generate synthetic metadata / generate synthetic spending data','Code uses synthetic spending placeholder; not real game training data'),
 ('GI69S_unity_appendix','unity-technical-appendix','author technical appendix','2022-12-09 (OSF metadata)','word/document.xml; extracted paragraph 3','Wasserstein distribution clustering; not Axon/Vector production architecture'),
 ('GI69S_unity_preprint','unity-osf','public preprint metadata','2022-11-23 published; API modified 2025-11-09','attributes.description; has_data_links=no','69,144,363 spenders,2873 games,624 days; paper license is not data access'),
 ('GI69S_unity_research_route','unity-research','official current web route','publication unknown; observed 2026-11-20','redirect final_url unity.com/learn','Paper historical research URL currently redirects; no automatic data application entitlement'),
 ('GI69S_uken_participant','uken-case2-readme','original competition participant description','2015 competition; README history separately captured','Dataset; target variables;44-column dictionary; Details','300000 rows;250000 labeled/50000 unlabeled; explicitly no permission to upload raw data'),
 ('GI69S_uken_poster','uken-poster-source','participant poster source','September2015 as stated','lines 73,136,139-143,210-228','D30 retention definition; reported analysis is not independently replicated'),
 ('GI69S_uken_code','uken-analysis-source','participant analysis code','header Updated December6 2015','header; data read; feature transformations; training code','Raw Data/user_stats file absent; no replay attempted'),
 ('GI69S_uken_tree','uken-case2-tree','GitHub repository manifest','snapshot 2026-11-20','tree[].path/size','No original training dataset in returned tree; predictions.csv not downloaded'),
 ('GI69S_uken_synthetic','uken-modern-readme','independent demo author statement','publication not independently verified','Datasets section; lines94/208-214','310K project explicitly synthetic and inspired by Uken; excluded'),
 ('GI69S_apple_aa','apple-adattribution-markdown','official platform documentation','page date unstated; snapshot2026-11-20','Overview/three participants/postback data tier/user- or device-specific data','Signed conversion attribution; not individual revenue ledger or runtime training ACK'),
 ('GI69S_apple_sk','apple-skan-markdown','official platform documentation','page date unstated; snapshot2026-11-20','Overview/advertised app conversion value/postback','Separate attribution feedback from pre-ad request context'),
 ('GI69S_ageishtaria','ltv-deep-paper','original research paper','arXiv2018; DOI10.1109/BigData.2018.8622151','Dataset section; lines309-355 of extraction','Real game research,32 months; no verified raw download or data reuse permission'),
 ('GI69S_mag_site','mag-corporate-research','official company public page','publication unknown; snapshot2026-11-20','page body; research query returned corporate homepage','Establishes company only; does not identify alleged five-game dataset'),
]
sources=[]
for sid,key,kind,date,pos,claim in selected:
    x=next(x for x in fetches if x['id']==key)
    assert x.get('status')==200,(sid,x)
    sources.append(dict(id=sid,path=x['path'].replace('\\','/'),url=x['url'],sha256=x['sha256'],source_date=date,reviewed_utc=now,evidence_kind=kind,original_position=pos,claim=claim,permission_conditions='Public document read only; no inherited permission to use restricted player data',production_actual_proven=False,observed_target_game_delivery=False,server_model_training=False))
write('game-industry69/SOURCE_EVIDENCE.json',sources)

reused=[]
for path in ['client-growth/SOURCE_EVIDENCE.complete.json','cross-sdk/CODE_EVIDENCE.json','auction/CODE_EVIDENCE.json','core-insights/CODE_EVIDENCE.json','model-architecture/SOURCE_EVIDENCE.json','vector/CODE_EVIDENCE.json']:
    for x in load(path):
        p=R/x['path']
        assert p.exists(),x['path']
        if x.get('sha256'):assert sha(p)==x['sha256'],(path,x['id'])
        reused.append(dict(x,origin_catalog=path))
write('game-industry69/REUSED_EVIDENCE.json',reused)
new_specs=[
 ('GI69C01','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.kt',20,45,'4.17.0','GetOperativeEventRequest.invoke','Callers provide opportunityId/tracking token/type; event creates new eventId and serializes context'),
 ('GI69C02','ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/OperativeEventObserver.kt',38,60,'4.17.0','OperativeEventObserver.invoke','Repository flow -> UniversalRequest -> persisted work item -> background job; fallback event sender'),
 ('GI69C03','ThirdPartySDKs/AppsFlyer/Android/6.17.5/decompiled/com/appsflyer/AFAdRevenueData.java',16,64,'6.17.5','AFAdRevenueData.constructor/getters','Separate network,mediation,currency,revenue; precision not one of these four constructor fields'),
 ('GI69C04','ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/AdjustAdRevenue.java',6,49,'5.8.1','AdjustAdRevenue.setRevenue/setAdRevenueNetwork/setAdRevenueUnit/setAdRevenuePlacement','Caller supplies currency,amount,network,unit,placement; class does not verify settlement'),
 ('GI69C05','ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/PackageBuilder.java',920,948,'5.8.1','PackageBuilder ad-revenue parameter writer','Revenue metadata into MMP package,not a direct Axon/Vector production postback'),
]
code=[]
matrix=load('cross-sdk/SDK_MATRIX.json')
for sid,path,a,b,version,method,meaning in new_specs:
    p=R/path;lines=p.read_text(encoding='utf-8').splitlines()
    packages=[]
    for item in matrix:
        if item['version']!=version:continue
        if not any(k.lower() in path.lower() and k.lower() in item['sdk'].lower() for k in ['Unity/Ads','AppsFlyer','Adjust']):continue
        for artifact in item.get('artifacts',[]):
            if artifact['path'].endswith(('.aar','-sources.jar')):
                original=R/artifact['path']
                assert original.exists() and sha(original)==artifact['sha256'],artifact['path']
                packages.append(artifact)
    assert packages,(sid,version,path)
    code.append(dict(id=sid,path=path,sha256=sha(p),start_line=a,end_line=b,version=version,class_or_method=method,meaning=meaning,excerpt='\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines) if a<=i+1<=b),package_provenance_catalog='cross-sdk/SDK_MATRIX.json',verified_original_packages=packages,reviewed_utc=now,actual_target_game_call=False,production_successful_send=False,server_received=False,server_model_training=False))
write('game-industry69/CODE_EVIDENCE.json',code)

rows=[]
def row(key,field,origin,time,pre,post,serialize,receiver,scope,condition,ids,limit):
    rows.append(dict(id=key,field=field,source=origin,generated_at=time,pre_current_ad_available=pre,post_display=post,serialization=serialize,receiver=receiver,id_scope=scope,privacy_and_trigger=condition,evidence_ids=ids,production_receipt='UNKNOWN',model_consumption='UNKNOWN',limit=limit))
row('T01','MAX ad_unit_id/ad_format/sdk/app/device','MAX collector + developer ad load','request build','YES','NO','a6.g and request body','MAX mediation endpoint','app/ad unit/device context','SDK configured; privacy filtering applies','CGS32;CGS33;MAX-fetch-payload','Private SDK JSON is not full server OpenRTB')
row('T02','MAX signal_data','network adapter collectSignal','before request or cache hit','YES; freshness depends TTL','NO','a6.i JSONArray','MAX mediation endpoint,chosen network signal path','network-defined opaque token','adapter eligible;privacy forwarding;timeout/TTL','CGS23;CGS24;CGS25;CGS27;CGS28;CGS32','Do not decode opaque token into claimed model features')
row('T03','MAX previous_request/previous winning network/mediation_stats','earlier request/load/mediation lifecycle','before next request','YES for prior history','Prior lifecycle only','a6 ad_info/mediation_stats gated blocks','MAX mediation endpoint','local session/ad unit','feature flags and data presence','CGS34;CGS35;CGS36;CGS37;CGS38','ars/ar are counts,not dollar income;not proof of cross-app history')
row('T04','MAX optional user_data/publisher user ID','explicit developer setter + flags','setter before request','CONDITIONAL','NO','optional user_data branch','MAX endpoint if enabled','developer-defined identity scope','explicit assignment/flags/privacy contract','CGS34;MAX-fetch-adunit-history','Same payload IDs do not prove server matching or event-to-ad join')
row('T05','Unity tokenId/tokenNumber/sessionCounters','AndroidBuildHeaderBiddingToken','token build after bounded init','YES;not observed bid_time','NO','HeaderBiddingToken protobuf/base64/version prefix','mediation token consumer','token/session','SDK init and callbacks','CGS01;CGS02;CGS03;CGS17','Request IDs and counters are not personal cross-game profiles')
row('T06','Unity staticDeviceInfo/dynamicDeviceInfo','Android device repositories','cached static/fresh dynamic at build','YES','NO','token/adRequest proto','mediation or Unity gateway','app/device/context','platform/provider and privacy state','CGS09;CGS19;CGS20;CGS21','Device context is observable;actual model-feature schema unknown')
row('T07','Unity allowed GAID/App Set ID/Firebase Analytics appInstanceId','privacy device info + FId bridge','getter/cache and token build','CONDITIONAL','NO','allowedPii/pII serialization','Unity request/token receiver','advertising/install app-set scopes differ','allowlist and provider/privacy state;cached getter may prewarm','CGS10;CGS11;CGS12;CGS13;CGS14;CGS15;CGS16','fid here is NOT Firebase Installations FID;no proven cross-app join')
row('T08','Unity opportunityId/placement/adFormat/TCF','ad load caller/configuration','before current request','YES','NO','AndroidGetAdRequest','Unity gateway','ad opportunity/placement/consent','only configured optional fields;TCF present','CGS21;CGS23;Unity-request','MAX adapter observed format only;do not invent optional placement values')
row('T09','Unity loaded/shown campaignState,dataVersion','viewer bridge + campaign repository','load/show from earlier ads','YES for later opportunities','Prior load/show','token/adRequest campaignState','Unity gateway/token consumer','opportunity keyed in-memory map','viewer update + retention/removal rules','CGS04;CGS06;CGS07;CGS08','Opaque campaign data is not decoded gameplay or long-term personal history')
row('T10','LevelPlay per-network bidding data/token/results','9.5 q3/g2/Q1','pre-auction token collection','YES with timeout','NO','network bidding map/callback','LevelPlay auction module/endpoint','provider instance/auction','SDK/network eligibility,privacy config','CGS39;CGS40;CGS41','Collector existence does not disclose complete token contents')
row('T11','LevelPlay returned price/adMarkup/serverData/loadTimeout/nurl','9.4 response parser q2','server auction response before rendering','RESPONSE after current bid','NO','response parsing','SDK then selected adapter/notifier','auction/ad load','valid response/fallback','LP-response-notices;LP-fallback','Price returned before render is not realized revenue')
row('T12','MAX revenue/precision/network/adUnit/creative','MaxAd response metadata + revenue callback','price may arrive at load;callback after impression','Price estimate MAY precede display','Revenue callback YES','MaxAd.getRevenue/getRevenuePrecision and game wrapper','game developer then configured SDKs','economic impression metadata','availability gate;getRevenue may return0/-1;callback required','MAX-revenue-response;XS43','Retain exact/estimated/publisher-defined;not bank settlement')
row('T13','LevelPlay revenue/precision/auctionId/adNetwork','LevelPlayAdInfo public API','auction metadata/load/display callbacks','metadata MAY precede display','ILRD belongs to impression lifecycle','getters observed in existing API audit','developer callback;MMP if wired','auction/ad','listener wiring and field availability;callback path not newly fully traced','levelplay_9.3.0;levelplay_9.4.0;levelplay_9.5.0','API getter alone does not prove four games invoke callback or realized amount')
row('T14','Unity operative event eventId/eventType/opportunityId/trackingToken','GetOperativeEventRequest caller','ad lifecycle operative API invocation','Earlier feedback can precede NEXT ad','Lifecycle-specific;not all are impressions','operativeEvent -> UniversalRequest -> persisted job/fallback','Unity event sender/gateway','event vs ad opportunity distinct','observer active;storage/send policy','GI69C01;GI69C02','Association fields proven;actual impression/click callers require independent event-type callsite')
row('T15','Exchange request id/impid vs nurl/lurl/burl','published exchange protocols','auction/load/render stages','id/imp before bid','burl after render','OpenRTB request/response and callbacks','DSP/exchange/trackers','auction/impression','bid validity,privacy filters,network callback','auction/PROTOCOL_FIELDS.json;36_AppLovin_OpenRTB与竞价协议.md;37_Unity_OpenRTB与竞价协议.md','Win notice is not billed impression;SDK-cloud fields cannot reconstruct all OpenRTB enrichment')
row('T16','AppsFlyer monetizationNetwork/mediationNetwork/currency/revenue','ILRD callback + AFAdRevenueData','after observed ad revenue callback','NOT for same impression outcome','YES for realized callback','logAdRevenue -> AF revenue SDK package','AppsFlyer then partner only if configured','MMP app/user plus economic event','developer call;consent;partner share/mapping;dedup','GI69C03;XS43;CGS44;CGS45','Rotate also ad_revenue2/4;do not triple-count;server partner enablement unknown')
row('T17','Adjust revenue/currency/network/unit/placement','AdjustAdRevenue caller','after caller observed revenue','NOT same-impression outcome','YES if genuine ILRD input','PackageBuilder ad_revenue parameters -> queue','Adjust then permitted configured partners','MMP event/session/attribution','privacy state,event source,sharing switches','GI69C04;GI69C05;CGS46;CGS50','Setter accepts data;does not certify source money or forwarding ACK')
row('T18','MMP install_ts/event_time/campaign/source/was_conversion_attributed','attribution and postback server','click/install/event processed later','campaign context may preexist;outcome NO','AFTER attribution/event','official server partner contract','Unity/AppLovin partner ingress if enabled','source-specific attribution IDs','Activate Partner/all-source/revenue mapping/window','CGS43;CGS44;CGS46;CGS48;CGS49;CGS50','Unattributed-to-Unity can include another network or organic;not duplicate Unity installs')
row('T19','GRT/AdWorth/threshold value','game rules/counters/config','post-install rule fires','NO for first acquisition bid','Post-install','Firebase/AF/Meta/Adjust chosen routing','configured analytics/MMP receivers','internal rule/event','threshold/window/once and remote event mapping','49_行为价值事件端到端调用链.md;ThirdPartySDKs/BUSINESS_TRACES.json','Proxy value is not real IAA/IAP;direct MAX EventService not inferred')
row('T20','Unity IAP paid/fulfilled/TransactionID/PriceMicro','store order + catalog metadata','purchase lifecycle after install','NO for first acquisition bid','Post-install purchase','IAP protobuf gateway or Runtime Insights','Unity Insights/native boundary','order/event/journey IDs differ','IAP5.5.1 callbacks/platform compile;optional IDs have own gates','XS07;XS08;XS09;XS10;XS12;XS13;XS40','Paid+fulfilled one order;metadata price not necessarily actual net paid;Vector field lineage unknown')
row('T21','Firebase AppInstanceId/AppId/SessionId vs FID','Analytics reflection vs Installations/RC','identity getter and configuration fetch','Some historical IDs CONDITIONAL','NO mandatory relation','Unity Ads and IAP optional fields;RC separate fetch','Unity Ads/Insights vs Firebase RC','app instance/config/session/install differ','AdsIntent+remote allowlist for IAP;Ads AllowedPii;separate RC rules','CGS11;XS01;XS02;XS03;XS24;XS25;55_跨SDK身份价值血缘最终核验.md','No evidence automatic forwarding of all Firebase gameplay events into Axon/Vector')
row('T22','Remote event filters/schema/identity allowlists/experiments','SDK server config and package versions','config fetch/init/response before subsequent calls','YES for controls','Controls future events','MAX axon_events;Unity allowedPii;IAP allowlist;RC ABT','respective SDK modules','schema/config/session','only actual branch/version;local defaults not live config','CGS16;XS04;XS05;XS26;XS27;XS31;XS32','Remote control is not model inference;5.5.1 Firebase-session writer fix not new natural-person graph')
row('T23','SKAN/AdAttributionKit network identity/signed ad context','registered network + publisher app','signed attributable ad before conversion','YES ad context only','NO','platform attributable-ad API','OS attribution system','network/campaign source not user ID','Apple registration and applicable framework config','GI69S_apple_aa;GI69S_apple_sk','Android SDK code cannot prove iOS target-app adoption')
row('T24','SKAN/AdAttributionKit fine/coarse conversion value/did-win/postback','advertised app updates + Apple attribution','post-install/reengagement conversion windows','NO future outcome before same bid','YES delayed conversion feedback','signed privacy-tiered postback','eligible ad networks;developer optional copies','attribution transaction/campaign,not personal cross-app ID','crowd anonymity,thresholds,app opt-in and network eligibility','GI69S_apple_aa;GI69S_apple_sk','did-win means attribution winner,not auction winner;conversion code not raw exact revenue ledger')
table('SDK_FIELD_TIMELINE.csv',rows)
write('game-industry69/SDK_FIELD_TIMELINE.json',rows)

catalog=[
 dict(id='GI69D01',name='Uken SFU2015 competition',kind='actual-game participant documentation;data restricted',row_scope='300000 rows as participant reports',value='revenue measure;scaling/currency/refunds UNKNOWN',time='install/first-event dates;observation cutoff UNKNOWN',zero='event-never-missing documented;complete user observation UNKNOWN',license='Participant explicitly cannot upload;NDA/full reuse terms not obtained',actual_data='NOT ACQUIRED',admission='STOP',future_value='Potential only after original contract and time coverage',multi_game='one unnamed game;no transfer pair',sources='GI69S_uken_participant;GI69S_uken_poster;GI69S_uken_code'),
 dict(id='GI69D02',name='Unity Many Faces of Monetisation',kind='real iOS IAP paper',row_scope='2873 games;69144363 game-scoped spenders;461996143 transactions',value='IAP USD converted at event-date FX;not total game income',time='2020-08-01..2022-04-16;624 days;received_at unavailable',zero='payers only;no all-install denominator',license='Private Unity institutional legal agreement;authors cannot share or facilitate access',actual_data='NO;paper/appendix/R only',admission='STOP',future_value='No current training;conditional payer forecasting only if separately permitted timestamped data',multi_game='2873 in original private study;no cross-game personal key',sources='GI69S_unity_paper;GI69S_unity_osf;GI69S_unity_code'),
 dict(id='GI69D03',name='MAG five-game day-level operations lead',kind='TASK-SUPPLIED LEAD;unresolved primary identity',row_scope='five games claimed in task;not independently verified',value='DAU/IAP count/rewarded views/product price claimed;IAA amount UNKNOWN',time='daily claimed;dates and coverage UNKNOWN',zero='aggregate rows/missing days UNKNOWN',license='NOT VERIFIED',actual_data='NO',admission='STOP',future_value='Day-level panel could study aggregate association only after source verified',multi_game='claimed five products;not verified independent datasets',sources='GI69S_mag_site;FETCH_MANIFEST.json search boundary'),
 dict(id='GI69D04',name='Age of Ishtaria LTV2018 research',kind='real game original research',row_scope='single game;paying-user/whale analysis',value='IAP spending;plot normalized0..1;not real ILRD',time='2014-09-24..2017-05-01',zero='full installation population not certified by file audit',license='No raw file + dataset permission verified;paper openness not data permission',actual_data='NO;paper only',admission='STOP',future_value='Methodological evidence;not runnable data benchmark',multi_game='one product',sources='GI69S_ageishtaria'),
 dict(id='GI69D05',name='Uken-inspired310K Live-Ops GitHub demo',kind='EXCLUDED_SYNTHETIC',row_scope='synthetic310000',value='generated spending,not economic receipts',time='generated',zero='generated',license='MIT for project does not make simulated records real',actual_data='README only;no generated rows acquired',admission='EXCLUDED',future_value='No empirical player prediction claim allowed',multi_game='simulated only',sources='GI69S_uken_synthetic'),
 dict(id='GI69D06',name='Flood-It Google Analytics demo',kind='REUSED68;obfuscated demo',row_scope='official schema only;no Cloud rows',value='actual monetary labels not verified',time='114 documented days;actual table not queried',zero='UNKNOWN',license='dataset scope not verified in68',actual_data='NO;prior doc snapshot only',admission='STOP',future_value='No new evidence repairs68 admission gaps',multi_game='one game;platforms not independent products',sources='public-experiments/round68/sources/google-game.txt;68_DATASET_CATALOG.csv'),
]
table('DATASET_ADMISSION.csv',catalog)
write('game-industry69/DATASET_ADMISSION.json',catalog)

catalog_md=['# 69游戏行业专项原始来源索引','',f'审查时间：{now}。内容哈希以原始响应字节为准；HTTP200不等于有效数据下载。搜索失败、无关结果、404、挑战页均在FETCH_MANIFEST.json保留，不用来证明数据不存在。','', '| ID | 原始URL | 本地原件 | SHA256 | 原始位置/证明边界 |','|---|---|---|---|---|']
for x in sources:catalog_md.append(f"| {x['id']} | {x['url']} | {x['path']} | `{x['sha256']}` | {x['original_position']}；{x['claim']} |")
catalog_md+=['','新代码片段：CODE_EVIDENCE.json。复用来源逐对象保存在REUSED_EVIDENCE.json，含原路径、类/方法、行号与本轮重算哈希；原包对应cross-sdk/SDK_MATRIX.json与各provenance.json。','', '未下载Uken的predictions.csv；预测输出不是原始玩家账本，也未确认可再用许可。Unity Code for Publication.R只做静态阅读，未执行合成生成或训练。','', 'MAG相关候选Incentivized Actions in Freemium Games (10.1287/msom.2020.0925)只有书目/摘要、发布页403，尚未证明与任务所指五款游戏数据一致，因此未登记为MAG数据源。']
(D/'SOURCE_CATALOG.md').write_text('\n'.join(catalog_md)+'\n',encoding='utf-8')
print(json.dumps({'sources':len(sources),'new_code':len(code),'reused_verified':len(reused),'timeline_rows':len(rows),'datasets':len(catalog),'fetches':len(fetches)},indent=2))
