# AppLovin Exchange / MAX 协议与竞价路径

2026-11-19。**以取得的AppLovin官方oRTB规范和MAX13.6.4发行包为证据；不是Axon私有广告主出价接口的完整逆向。**

## 1. 实际取得的官方材料

有效规范基址为`https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/`：

- [Introduction](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/introduction)、[Bid requests](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/bid-requests)、[Bid responses](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/bid-responses)、[Creative types](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/creative-types)、[Changelog](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/changelog)。[BP01](EVIDENCE_INDEX.md#bp01)
- [Auction dynamics](https://support.applovin.com/en/max/demand-partners/auction-dynamics)、[SDK bidder onboarding](https://support.applovin.com/en/max/demand-partners/sdk-bidder-testing-and-integration-process)。[BP03](EVIDENCE_INDEX.md#bp03)
- 原始HTML与逐表字段：[auction/al-request.raw](auction/al-request.raw)、[al-response.raw](auction/al-response.raw)、[PROTOCOL_FIELDS.json](auction/PROTOCOL_FIELDS.json)。请求146行、响应66行包含辅助宏/tracking表；不是146个所有流量必带的特征。

【无法确认】旧`/partners/ad-exchange/...`地址跳首页、部分best-practices返回HTTP200的404页面；都记录为无效候选，未用它们证明协议。

## 2. 全字段覆盖和主要对象

**【官方协议证实】单请求一个`imp[]`，不支持每bidder多seat，忽略`wseat`。** OpenRTB2.5作为基线；SDK bidder入驻页也提兼容2.3/2.5，不能因此宣称与全标准任意组合完全一致。

| 对象 | 本轮原表覆盖 | 关键语义/条件 |
|---|---|---|
| request | `id/app/at/bapp/badv/bcat/device/ext/imp/regs/source/tmax/user`及嵌套属性 | `at=1`；默认`tmax=500ms`；`bapp`opt-in最多30项，`badv`最多30；表中部分仅DSP |
| `app` | bundle、cat、content及url/ext、orientation_lock、id/name、publisher及ext/id/name、storeurl、ver | `publisher.ext.installed_sdk`可给SDK bidder名称/版本，DSP的id为APPLOVIN_EXCHANGE；publisher ID为供给方，不是玩家 |
| `device` | carrier、connectiontype、devicetype、dnt、ext.atts/ifv、geo、h/w、hwv、ifa、ip/ipv6、js、language、lmt、make、mccmnc、model、os/osv、pxratio、ua | GDPR未同意时ifa/IP等有抑制；表“always passed”不能覆盖正文隐私条件；iOS `ifv`仅IDFA不可用/全零时 |
| `device.geo` | city/country/dma、ext.isp/org、ipservice、locale/metro/region/type/zip | 明确部分来自IP与MaxMind；没有据此推断GPS或精确定位 |
| `imp[]` | banner/video/native、floor、displaymanager/version、exp、ext.ad_unit_name/SKAN、id、instl、metric、rwdd、secure、tagid | floor默认USD；**bid须大于floor**；`exp=14400`是可延迟展示提示；rewarded用rwdd及video.ext.videotype等 |
| `imp.metric[]` | type/value/vendor | 仅DSP字段；session_duration、session_depth及各格式depth；特定depth无展示/30分钟不活跃可0；不是游戏关卡LTV |
| video/banner/native | 全部原表含尺寸、MIME、protocol/api、blocked attributes、native request/assets等 | banner和video可同在一个imp，表示可支持的格式，不是两次售出；CTV仅video/VAST；native用1.2 |
| user | id、data/name/segment、ext及consent/gdpr | `user.id`明确定义为**每App的AppLovin设备ID**；`user.data.segment.signal`仅SDK bidders的adapter自定义token，不是DSP统一明文身份资料 |
| source/regs/ext | `source.ext.schain`、法规/同意扩展等 | 供给链、法规与扩展；不能从存在`ext`推断任意游戏事件、RampID或CUID都发给DSP |

完整原始描述、必传条件与出处逐行保存在[字段目录](auction/PROTOCOL_FIELDS.md)。**本轮“完整”限于取得文档的全部表格，不包括闭源服务器未公开扩展。**

## 3. 响应和无效报价

【官方协议证实】响应最大4KB；`HTTP204`明确无报价。`id`匹配request，`seatbid[].bid[]`至少一个；响应`cur`只接受/默认USD，Introduction又明确忽略`cur`，因此接入者必须按USD出数值，不能把写CNY当自动换汇。

`bid`关键字段：`id/impid/price/adm/adomain/cat/crid/burl`；bundle在SKAN存在时必需；`adid/api/apis/attr/cid/dealid/ext/h/w/lurl/nurl/protocol`等条件见原表。DSP必须提供创意markup；SDK bidder由自己SDK渲染，可不交实际markup、使用适配器回传数据，**不能把DSP必填校验机械套到SDK bidder**。

【官方协议证实】创意/报价过滤包括：低于或等于floor、空/零报价、publisher blocked bundle/domain/category、错误app bundle、非法adomain、markup格式/安全/广告类型。`adomain`使用第一项及顶级广告主域，不是带协议/路径的落地URL；`crid`应稳定标识同一创意。并非响应中最高数字就能胜出。

【官方协议证实】Auction dynamics明确最高CPM有效来源胜出、与发布者非竞价waterfall需求合并。**非竞价来源的估计/配置CPM不等于新一轮DSP真实报价**；SDK再加载可能失败，故后续failover、无展示与账务需单列。

## 4. 赢标、输标、计费及点击：三个时点

| 字段/路径 | 触发与接收方 | 不能误解为 |
|---|---|---|
| `bid.nurl` | 【官方协议证实】拍卖完成并把广告发送到设备阶段；Dynamics说明SDK bidder成功load后通知；DSP接收 | 不是已经展示/计费或已安装 |
| `bid.lurl` | 【官方协议证实】错误/无效bid、load失败，或另一个赢家load后；接收loser配置的端点 | 不是所有请求保证有成功通知，尤其未响应时未必取得URL |
| `bid.burl` | 【官方协议证实】设备render：视频开始、图像展示；DSP必须用于impression/spend核算 | 不能按`nurl+burl+imptrackers`三次累计支出 |
| `bid.ext.imptrackers` | 【官方协议证实】第三方展示跟踪，server-side；另有native eventtrackers | 与burl的财务口径不可混用 |
| HTML/VAST/native点击 | 【官方协议证实】HTML/native点击、VAST ClickTracking多为客户端；VAST impression tracker服务器侧；具体按格式 | 点击不是安装、奖励回调不是美元收入 |

【官方协议证实】通知宏是重要的可见性证据：

- `${AUCTION_ID}`、`${AUCTION_BID_ID}`：关联本次请求/响应。
- `${AUCTION_LOSS}`：loss reason，仅lurl。
- `${AUCTION_PRICE}`：文档明确nurl和lurl均可获得最终clearing price，无赢家为0，最多六位小数。**不是所有对手的完整bid向量或用户数据。**
- `${AUCTION_MINIMUM_BID_TO_WIN}`：文档定义第二高价，只对winner有意义；仅一个有效bid为0。第一价格仍按自己的报价付费，不能按这个宏误改为第二价格。

AppLovin接口文档提供部分clearing反馈，与官方“Axon不摄入其他bidder出价/用户数据”的模型声明需同时保留；本轮不把公开宏升格为Axon内部训练特征。[BP08](EVIDENCE_INDEX.md#bp08)

## 5. 缓存、timeout及版本细节

【官方协议证实】Certain ads缓存同session最多四小时，通常几分钟；`imp.exp`告知潜在延迟，不保证必展示。视频素材下载10秒timeout不是DSP500ms征价窗口；SDK signal timeout、MAX cloud请求timeout、创意下载timeout、缓存TTL是四个不同层级。

【官方协议证实】Changelog列2023-07要求压缩gzip，2023-04所有DSP启用Smart Throttling，2022-09回调增加`X-Device-IP/X-Device-User-Agent`，2021-12增加iOS `device.ext.ifv`。这证明接口演进/分流能力，**没有恢复throttling特征、阈值或流量分配算法**。Creative页与旧changelog对某些VAST Wrapper支持存在时间/平台差异，不自行裁定所有SDK均同规则。

## 6. 实际SDK追踪，不能把OpenRTB当移动端原始协议

官方MAX13.6.4 jar原始SHA256见[SDK_AUDIT](auction/SDK_AUDIT.json)，选类源码与19段原始行号见[CODE_EVIDENCE](auction/CODE_EVIDENCE.json)。[BP04](EVIDENCE_INDEX.md#bp04)

| 调用链 | 原始位置 | 已证/未证 |
|---|---|---|
| adapter信号 | `MediationServiceImpl.collectSignal`，`:221–310` | 【SDK代码证实】资格、初始化、成功/错误回调和收集timeout；没有执行收集 |
| 形成广告请求 | `com.applovin.impl.a6.g` `:113–156`→`run` `:182–212` | 【SDK代码证实】collector→ad unit、`signal_data`、`mediation_stats`、可选user_data→POST到配置构造的MAX服务器；不是发给所有DSP的OpenRTB JSON |
| 前序上下文 | `a6.f(JSONObject)` `:221–270` | 【SDK代码证实】previous_request_id、previous_loaded_request_id、previous winner分支；不能据字段存在认定Axon将竞争网络数据用于训练 |
| 响应处理 | `l6`构造/`run`、`ads`数组；`c3`的`bid_response`getter `:241` | 【SDK代码证实】解析服务器给定候选/返回数据，由网络SDK/适配器载入；未恢复服务器最高CPM筛选实现 |
| fallback与反馈 | `l6:171–219`、`MediationServiceImpl.processWaterfallInfoPostback:322–377` | 【SDK代码证实】加载/响应耗时、waterfall报告、failover路径；不是公网postback送达证明 |
| expiration及收入 | `g3.n0`读取`ad_expiration_ms`，剩余时间按elapsedRealtime；`c3.getRevenue/getRevenuePrecision` | 【SDK代码证实】每广告有效期与金额精度，不证明已结算现金；ILRD的exact/estimated/publisher_defined须保留 |

## 7. 与Axon的边界

【官方公开证实】Axon预测展示对具体广告主的价值、选择与目标匹配的用户并竞价；Exchange公开机制消费的是需求端返回的CPM，不暴露pInstall、D28LTV、训练权重或预算策略。[39](39_Axon_Vector预测与出价机制.md)

【无法确认】MAX服务器私有完整请求→所有DSP字段映射、各bidder实际资格、throttling、tie-break、净收入/服务费处理、预算和模型更新均没有被本轮恢复；报告不以离线自编代码代替这些未知。
