# 安装前竞价信号与Token血缘

2026-11-19。本轮继续客户端痕迹，不进行真实用户实验；旧[56号资产审计](56_数据资产与授权可得性审计.md)和全部历史产物保留。复用并验哈希的官方发行包：[版本/原包](client-growth/PACKAGE_PROVENANCE.json)；本轮选类反编译与字节码记录：[DECOMPILE](client-growth/DECOMPILE.json)、[follow-up](client-growth/DECOMPILE_FOLLOWUP.json)、[final](client-growth/DECOMPILE_FINAL.json)。没有执行SDK或生产Token，不采集身份。

## 结论

【SDK代码证实】**广告机会的输入不只有设备和广告位：Unity Ads外层Token带会话计数、HB seq/wins/starts、已加载/展示广告状态；MAX请求可携带前次请求/获胜网络以及受开关控制的历史请求次数。**这些是明确的广告生命周期线索，足以支持“存在行为上下文通道”的结论；是否有效区分未来高LTV玩家、是否进入Axon/Vector特征或带来ROAS增益仍【无法确认】。

本轮没有把Token整体视为加密黑箱，也没有反过来声称解码了模型特征：Unity公开源码可见外层protobuf构造与base64编码；内层sessionToken、campaign.data、Google QueryInfo等仍不透明。base64不是加密，但不透明字节也不自动具有可知语义。[CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS02](client-growth/SOURCE_CATALOG.md#cgs02)、[CGS06](client-growth/SOURCE_CATALOG.md#cgs06)、[CGS25](client-growth/SOURCE_CATALOG.md#cgs25)。

## 1. 四条广告机会链

| 链 | 已见入口→生成→封装 | 实际边界 |
|---|---|---|
| MAX→Unity Ads | collectSignal先更新隐私metadata→UnityAds.getToken(new TokenConfiguration(format))→回调token→MAX collector | 本适配器只传format；不能说placement/mediationAdUnit/extras全部已填。SDK支持不等于该调用传入。[CGS23](client-growth/SOURCE_CATALOG.md#cgs23)、[CGS24](client-growth/SOURCE_CATALOG.md#cgs24) |
| MAX→Google | createAdRequestWithParameters(true,format,...)→QueryInfo.generate→callback | query_info_type、placement_req_id有代码；信号内容/模型含义未解。[CGS25](client-growth/SOURCE_CATALOG.md#cgs25)、[CGS26](client-growth/SOURCE_CATALOG.md#cgs26) |
| Unity Ads独立请求 | AndroidGetAdRequest→设备/会话/campaignState/机会与广告位→UniversalRequest | 私有protobuf，不等于Unity Exchange服务器OpenRTB。[CGS21](client-growth/SOURCE_CATALOG.md#cgs21) |
| LevelPlay9.5选定类 | 多network callable→WorkerManager期限→成功map/错误/超时→provider instance汇总 | 明确并行采集和opaque map；本轮未恢复全cloud请求及TTL，不伪造完整字段语义。[CGS39](client-growth/SOURCE_CATALOG.md#cgs39)—[CGS41](client-growth/SOURCE_CATALOG.md#cgs41) |

MAX内部collectSignal先查缓存，未命中才按初始化策略调provider；成功缓存并回调，配置超时可结束采集。`a6`把signal_data放入后续POST请求，交任务调度器；请求构造不等于研究中成功发出。[CGS27](client-growth/SOURCE_CATALOG.md#cgs27)、[CGS32](client-growth/SOURCE_CATALOG.md#cgs32)、[CGS33](client-growth/SOURCE_CATALOG.md#cgs33)。MAX中介请求≠Axon广告主购量报价；LevelPlay中介拍卖≠Vector预测模型。

## 2. Unity Ads：从“可能有历史”推进到明确写入点

4.17.0原始官方sources与4.18.1 AAR选类都显示：token生成先取当前TokenCounters快照，再增加seq；写入快照seq/wins/starts。wins/starts/reset由广告WebView暴露函数调用；没有恢复所有viewer实际触发时刻，因此不把函数名当“每次赢标必然触发一次”的证明。会话计数从本地state读取，但gateway响应也能替换sessionCounters。[CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS03](client-growth/SOURCE_CATALOG.md#cgs03)、[CGS05](client-growth/SOURCE_CATALOG.md#cgs05)、[CGS16](client-growth/SOURCE_CATALOG.md#cgs16)、[CGS22](client-growth/SOURCE_CATALOG.md#cgs22)。

CampaignRepository以opportunityId为键保存状态；加载成功写loadTimestamp，viewer markShown写showTimestamp，后续分成shownCampaigns/loadedCampaigns。viewer提供data/dataVersion并以base64写入Campaign.data；本轮没有解读data为用户Embedding、关卡、历史购买或LTV。状态是内存map，有removeState，不证明持久跨App历史。[CGS04](client-growth/SOURCE_CATALOG.md#cgs04)、[CGS06](client-growth/SOURCE_CATALOG.md#cgs06)、[CGS07](client-growth/SOURCE_CATALOG.md#cgs07)、[CGS08](client-growth/SOURCE_CATALOG.md#cgs08)。

**新增身份来源核验：**这里`Pii.fid`的真实getter是`com.google.firebase.analytics.FirebaseAnalytics.getAppInstanceId()`，不是FirebaseInstallations.getId。DI显式绑定CachedFIdDataSource(AndroidFIdDataSource)，后者通过reflection bridge调用getter。`allowed.fid`控制payload字段填入；CachedFIdDataSource构造会预热delegate，所以“字段受门控”不能扩写成“getter从不提前读取”。没有因此作合规裁定，也没有实际读取ID。[CGS10](client-growth/SOURCE_CATALOG.md#cgs10)—[CGS15](client-growth/SOURCE_CATALOG.md#cgs15)。

Unity Ads自身的AllowedPii可由gateway更新，初值为空；GAID/openAdID、AppSet和fid分别有字段门控。它不是IAP的AdsIntent+ConnectionsSettings允许列表；不能把53—55号IAP的门控条件强行套到广告SDK。用户同意/OS限制/服务器配置与具体数据用途需分层核验。[CGS09](client-growth/SOURCE_CATALOG.md#cgs09)、[CGS10](client-growth/SOURCE_CATALOG.md#cgs10)、[CGS16](client-growth/SOURCE_CATALOG.md#cgs16)。

## 3. Token生成、缓存与“安装前”时序

Unity异步Token流程按远程adOperations配置有界等待初始化；随后读取当时state生成protobuf，base64并加`2:`前缀。static信息可来自缓存，dynamic每次读取；sessionToken由较早服务器响应提供，缺失则用init或limited分支。不能声称所有字段都在实际竞价同一毫秒新鲜产生，也不能把limited理解为不含标识。[CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS02](client-growth/SOURCE_CATALOG.md#cgs02)、[CGS09](client-growth/SOURCE_CATALOG.md#cgs09)、[CGS17](client-growth/SOURCE_CATALOG.md#cgs17)、[CGS18](client-growth/SOURCE_CATALOG.md#cgs18)。

MAX缓存实现已进一步核实：

- `signal_expiration_ms`缺省-1；SignalCacheManager只有TTL>0才缓存。`signal_cache_level`缺省AD_FORMAT，可按AD_UNIT_ID或ALL作用域配置。不得写成默认永远缓存所有Token。[CGS28](client-growth/SOURCE_CATALOG.md#cgs28)—[CGS30](client-growth/SOURCE_CATALOG.md#cgs30)。
- wrapper记录`SystemClock.elapsedRealtime()`；age>TTL判失效，命中后失效移除。TTL检查用单调时钟，不依赖手机墙钟。[CGS31](client-growth/SOURCE_CATALOG.md#cgs31)。
- `ad_expiration_ms`缺省4小时是广告缓存，不是信号TTL。缓存/刷新配置可能远程覆盖，生产值未知。[CGS30](client-growth/SOURCE_CATALOG.md#cgs30)。

本轮“安装前可用”是**该候选广告首次安装之前的当前广告机会**，并且只限生成Token时已有状态；既有媒体App广告历史不等于未来广告主App的安装后事件。实际token_age、bid_time和服务端特征as-of未取得；不把预缓存时刻当最终竞价时刻。

## 4. MAX历史字段不是神秘收入分数

`a6.ad_info.extra_parameters`可序列化previous_request_id、previous_loaded_request_id、previous_winning_network/name、queued_ad_networks/names；esc分支还可将部分winner名称替换为AppLovin值。它说明媒体侧广告历史上下文，不代表提供竞争者报价或竞争者用户数据。[CGS34](client-growth/SOURCE_CATALOG.md#cgs34)。

`mediation_stats.arpau/arpaf`受`umsm`控制，包内默认false。追踪`w3.f="ar"`→`y3.a(w3,x3)`加1→a6读取session计数，**不能把ar凭缩写猜成ad revenue**。`ttdasi_ms`来自特定callback中`currentTimeMillis - sdk.M()`；只报告该赋值，不把M来源未核实的值称作“安装时长/LTV”。[CGS32](client-growth/SOURCE_CATALOG.md#cgs32)、[CGS35](client-growth/SOURCE_CATALOG.md#cgs35)—[CGS38](client-growth/SOURCE_CATALOG.md#cgs38)。

## 5. 逐字段表

下表中的“竞价前”只表示token回调/请求构造前已有，**非观测到服务端bid-time快照**。完整字段来源、生成时间、scope、门控、序列化、接收方及未知项见[PREBID_FIELD_LINEAGE.json](client-growth/PREBID_FIELD_LINEAGE.json)。

| 字段/组 | 来源与生成时点 | scope与隐私条件 | 竞价前与序列化结论 | 证据 |
|---|---|---|---|---|
| Unity tokenId/tokenNumber | GetByteStringId / caller token counter；token build | one token, not player；SDK initialization/shouldInitialize and token callback conditions | HeaderBiddingToken tokenId/tokenNumber -> protobuf/base64；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS02](client-growth/SOURCE_CATALOG.md#cgs02)、[CGS17](client-growth/SOURCE_CATALOG.md#cgs17) |
| Unity clientInfo | GetClientInfo；token build | app/SDK context；initialization branch | HeaderBiddingToken.clientInfo；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01) |
| Unity adFormat/bannerSize/placementId/mediationAdUnitId | TokenConfiguration from caller；token call | placement/request；only supplied optional fields; MAX Unity selected adapter supplies format only | HeaderBiddingToken optional fields；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS23](client-growth/SOURCE_CATALOG.md#cgs23) |
| Unity extras/mediationInfo | caller TokenConfiguration；token call | developer/mediation defined；must be explicitly populated | extras.putAll; mediationInfo converter；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS23](client-growth/SOURCE_CATALOG.md#cgs23) |
| Unity timestamps | GetSharedDataTimestamps；build-time | event/token；SDK timing conditions | HeaderBiddingToken.timestamps；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01) |
| Unity sessionCounters | AndroidSessionRepository local values and gateway response updates；prior SDK lifecycle and response; read at build | SDK process/session state；API/lifecycle and server configuration; no per-game production observation | HeaderBiddingToken.sessionCounters；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS03](client-growth/SOURCE_CATALOG.md#cgs03)、[CGS16](client-growth/SOURCE_CATALOG.md#cgs16) |
| Unity tokenCounters.seq/wins/starts | sessionRepository; seq increment, viewer exposed win/start/reset hooks；snapshot before seq increment; prior callbacks | process/session; explicit reset；viewer-side callback reachability; not unconditional autonomous observation | tokenCounters seq/wins/starts；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS03](client-growth/SOURCE_CATALOG.md#cgs03)、[CGS05](client-growth/SOURCE_CATALOG.md#cgs05) |
| Unity campaignState.shown/loaded | opportunity map and timestamps；previous load/show updates | opportunity-keyed in-memory map；must have state entries; removal supported | shownCampaigns/loadedCampaigns in HeaderBiddingToken and AdRequest；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS04](client-growth/SOURCE_CATALOG.md#cgs04)、[CGS06](client-growth/SOURCE_CATALOG.md#cgs06)、[CGS07](client-growth/SOURCE_CATALOG.md#cgs07)、[CGS08](client-growth/SOURCE_CATALOG.md#cgs08)、[CGS21](client-growth/SOURCE_CATALOG.md#cgs21) |
| Unity campaign.data/dataVersion | WebView updateCampaignState base64 input；viewer update | opportunity/placement；requires nonempty data and nonzero version | stored Campaign.data -> campaignState -> token/request；生产bid时刻/训练未证 | [CGS04](client-growth/SOURCE_CATALOG.md#cgs04)、[CGS06](client-growth/SOURCE_CATALOG.md#cgs06)、[CGS01](client-growth/SOURCE_CATALOG.md#cgs01) |
| Unity staticDeviceInfo | device/app APIs; cachedStaticDeviceInfo after full session；init/fetch cache, may later update | device/app context；OS/platform availability; cache semantics | staticDeviceInfo in init/limited/full branches；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS09](client-growth/SOURCE_CATALOG.md#cgs09)、[CGS19](client-growth/SOURCE_CATALOG.md#cgs19) |
| Unity dynamicDeviceInfo | AndroidDynamicDeviceInfoDataSource.fetch；each selected read | current device/app state；OS return/permissions may limit data | dynamicDeviceInfo -> token / AdRequest；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS09](client-growth/SOURCE_CATALOG.md#cgs09)、[CGS20](client-growth/SOURCE_CATALOG.md#cgs20)、[CGS21](client-growth/SOURCE_CATALOG.md#cgs21) |
| Unity pii.advertisingId/openAdvertisingTrackingId | AdvertisingId/OpenAdvertisingId；getter/binder available at read | ad ID with reset/privacy limits；allowed.idfa; SDK initializes underlying provider once; separate consent/OS constraints | Pii optional bytes -> token/shared request；生产bid时刻/训练未证 | [CGS10](client-growth/SOURCE_CATALOG.md#cgs10)、[CGS16](client-growth/SOURCE_CATALOG.md#cgs16)、[CGS01](client-growth/SOURCE_CATALOG.md#cgs01) |
| Unity pii.appsetId | AndroidAppSetIdDataSource；async fetch/cache | Google provider-defined app-set scope；allowed.appsetId; gateway response can start collection | optional Pii.appsetId -> token；生产bid时刻/训练未证 | [CGS10](client-growth/SOURCE_CATALOG.md#cgs10)、[CGS16](client-growth/SOURCE_CATALOG.md#cgs16)、[CGS01](client-growth/SOURCE_CATALOG.md#cgs01) |
| Unity pii.fid | FirebaseAnalytics.getAppInstanceId via FId bridge；CachedFIdDataSource constructor prewarm; completion cached | Firebase Analytics app instance；allowed.fid gates payload field; prewarm getter itself has separate timing | Pii.fid -> HeaderBiddingToken.pii；生产bid时刻/训练未证 | [CGS10](client-growth/SOURCE_CATALOG.md#cgs10)、[CGS11](client-growth/SOURCE_CATALOG.md#cgs11)、[CGS12](client-growth/SOURCE_CATALOG.md#cgs12)、[CGS13](client-growth/SOURCE_CATALOG.md#cgs13)、[CGS14](client-growth/SOURCE_CATALOG.md#cgs14)、[CGS15](client-growth/SOURCE_CATALOG.md#cgs15)、[CGS01](client-growth/SOURCE_CATALOG.md#cgs01) |
| Unity sessionToken | gateway mutableData sessionToken；previous server response | server-defined session；present/full-session branch | HeaderBiddingToken.sessionToken；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS16](client-growth/SOURCE_CATALOG.md#cgs16) |
| Unity limitedSessionToken | AndroidGetLimitedSessionToken；token build when sessionToken absent | app installation/session；fallback branch | LimitedSessionToken/initializationData fields；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS18](client-growth/SOURCE_CATALOG.md#cgs18) |
| Unity TCF | TcfRepository.tcfString；current stored consent metadata | consent context；optional if repository value exists | optional tcf protobuf bytes；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS21](client-growth/SOURCE_CATALOG.md#cgs21) |
| Unity offerwallEnabled/scarSignalsCollected | OfferwallManager and eligibility check；token build | SDK feature state；eligible formats and manager connection | bool fields；生产bid时刻/训练未证 | [CGS01](client-growth/SOURCE_CATALOG.md#cgs01)、[CGS02](client-growth/SOURCE_CATALOG.md#cgs02) |
| MAX Unity signal | UnityAds.getToken(TokenConfiguration(format))；collectSignal callback | per token/request with optional scoped cache；updatePrivacyConsent before API; provider native gates | callback token -> MAX signal wrapper；生产bid时刻/训练未证 | [CGS23](client-growth/SOURCE_CATALOG.md#cgs23)、[CGS24](client-growth/SOURCE_CATALOG.md#cgs24)、[CGS27](client-growth/SOURCE_CATALOG.md#cgs27) |
| MAX Google QueryInfo signal | QueryInfo.generate(context,format,AdRequest)；network SDK callback | request context；Google AdRequest/consent/provider rules | provider callback string; no decoder here；生产bid时刻/训练未证 | [CGS25](client-growth/SOURCE_CATALOG.md#cgs25)、[CGS26](client-growth/SOURCE_CATALOG.md#cgs26) |
| MAX signal_data | provider signal callbacks -> collection array；collect then request build; cache may precede current request | network/format/ad-unit cache key；per-provider initialization, timeout, expiration/cache spec | a6 puts signal_data JSON; POST builder scheduled；生产bid时刻/训练未证 | [CGS27](client-growth/SOURCE_CATALOG.md#cgs27)、[CGS28](client-growth/SOURCE_CATALOG.md#cgs28)、[CGS29](client-growth/SOURCE_CATALOG.md#cgs29)、[CGS30](client-growth/SOURCE_CATALOG.md#cgs30)、[CGS31](client-growth/SOURCE_CATALOG.md#cgs31)、[CGS32](client-growth/SOURCE_CATALOG.md#cgs32)、[CGS33](client-growth/SOURCE_CATALOG.md#cgs33) |
| MAX ad_info.previous_* / queued_* | SDK per-ad-unit previous request/load/winner and queue；prior request/load/result state read before next load | ad unit / request / SDK state；previous result exists; esc branch can substitute AppLovin values | ad_info.extra_parameters；生产bid时刻/训练未证 | [CGS34](client-growth/SOURCE_CATALOG.md#cgs34) |
| MAX mediation_stats.arpau/arpaf | w3.f=ar; y3 count increments；prior request updates then request-time read | session scope in reader；umsm config default false; production unknown | optional mediation_stats JSON；生产bid时刻/训练未证 | [CGS32](client-growth/SOURCE_CATALOG.md#cgs32)、[CGS35](client-growth/SOURCE_CATALOG.md#cgs35)、[CGS36](client-growth/SOURCE_CATALOG.md#cgs36)、[CGS37](client-growth/SOURCE_CATALOG.md#cgs37) |
| MAX mediation_stats.ttdasipa_ms | w3.g ttdasi_ms and mediation callback timing；after prior display/revenue-related callback before later request | session/ad context；umsm flag; callback reached | optional per-ad timing map；生产bid时刻/训练未证 | [CGS32](client-growth/SOURCE_CATALOG.md#cgs32)、[CGS38](client-growth/SOURCE_CATALOG.md#cgs38) |
| MAX optional user_data | AppLovinUserData object converted to map；request build | developer-defined identifier namespace；send_user_data enabled AND object/map present | optional user_data JSON；生产bid时刻/训练未证 | [CGS34](client-growth/SOURCE_CATALOG.md#cgs34) |
| LevelPlay per-provider biddingData | parallel network callables -> success map；pre-auction signal collection | provider instance / auction；initialized/ad-unit conditions and worker deadline | C0118g2 instance-name map; no full cloud wire chain claimed；生产bid时刻/训练未证 | [CGS39](client-growth/SOURCE_CATALOG.md#cgs39)、[CGS40](client-growth/SOURCE_CATALOG.md#cgs40)、[CGS41](client-growth/SOURCE_CATALOG.md#cgs41) |

## 6. 仅服务器OpenRTB字段及不可证明的转码

【官方公开证实】既有35—38号协议已核实`imp/device/app/user/regs/source`、bidfloor/currency/at/tmax、隐私/身份及通知字段。它们属于交易所与DSP的服务器接口契约。客户端可能提供部分源数据，但本轮没有完整证明：

- `SDK app/PII/cuid/AppSet → OpenRTB具体user/device字段`的服务器映射；不能凭字段同名判等。
- floor、DSP seat、schain、最终tmax、auction type、胜负/计费通知等由服务器/中介流程形成或配置；SDK局部配置不能当最终出站请求。
- Unity RampID商业能力≠每包都带eids；MAX previous winner≠竞争者报价输入；当前sessionToken≠已解码身份图谱。

协议原始字段/页面/哈希复用[36](36_AppLovin_OpenRTB与竞价协议.md)、[37](37_Unity_OpenRTB与竞价协议.md)、[38](38_双方竞价字段差分.md)及[原证据索引BP](EVIDENCE_INDEX.md#bp01)。没有新抓包，没有访问生产竞价端点。

**版本上限：**Unity4.17/4.18所选Token外层路径有双版本代码；MAX新增深追仅13.6.4，不能外推13.2/13.6.2/13.6.3全部一致；LevelPlay9.3/9.4复用24/37号public接口和配置证据，本轮新内部collector仅9.5。未完整追踪的版本/协议均保持未知。
