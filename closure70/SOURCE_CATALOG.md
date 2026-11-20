# 70号新增与复用证据索引

审查时间：2026-11-20T04:33:25.081125+00:00。全部新增资料为公开文档GET或已有发行包静态分析；没有生产事件或真实身份采集。

## 新官方来源

| ID | URL | 原件 | SHA256 | 可证上限 |
|---|---|---|---|---|
| CL70S01 | https://www.sfu.ca/stat-actsci.html | closure70/sources/sfu-stat-current.raw | `383b61fa8cbba7d01849502a17d024b86649a42e995178467dbcd441324275e7` | Correct present department URL discovered through official SFU directory;not confirmation of2015 data custodian |
| CL70S02 | https://www.sfu.ca/stat-actsci/contact-us.html | closure70/sources/sfu-contact.raw | `55104cdf860405365f4051dac2418e11f3b68e4b53cab9c6ec6fac83c040d2ad` | Verified general/admin contact route;not data-sharing permission |
| CL70S03 | https://www.sfu.ca/stat-actsci/department/consulting.html | closure70/sources/sfu-consulting.raw | `e999f6479975a0f8af499a0b254cc2b2786b24656c42879a410c9f3a482e8590` | SCS current public liaison;contractual statistical work does not grant old Uken dataset |
| CL70S04 | https://uken.com/company | closure70/sources/uken-company.raw | `f2b32ec0a8976b6f4ddc6b6cbf1d5278dddd727be931172f84f5d00df9e0acc3` | Company contact support@uken.com;not a dedicated dataset application |
| CL70S05 | https://uken.com/privacy | closure70/sources/uken-public-privacy.raw | `52d0dde0f85da878caa7417e96b39c47d05604b5cb98bddcb9beec9c8bddb731` | Current policy names Uken Inc controller;not2015 ownership proof or third-party research license |
| CL70S06 | https://arxiv.org/abs/1811.12799 | closure70/sources/age-arxiv-record.raw | `76d63fc1386765031c939399d135459f45e2bcb092ba90efda78f4d97383f813` | Original arXiv author/DOI/version metadata;paper availability does not authorize raw player data |

## 新代码关联片段

