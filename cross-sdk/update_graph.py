from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
baseline=R/'EVIDENCE_GRAPH.before47.json'
g=json.loads(baseline.read_text(encoding='utf-8'))
evidence=json.loads((R/'CODE_EVIDENCE.json').read_text(encoding='utf-8'))
old_nodes={n['id'] for n in g['nodes']}
def node(id,label,company,stage):
 if id not in old_nodes:g['nodes'].append(dict(id=id,label=label,company=company,stage=stage));old_nodes.add(id)
for a in [
 ('U_ugs_identity','Authentication/Core identity components','Unity','association'),
 ('U_analytics_identity','UGS Analytics IdentityManager','Unity','association'),
 ('U_analytics_collect','UGS Analytics buffer and collect endpoint','Unity','measurement'),
 ('U_firebase_ids','Firebase Analytics getters','Google','data_source'),
 ('U_iap_identity','IAP PlayerIdentity and purchase envelope','Unity','association'),
 ('U_connections','IAP remote connections allowlist','Unity','configuration'),
 ('U_insights','IAP Insights protobuf and gateway/runtime','Unity','measurement'),
 ('G_frc','Firebase Remote Config and assignment metadata','Google','configuration'),
 ('G_fa','Firebase Analytics events/user properties','Google','measurement'),
 ('G_google_request','Google Ads placement request context','Google','auction'),
 ('M_meta_provider','Facebook signed AttributionId provider','Meta','association'),
 ('M_adjust','Adjust SDK events/device request context','Adjust','measurement'),
 ('M_remote','Adjust remote trigger response','Adjust','configuration'),
 ('M_af','AppsFlyer ad revenue API','AppsFlyer','measurement'),
 ('GAME_rotate','Rotate Rings original revenue wrapper','game','business'),
 ('S_singular','Singular event/custom user APIs','Singular','measurement')]:node(*a)
node('S_developer_input','Developer-supplied event JSON and custom user ID','developer','data_source')

def edge(id,a,b,claim,refs,sdk,version,chain,conditions,old_edges,business=False,request=False,status='sdk',missing='Production delivery, server interpretation and training use not established'):
 ss=[next(x for x in evidence if x['id']==r) for r in refs]
 g['edges'].append(dict(id=id,source=a,target=b,claim=claim,status=status,
  evidence_level='【原版游戏代码证实】' if business else '【无法确认】' if status=='unknown' else '【官方SDK代码证实】',
  source_ids=refs,sdk=sdk,version=version,sha256=[dict(path=x['path'],sha256=x['sha256'],official_package=x['official_package']) for x in ss],
  class_method_lines=[dict(path=x['path'],method=x['class_or_method'],start_line=x['start_line'],end_line=x['end_line']) for x in ss],
  data_provider=a,data_receiver=b,explicit_call_chain=chain,permission_conditions=conditions,
  six_layers=dict(sdk_capability=status!='unknown',actual_game_business_callsite=business,
   request_construction_code=request,production_successful_send=False,server_received=False,server_model_training=False),
  production_actual_proven=False,observed_target_game_delivery=False,
  production_evidence='static analysis only, SDK never initialized',applies_to='original game static callsite' if business else 'standalone SDK capability, not target-game integration',
  supplements_original_edges=old_edges,missing_evidence=missing,diagram_style='dashed' if status=='unknown' else 'solid',reviewed_utc=now))

