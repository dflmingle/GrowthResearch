"""Append-only client trace evidence with package provenance and scope."""
from pathlib import Path
import datetime, hashlib, json, re, zipfile

R=Path(__file__).resolve().parent.parent;O=R/'client-growth'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
U='ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/'
G=json.loads((O/'EVIDENCE_GRAPH.before_client56.json').read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')

PACKAGES={
 'UA417':'Unity/Ads/4.17.0','UA418':'Unity/Ads/4.18.1','MAX':'AppLovin/MAX/13.6.4',
 'LP950':'Unity/LevelPlay/9.5.0','MU':'AppLovin/Adapter-unityads-adapter/4.18.1.0',
 'MG':'AppLovin/Adapter-google-adapter/25.4.0.0',
}
packages={}
for ident,folder in PACKAGES.items():
 base=R/'ThirdPartySDKs'/folder;p=json.loads((base/'provenance.json').read_text('utf-8'))
 artifacts=[]
 for a in p['artifacts']:
  path=R/'ThirdPartySDKs'/Path(a['path'].replace('\\','/'))
  if path.suffix not in ('.aar','.jar'):continue
  assert sha(path)==a['sha256'],path
  artifacts.append(dict(a,path=path.relative_to(R).as_posix()))
 packages[ident]=dict(sdk=folder,version=p['version'],artifacts=artifacts,
   scope='official standalone artifacts; not proof target-game integration or online enablement')

specs=[
 ('01','UA417',U+'ads/core/domain/AndroidBuildHeaderBiddingToken.kt',33,89,'AndroidBuildHeaderBiddingToken.invoke','Token outer fields, current state, cached static information and seq/wins/starts snapshot.'),
 ('02','UA417',U+'ads/core/domain/CommonGetHeaderBiddingToken.kt',13,28,'CommonGetHeaderBiddingToken.invoke','Protobuf bytes -> base64 -> version2 prefix; opaque nested values not decoded.'),
 ('03','UA417',U+'ads/core/data/repository/AndroidSessionRepository.kt',77,175,'AndroidSessionRepository session/counters','Memory-local counters; explicit increment/reset; no proven global player history.'),
 ('04','UA417',U+'ads/core/data/repository/AndroidCampaignRepository.kt',11,50,'AndroidCampaignRepository','Map by opportunity ID; loaded/shown partition; explicit removal; no persistent full-game history proven.'),
 ('05','UA417',U+'ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt',405,415,'HB WebView counter hooks','WebView exposed hooks increment/reset token counters; exact viewer-side call conditions not public here.'),
 ('06','UA417',U+'ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt',467,494,'updateCampaignState','Viewer provides base64 data/dataVersion; native client sets placement/opportunity; contents opaque.'),
 ('07','UA417',U+'ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt',274,277,'markCampaignStateShown','Show timestamp writer; can later contribute to next-request state.'),
 ('08','UA417',U+'ads/core/domain/AndroidHandleGatewayAdResponse.kt',204,215,'AndroidHandleGatewayAdResponse.invoke','Load success writes timestamp before storing loaded ad.'),
 ('09','UA417',U+'ads/core/data/repository/AndroidDeviceInfoRepository.kt',21,48,'AndroidDeviceInfoRepository','Fresh dynamic read vs cached static; AllowedPii starts default-empty; PII provider uses current allowlist.'),
 ('10','UA417',U+'ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt',20,58,'AndroidPrivacyDeviceInfoDataSource.fetch','Serialization population gates for ad ID/fid/App Set; not full read/consent audit.'),
 ('11','UA417',U+'ads/core/data/datasource/AndroidFIdDataSource.kt',10,29,'AndroidFIdDataSource.invoke','Reflection bridge calls getAppInstanceId, not FirebaseInstallations.getId.'),
 ('12','UA417',U+'services/core/fid/Constants.kt',1,14,'FId Constants','Target explicitly FirebaseAnalytics; fid name must not be expanded as FirebaseInstallations ID.'),
 ('13','UA417',U+'services/core/fid/FIdBridge.kt',7,24,'FIdBridge.getAppInstanceId','Explicit FirebaseAnalytics task getter via generic bridge.'),
 ('14','UA417',U+'ads/core/data/datasource/CachedFIdDataSource.kt',11,35,'CachedFIdDataSource','Constructor prewarms delegate; returns null until completed. Field gate is not proof getter never runs beforehand.'),
 ('15','UA417',U+'services/core/di/ServiceProvider.kt',1188,1195,'ServiceProvider FIdDataSource binding','Actual DI binds cached Android Firebase Analytics bridge.'),
 ('16','UA417',U+'ads/core/domain/AndroidHandleGatewayUniversalResponse.kt',28,54,'HandleGatewayUniversalResponse','Server response can update allowedPii/session counters/sessionToken/privacy/cache; opaque contents and production states unknown.'),
 ('17','UA417',U+'ads/core/domain/CommonInitAwaitingGetHeaderBiddingToken.kt',40,105,'CommonInitAwaitingGetHeaderBiddingToken','Initialization wait bounded by config; snapshot built after await; callback on ready; not real-time auction timestamp.'),
 ('18','UA417',U+'ads/core/domain/AndroidGetLimitedSessionToken.kt',16,35,'AndroidGetLimitedSessionToken.invoke','Session/install/context fields when full token absent; limited does not mean no data.'),
 ('19','UA417',U+'ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt',73,140,'AndroidStaticDeviceInfoDataSource static fields','Bundle/version/model/display/stores/install source etc; OS build fingerprint is not proof of custom fingerprinting graph.'),
 ('20','UA417',U+'ads/core/data/datasource/AndroidDynamicDeviceInfoDataSource.kt',57,99,'AndroidDynamicDeviceInfoDataSource.fetch','Language/network/free memory/battery/foreground/tracking limits etc read into proto.'),
 ('21','UA417',U+'ads/core/domain/AndroidGetAdRequest.kt',31,65,'AndroidGetAdRequest.invoke','Ad opportunity request fields -> UniversalRequest; private protocol distinct from server OpenRTB.'),
 ('22','UA418','client-growth/java/unity-4181/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.java',178,350,'4.18.1 AndroidBuildHeaderBiddingToken.invoke','Actual AAR decompile confirms same inspected outer token fields/counters; not complete version equality.'),
 ('23','MU','cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java',101,109,'UnityAdsMediationAdapter.collectSignal','MAX context -> privacy update -> Unity format token -> signal callback; no token feature decoding.'),
 ('24','MU','cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java',268,295,'UnityAdsMediationAdapter.updatePrivacyConsent','Conditional MAX hasUserConsent/doNotSell to Unity metadata; null values not fabricated consent.'),
 ('25','MG','cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java',224,228,'GoogleMediationAdapter.collectSignal','QueryInfo generation accepts configured AdRequest; Google signal content opaque.'),
 ('26','MG','cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java',458,505,'GoogleMediationAdapter.createAdRequestWithParameters','Bidding query_info_type and placement_req_id; event_id request association not player ID.'),
 ('27','MAX','client-growth/java/max-dispatch/com/applovin/impl/mediation/MediationServiceImpl.java',221,305,'MediationServiceImpl.collectSignal','Cache first; initialization conditions; callback success caches; bounded signal timeout.'),
 ('28','MAX','client-growth/java/max-history-cache/com/applovin/impl/g5.java',18,73,'g5 SignalCacheManager','Cache only TTL>0; scoped key by format/unit/all; stale returns null; no persistent user graph.'),
 ('29','MAX','client-growth/java/max-1364/com/applovin/impl/i5.java',14,39,'i5 signal provider spec','Per-provider signal TTL/cache overrides and initialized-only preference.'),
 ('30','MAX','client-growth/java/max-1364/com/applovin/impl/v3.java',85,117,'MAX configuration defaults','Signal expiration default -1, cache level AD_FORMAT; ad expiration4h unrelated to signal TTL.'),
 ('31','MAX','client-growth/g5$c.javap.txt',9,43,'g5$c bytecode cache age check','SystemClock.elapsedRealtime; expiry when age>TTL, independent wall clock.'),
 ('32','MAX','client-growth/java/max-1364/com/applovin/impl/a6.java',103,157,'a6 mediated ad request body','signal_data and optional mediation_stats are serialized into next ad request.'),
 ('33','MAX','client-growth/java/max-1364/com/applovin/impl/a6.java',164,212,'a6.run','POST request builder scheduled with mediation endpoint/backup/timeouts; static only.'),
 ('34','MAX','client-growth/java/max-1364/com/applovin/impl/a6.java',221,268,'a6.ad_info/user_data','Previous request, previous loaded/winning network, queue info; optional user_data gate; not rival bid prices.'),
 ('35','MAX','client-growth/java/max-history-cache/com/applovin/impl/w3.java',24,29,'w3 metric names and scopes','ars/session-install, ar/session, ttdasi_ms/session; ar updated by count increment not money.'),
 ('36','MAX','client-growth/java/max-history-cache/com/applovin/impl/y3.java',103,147,'y3 metric update/read','a(w3,x3) increments long by1; read defaults to session scope; no revenue interpretation.'),
 ('37','MAX','client-growth/java/max-history-cache/com/applovin/impl/c5.java',788,798,'c5 umsm flag','umsm default false (bool defined Boolean.FALSE); production override unknown.'),
 ('38','MAX','client-growth/java/max-dispatch/com/applovin/impl/mediation/MediationServiceImpl.java',408,417,'MediationServiceImpl timestamp stats write','ttdasi_ms assigned wall time since SDK reference M under umsm; no label of future user LTV.'),
 ('39','LP950','client-growth/java/lp-follow/com/ironsource/C0318q3.java',14,48,'LevelPlay9.5 q3 collector','Parallel worker callable tokens and timeout results; not complete auction field semantics.'),
 ('40','LP950','client-growth/java/lp-follow/com/ironsource/C0118g2.java',70,100,'LevelPlay9.5 g2 bidding data','Provider instance -> bidding map; opaque per-provider data, not decoded long-term model inputs.'),
 ('41','LP950','client-growth/java/levelplay-950/com/ironsource/Q1.java',161,187,'LevelPlay9.5 Q1 collection completion','Collection success/errors/timeouts retained per network before callback.'),
]
docs=[
 ('42','vector/doc-roas-campaign-best-practices.txt',36,70,'ROAS prelaunch data and all-source sharing','https://docs.unity.com/en-us/grow/acquire/campaigns/roas/roas-campaign-best-practices.md'),
 ('43','client-growth/unity-attribution-types.md',28,80,'Attributed/unattributed/organic definitions','https://docs.unity.com/en-us/grow/acquire/partner-integration/attribution/introduction.md'),
 ('44','vector/doc-integrate-appsflyer-with-unity.txt',113,183,'Unity AppsFlyer install/event sharing scopes and maps','https://docs.unity.com/en-us/grow/acquire/partner-integration/appsflyer/integrate-appsflyer-with-unity.md'),
 ('45','vector/doc-integrate-appsflyer-with-unity.txt',185,273,'Unity AppsFlyer revenue connection/permissions','https://docs.unity.com/en-us/grow/acquire/partner-integration/appsflyer/integrate-appsflyer-with-unity.md'),
 ('46','vector/doc-integrate-adjust-with-unity.txt',43,115,'Unity Adjust all-sources and dedicated revenue mapping','https://docs.unity.com/en-us/grow/acquire/partner-integration/adjust/integrate-adjust-with-unity.md'),
 ('47','vector/doc-intro-to-roas-campaigns.txt',79,116,'Learning maturity/thresholds','https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md'),
 ('48','vector/doc-send-postbacks.txt',28,109,'Unity S2S IDs/time/attribution/revenue contract','https://docs.unity.com/en-us/grow/acquire/partner-integration/custom/send-postbacks.md'),
 ('49','axon/doc-appsflyer.txt',183,241,'AppLovin AppsFlyer all-sources mapping and excluded purchase revenue','https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/appsflyer'),
 ('50','axon/adjust-applovin.txt',89,127,'Adjust Axon partner/source choices and unmapped events','https://help.adjust.com/en/partner-setup/applovin'),
 ('51','nongame/applovin-axon-about.txt',54,73,'Axon model inputs/advertiser-shared data and explicit exclusions','https://legal.applovin.com/about-applovins-axon-ai/'),
 ('52','axon/doc-in-app-purchase-revenue-sharing.txt',13,26,'AppLovin checkout revenue semantic restrictions','https://support.applovin.com/en/growth/promoting-your-apps/troubleshooting/in-app-purchase-revenue-sharing'),
 ('53','vector/unity-vector-correct.txt',10,43,'Vector product correlations and postback sources','https://unity.com/products/unity-ads/vector'),
]
sources=[]
for ident,package,path,a,b,method,meaning in specs:
 p=R/path;lines=p.read_text('utf-8-sig').splitlines();b=min(b,len(lines));assert a<=b
 if package not in packages:raise ValueError(package)
 row=dict(id='CGS'+ident,product=packages[package]['sdk'],version=packages[package]['version'],path=path,
  sha256=sha(p),start_line=a,end_line=b,class_or_method=method,meaning=meaning,
  excerpt='\n'.join(f'{i}: {lines[i-1]}' for i in range(a,b+1)),official_packages=packages[package]['artifacts'],
  evidence_level='【SDK代码证实】',evidence_priority='B',reviewed_utc=NOW,
  actual_game_business_callsite=False,production_delivery=False,server_received=False,model_training_proven=False,
  six_layers=dict(sdk_capability=True,actual_game_business_callsite=False,request_construction_code=False,
    production_successful_send=False,server_received=False,server_model_training=False),
  source_view='official sources JAR' if '/sources/' in path else 'decompiler or javap view of official release')
 sources.append(row)
for ident,path,a,b,title,url in docs:
 p=R/path;lines=p.read_text('utf-8-sig').splitlines();b=min(b,len(lines))
 date=next((l.split(': ',1)[1] for l in lines[:10] if l.startswith('last_updated: ')),None)
 sources.append(dict(id='CGS'+ident,product=title,path=path,sha256=sha(p),start_line=a,end_line=b,url=url,
  excerpt='\n'.join(f'{i}: {lines[i-1]}' for i in range(a,b+1)),evidence_level='【官方公开证实】',evidence_priority='A',
  source_date=date or 'page date not stated; cached/reviewed 2026-11-19',reviewed_utc=NOW,
  production_delivery=False,server_received=False,model_training_proven=False,
  scope='official product/integration statement, not observed target-game enablement'))
save(O/'PACKAGE_PROVENANCE.json',packages);save(O/'SOURCE_EVIDENCE.json',sources)
cat=['# 客户端买量痕迹证据目录','','新编号CGS不替换原S/XS/C53S。代码可达性不是生产送达或训练证明。','']
for s in sources:
 cat += [f'<a id="{s["id"].lower()}"></a>',f'## {s["id"]} · {s.get("class_or_method",s["product"])}','',
   f'[{s["path"]}:L{s["start_line"]}](../{s["path"]})','',s['evidence_level']+' '+s.get('meaning',s['product']),
   '',f'文件SHA256：`{s["sha256"]}`。','']
 if 'url' in s:cat += [f'[官方原文]({s["url"]})；资料日期：{s["source_date"]}。','']
 for a in s.get('official_packages',[]):cat += [f'原包 [{a["path"]}](../{a["path"]}) SHA256 `{a["sha256"]}`；[发行来源]({a["url"]})。','']
(O/'SOURCE_CATALOG.md').write_text('\n'.join(cat),'utf-8')
print('Sources',len(sources),'packages',len(packages),'all reused release hashes verified')
