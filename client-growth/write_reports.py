"""Evidence-scoped reconstruction, not a recovered production prediction model."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent.parent;O=R/'client-growth'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
sources=json.loads((O/'SOURCE_EVIDENCE.json').read_text('utf-8'))
S={s['id']:s for s in sources}
def cite(n):return f'[CGS{n:02d}](client-growth/SOURCE_CATALOG.md#cgs{n:02d})'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')

fields=[]
def field(name,source,generated,meaning,scope,gate,prebid,serial,receiver,ids,unknown):
 fields.append(dict(field=name,source=source,generated_at=generated,semantics=meaning,identifier_scope=scope,
   privacy_and_permission=gate,prebid_availability=prebid,serialization=serial,known_receiver=receiver,
   source_ids=[f'CGS{i:02d}' for i in ids],evidence_level='【SDK代码证实】',
   unknown=unknown,actual_target_game_enablement=False,production_received=False,model_use_proven=False))
P='Generated before token callback; can precede this auction, but no observed server bid_time or freshness guarantee'
N='No field-to-feature mapping or production training use proven'
field('Unity tokenId/tokenNumber','GetByteStringId / caller token counter','token build','request/token correlation','one token, not player','SDK initialization/shouldInitialize and token callback conditions',P,'HeaderBiddingToken tokenId/tokenNumber -> protobuf/base64','mediation token consumer',[1,2,17],N)
field('Unity clientInfo','GetClientInfo','token build','SDK/platform/mediation context','app/SDK context','initialization branch',P,'HeaderBiddingToken.clientInfo','mediation token consumer',[1],N)
field('Unity adFormat/bannerSize/placementId/mediationAdUnitId','TokenConfiguration from caller','token call','requested advertising format/context','placement/request','only supplied optional fields; MAX Unity selected adapter supplies format only',P,'HeaderBiddingToken optional fields','mediation token consumer',[1,23],'Do not invent placement/unit fields for MAX adapter when it only passes format')
field('Unity extras/mediationInfo','caller TokenConfiguration','token call','free-form optional metadata','developer/mediation defined','must be explicitly populated',P,'extras.putAll; mediationInfo converter','mediation token consumer',[1,23],'Map support does not prove gameplay/history values passed')
field('Unity timestamps','GetSharedDataTimestamps','build-time','clock/context','event/token','SDK timing conditions',P,'HeaderBiddingToken.timestamps','mediation token consumer',[1],'Not certified real-time auction timestamp or exact training available_at')
field('Unity sessionCounters','AndroidSessionRepository local values and gateway response updates','prior SDK lifecycle and response; read at build','loads/banner impressions/focus/time counters','SDK process/session state','API/lifecycle and server configuration; no per-game production observation',P,'HeaderBiddingToken.sessionCounters','mediation token consumer',[1,3,16],'Not all local-only; server may replace counters; no global history semantics proved')
field('Unity tokenCounters.seq/wins/starts','sessionRepository; seq increment, viewer exposed win/start/reset hooks','snapshot before seq increment; prior callbacks','HB operation counts','process/session; explicit reset','viewer-side callback reachability; not unconditional autonomous observation',P,'tokenCounters seq/wins/starts','mediation token consumer',[1,3,5],'Not reward count, ad revenue, future install or proof all viewer hooks fire')
field('Unity campaignState.shown/loaded','opportunity map and timestamps','previous load/show updates','current SDK ad campaign state','opportunity-keyed in-memory map','must have state entries; removal supported',P,'shownCampaigns/loadedCampaigns in HeaderBiddingToken and AdRequest','mediation token consumer / gateway',[1,4,6,7,8,21],'campaign data bytes opaque; not MMP acquisition campaign or proven cross-app LTV vector')
field('Unity campaign.data/dataVersion','WebView updateCampaignState base64 input','viewer update','opaque campaign blob','opportunity/placement','requires nonempty data and nonzero version',P,'stored Campaign.data -> campaignState -> token/request','mediation token consumer / gateway',[4,6,1],'No decoding of opaque data or identification of features/embedding')
field('Unity staticDeviceInfo','device/app APIs; cachedStaticDeviceInfo after full session','init/fetch cache, may later update','bundle/version/model/OS/display/RAM/store/install source etc','device/app context','OS/platform availability; cache semantics',P,'staticDeviceInfo in init/limited/full branches','token consumer/gateway',[1,9,19],'Not historical player value; full branch may use stale cached fields')
field('Unity dynamicDeviceInfo','AndroidDynamicDeviceInfoDataSource.fetch','each selected read','network/battery/locale/free-memory/foreground/tracking limits','current device/app state','OS return/permissions may limit data',P,'dynamicDeviceInfo -> token / AdRequest','token consumer/gateway',[1,9,20,21],N)
field('Unity pii.advertisingId/openAdvertisingTrackingId','AdvertisingId/OpenAdvertisingId','getter/binder available at read','allowed advertising IDs','ad ID with reset/privacy limits','allowed.idfa; SDK initializes underlying provider once; separate consent/OS constraints',P,'Pii optional bytes -> token/shared request','token consumer/gateway',[10,16,1],'Field-population gate != proof every underlying provider read is consent-delayed')
field('Unity pii.appsetId','AndroidAppSetIdDataSource','async fetch/cache','Google App Set ID','Google provider-defined app-set scope','allowed.appsetId; gateway response can start collection',P,'optional Pii.appsetId -> token','token consumer/gateway',[10,16,1],'Not automatic same as GAID/IDFV/RampID; cross-app reach not proven here')
field('Unity pii.fid','FirebaseAnalytics.getAppInstanceId via FId bridge','CachedFIdDataSource constructor prewarm; completion cached','Firebase Analytics App Instance ID','Firebase Analytics app instance','allowed.fid gates payload field; prewarm getter itself has separate timing',P,'Pii.fid -> HeaderBiddingToken.pii','token consumer/gateway',[10,11,12,13,14,15,1],'NOT FirebaseInstallations FID; no server join with IAP AppInstanceId proved')
field('Unity sessionToken','gateway mutableData sessionToken','previous server response','opaque server session linkage','server-defined session','present/full-session branch',P,'HeaderBiddingToken.sessionToken','token consumer; then server-specific consumption',[1,16],'Not decoded identity/model; no proved account/device graph')
field('Unity limitedSessionToken','AndroidGetLimitedSessionToken','token build when sessionToken absent','sessionId,IDFI,gameId,device/OS,mediation','app installation/session','fallback branch',P,'LimitedSessionToken/initializationData fields','token consumer/gateway',[1,18],'Limited mode still contains allowed context; not proof zero tracking')
field('Unity TCF','TcfRepository.tcfString','current stored consent metadata','privacy framework string','consent context','optional if repository value exists',P,'optional tcf protobuf bytes','token consumer/gateway',[1,21],'Not proof valid consent or purpose authorization by server')
field('Unity offerwallEnabled/scarSignalsCollected','OfferwallManager and eligibility check','token build','feature/collection state','SDK feature state','eligible formats and manager connection',P,'bool fields','token consumer/gateway',[1,2],'Not user value or independent monetization effect')
field('MAX Unity signal','UnityAds.getToken(TokenConfiguration(format))','collectSignal callback','opaque network bidding signal','per token/request with optional scoped cache','updatePrivacyConsent before API; provider native gates',P,'callback token -> MAX signal wrapper','MAX mediation collector',[23,24,27],'SDK exchange of signal is not sharing full gameplay/labels between Axon and Vector')
field('MAX Google QueryInfo signal','QueryInfo.generate(context,format,AdRequest)','network SDK callback','opaque Google query signal','request context','Google AdRequest/consent/provider rules',P,'provider callback string; no decoder here','MAX mediation collector',[25,26],'Cannot infer Google model features or Google organic users from token')
field('MAX signal_data','provider signal callbacks -> collection array','collect then request build; cache may precede current request','network signals and metadata','network/format/ad-unit cache key','per-provider initialization, timeout, expiration/cache spec',P,'a6 puts signal_data JSON; POST builder scheduled','MAX mediated-ad endpoint / ms.applovin.com configurable base',[27,28,29,30,31,32,33],'Exact endpoint path/helper and server OpenRTB conversion not reconstituted in these slices')
field('MAX ad_info.previous_* / queued_*','SDK per-ad-unit previous request/load/winner and queue','prior request/load/result state read before next load','media-side request and winning network context','ad unit / request / SDK state','previous result exists; esc branch can substitute AppLovin values',P,'ad_info.extra_parameters','MAX mediated-ad request',[34],'Winning network name is not other bidders bid prices/user data or proof Axon training')
field('MAX mediation_stats.arpau/arpaf','w3.f=ar; y3 count increments','prior request updates then request-time read','request counts by ad-unit/format','session scope in reader','umsm config default false; production unknown',P,'optional mediation_stats JSON','MAX mediated-ad request',[32,35,36,37],'ar is not ad revenue; SDK statistic existence not training input')
field('MAX mediation_stats.ttdasipa_ms','w3.g ttdasi_ms and mediation callback timing','after prior display/revenue-related callback before later request','time since SDK reference M in source','session/ad context','umsm flag; callback reached',P,'optional per-ad timing map','MAX mediated-ad request',[32,38],'Not time-to-install or label-maturity; exact M origin not established here')
field('MAX optional user_data','AppLovinUserData object converted to map','request build','developer-supplied optional data','developer-defined identifier namespace','send_user_data enabled AND object/map present',P,'optional user_data JSON','MAX mediated-ad request',[34],'No target game actual AppLovinUserData content or server identity match proved')
field('LevelPlay per-provider biddingData','parallel network callables -> success map','pre-auction signal collection','opaque provider signals + result/timeout handling','provider instance / auction','initialized/ad-unit conditions and worker deadline',P,'C0118g2 instance-name map; no full cloud wire chain claimed','LevelPlay collection completion; network stage incomplete here',[39,40,41],'Inner provider fields, TTL, complete request/network route and Vector mapping unknown')
save(O/'PREBID_FIELD_LINEAGE.json',fields)

report56=f'''# 安装前竞价信号与Token血缘

2026-11-19。本轮继续客户端痕迹，不进行真实用户实验；旧[56号资产审计](56_数据资产与授权可得性审计.md)和全部历史产物保留。复用并验哈希的官方发行包：[版本/原包](client-growth/PACKAGE_PROVENANCE.json)；本轮选类反编译与字节码记录：[DECOMPILE](client-growth/DECOMPILE.json)、[follow-up](client-growth/DECOMPILE_FOLLOWUP.json)、[final](client-growth/DECOMPILE_FINAL.json)。没有执行SDK或生产Token，不采集身份。

## 结论

【SDK代码证实】**广告机会的输入不只有设备和广告位：Unity Ads外层Token带会话计数、HB seq/wins/starts、已加载/展示广告状态；MAX请求可携带前次请求/获胜网络以及受开关控制的历史请求次数。**这些是明确的广告生命周期线索，足以支持“存在行为上下文通道”的结论；是否有效区分未来高LTV玩家、是否进入Axon/Vector特征或带来ROAS增益仍【无法确认】。

本轮没有把Token整体视为加密黑箱，也没有反过来声称解码了模型特征：Unity公开源码可见外层protobuf构造与base64编码；内层sessionToken、campaign.data、Google QueryInfo等仍不透明。base64不是加密，但不透明字节也不自动具有可知语义。{cite(1)}、{cite(2)}、{cite(6)}、{cite(25)}。

## 1. 四条广告机会链

| 链 | 已见入口→生成→封装 | 实际边界 |
|---|---|---|
| MAX→Unity Ads | collectSignal先更新隐私metadata→UnityAds.getToken(new TokenConfiguration(format))→回调token→MAX collector | 本适配器只传format；不能说placement/mediationAdUnit/extras全部已填。SDK支持不等于该调用传入。{cite(23)}、{cite(24)} |
| MAX→Google | createAdRequestWithParameters(true,format,...)→QueryInfo.generate→callback | query_info_type、placement_req_id有代码；信号内容/模型含义未解。{cite(25)}、{cite(26)} |
| Unity Ads独立请求 | AndroidGetAdRequest→设备/会话/campaignState/机会与广告位→UniversalRequest | 私有protobuf，不等于Unity Exchange服务器OpenRTB。{cite(21)} |
| LevelPlay9.5选定类 | 多network callable→WorkerManager期限→成功map/错误/超时→provider instance汇总 | 明确并行采集和opaque map；本轮未恢复全cloud请求及TTL，不伪造完整字段语义。{cite(39)}—{cite(41)} |

MAX内部collectSignal先查缓存，未命中才按初始化策略调provider；成功缓存并回调，配置超时可结束采集。`a6`把signal_data放入后续POST请求，交任务调度器；请求构造不等于研究中成功发出。{cite(27)}、{cite(32)}、{cite(33)}。MAX中介请求≠Axon广告主购量报价；LevelPlay中介拍卖≠Vector预测模型。

## 2. Unity Ads：从“可能有历史”推进到明确写入点

4.17.0原始官方sources与4.18.1 AAR选类都显示：token生成先取当前TokenCounters快照，再增加seq；写入快照seq/wins/starts。wins/starts/reset由广告WebView暴露函数调用；没有恢复所有viewer实际触发时刻，因此不把函数名当“每次赢标必然触发一次”的证明。会话计数从本地state读取，但gateway响应也能替换sessionCounters。{cite(1)}、{cite(3)}、{cite(5)}、{cite(16)}、{cite(22)}。

CampaignRepository以opportunityId为键保存状态；加载成功写loadTimestamp，viewer markShown写showTimestamp，后续分成shownCampaigns/loadedCampaigns。viewer提供data/dataVersion并以base64写入Campaign.data；本轮没有解读data为用户Embedding、关卡、历史购买或LTV。状态是内存map，有removeState，不证明持久跨App历史。{cite(4)}、{cite(6)}、{cite(7)}、{cite(8)}。

**新增身份来源核验：**这里`Pii.fid`的真实getter是`com.google.firebase.analytics.FirebaseAnalytics.getAppInstanceId()`，不是FirebaseInstallations.getId。DI显式绑定CachedFIdDataSource(AndroidFIdDataSource)，后者通过reflection bridge调用getter。`allowed.fid`控制payload字段填入；CachedFIdDataSource构造会预热delegate，所以“字段受门控”不能扩写成“getter从不提前读取”。没有因此作合规裁定，也没有实际读取ID。{cite(10)}—{cite(15)}。

Unity Ads自身的AllowedPii可由gateway更新，初值为空；GAID/openAdID、AppSet和fid分别有字段门控。它不是IAP的AdsIntent+ConnectionsSettings允许列表；不能把53—55号IAP的门控条件强行套到广告SDK。用户同意/OS限制/服务器配置与具体数据用途需分层核验。{cite(9)}、{cite(10)}、{cite(16)}。

## 3. Token生成、缓存与“安装前”时序

Unity异步Token流程按远程adOperations配置有界等待初始化；随后读取当时state生成protobuf，base64并加`2:`前缀。static信息可来自缓存，dynamic每次读取；sessionToken由较早服务器响应提供，缺失则用init或limited分支。不能声称所有字段都在实际竞价同一毫秒新鲜产生，也不能把limited理解为不含标识。{cite(1)}、{cite(2)}、{cite(9)}、{cite(17)}、{cite(18)}。

MAX缓存实现已进一步核实：

- `signal_expiration_ms`缺省-1；SignalCacheManager只有TTL>0才缓存。`signal_cache_level`缺省AD_FORMAT，可按AD_UNIT_ID或ALL作用域配置。不得写成默认永远缓存所有Token。{cite(28)}—{cite(30)}。
- wrapper记录`SystemClock.elapsedRealtime()`；age>TTL判失效，命中后失效移除。TTL检查用单调时钟，不依赖手机墙钟。{cite(31)}。
- `ad_expiration_ms`缺省4小时是广告缓存，不是信号TTL。缓存/刷新配置可能远程覆盖，生产值未知。{cite(30)}。

本轮“安装前可用”是**该候选广告首次安装之前的当前广告机会**，并且只限生成Token时已有状态；既有媒体App广告历史不等于未来广告主App的安装后事件。实际token_age、bid_time和服务端特征as-of未取得；不把预缓存时刻当最终竞价时刻。

## 4. MAX历史字段不是神秘收入分数

`a6.ad_info.extra_parameters`可序列化previous_request_id、previous_loaded_request_id、previous_winning_network/name、queued_ad_networks/names；esc分支还可将部分winner名称替换为AppLovin值。它说明媒体侧广告历史上下文，不代表提供竞争者报价或竞争者用户数据。{cite(34)}。

`mediation_stats.arpau/arpaf`受`umsm`控制，包内默认false。追踪`w3.f="ar"`→`y3.a(w3,x3)`加1→a6读取session计数，**不能把ar凭缩写猜成ad revenue**。`ttdasi_ms`来自特定callback中`currentTimeMillis - sdk.M()`；只报告该赋值，不把M来源未核实的值称作“安装时长/LTV”。{cite(32)}、{cite(35)}—{cite(38)}。

## 5. 逐字段表

下表中的“竞价前”只表示token回调/请求构造前已有，**非观测到服务端bid-time快照**。完整字段来源、生成时间、scope、门控、序列化、接收方及未知项见[PREBID_FIELD_LINEAGE.json](client-growth/PREBID_FIELD_LINEAGE.json)。

| 字段/组 | 来源与生成时点 | scope与隐私条件 | 竞价前与序列化结论 | 证据 |
|---|---|---|---|---|
'''
for f in fields:
 report56+=f"| {f['field']} | {f['source']}；{f['generated_at']} | {f['identifier_scope']}；{f['privacy_and_permission']} | {f['serialization']}；生产bid时刻/训练未证 | {'、'.join(cite(int(i[-2:])) for i in f['source_ids'])} |\n"
report56+='''
## 6. 仅服务器OpenRTB字段及不可证明的转码

【官方公开证实】既有35—38号协议已核实`imp/device/app/user/regs/source`、bidfloor/currency/at/tmax、隐私/身份及通知字段。它们属于交易所与DSP的服务器接口契约。客户端可能提供部分源数据，但本轮没有完整证明：

- `SDK app/PII/cuid/AppSet → OpenRTB具体user/device字段`的服务器映射；不能凭字段同名判等。
- floor、DSP seat、schain、最终tmax、auction type、胜负/计费通知等由服务器/中介流程形成或配置；SDK局部配置不能当最终出站请求。
- Unity RampID商业能力≠每包都带eids；MAX previous winner≠竞争者报价输入；当前sessionToken≠已解码身份图谱。

协议原始字段/页面/哈希复用[36](36_AppLovin_OpenRTB与竞价协议.md)、[37](37_Unity_OpenRTB与竞价协议.md)、[38](38_双方竞价字段差分.md)及[原证据索引BP](EVIDENCE_INDEX.md#bp01)。没有新抓包，没有访问生产竞价端点。

**版本上限：**Unity4.17/4.18所选Token外层路径有双版本代码；MAX新增深追仅13.6.4，不能外推13.2/13.6.2/13.6.3全部一致；LevelPlay9.3/9.4复用24/37号public接口和配置证据，本轮新内部collector仅9.5。未完整追踪的版本/协议均保持未知。
'''

report57=f'''# 自然量与跨渠道价值学习信号

2026-11-19。核心结论：**同一广告主App的自然量/其他渠道用户可以通过授权MMP共享成为Unity公开支持的学习数据；AppLovin也有all-source/organic共享契约，因此不是Unity独占能力。** 这是官方产品/集成契约，不证明四款游戏实际开启，更不等于将其他广告主App的个人历史自动拿来训练。

## 1. Unity公开的完整契约能还原到哪里

【官方公开证实】Unity ROAS best practices（2026-03-05快照）明确建议：**新ROAS活动前至少两周**提供Unity SDK额外数据及对应unattributed post-install postback，以帮助训练、改善初始预测、缩短学习阶段；这批数据**不计入学习阈值**。同页要求包括attributed/unattributed/organic全用户数据，Purchase/Ad Revenue带数值和收入，postback window设Lifetime或最大可用值。{cite(42)}。

“unattributed”在这里是**未归因给Unity**，不是MMP不知道归属。新取得的Unity attribution页明确：其他广告网络带来安装算Unattributed；organic也被Unity计入Unattributed。多数MMP默认不共享这些数据，需要显式配置。不是同一个标签被归因两次，也不意味着把自然量计为Unity新增安装或投放回报。{cite(43)}。

学习阈值另行要求：IAA D0为1000归因安装+正成熟D0广告收入；IAA D7/D28为1000归因安装+正成熟D7广告收入；IAP D7/D28为75位D7成熟付费者；Hybrid为1000归因安装+正D7广告收入+35位D7成熟付费者。**D28优化学习门槛用D7，不等于D28效果已成熟。** 有效层级与后台状态依活动核对，不能把1000视为整个模型训练集只有1000人。{cite(47)}。

SDK data文档句子没有逐字段列出“哪些广告SDK/引擎/IAP字段对应训练feature”。不能用这句话证明通用UGS Analytics或所有Runtime玩法自动上传Vector；本轮56号展示的是独立广告SDK信号可达性，53—55号展示的是IAP/Insights另一通道。

## 2. 由谁生成，谁转发，谁授权

| 数据 | 来源/传输 | 必要配置/权限 | 可证上限 |
|---|---|---|---|
| 设备/广告位/会话/Token/广告互动 | Unity Ads SDK/广告生命周期→Unity gateway/中介 | SDK配置、AllowedPii、TCF/隐私/平台条件 | 【SDK代码证实】构造；无四款生产接收 |
| 安装、归因、会话 | 游戏/MMP SDK→MMP服务器；Unity partner postback | 正确advertiser Game ID、partner启用、全来源共享、用途授权 | 【官方公开证实】共享契约；客户端包只证明MMP入口，不证明partner开关 |
| 逐展示IAA金额 | MAX/LevelPlay等ILRD→游戏/MMP收入API，或允许的S2S收入源 | 正确ad_revenue通道、精度/币种、SDK/S2S对账和去重 | 【SDK代码证实】金额接口；【官方公开证实】Unity映射；非自动训练ACK |
| 真实IAP金额 | 商店/验单/游戏SDK→MMP purchase→partner | 校验金额、paid/fulfilled去重、退款/税费/币种、后台映射 | 真实经济事件是标签候选，不能用catalog价格替代 |
| IAP5.5.1→Insights | Core身份/购买阶段/Firebase可选ID→protobuf gateway或native | AdsIntent+远程ID允许列表；购买事件本身不受广告同意总闸控制 | 复用53—55已证；逐事件Insights→Vector训练仍未知 |
| Analytics6.3 | RecordEvent→Buffer/Dispatcher→UGS collect | AnalyticsIntent/初始化/项目环境 | Analytics接收通道不是已证Vector训练通道 |
| Singular12.17 | eventJSON/customRevenue→SDK内部对象入口 | 开发者调用、partner配置、收入事件定义 | 47—52只追到部分API，不补造完整发送/Unity postback契约 |
| Runtime/Game DNA | Unity产品与DDF用途公开说明 | collection、usage、终端同意及产品用途独立 | 官方类别与部分接口，非四款字段级生产训练 |

IAP/Analytics精确原包/方法/序列化证据：[53](53_Unity_Core身份提供者与生命周期.md)、[54](54_Unity_Insights事件协议与接收边界.md)、[55](55_跨SDK身份价值血缘最终核验.md)；MMP队列与收入原方法：[16](16_Adjust_AppsFlyer归因与Postback.md)、[49](49_行为价值事件端到端调用链.md)。Singular未完全恢复，保留边界。

## 3. Unity MMP的实际共享开关

**AppsFlyer：**官方集成指引明确Activate Partner，分享organic/non-organic标记，安装默认postback选All media sources including organic；in-app postback与Lifetime窗口另开；映射launch/session、af_purchase→purchase、af_ad_revenue→ad_revenue与level_complete。收入共享另有Get ad revenue data、Revenue Settings产品权限/ROI360、SDK impression-level与device-level S2S组合，以及partner权限。{cite(44)}、{cite(45)}。

文档还出现Advanced Privacy、密钥/服务账号等后台操作；这里只记录原文作为集成条件，**没有执行开关、提取凭证，也不建议绕过用户隐私选择**。运营方应核对当前MMP、合同及适用隐私条件；文档产品建议不替代合法授权。AppsFlyer SDK在游戏里存在，不能证明所有这些配置已启用。

**Adjust：**激活Unity Ads、正确advertiser Game ID、Data from all attribution sources、Sessions/收入/参数等共享和事件mapping。广告收入必须走dedicated ad_revenue且账户支持，否则不传；错误映射可能破坏优化。publisher Game ID不可当advertiser Game ID。{cite(46)}、{cite(48)}。

custom S2S契约含gamer_id/aid/ifa等身份参数、campaign_id、advertiser game_id、install_ts及事件时间、event=session/purchase/ad_revenue、value/currency或revenue_usd，was_conversion_attributed=1/0明确区分归因给Unity与否。**参数能携带≠身份匹配已成功。** 历史接口文档称某些ID必填，不能据此绕过ATT、GAID限制或认为受限设备必有可匹配标识。{cite(48)}。

## 4. Axon：有同类供给能力，但不能照搬Unity学习规则

【官方公开证实】AppLovin AppsFlyer指引同样要求/支持all sources including organic：app open→landing（无金额），真正支付收入→checkout（带value/revenue），其他事件→postinstall（无金额）；Lifetime事件窗口在相邻配置。Adjust官方partner说明可选全部来源或仅Axon归因，未mapping事件不共享，分享session和收入有独立条件；其“默认活动”列表与session高量需另开说明存在文字层级差异，不能读成全部默认打开。{cite(49)}、{cite(50)}。

AppLovin官方Axon说明直接确认：模型使用设备/网络、App/广告/其他数字属性互动、MAX胜负通知，以及广告主**选择共享**的自有数据；按对该广告主展示价值出价。同时明确排除敏感个人数据、竞争者报价与竞争者用户数据。MAX请求即使含前次网络名，也不能反推Axon训练用了竞争者全部用户/价格；Ad Review也不能作该推断。{cite(51)}；原反证S24保留。

**不能外推的Unity机制：**本轮没有取得AppLovin与Unity相同的“至少两周”“1000/75/35”“D0/D7/D28退出规则”契约，也没有Axon逐特征as-of/成熟度/更新作业。all-source postback存在不等于具体生产模型已学习每个事件。

## 5. 哪些是真实价值标签，哪些不能混入

| 候选 | 对闭环的合适用途 | 必须保留的边界 |
|---|---|---|
| IAA逐展示收入+时间/币种/precision | 同安装cohort累计D0/D7/D28真实广告价值候选；可独立汇总 | exact/estimated/publisher_defined分开；同经济展示多SDK副本不重复计收；回调价不是银行结算 |
| 验单购买/实际扣款 | IAP/Hybrid价值目标候选 | 生命周期、退款、税费/平台口径；AppLovin checkout文档要用户支付全额含税费，不能直接套本地净利润口径 |
| session/level/rewarded/interstitial counts | 活跃/留存/消费机会代理，可能补充早期预测 | 不是美元收入，广告完成/发奖不是ILRD |
| GRT/AdWorth来源权重、国家阈值 | 业务分层/价值代理，独立评估是否增量 | 不能改名成真实purchase或与原始收入相加；线上规则和平台消费未证 |
| IAP metadata PriceMicro | 交易上下文/商品目录价格 | 不是必然最终成交额；intent/auth/failed也可能有其他上下文，不能直接做支付标签 |

AppLovin明确禁止广告收入、预测LTV、其他App支付归入IAP/checkout；真实收入通道要按各平台口径。{cite(52)}。本地57号尚无真实实验，旧56数据审计结论仍成立；本轮只有机制契约，不给伪造精度或效果数字。

## 6. 自然量如何可能帮助冷启动

【官方公开证实】Unity明确说预启动unattributed+SDK数据可帮助训练；AppLovin明确接受开发者选择共享的数据且有all-source契约。**同一目标App**的历史自然/跨渠道用户能提供“这个游戏的何种玩家产生何种收入/活跃”的先验样本，而不必等待新活动买来全部用户。它不必以“已知新用户在该目标App的未来行为”为前提。

【合理推断】样本扩大有机会改善冷启动和价值校准；但自然量与付费流量分布不同，采样/归因/收入策略偏差可能降低甚至反转收益。所谓Lifetime postback窗口也不能证明平台自动补发SDK集成前全部历史或能随意回填不可用数据；需实际S2S/backfill契约。

【无法确认】两平台具体混合权重、是否/如何跨广告主迁移、去重/退款/迟到策略、覆盖与训练增益。分享来源更广不等于模型肯定更好。
'''

for name,body in [('56_安装前竞价信号与Token血缘.md',report56),('57_自然量与跨渠道价值学习信号.md',report57)]:
 (R/name).write_text(body,'utf-8')
print('Reports56/57 and',len(fields),'prebid lineage records written')
