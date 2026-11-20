# 本轮关系边目录

实线仅表示给定静态代码或官方契约范围已证；不表示实际生产送达。旧图对象全部保留。

## CGE01 · Prior counters and loaded/shown campaign state are explicitly written into visible token outer protobuf

CG_U_history → CG_U_token；【SDK代码证实】。

来源：[CGS01](SOURCE_CATALOG.md#cgs01), [CGS02](SOURCE_CATALOG.md#cgs02), [CGS03](SOURCE_CATALOG.md#cgs03), [CGS04](SOURCE_CATALOG.md#cgs04), [CGS05](SOURCE_CATALOG.md#cgs05), [CGS06](SOURCE_CATALOG.md#cgs06), [CGS07](SOURCE_CATALOG.md#cgs07), [CGS08](SOURCE_CATALOG.md#cgs08), [CGS22](SOURCE_CATALOG.md#cgs22)

调用链：viewer win/start/reset and campaign update -> repositories; build token snapshots state -> protobuf -> base64 version2
条件：prior callbacks and initialization branch; campaign data opaque; server may update session counters
未证：No per-target-game token capture, bid-time freshness or model feature mapping

## CGE02 · Unity Ads fid is populated from FirebaseAnalytics.getAppInstanceId via cached reflection bridge

U_firebase_ids → CG_U_pii；【SDK代码证实】。

来源：[CGS10](SOURCE_CATALOG.md#cgs10), [CGS11](SOURCE_CATALOG.md#cgs11), [CGS12](SOURCE_CATALOG.md#cgs12), [CGS13](SOURCE_CATALOG.md#cgs13), [CGS14](SOURCE_CATALOG.md#cgs14), [CGS15](SOURCE_CATALOG.md#cgs15)

调用链：ServiceProvider -> CachedFIdDataSource(AndroidFIdDataSource) -> FIdBridge -> FirebaseAnalytics.getAppInstanceId -> Pii.fid
条件：allowed.fid gates field population; cache constructor prewarms getter; Firebase/OS and applicable consent restrictions separate
未证：No cross-app ID equality, successful matching or target-game production value

## CGE03 · Gateway response can update AllowedPii controlling token PII fields

CG_U_gateway_config → CG_U_pii；【SDK代码证实】。

来源：[CGS09](SOURCE_CATALOG.md#cgs09), [CGS10](SOURCE_CATALOG.md#cgs10), [CGS16](SOURCE_CATALOG.md#cgs16)

调用链：UniversalResponse mutableData.allowedPii -> SessionRepository -> DeviceInfoRepository -> privacyDataSource.fetch
条件：AllowedPii initially default-empty; ad provider init can occur before field gate; OS and purpose consent separate
未证：Actual deployed allowlists, complete underlying getter collection gates and production use

## CGE04 · MAX Unity adapter requests format-specific token and returns it through signal callback

CG_U_token → CG_MAX_collect；【SDK代码证实】。

来源：[CGS23](SOURCE_CATALOG.md#cgs23), [CGS24](SOURCE_CATALOG.md#cgs24), [CGS27](SOURCE_CATALOG.md#cgs27)

调用链：UnityAdsMediationAdapter.collectSignal -> updatePrivacyConsent -> UnityAds.getToken(TokenConfiguration(format)) -> callback -> MAX collector
条件：MAX consent/doNotSell only when supplied; provider initialization/callback conditions; no decoding token
未证：Which target-game opportunity invoked adapter and whether token arrived at downstream DSP

## CGE05 · Collected provider signal_data is serialized into MAX POST request construction

CG_MAX_collect → CG_MAX_request；【SDK代码证实】。

来源：[CGS25](SOURCE_CATALOG.md#cgs25), [CGS26](SOURCE_CATALOG.md#cgs26), [CGS27](SOURCE_CATALOG.md#cgs27), [CGS28](SOURCE_CATALOG.md#cgs28), [CGS29](SOURCE_CATALOG.md#cgs29), [CGS30](SOURCE_CATALOG.md#cgs30), [CGS31](SOURCE_CATALOG.md#cgs31), [CGS32](SOURCE_CATALOG.md#cgs32), [CGS33](SOURCE_CATALOG.md#cgs33)

调用链：Unity/Google provider signal -> cache or collect callback -> signal array -> a6.i puts signal_data -> a6.run POST scheduled
条件：network-specific conditions; signal TTL only caches if >0; format/unit/all scope; timeout; Google QueryInfo opaque
未证：Actual HTTP success, server reception, OpenRTB mapping and Axon bidder features

## CGE06 · MAX request includes prior request/network context and optionally request-count statistics

CG_MAX_history → CG_MAX_request；【SDK代码证实】。

来源：[CGS32](SOURCE_CATALOG.md#cgs32), [CGS34](SOURCE_CATALOG.md#cgs34), [CGS35](SOURCE_CATALOG.md#cgs35), [CGS36](SOURCE_CATALOG.md#cgs36), [CGS37](SOURCE_CATALOG.md#cgs37), [CGS38](SOURCE_CATALOG.md#cgs38)

调用链：ad-unit previous request/load/winner -> a6 ad_info.extra_parameters; w3.ar +1 counts -> gated mediation_stats
条件：umsm default false; production override unknown; previous data may not exist; user_data separate object/flag
未证：Not monetary LTV; SDK M reference time unproven; not evidence of competitor bids/users in model

## CGE07 · LevelPlay9.5 gathers concurrent provider responses with deadline and instance-keyed bidding maps

CG_LP_collect → CG_LP_map；【SDK代码证实】。

来源：[CGS39](SOURCE_CATALOG.md#cgs39), [CGS40](SOURCE_CATALOG.md#cgs40), [CGS41](SOURCE_CATALOG.md#cgs41)

调用链：provider callables -> workerManager deadline -> success/error/timeout -> provider instance bidding map
条件：provider initialization, availability and timeout; provider data opaque
未证：Complete cloud wire format, full TTL lifecycle, target-game invocation and Vector feature use

## CGE08 · Unity explicitly recommends prelaunch unattributed postbacks plus SDK data to train models; not counted toward learning threshold

CG_Allsource → U_predict；【官方公开证实】。

来源：[CGS42](SOURCE_CATALOG.md#cgs42), [CGS43](SOURCE_CATALOG.md#cgs43), [CGS53](SOURCE_CATALOG.md#cgs53)

调用链：same advertiser app all-source install/session/purchase/ad revenue -> authorized MMP sharing -> Unity product-level learning statement
条件：at least two weeks recommended; lifetime/max window; purpose/privacy authorization and partner setup
未证：Per-field training lineage, actual target-game sharing, historical backfill and measured lift

## CGE09 · Unity AppsFlyer contract supports organic/non-organic installs and mapped sessions/purchase/ad revenue with sharing permissions

M_af → CG_U_receiver；【官方公开证实】。

来源：[CGS44](SOURCE_CATALOG.md#cgs44), [CGS45](SOURCE_CATALOG.md#cgs45)

调用链：Activate Partner -> correct advertiser Game ID -> all-source default installs and in-app postbacks -> purchase/ad_revenue mapping
条件：background partner activation; event/revenue sharing scope and product permissions; privacy restrictions
未证：Target-game configuration, successful delivery, receipt and use

## CGE10 · Unity Adjust requires all-source selection, event maps and dedicated ad_revenue path/account capability

M_adjust → CG_U_receiver；【官方公开证实】。

来源：[CGS46](SOURCE_CATALOG.md#cgs46), [CGS48](SOURCE_CATALOG.md#cgs48)

调用链：Unity Ads partner + advertiser Game ID -> data source selection -> sessions/revenue sharing and event mapping -> Unity postback
条件：partner/account permissions; ad revenue dedicated path; valid privacy and source scope
未证：Target-game switches and production ad revenue postback ACK

## CGE11 · Unity ROAS product specifies post-install learning and mature cohort thresholds; D28 learning threshold uses D7 data

CG_U_receiver → U_predict；【官方公开证实】。

来源：[CGS47](SOURCE_CATALOG.md#cgs47), [CGS53](SOURCE_CATALOG.md#cgs53)

调用链：post-install revenue/installs -> learning threshold by optimization objective and cohort window
条件：IAA/IAP/Hybrid objective; D7 maturity; separate learning thresholds, not entire training sample count
未证：Actual labels, feature construction, model weights and target-game production training

## CGE12 · Unity S2S contract carries permitted identifiers, campaign/game/install/event time, attribution flag and revenue

U_mmp → CG_U_receiver；【官方公开证实】。

来源：[CGS43](SOURCE_CATALOG.md#cgs43), [CGS48](SOURCE_CATALOG.md#cgs48)

调用链：MMP-authorized secondary postback -> gamer_id/aid/ifa + advertiser game_id/campaign + install_ts/time + attributed flag/value
条件：valid applicable privacy controls; identifier availability; correct advertiser rather than publisher Game ID
未证：Successful join, match rates, deduplication, delayed feedback and target-game receipt

## CGE13 · Axon explicitly discloses device/network, engagement, own MAX win/loss and advertiser-shared data for continual models and advertiser-value bidding

A_context → A_predict；【官方公开证实】。

来源：[CGS51](SOURCE_CATALOG.md#cgs51)

调用链：official described collected/partner-shared data -> model continual learning -> impression value for advertiser -> bidding
条件：advertiser voluntary data; excludes sensitive/protected/children and other bidder bid/user data
未证：Per-field features, model structure, target-game calls, production delivery and measured contribution

## CGE14 · AppLovin AppsFlyer partner mapping supports all media sources including organic; checkout excludes IAA/predicted LTV

M_af → CG_A_receiver；【官方公开证实】。

来源：[CGS49](SOURCE_CATALOG.md#cgs49), [CGS52](SOURCE_CATALOG.md#cgs52)

调用链：AF configured event -> landing/checkout/postinstall; source scope and value/revenue choice -> AppLovin partner contract
条件：partner enabled and authorized; checkout only direct actual user payments; correct event window
未证：Game-specific event mapping/receipt; no IAA via checkout; no implicit MAX EventService routing

## CGE15 · Adjust Axon partner offers all-sources versus Axon-only, revenue sharing and explicit mapped events

M_adjust → CG_A_receiver；【官方公开证实】。

来源：[CGS50](SOURCE_CATALOG.md#cgs50), [CGS52](SOURCE_CATALOG.md#cgs52)

调用链：partner data sharing activation -> source scope -> optional sessions/revenue + mapping; unmapped events not shared
条件：actual partner configuration; session callback high-volume opt-in; in-app revenue semantics
未证：Target-game enablement, server receipt and selected optimization objective

## CGE16 · MAX EventService has event-name gated structured/legacy envelope and scheduled postback implementation

A_max → CG_MAX_queue；【SDK代码证实】。

来源：[XS31](../EVIDENCE_INDEX.md#xs31), [XS32](../EVIDENCE_INDEX.md#xs32), [XS33](../EVIDENCE_INDEX.md#xs33)

调用链：trackEvent -> axon_events choice -> structured or legacy payload -> scheduled postback
条件：13.7 standalone evidence; prior20-22 cover actual target versions; optional user_data and dedupe inputs not automatic
未证：Specific game business caller, successful send, reception and training

## CGE17 · No complete mapping established from private SDK signals to server-side Unity/OpenRTB fields or final bidder inputs

CG_MAX_request → U_exchange；【无法确认】。

来源：[CGS01](SOURCE_CATALOG.md#cgs01), [CGS21](SOURCE_CATALOG.md#cgs21), [CGS32](SOURCE_CATALOG.md#cgs32), [CGS33](SOURCE_CATALOG.md#cgs33)

调用链：Known private protobuf/JSON builders stop before documented exchange/DSP mapping
条件：Do not initialize SDK or probe production bidding; inspect authorized server traces only
未证：Server serializer/field lineage and authorized request trace; opaque token fields stay unknown

## CGE18 · Session/ad history serialization does not prove each field becomes a Vector pre-install feature or useful LTV signal

CG_U_token → U_features；【无法确认】。

来源：[CGS01](SOURCE_CATALOG.md#cgs01), [CGS04](SOURCE_CATALOG.md#cgs04), [CGS16](SOURCE_CATALOG.md#cgs16), [CGS53](SOURCE_CATALOG.md#cgs53)

调用链：Token serialization known; exact feature ingestion and bid-time as-of unknown
条件：Install-before time separation, purpose authorization and per-field availability required
未证：Feature schema, as-of joins, training provenance and controlled ablation

## CGE19 · AppLovin target-game receipt, canonical revenue rows and field-level LTV label generation remain unproven

CG_A_receiver → A_labels；【无法确认】。

来源：[CGS49](SOURCE_CATALOG.md#cgs49), [CGS50](SOURCE_CATALOG.md#cgs50), [CGS51](SOURCE_CATALOG.md#cgs51), [CGS52](SOURCE_CATALOG.md#cgs52)

调用链：Public postback contract -> unknown receipt/join/dedup/maturity/training dataset
条件：actual authorized sharing; IAA distinct from IAP checkout; field-level privacy and time scope
未证：Partner export/ACK, canonical revenue ledger, training-data lineage and dataset version

## CGE20 · Unity public learning contract is not event-by-event proof of receipt, joins, mature canonical label rows or model ingestion

CG_U_receiver → U_labels；【无法确认】。

来源：[CGS42](SOURCE_CATALOG.md#cgs42), [CGS47](SOURCE_CATALOG.md#cgs47), [CGS48](SOURCE_CATALOG.md#cgs48)

调用链：Product-level learning established; specific postback -> canonical label transformation not visible
条件：attributed/unattributed separated; real revenue vs proxy; consent, cohort maturity and bid-time isolation
未证：Authorized delivery logs, joins, dedup/refund/FX/delay handling and model data lineage

## CGE21 · Rotate original wrapper sends the same double revenue into AFAdRevenueData plus separate ad_revenue2/4 paths

GAME_rotate → M_af；【SDK代码证实】。

来源：[XS43](../EVIDENCE_INDEX.md#xs43)

调用链：g8.a original revenue wrapper -> AFAdRevenueData(network,APPLOVIN_MAX,USD,d); eventTracking ad_revenue2; ad_revenue4 callback
条件：actual original game method reached; original runtime rules, privacy and API conditions
未证：Successful MMP delivery; downstream partner sharing and dedup of alternative events

## CGE22 · No complete target-game specific value rule -> MAX EventService chain established; generic capability is insufficient

CG_Game_value → CG_MAX_queue；【无法确认】。

来源：[XS31](../EVIDENCE_INDEX.md#xs31), [XS32](../EVIDENCE_INDEX.md#xs32), [CGS34](SOURCE_CATALOG.md#cgs34)

调用链：Public generic event and optional user-data capabilities; four-game original call scan separately preserved in report20/XD01-XD02
条件：Car generic Unity/Metica bridge not proven concrete caller; no absence claim for native/reflection/hotfix/server paths
未证：Concrete business callsite/arguments plus production postback and reception; cannot infer from default event names

## CGE23 · AppLovin gaming product links MAX monetization with IAA/Blended ROAS and MMP-based UA; internal label schema is not disclosed

A_max → A_predict；【官方公开证实】。

来源：[CGS54](SOURCE_CATALOG.md#cgs54), [CGS51](SOURCE_CATALOG.md#cgs51)

调用链：official Ad ROAS/Blended products + MAX integration/MMP prerequisites -> advertised acquisition optimization
条件：product eligibility, advertiser activation and authorized data use; no specific target-game campaign observation
未证：Exact MAX income rows -> Axon labels/features, receipt and incremental effect

## CGE24 · AppLovin tracking macros expose ad-response event ID shared by impression/click and permitted device/campaign context

A_feedback → A_mmp；【官方公开证实】。

来源：[CGS55](SOURCE_CATALOG.md#cgs55)

调用链：ad response tracking template -> EVENT_ID shared by click/impression + device/campaign macros -> MMP tracking contract
条件：advertiser tracking template; privacy/identifier availability; not raw target user data
未证：Actual configured URL, install mapping, privacy fallback and successful server matching
