from pathlib import Path
import json, re, csv, hashlib
R=Path(__file__).resolve().parent
ROOT=R.parent

# Capture exact local line references. These are excerpts, not runtime observations.
selections={
 'ad_request_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdRequest.kt',r'sessionCounters|DeviceInfo|placementId|campaignState|tcf|mediationAdUnitId|extras'),
 'bid_token_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt',r'tokenId|clientInfo|timestamps|pii|sessionToken|limitedSessionToken|campaignState|tcf|mediation|tokenCounters'),
 'shared_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt',r'Consent|pii|sessionToken|limitedSessionToken|timestamps'),
 'operative_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.kt',r'eventId|eventType|trackingToken|additionalData|sid|DeviceInfo|campaignState'),
 'queue_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/OperativeEventObserver.kt',r'isRunning|operativeEvents|fullRequest|universalRequestDataSource.set|backgroundWorker|catch|universalRequestEventSender'),
 'sender_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/UniversalRequestEventSender.kt',r'universalRequestTtlValidator|gatewayClient.request|requestPolicy|GatewayException|handleGatewayEventResponse'),
 'job_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/work/OperativeEventJob.kt',r'doWork|getOperativeRequestPolicy|catch|retry'),
 'hb_encoding_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonGetHeaderBiddingToken.kt',r'scarEligible|fetchSignals|toBase64|HB_TOKEN_VERSION'),
 'ad_callbacks_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/LegacyShowUseCase.kt',r'ShowEvent\.(Started|Clicked|Completed)|onUnityAdsShowClick|onUnityAdsShowComplete|onUnityAdsShowStart'),
 'ad_bridge_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt',r'sendOperativeEvent|SPECIFIED_BY_AD_PLAYER|additionalData'),
 'privacy_417':('ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java',r'allowedToSendPii|shouldSendNonBehavioral|ADVERTISING_TRACKING|getAdvertisingTrackingId'),
 'ad_request_418':('vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/ads/core/domain/AndroidGetAdRequest.java',r'setSessionCounters|setStaticDeviceInfo|setDynamicDeviceInfo|setPlacementId|setCampaignState|setTcf|setMediationAdUnitId|putAllExtras'),
 'operative_418':('vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.java',r'setEventId|setEventType|setTrackingToken|setAdditionalData|setSid|setCampaignState'),
 'runtime_consent':('vector/unity-runtime-cs-release.html',r'GetConsentState|SetConsentState|consentStateChanged|NativeMethod'),
 'runtime_state':('vector/unity-runtime-cs-release-state.html',r'AdsIntent|AnalyticsIntent|Unspecified'),
}
for ver,folder in [('9.3.0','LevelPlay'),('9.4.0','Dependency-mediation-sdk'),('9.5.0','LevelPlay')]:
 selections['levelplay_'+ver]=('vector/sdk/Unity/'+folder+'/'+ver+'/java/com/unity3d/mediation/LevelPlayAdInfo.java',r'getRevenue|getPrecision|getCountry|getAuctionId|getAdNetwork|optDouble\("revenue"\)|opt\("precision"\)')
selections['levelplay_privacy_950']=('vector/sdk/Unity/LevelPlay/9.5.0/java/com/unity3d/mediation/LevelPlay.java',r'setConsent|setDynamicUserId|setMetaData|void init')
out=[]
for key,(rel,pattern) in selections.items():
 p=ROOT/rel
 if not p.exists():out.append({'id':key,'path':rel,'error':'not present in selected decompilation'});continue
 lines=p.read_text(encoding='utf-8').splitlines()
 hits=[{'line':i,'text':s.strip()} for i,s in enumerate(lines,1) if re.search(pattern,s) and len(s)<1000]
 out.append({'id':key,'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'hits':hits})
(R/'CODE_EVIDENCE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')

fetches={}
for p in sorted(R.glob('fetches-*.json')):
 for row in json.loads(p.read_text(encoding='utf-8')):
  if isinstance(row,dict) and row.get('status')==200:fetches[row['id']]=row
(R/'PUBLIC_SOURCE_INDEX.json').write_text(json.dumps(fetches,ensure_ascii=False,indent=2),encoding='utf-8')

quarters=[('2025Q1',435,285,-4,186.934,None,1158.974,71),('2025Q2',440.944,287,-4,201.334,None,1259,77),('2025Q3',470.615,318,6,226.770,None,1405,68),('2025Q4',503,338,11,None,None,1658,66),('2026Q1',508.238,352,24,278.681,49,1842,59),('2026Q2',546.468,389,35,328.955,63,1924,53),('2026Q3',622.092,457,44,431.502,90,2185,55)]
rows=[]
for q,total,grow,yoy,strategic,syoy,app,ayoy in quarters:
 u='unity-q4-2025-final' if q=='2025Q4' else 'unity-ir-'+q[:4]+'-q'+q[-1]
 a='app-ir-'+q[:4]+'-q'+q[-1]
 assert u in fetches and a in fetches
 rows.append(dict(quarter=q,unity_total_usdm=total,unity_grow_usdm_rounded=grow,unity_grow_yoy_pct=yoy,unity_strategic_grow_usdm=strategic,unity_strategic_grow_yoy_pct=syoy,applovin_advertising_continuing_usdm=app,applovin_advertising_yoy_pct=ayoy,unity_source=fetches[u]['url'],applovin_source=fetches[a]['url'],notes='2025 strategic figures are 2026 restated comparators; other cells keep source precision; not advertiser ROAS'))
with (R/'FINANCIAL_COMPARISON.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('code groups',len(out),'public sources',len(fetches),'financial rows',len(rows))
