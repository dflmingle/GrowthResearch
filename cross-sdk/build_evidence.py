"""Static evidence only. Preserve every original input and original graph edge."""
from pathlib import Path
import json,hashlib,re,datetime,zipfile,subprocess,difflib
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk';NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Verify existing official packages before reuse. HTTP Last-Modified is not a release date.
matrix=[]
for p in sorted((ROOT/'ThirdPartySDKs').glob('*/*/*/provenance.json')):
 d=json.loads(p.read_text(encoding='utf-8'));vendor=p.parents[2].name;name=p.parent.parent.name;version=p.parent.name
 if not (vendor in ['Adjust','AppsFlyer','Unity','Metica'] or
         vendor=='AppLovin' and name in ['MAX','Adapter-unityads-adapter','Adapter-google-adapter','Adapter-facebook-adapter'] or
         vendor=='Google' and any(s in name for s in ['Firebase','Measurement','MobileAds','AdsIdentifier','AppSet','InstallReferrer']) or vendor=='Meta'):continue
 arts=[]
 for a in d.get('artifacts',[]):
  q=ROOT/'ThirdPartySDKs'/a.get('path','');q=q if q.is_file() else p.parent/Path(a.get('path','').replace('\\','/')).name
  if not q.is_file():continue
  h=sha(q);expected=a.get('sha256')
  if expected and h!=expected:raise ValueError('original artifact changed '+str(q))
  arts.append(dict(path=q.relative_to(ROOT).as_posix(),sha256=h,url=a.get('url'),http_last_modified=a.get('http_last_modified'),bytes=q.stat().st_size))
 matrix.append(dict(sdk=vendor+'/'+name,version=version,provenance=p.relative_to(ROOT).as_posix(),artifacts=arts,
   analysis_status='reused manifest/source; selected paths analysed, not whole-SDK equivalence',
   publication_date='unknown unless official changelog says otherwise; artifact Last-Modified separately recorded',
   source_status=d.get('status'),reused=True))
for p in sorted((R/'packages').glob('*/*/provenance.json')):
 d=json.loads(p.read_text(encoding='utf-8'));arts=[]
 for q in sorted(p.parent.iterdir()):
  if q.suffix in ['.tgz','.aar','.pom'] or q.name.endswith('-sources.jar'):
   declared=next((a for a in d.get('artifacts',[]) if Path(a.get('path','')).name==q.name),{})
   arts.append(dict(path=q.relative_to(ROOT).as_posix(),sha256=sha(q),url=declared.get('url',d.get('url')),http_last_modified=declared.get('last_modified'),bytes=q.stat().st_size))
 matrix.append(dict(sdk=d['sdk'],version=d['version'],provenance=p.relative_to(ROOT).as_posix(),artifacts=arts,
  publication_date=d.get('registry_time') or 'see package CHANGELOG; registry/archive time differs from release date',
  analysis_status='new official package; selected source paths audited',reused=False))
# Authentication and independent Axon already collected elsewhere; keep original locations.
for sdk,version,folder in [('Unity Authentication','3.9.0','identity-graph/sdk/authentication/3.9.0'),('AppLovin Axon','1.3.4','nongame/sdk/axon/1.3.4')]:
 p=ROOT/folder;arts=[dict(path=q.relative_to(ROOT).as_posix(),sha256=sha(q),bytes=q.stat().st_size,url='see existing provenance / EVIDENCE_INDEX') for q in p.iterdir() if q.suffix in ['.tgz','.aar']]
 matrix.append(dict(sdk=sdk,version=version,artifacts=arts,publication_date='not independently established',analysis_status='prior identity/API analysis reused',reused=True))