| ID | SDK/版本 | 类/方法 | 文件:行 | 字段用途与边界 |
|---|---|---|---|---|
| CL70C01 | AppLovin/Adapter-unityads-adapter 4.18.1.0 | collectSignal/loadInterstitialAd/loadRewardedAd/createAdLoadOptions/createAdShowOptions | cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java:101 | fresh biddingAdId generated at load,shared between load/show options;adMarkup from MAX bid response; MAX-to-Unity object correlation;no tokenId or MAX event_id equality assignment |
| CL70C02 | AppLovin/Adapter-unityads-adapter 4.17.0.0 | load/createAdLoadOptions/createAdShowOptions | closure70/java/adapter-417/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java:101 | same fresh UUID and load/show option bridge in adapter4.17.0.0; versions individually audited;not whole SDK equivalence |
| CL70C03 | Unity/Ads 4.17.0 | UnityAdsBaseOptions.setObjectId/getData | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/UnityAdsBaseOptions.java:8 | objectId written under exact JSON key; actual shared-key contract,not name similarity |
| CL70C04 | Unity/Ads 4.17.0 | LegacyLoadUseCase.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/LegacyLoadUseCase.kt:80 | load option objectId or generated UUID -> UUID ByteString -> Load; load ID is not necessarily token collection ID |
| CL70C05 | Unity/Ads 4.17.0 | LegacyLoadUseCase.getOpportunityId/getAdMarkup | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/LegacyLoadUseCase.kt:200 | exact objectId/adMarkup option getter; explicit mapping into opportunity,not user identity |
| CL70C06 | Unity/Ads 4.17.0 | AndroidLoad.invoke waterfall/header bidding branches | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidLoad.kt:80 | same opportunityId passed into request or HB config request;HB response trackingToken materialized into response; HB config call happens at load after markup;not original auction feature request |
| CL70C07 | Unity/Ads 4.17.0 | AndroidGetAdPlayerConfigRequest.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdPlayerConfigRequest.kt:16 | configurationToken + impressionOpportunityId + placement -> UniversalRequest; configurationToken not decoded;no equality with tokenId |
| CL70C08 | Unity/Ads 4.17.0 | AndroidHandleGatewayAdResponse.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse.kt:100 | AdObject gets caller opportunityId and response trackingToken; response context combines with local opportunity |
| CL70C09 | Unity/Ads 4.17.0 | AdObject viewer binding and repository insertion | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse.kt:148 | same adObject passed to viewer invocations;repository keyed by opportunity;load timestamp set; object lineage;load timestamp not exact display time |
| CL70C10 | Unity/Ads 4.17.0 | LegacyShowUseCase.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/LegacyShowUseCase.kt:85 | show options objectId selected;fallback placement repository poll; shared load/show ID only on matching options;invalid ID does not establish join |
| CL70C11 | Unity/Ads 4.17.0 | AndroidShow.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidShow.kt:23 | lookup by opportunity -> show same ad -> remove on completion; per-ad lifecycle;not persistent person graph |
| CL70C12 | Unity/Ads 4.17.0 | sendOperativeEvent | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt:156 | viewer invocation passes same adObject and base64 additionalData to event API; event type specified by ad player;payload opaque,not proven cash or exact click type |
| CL70C13 | Unity/Ads 4.17.0 | GetOperativeEventApi.invoke overloads | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/GetOperativeEventApi.kt:14 | adObject.opportunityId/trackingToken/playerServerId -> request builder -> repository flow; current token read;eventId is generated separately |
| CL70C14 | Unity/Ads 4.17.0 | updateTrackingToken | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt:298 | nonempty base64 trackingToken overwrites adObject.trackingToken; not immutable join key;pair with opportunity and token version/time |
| CL70C15 | Unity/Ads 4.17.0 | AndroidGetUniversalRequestSharedData.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt:19 | timestamps + session/limited token + consent/PII context; timestamp is client build time,not server receive/bid time |
| CL70C16 | Unity/Ads 4.17.0 | AndroidGetSharedDataTimestamps.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetSharedDataTimestamps.kt:12 | wall UTC and monotonic elapsed since SDK init; wall/monotonic meanings not interchangeable |
| CL70C17 | Unity/Ads 4.17.0 | UniversalRequestEventSender.invoke | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/UniversalRequestEventSender.kt:16 | TTL drop;GatewayException stop;otherwise handle response; job completion need not mean delivery;no observed production ACK |
| CL70C18 | AppLovin/MAX 13.6.4 | l6 constructor | auction/sdk/MAX-13.6.4/java/com/applovin/impl/l6.java:40 | full response passed to each ad object; event_id scope shared full-response context;not necessarily unique per impression |
| CL70C19 | AppLovin/MAX 13.6.4 | c3.S/R/T | auction/sdk/MAX-13.6.4/java/com/applovin/impl/c3.java:186 | revenue_event from per-ad revenue_parameters;T reads full-response event_id via b; revenue callback phase configurable;event_id not natural-person ID |
| CL70C20 | AppLovin/MAX 13.6.4 | o3 constructor | closure70/java/max-1364/com/applovin/impl/o3.java:30 | full response vs ad JSON stored separately;feature-flag wrapper branch; critical to full-response vs per-ad ID scope |
| CL70C21 | AppLovin/MAX 13.6.4 | o3.b(String,String) | closure70/java/max-1364/com/applovin/impl/o3.java:469 | read full response .g or .b; decompiler monitor syntax unreliable;bytecode checked |
| CL70C22 | AppLovin/MAX 13.6.4 | l6.a(c3,int) | auction/sdk/MAX-13.6.4/java/com/applovin/impl/l6.java:173 | winner tracker stores same c3 and constructs MaxAdWaterfallInfo; winner load is not billed impression |
| CL70C23 | AppLovin/MAX 13.6.4 | MediationWaterfallWinnerTracker.c/b/a/b | closure70/java/max-1364/com/applovin/impl/sdk/q.java:20 | c stores event_id by ad unit in map e;getter a returns it;separate d map for prior request; request history scoped ad unit,not user global history |
| CL70C24 | AppLovin/MAX 13.6.4 | a6.f(JSONObject) | client-growth/java/max-1364/com/applovin/impl/a6.java:221 | q.a(ad_unit)->previous_loaded_request_id in next request;winner network same tracker; explicit prior-response->next-request ID;not equal to current request ID |
| CL70C25 | AppLovin/MAX 13.6.4 | MaxAdWaterfallInfoImpl constructor | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MaxAdWaterfallInfoImpl.java:24 | c3.T passed to waterfall eventId; same ID copied,not independently generated |
| CL70C26 | AppLovin/MAX 13.6.4 | getEventId/full constructor | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MaxAdWaterfallInfoImpl.java:65 | event ID stored and returned; full constructor last argument persists |
| CL70C27 | AppLovin/MAX 13.6.4 | processWaterfallInfoPostback | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java:322 | ad_event_id to SDK telemetry;latency/start timestamp/network diagnostics to separate mwf_info payload; ad_event_id not necessarily present in mwf_info POST body;do not conflate two destinations |
| CL70C28 | AppLovin/MAX 13.6.4 | processRawAdImpression/processViewabilityAdImpressionPostback/processCallbackAdImpressionPostback | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java:409 | revenue_event suffix mimp/vimp/cimp selects onAdRevenuePaid with same c3;impression postback separately scheduled; three notification stages not three amounts;no generic dedup proof |
| CL70C29 | AppLovin/MAX 13.6.4 | x2.a(MaxAdRevenueListener,MaxAd,boolean) | closure70/java/max-1364/com/applovin/impl/x2.java:466 | same MaxAd forwarded on UI thread;null guard; callback does not itself certify settlement or MMP forwarding |
| CL70C30 | AppLovin/MAX 13.6.4 | Mediation postback scheduler a(...) | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java:726 | event name,ad object and macros -> g6 task; CUID/creative optional,not mandatory person join |
| CL70C31 | AppLovin/MAX 13.6.4 | g6 constructor/f/a | closure70/java/max-1364/com/applovin/impl/g6.java:31 | event type -> *_urls on same ad;event/network/unit/format headers;POST builder dispatch; server-provided URL templates opaque;do not assume every URL has clear event_id |
| CL70C32 | AppLovin/MAX 13.6.4 | g6.run | closure70/java/max-1364/com/applovin/impl/g6.java:111 | URL macro/query substitution/config mappings;arn_info;POST dispatch; request construction only;no production send/ACK |
| CL70C33 | AppLovin/MAX 13.6.4 | j2.a(c3) | closure70/java/max-1364/com/applovin/impl/j2.java:90 | ad_event_id from same c3.T plus bcode/creative/unit/format/DSP; not proof of payload sent to Axon training |
| CL70C34 | Unity/Ads 4.18.1 | getOpportunityId/getAdMarkup | closure70/java/unity-4181/com/unity3d/ads/core/domain/LegacyLoadUseCase.java:310 | objectId/adMarkup read from options also in4.18.1; selected getter comparison only |
| CL70C35 | Unity/Ads 4.18.1 | invoke | closure70/java/unity-4181/com/unity3d/ads/core/domain/AndroidGetAdPlayerConfigRequest.java:43 | configurationToken and impressionOpportunityId setters also present; not full equivalent protocol proof |
| CL70C36 | Unity/Ads 4.18.1 | invoke(adObject) | closure70/java/unity-4181/com/unity3d/ads/core/domain/events/GetOperativeEventApi.java:89 | opportunity/tracking token read from object also present; selected consumer check only |
| CL70C37 | AppLovin/MAX 13.6.4 | b(c3) load processing | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java:596 | revenue_event endsWith(load) invokes internal processing at load;separate load postback; no developer onAdRevenuePaid visible inside this method;do not claim early public ILRD |
| CL70C38 | AppLovin/MAX 13.6.4 | a(c3,a$a) click processing | auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java:683 | revenue_event endsWith(click) invokes same-object developer revenue callback and mclick task; public revenue callback is not restricted to the three impression branches;target configuration unknown |

所有源文件SHA256、原包AAR SHA256/官方URL、精确片段、触发条件、六层状态见CODE_EVIDENCE.json。同一文件多片段按相同哈希追溯；类名混淆与反编译锁语法不当作源程序语义，关键getter/UUID/POST构造另存javap视图核对。

DECOMPILE.json记录本轮匹配版本的9个选类反编译结果。首次MAX6类反编译入口为SelectJadx，输出限closure70/java/max-1364；BYTECODE_CHECK.json记录四组原JAR与javap的哈希。没有修改原JAR/AAR。

复用证据见REUSED_EVIDENCE.json（逐哈希已核验）；Unity公开交易附录继续复用69号原件，没有重下。MAG定点书目查询未匹配对应五游戏原始数据，未把无关结果列为有效MAG证据。

联系方式均源自机构/公司公开业务页，只用于申请准备；未发送、未冒用学术身份、未签NDA。
