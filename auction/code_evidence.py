from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent
R=ROOT/'auction'
rows=[]
def add(label,path,start,end,meaning):
 p=ROOT/path;s=p.read_text().splitlines()
 rows.append(dict(id=label,path=path,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),start_line=start,end_line=min(end,len(s)),
                  meaning=meaning,text='\n'.join(f'{i+1}: {l}' for i,l in enumerate(s) if start<=i+1<=end)))
M='auction/sdk/MAX-13.6.4/java/com/applovin/impl/'
L='auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/'
U='ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/'
for args in [
 ('MAX-fetch-payload',M+'a6.java',113,156,'collector, signal_data, mediation_stats; SDK-cloud private JSON, not Exchange OpenRTB'),
 ('MAX-fetch-send',M+'a6.java',182,212,'POST request construction; timeout config is SDK-cloud layer'),
 ('MAX-fetch-adunit-history',M+'a6.java',221,270,'ad unit, previous requests/winner, optional user_data'),
 ('MAX-waterfall-parse',M+'l6.java',40,86,'server ads array -> client mediated ad objects'),
 ('MAX-waterfall-loading',M+'l6.java',171,219,'loaded response and failover cache path; not server highest bid sorter'),
 ('MAX-signal-timeout',M+'mediation/MediationServiceImpl.java',221,310,'adapter eligibility, signal callback, timeout'),
 ('MAX-waterfall-report',M+'mediation/MediationServiceImpl.java',322,377,'waterfall metrics and response latency postback construction'),
 ('MAX-expiration',M+'g3.java',25,36,'ad_expiration_ms from ad/config'),
 ('MAX-expiration-remaining',M+'g3.java',91,115,'remaining lifetime from elapsed realtime; not universal 4h guarantee'),
 ('MAX-revenue-response',M+'c3.java',125,153,'revenue and precision accessors, not final settlement proof'),
 ('MAX-bid-response',M+'c3.java',232,246,'bid_response accessor; original method names are obfuscated'),
 ('LP-auction-candidates',L+'AbstractC0163i3.java',863,931,'candidate preparation and auction handler invocation'),
 ('LP-fallback',L+'AbstractC0163i3.java',944,992,'auction state, response waterfall and fallback on error'),
 ('LP-response-notices',L+'C0325q2.java',160,190,'original com.ironsource.q2 response parser: price/adMarkup/serverData/loadTimeout and nurl/lurl/burl arrays'),
 ('LP-timeout-config','auction/sdk/LevelPlay-9.4.0/java/com/ironsource/Ve.java',485,503,'auctionTimeout default parse is SDK-cloud layer; not DSP tmax'),
 ('Unity-request',U+'domain/AndroidGetAdRequest.kt',27,72,'protobuf ad request with placement, opportunity, session and device/TCF'),
 ('Unity-bid-token',U+'domain/AndroidBuildHeaderBiddingToken.kt',34,104,'init/full/limited session token, pii, TCF, format, counters'),
 ('Unity-token-serialization',U+'domain/CommonGetHeaderBiddingToken.kt',15,39,'protobuf bytes -> base64 with version prefix; not encryption or model weights'),
 ('Unity-shared-data',U+'domain/AndroidGetUniversalRequestSharedData.kt',19,40,'consent and allowed PII shared layer'),
]:add(*args)
(R/'CODE_EVIDENCE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('code excerpts',len(rows))