(R/'SDK_MATRIX.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2),encoding='utf-8')

P='cross-sdk/packages/purchasing/5.5.1/extracted/package/'
O='cross-sdk/packages/purchasing/5.4.0/extracted/package/'
A='cross-sdk/packages/services.analytics/6.3.0/extracted/package/'
F='ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/'
D='ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/'
sources=[]
def add(id,sdk,version,path,marker,after=30,before=0,method='',meaning=''):
 p=ROOT/path;lines=p.read_text(encoding='utf-8').splitlines();hits=[i for i,s in enumerate(lines) if marker in s]
 if not hits:raise ValueError((id,path,marker))
 i=hits[0];start=max(0,i-before);end=min(len(lines),i+after)
 mm=next((x for x in matrix if x['version']==version and (sdk==x['sdk'] or sdk in x['sdk'])),None)
 archive=next((x for x in (mm or {}).get('artifacts',[]) if x['path'].endswith(('.tgz','.aar'))),None)
 s=dict(id=id,sdk=sdk,version=version,path=path,sha256=sha(p),class_or_method=method or marker,
  start_line=start+1,end_line=end,excerpt='\n'.join(f'{j+1}: {lines[j]}' for j in range(start,end)),
  official_package=archive,meaning=meaning,reviewed_utc=NOW,evidence_level='【官方SDK源码/发行包静态代码证实】',
  game_business_callsite=False,production_delivery=False,server_received=False,model_training_proven=False)
 sources.append(s);return s

add('XS01','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/PlayerData.cs','public async Task<PlayerIdentity> CreatePlayerIdentityAsync',76,method='PlayerData.CreatePlayerIdentityAsync',meaning='Consent + remote allowlist -> optional advertising/Firebase IDs -> PlayerIdentity')
add('XS02','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/PlayerData.cs','internal async Task<(string? appInstanceId',54,method='PlayerData.FetchEnabledFirebaseIdsAsync',meaning='Explicit Firebase getter assignment, allowed attributes and caches')
add('XS03','com.unity.purchasing','5.5.1',P+'Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs','public async Task<string?> FetchAppInstanceIdAsync',65,method='FirebaseAnalyticsClient.FetchAppInstanceIdAsync/FetchSessionIdValueAsync',meaning='JNI calls FirebaseAnalytics.getAppInstanceId/getSessionId; missing provider -> null')
add('XS04','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/ConnectionsSettingsClient.cs','public HashSet<string> CachedEnabledAttributes',48,method='ConnectionsSettingsClient.CachedEnabledAttributes/FetchAndCacheAsync',meaning='session-global allowlist, empty until successful async fetch, retries on later miss')
add('XS05','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/ConnectionsSettingsClient.cs','protected virtual async Task<HashSet<string>?> FetchEnabledAttributesAsync',83,method='ConnectionsSettingsClient.FetchEnabledAttributesAsync/ParseEnabledAttributes/PostAsync',meaning='project/install context -> endpoint; true attributeOverride entries -> allowlist; timeout10')
add('XS06','com.unity.purchasing','5.5.1',P+'Runtime/Stores/ServicesCore/CoreRegistryHelper.cs','public string? InstallationId =>',19,method='CoreRegistryHelper properties',meaning='Explicit IPlayerId/IExternalUserId component getters, not equal by field name')
add('XS07','com.unity.purchasing','5.5.1',P+'Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs','private protected override void SendPurchasePaidEvent',40,method='GooglePlayStoreExtendedPurchaseService.SendPurchasePaidEvent/SendPurchaseFulfilledEvent',meaning='Concrete purchase callbacks -> separate paid/fulfilled events and store receipt payload')
add('XS08','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','public async void SendPurchasePaidEvent',55,method='PurchaseEventEmitter.SendPurchasePaidEvent/SendPurchaseFulfilledEvent',meaning='Separate lifecycle variants; awaiting identity; Forward per cart item')
add('XS09','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','internal static void Forward(IAPSDKEvent iaps)',50,method='PurchaseEventEmitter.Forward/ForwardGateway/ForwardModule',meaning='protobuf bytes -> conditional EngineDiagnostics module OR HTTP gateway; schema headers; not observed send')
add('XS10','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','IAPSDKEvent BuildEnvelope(',45,method='PurchaseEventEmitter.BuildEnvelope',meaning='UUID, UTC, Firebase session/app, project/environment, consent, identities, order')
add('XS11','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','internal static PlayerIdentity MapIdentity(',16,method='PurchaseEventEmitter.MapIdentity',meaning='UGS PlayerId, external UserId, AnalyticsId and platform IDs explicitly co-packaged')
add('XS12','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','static Sku BuildSku(',23,method='PurchaseEventEmitter.BuildSku',meaning='metadata price * 1e6, currency, quantity; catalog price not guaranteed final settlement')
add('XS13','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs','static void SerializeIaps(Stream s, IAPSDKEvent e)',56,method='PurchaseEventProtobufWriter.SerializeIaps',meaning='Firebase session explicitly serialized tag4; event IDs and schema envelope')
add('XS14','com.unity.purchasing','5.4.0',O+'Runtime/Stores/Data/PlayerData.cs','string? appInstanceId = null;',65,method='PlayerData.CreatePlayerIdentityAsync (older)',meaning='Firebase fetches commented out; mere fields did not establish live bridge')
add('XS15','com.unity.purchasing','5.4.0',O+'Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs','static void SerializeIaps(Stream s, IAPSDKEvent e)',53,method='SerializeIaps (older)',meaning='Firebase session field4 not written in selected older release')
add('XS16','com.unity.purchasing','5.5.1',P+'CHANGELOG.md','## [5.5.1]',12,method='Official package CHANGELOG 5.5.1',meaning='Official acknowledgement of missing Firebase session serialization fix')
add('XS17','com.unity.purchasing','5.5.1',P+'CHANGELOG.md','## [5.4.3]',13,method='Official package CHANGELOG 5.4.3',meaning='Google Analytics ID authorization and engine Insights route evolution')
add('XS18','com.unity.services.analytics','6.3.0',A+'Runtime/AnalyticsService.cs','internal static void Initialize(CoreRegistry registry)',58,method='AnalyticsService.Initialize',meaning='Authentication/Core components -> IdentityManager -> BufferX/Dispatcher; registers Analytics IDs')
add('XS19','com.unity.services.analytics','6.3.0',A+'Runtime/IdentityManager.cs','public IdentityManager(',46,method='IdentityManager constructor/Initialize',meaning='External UserId preferred else installation ID; UGS PlayerId separate property')
add('XS20','com.unity.services.analytics','6.3.0',A+'Runtime/Runtime/BufferX.cs','if (!String.IsNullOrEmpty(m_UserIdentity.PlayerId))',18,5,method='BufferX event header writing',meaning='Distinct player ID included in event payload, not automatically equal UserId')
add('XS21','com.unity.services.analytics','6.3.0',A+'Runtime/Runtime/Dispatcher.cs','void UploadCompleted(long responseCode)',66,method='Dispatcher.UploadCompleted',meaning='2xx and4xx both discard; network/5xx retain and flush disk; client ACK != training ACK')
add('XS22','com.unity.services.analytics','6.3.0',A+'Runtime/ConsentManager.cs','void DataFrameworkConsentChanged(',54,method='ConsentManager.DataFrameworkConsentChanged',meaning='AnalyticsIntent handling; legacy flow cannot mix; not equivalent AdsIntent')
add('XS23','com.unity.services.analytics','6.3.0',A+'CHANGELOG.md','## [6.1.0]',15,method='Official Analytics changelog6.1.0',meaning='DDF integration and conditional automatic start; no unconditional collection')
add('XS24','Google/FirebaseRemoteConfig','24.0.1',F+'internal/ConfigFetchHttpClient.java','requestBodyMap.put(INSTANCE_ID, installationId);',43,method='ConfigFetchHttpClient.createFetchRequestBody',meaning='FID not Analytics app instance ID; includes Analytics user properties/custom signals')
add('XS25','Google/FirebaseRemoteConfig','24.0.1',F+'RemoteConfigComponent.java','Personalization personalization =',17,method='RemoteConfigComponent.get',meaning='value-read listener wired to personalization.logArmActive')
add('XS26','Google/FirebaseRemoteConfig','24.0.1',F+'internal/Personalization.java','public void logArmActive(',67,method='Personalization.logArmActive',meaning='assignment + internal choice event to Analytics; choice-level in-memory dedup')
add('XS27','Google/FirebaseRemoteConfig','24.0.1',F+'FirebaseRemoteConfig.java','void updateAbtWithActivatedExperiments(',23,method='FirebaseRemoteConfig.updateAbtWithActivatedExperiments',meaning='activated experiments -> FirebaseABTesting.replaceAllExperiments, optional provider')
add('XS28','AppLovin/Adapter-unityads-adapter','4.18.1.0','cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java','public void collectSignal(',13,method='UnityAdsMediationAdapter.collectSignal',meaning='Privacy first -> Unity token -> MAX callback; token not a global user ID')
add('XS29','AppLovin/Adapter-unityads-adapter','4.18.1.0','cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java','MetaData privacyMetaData =',17,method='UnityAdsMediationAdapter.updatePrivacyConsent',meaning='MAX consent and do-not-sell explicitly converted to Unity metadata')
add('XS30','AppLovin/Adapter-google-adapter','25.4.0.0','cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java','String eventId = BundleUtils.getString("event_id"',23,method='GoogleMediationAdapter ad request builder',meaning='MAX event_id -> Google placement_req_id; consent npa/rdp; request ID is not user ID')
add('XS31','AppLovin/MAX','13.7.0','cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java','public void trackEvent(String str, Map<String, ?> map, Map<String, Object> map2)',15,method='EventServiceImpl.trackEvent',meaning='Remote-resolvable axon_events determines protocol; not every name generated automatically')
add('XS32','AppLovin/MAX','13.7.0','cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java','private Map a(String str, Map map, Map map2, Map map3)',49,method='EventServiceImpl structured payload',meaning='event data + optional dedupe/user_data + visitInfo; familiar 13.6.4 path persists')
add('XS33','AppLovin/MAX','13.7.0','cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java','private void a(String str, Map map, Map map2)',35,method='EventServiceImpl scheduler/postback builder',meaning='actual request construction code; not observed production request')
add('XS34','Adjust/Android','5.8.1',D+'DeviceInfo.java','private String getFacebookAttributionId(',48,method='DeviceInfo.getFacebookAttributionId',meaning='official Facebook signature check -> exported attribution provider; no account login identity inferred')
add('XS35','Adjust/Android','5.8.1',D+'ActivityHandler.java','private void processRemoteTriggersI(',53,method='ActivityHandler.processRemoteTriggersI',meaning='backend remote_triggers label/payload -> registered main-thread callback')
add('XS36','Adjust/Android','5.8.1',D+'ActivityHandler.java','private boolean shouldProcessEventI(',18,method='ActivityHandler.shouldProcessEventI',meaning='optional finite local event dedup, not global exact-once')
add('XS37','Adjust/Android','5.8.1','cross-sdk/adjust-changelog.raw','### Version 5.8.1',36,method='Adjust official CHANGELOG',meaning='5.6 remote triggers;5.7 sharing settings;5.8 disableDeviceIdsReading')
add('XS38','Singular Android','12.17.0','cross-sdk/java/singular-1217/com/singular/sdk/Singular.java','public static boolean eventJSON(',45,method='Singular.eventJSON/customRevenue',meaning='generic event -> SingularInstance.logEvent; caller-supplied revenue flag not verified purchase')
add('XS39','Singular Android','12.17.0','cross-sdk/java/singular-1217/com/singular/sdk/Singular.java','public static void setCustomUserId(',27,method='Singular.setCustomUserId/unsetCustomUserId',meaning='explicit SDK user ID setter; no target-game callsite or automatic MMP shared identity')
add('XS40','com.unity.purchasing','5.5.1',P+'Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs','const string k_InsightsIngestUrl',53,method='PurchaseEventEmitter gateway endpoint and branch',meaning='Literal endpoint belongs to Insights, not an explicitly named Vector training endpoint')
add('XS41','com.unity.purchasing','5.5.1',P+'Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs','public async Task<string?> FetchAppIdAsync()',42,method='FirebaseAnalyticsClient.FetchAppIdAsync',meaning='FirebaseApp options ApplicationId is app/project context, not per-user identity')
add('XS42','com.unity.purchasing','5.5.1',P+'Runtime/Purchasing/Core/Purchasing/PurchaseService.cs','SendPurchasePaidEvent(order);',12,12,method='PurchaseService purchase lifecycle callsite',meaning='SDK-internal concrete callsite, not target-game runtime observation')
game=add('XS43','AppsFlyer/Android','6.17.5','rotate-rings/static/java/classes2.dex/g8/a.java','AppsFlyerLib.getInstance().logAdRevenue(',18,9,method='Rotate original g8.a revenue wrapper',meaning='Original game USD double -> AFAdRevenueData; also ad_revenue2/ad_revenue4; consumer dedup unknown')
game['game_business_callsite']=True
game['evidence_level']='【原版游戏代码证实】'
game['game']='Rotate Rings 1.2.4'
add('XS44','Adjust/Android','5.8.1',D+'PackageBuilder.java','PackageBuilder.addString(parameters, "fb_id", deviceInfo.fbAttributionId);',12,6,method='PackageBuilder session parameters',meaning='Explicit provider return -> fb_id request parameter; conditional null filtering')

# Reuse previously disassembled actual game callsites instead of re-decompiling whole APKs.
old=json.loads((ROOT/'ThirdPartySDKs/BUSINESS_TRACES.json').read_text(encoding='utf-8'))
chosen=[]
for slug in ['meowdoku','rotate-rings','car-race']:
 matches=[x for x in old if x['slug']==slug and any(k in ' '.join(x.get('matches',[])) for k in ['setCustomerUserId','logAdRevenue','setUserIdentifier','trackAdRevenue'])]
 for x in matches[:2]:
  p=ROOT/'ThirdPartySDKs'/x['file'];lines=p.read_text(encoding='utf-8').splitlines()
  chosen.append({**x,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'game_business_callsite':True,'scope':'actual original DEX callsite static evidence; runtime delivery unknown'})
(R/'GAME_CALLS_REUSED.json').write_text(json.dumps(chosen,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'CODE_EVIDENCE.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')

# Selected public API deltas from the actual bytecode (not method body equivalence).
api=[]
for sdk,a,b,classes in [
 ('MAX','ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar','ThirdPartySDKs/AppLovin/MAX/13.7.0/classes.jar',['com.applovin.sdk.AppLovinSdk','com.applovin.sdk.AppLovinSdkSettings','com.applovin.sdk.AppLovinEventService']),
 ('Adjust','ThirdPartySDKs/Adjust/Android/5.5.0/classes.jar','ThirdPartySDKs/Adjust/Android/5.8.1/classes.jar',['com.adjust.sdk.Adjust','com.adjust.sdk.AdjustConfig','com.adjust.sdk.AdjustEvent'])]:
 for c in classes:
  x=subprocess.run(['javap','-classpath',str(ROOT/a),c],capture_output=True,text=True)
  y=subprocess.run(['javap','-classpath',str(ROOT/b),c],capture_output=True,text=True)
  if x.returncode or y.returncode:raise RuntimeError(c+' javap failed')
  aa=[s.strip() for s in x.stdout.splitlines() if 'public ' in s];bb=[s.strip() for s in y.stdout.splitlines() if 'public ' in s]
  api.append(dict(sdk=sdk,before=a,after=b,class_name=c,added=sorted(set(bb)-set(aa)),removed=sorted(set(aa)-set(bb))))
(R/'API_DELTAS.json').write_text(json.dumps(api,ensure_ascii=False,indent=2),encoding='utf-8')
print('matrix',len(matrix),'source excerpts',len(sources),'reused game callsites',len(chosen))