edge('XU01','U_ugs_identity','U_analytics_identity','Authentication PlayerId and Core external UserId explicitly consumed separately by Analytics',['XS18','XS19'],'Unity Analytics','6.3.0','CoreRegistry.IPlayerId/IExternalUserId -> IdentityManager; UserId=ExternalId else InstallId; PlayerId separate','Components available; analytics consent; project scope',['U03','U04','U15'])
edge('XU02','U_analytics_identity','U_analytics_collect','Identity values included in analytics event buffer and dispatcher',['XS18','XS20','XS21','XS22'],'Unity Analytics','6.3.0','IdentityManager -> BufferX userID/unityPlayerID -> Dispatcher POST collect','AnalyticsIntent or valid legacy flow; no actual events generated',['U04','U15'],request=True)
edge('XU03','U_firebase_ids','U_iap_identity','Firebase instance/session/app getters explicitly assigned into IAP identity/envelope',['XS01','XS02','XS03','XS41'],'Unity IAP + Firebase','5.5.1','JNI Firebase getters -> PlayerData -> PlayerIdentity -> envelope; appId is app context','AdsIntent granted AND enabledAttributes AND Firebase available; optional results may be null',['U03','U09'])
edge('XU04','U_connections','U_iap_identity','Remote true attributeOverride values gate IAP identifier collection',['XS04','XS05','XS01'],'Unity IAP','5.5.1','connections settings response -> bool allowlist -> EnabledAttributes -> conditional getters','empty before fetch; project/install context; ads consent also needed',['U08','U09'],request=True)
edge('XU05','U_ugs_identity','U_iap_identity','UGS player/external/analytics IDs co-packaged with purchase identity',['XS06','XS11','XS01'],'Unity IAP','5.5.1','CoreRegistryHelper.PlayerId/ExternalUserId and AnalyticsService.GetAnalyticsUserID -> MapIdentity','Optional component/compile flags; IDs remain distinct, no universal account inferred',['U03','U09','U15'])
edge('XU06','U_iap_identity','U_insights','Purchase lifecycle builds protobuf with identity, transaction, metadata price and consent; gateway or runtime path',['XS07','XS08','XS09','XS10','XS12','XS13','XS40','XS42'],'Unity IAP','5.5.1','PurchaseService -> GooglePlayStoreExtendedPurchaseService -> PurchaseEventEmitter -> protobuf -> ForwardGateway or EngineDiagnostics','Concrete SDK lifecycle; metadata price not final settlement; compile branch; no transport success observed',['U05','U09'],request=True)
edge('XU07','U_insights','U_predict','Exact IAP Insights rows into Vector feature/label training remain unproven',['XS09','XS40'],'Unity IAP / Vector','5.5.1','Insights receiver -> UNKNOWN training dataset -> Vector','Official general IAP/Vector product linkage in S21 does not prove per-row training',['U09'],status='unknown',missing='dataset lineage, production consumer, allowed purposes, label precision/maturity and training job')
edge('XG01','G_fa','G_frc','Remote Config fetch includes Analytics user properties and custom signals with Firebase installation context',['XS24'],'Firebase Remote Config','24.0.1','Analytics properties map + FID + customSignals -> createFetchRequestBody','Analytics provider must be available; FID is not Analytics app instance ID',['U04'],request=True)
edge('XG02','G_frc','G_fa','Personalization value reads and activated ABT metadata call Analytics/ABT APIs',['XS25','XS26','XS27'],'Firebase Remote Config','24.0.1','parameter listener -> logArmActive -> personalization_assignment/_fpc; activate -> replaceAllExperiments','default supported app/namespace; nonempty choiceId; local choice dedup; optional connector',['U08'])
edge('XA01','A_max','U_ads','MAX Unity adapter passes privacy and asks Unity SDK token then returns it to MAX',['XS28','XS29'],'MAX UnityAds adapter','4.18.1.0','MAX signal parameters -> Unity metadata -> UnityAds.getToken(TokenConfiguration(format)) -> MAX onSignalCollected','consent translated only when known; actual adapter selected/runtime unobserved',['A02','U01','U03'])
edge('XA02','A_max','G_google_request','MAX server event_id explicitly assigned to Google placement_req_id',['XS30'],'MAX Google adapter','25.4.0.0','serverParameters.event_id -> networkExtras.placement_req_id -> Google request builder','nonempty event_id; npa/rdp conditions; request correlation not user identity',['A02'],request=True)
edge('XA03','M_meta_provider','M_adjust','Adjust can read signed official Facebook app attribution provider as fbAttributionId',['XS34','XS44'],'Adjust Android','5.8.1','official package/signature -> ContentResolver aid -> fbAttributionId -> PackageBuilder.fb_id','reading enabled; package visible/provider accessible; all errors return null; not Facebook account ID',['A02'],request=True)
edge('XA04','M_remote','M_adjust','Backend remote_triggers can dispatch label/payload to registered callback',['XS35','XS37'],'Adjust Android','5.8.1','response.json.remote_triggers -> AdjustRemoteTrigger -> main-thread listener','nonempty trigger and listener registered; target-game listener not established',['A08'])
edge('XM01','GAME_rotate','M_af','Original Rotate USD revenue double and network -> AFAdRevenueData; parallel custom events separate',['XS43'],'AppsFlyer Android / Rotate Rings','6.17.5 / game1.2.4','g8.a wrapper -> logAdRevenue(AFAdRevenueData(network,APPLOVIN_MAX,USD,d)); ad_revenue2/4 separate','SDK instance exists; monetary precision upstream unknown; catch/error branches',['A06','A08','U05'],business=True)
edge('XM02','S_developer_input','S_singular','Standalone Singular accepts event JSON and developer CUID; no automatic cross-MMP ID relation proven',['XS38','XS39'],'Singular Android','12.17.0','eventJSON -> SingularInstance.logEvent; setCustomUserId -> saveCustomUserId','SDK initialized; nonempty event; no target-game integration evidence',['A08'],missing='Full internal queue/transport, target-game usage, partner postback and training use')

for s in evidence:
 g['sources'].append({**s,'evidence_priority':'B','product':s['sdk']+' '+s['version'],'reviewed_utc':now,
  'source_date':'exact package/version; release date in provenance/changelog','url':(s['official_package'] or {}).get('url')})
g['schema_version']='1.1'
g['cross_sdk_extension']=dict(utc=now,baseline='cross-sdk/EVIDENCE_GRAPH.before47.json',baseline_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),added_edges=15,added_sources=len(evidence),notes='Old nodes, edges and sources preserved. No production or training flags promoted.')
(ROOT/'prediction-system/EVIDENCE_GRAPH.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'EVIDENCE_GRAPH.after52.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
print('updated graph',len(g['nodes']),'nodes',len(g['edges']),'edges',len(g['sources']),'sources')
