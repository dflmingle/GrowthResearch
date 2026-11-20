# Unity Exchange / LevelPlay / Unity Ads 协议与竞价路径

2026-11-19。**已取得请求、响应、接入、loss、隐私及iOS/SKAN官方协议；SDK静态代码只证明客户端封装与后处理，不是Vector模型源码。**

## 1. 原始规范与版本边界

官方来源：[Introduction](https://docs.unity.com/en-us/grow/programmatic/unity-exchange)、[Getting started](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/get-started)、[Bid requests](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-requests)、[Bid responses](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-responses)、[Loss notifications](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/loss-notifications)、[Data privacy](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/data-privacy)、[iOS14 support](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/ios14-support)。[BP02](EVIDENCE_INDEX.md#bp02)

取得Markdown页面标记更新2026-04-27。Introduction称基于OpenRTB2.6并有其他扩展，而get-started要求支持2.5；不能删掉其中一个以制造无冲突的单版本实现。原始全部表行见[PROTOCOL_FIELDS](auction/PROTOCOL_FIELDS.md)：request82、response54、privacy5、SKAN20、loss71，包含辅助参数/原因码，不全是请求字段。

## 2. 请求对象和字段

| 对象 | 原始表字段概览 | 实际语义与条件 |
|---|---|---|
| request | id、imp、pmp、app、device、user、at、tmax、bcat/bapp、source、regs | 单个imp，通常id=1；at=1；正文“when available”而非所有字段必传 |
| imp | banner/video、bidfloor、displaymanager/version、id、instl、secure、tagid及SKAN扩展 | floor表明确USD；格式、尺寸、MIME、API/protocol与blocked属性按子表；不从未列native就断言所有Unity产品无native |
| app/publisher | id/name/bundle/publisher/storeurl，publisher.id | 发布者App、商店身份与供给方ID，不是广告主包/用户账户 |
| device | connectiontype/devicetype/geo/hwv/ifa/ip/language/lmt/make/model/os/osv/ua/carrier | 环境与广告标识；部分geo属性只在示例出现，不能视为必传或精确GPS采集承诺 |
| source | pchain、schain、`source.ext.omidpn/omidpv/header_bidding/fd` | `header_bidding`1竞价/0waterfall；`fd`0exchange决策/1上游；schain节点asi/sid/rid/hp等。本轮保留文档的source.schain路径，不静默改为标准其他版本路径 |
| pmp/deal | deals/private_auction；deal.id/at | 文档列在请求对象并解释deal；at=3可表示约定deal price。与“全部普通拍卖at=1”是不同层级，不把所有交易都套单一规则 |
| regs/user | COPPA/GDPR/us_privacy/LGPD及consent | 隐私专页分别说明发送条件与过滤，不把user对象存在当身份图谱 |
| iOS补充 | device.ext.atts、device.ext.ifv、SKAN sourceapp/skadnetids/versions等 | 以iOS专页补充核心表没有列的属性；ifv为iOS IDFV，不是Android App Set ID |

【官方协议证实】Exchange向DSP端点HTTP POST JSON，HTTPS、压缩/连接复用有明确约束。移动端Unity Ads protobuf与Exchange→DSP JSON为不同接口；没有取得逐字段服务端转码全表。[BP02](EVIDENCE_INDEX.md#bp02) [BP05](EVIDENCE_INDEX.md#bp05)

## 3. timeout：不能把所有场景写死200ms

【官方协议证实】请求`tmax`表建议200ms，响应正文写maximum200ms，banner示例却为500ms；最新get-started进一步说明：

> waterfall auction的TMAX按DSP seat配置，最高1000ms；bidding auction由mediation配置，从Unity处理时间扣除50ms；两种情形均在请求中告知DSP响应预算。

**实现必须遵守当次tmax及伙伴配置，并核实文档冲突；不能用示例值当全球硬限。** 也不能把LevelPlay私有auctionTimeout的10秒默认解析与DSP响应窗口直接比较。[BP02](EVIDENCE_INDEX.md#bp02) [BP06](EVIDENCE_INDEX.md#bp06)

## 4. 响应、币种和创意要求

【官方协议证实】响应id返回request id，`cur`必需，seatbid/bid/seat等见表；price为CPM，正数且非加密，最多三位小数、优选两位。`cur`需匹配`adsource`配置且`exchange_rate`不为空，否则忽略；可支持USD及CNY等，**不意味着任意请求自动允许所有币种**。

【官方协议证实】bid原表包括`id/impid/price/adid/nurl/burl/iurl/cid/crid/dealid/cat/adm/adomain/bundle/attr/w/h/api`；bid.ext有`appid/appname/storeurl/imptrackers/length/crtype`、SKOverlay/ProductPage/AutoStoreKit及ClickableVideo扩展。`crtype`原表必需。应用广告的bundle/storeurl和adomain等具有额外平台要求。

【官方协议证实】seatbid段写可返回多个seat，但只用一个，并写选择`bid.id`与`impression.id`相等的seat，多个则随机；与此同时bid表把`impid`明确为impression关联键。**这里有潜在文字/选择规则歧义，不能暗自改成标准再宣称恢复服务器实现。** 本地模拟仅使用一个seat/一个bid，不模拟未证多seat规则。[BP02](EVIDENCE_INDEX.md#bp02)

【官方协议证实】支持HTTP204、空JSON、well-formed nbr等显式no-bid；不明确响应可能被当timeout。无效/被过滤原因包括零/缺失价格、无markup、domain或auction/deal ID错误、below floor、publisher block、拒审/安全/创意质量等；不能仅按最高CPM选取。

## 5. 赢输标、计费、缓存与点击

| 机制 | 官方已知内容 | 限制 |
|---|---|---|
| `nurl` | 原文明确在render/delivery时ping，也作为billable impression计数；无burl时有独有要求 | 不套用AppLovin的load阶段win通知 |
| `burl` | winning bid变成billable时触发，具体依exchange policy；可替换价格宏 | 与nurl同时存在不等于付两笔钱 |
| `bid.ext.imptrackers` | 与billable impression一致，可代替burl；文档给条件必需要求 | 实施条件以伙伴契约核实，不能把多个tracker累加计费 |
| `lurl` | loss专页独立定义，替换`${AUCTION_LOSS}`，支持时通知 | 核心bid表没有列出不能当不支持；没有lurl就不能假定回传 |
| 预缓存 | 赢标后拉取HTML/trackers到客户端，用户体验广告时才计展示与其他tracker | 仅获胜/预加载不构成收入；公开loss2说明可能过期，通用TTL未取得 |
| 展示价格宏 | `${AUCTION_PRICE}`及可选`${AUCTION_PRICE:BF}`混淆 | BF为公开说明的Blowfish ECB/PKCS5+URL-safe Base64，并非接口要求用加密价格出价；未取得/使用生产key |
| 点击/完成/奖励 | SDK有广告事件与回调，格式内有相应跟踪 | 不把点击、播放完成、奖励或归因安装混为同一事件 |

【官方协议证实】Loss表包含1–9、101/102/104、200系列及>999平台自定义原因；例如102更高价获胜、2曝光机会过期、3可能no-fill/未响应/validator失败。相同数字必须按平台文档解释，不能把所有loss码当一套完全同义的通用IAB词典。

## 6. 设备、身份与隐私过滤

【官方协议证实】`user.ext.consent="0"`时设备ID全零、IP遮罩；LGPD opt-out说明移除IDFA/AAID/IP；其他法规flags按适用条件。`ifa`可能跨合法请求关联设备，但`bidrequest.id/imp.id`只是拍卖/广告机会标识。

【官方公开证实】Unity Exchange支持美加RampID受众激活；**本轮取得的bid/隐私/SKAN页仍没有Unity专用RampID wire字段。** IAB的eids是标准能力，不能把它补成已捕获的Unity生产payload。UGS PlayerId/UPA邮箱→竞价字段没有已证映射。[BP07](EVIDENCE_INDEX.md#bp07) [32](32_Unity身份互通与RampID.md)

## 7. Unity Ads客户端：实际数据流

官方4.17.0 sources.jar复用，4.18.1既有反编译作范围对照；原始位置见[CODE_EVIDENCE](auction/CODE_EVIDENCE.json)。[BP05](EVIDENCE_INDEX.md#bp05)

1. **【SDK代码证实】**`AndroidGetAdRequest.invoke`：sessionCounters、static/dynamicDeviceInfo、impressionOpportunityId、placementId、campaignState、TCF、mediationAdUnitId/extras→protobuf `AdRequest`→`UniversalRequest`。
2. **【SDK代码证实】**`AndroidBuildHeaderBiddingToken.invoke`：clientInfo、timestamps、可选格式/placement/mediation、PII、TCF、session/campaign、tokenCounters(seq/wins/starts)；初始化/limited/full session分支不同。
3. **【SDK代码证实】**`CommonGetHeaderBiddingToken.invoke`：protobuf bytes→Base64→`2:`前缀；这是编码而非加密或模型权重；未收集任何真实token。
4. **【SDK代码证实】**`AndroidGetUniversalRequestSharedData`与PII datasource有consent/allowed标志。SDK广告operative事件的持久化/重试路径沿用[24号报告](24_Unity与AppLovin技术对比.md)，不等同每次生产事件送达。

`campaignState`是网络广告上下文，不能自动解释为MMP归因campaign；wins/starts是token/广告计数，不是玩家关卡或真实广告美元收入。

## 8. LevelPlay私有竞价路径

实际分析9.4.0实现jar，不是只看壳AAR；SHA256`eb1d282be3077344fe560d98e5f5a8462e99489ce2faaf5fc99fd79cdd6b8120`。JADX因Windows大小写冲突重命名的类保留原始注释：[BP06](EVIDENCE_INDEX.md#bp06)

- **【SDK代码证实】**原`com.ironsource.i3`→反编译`AbstractC0163i3`：候选/token收集、无candidate失败、调用auction handler、auction ID/state核验、返回waterfall、error时可转fallback。`:894–989`为关键段。
- **【SDK代码证实】**原`com.ironsource.q2`→`C0325q2`：解析`instance/adMarkup/serverData/adData/price/loadTimeout/order`及`notifications.burl/lurl/nurl`数组。**这不是公开OpenRTB BidResponse本身**，不能拿它的`price`排序代码声称服务器出价算法已恢复。
- **【SDK代码证实】**`Ve`配置解析有`auctioneerURL/auctionTrials/auctionTimeout`及重试/加载配置，部分分支default10000ms；是SDK→cloud生命周期，不是Unity Exchange DSP的tmax。
- **【无法确认】**未恢复LevelPlay完整服务器路由、实时排序、floor优化和最终净收益决策；也没有证明LevelPlay每个第三方bid进入Vector训练。

## 9. 与Vector的边界

**【官方公开证实】**Vector与ROAS产品按预测收入动态竞价，Exchange可接外部DSP，LevelPlay可接其他网络。三者不是同一决策引擎。Exchange获胜只证明当前有效报价选择，不证明Vector选择了那个广告；Vector完整预测机制见[39](39_Axon_Vector预测与出价机制.md)。
