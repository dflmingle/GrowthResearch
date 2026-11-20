# Unity 非游戏 App、Runtime 与广告交易数据

2026-11-19。**Unity 的非游戏入口不只 Runtime：原生 Ads SDK、中介、MMP、Exchange、外部分析链接都能独立产生数据。反过来，非游戏 App 接入 Unity Ads 不证明它使用 Unity 引擎，更不证明 Runtime 数据进入 Vector。**

## 1. 实际非游戏接入证据

【公开资料证实】本轮找到三个明确具名的非游戏样本，而不是由 SDK 功能推演案例：

| 产品 | 原始披露 | 可支持的结论 | 无法支持的结论 |
|---|---|---|---|
| ReelShort（短剧） | [Play所链政策](https://crazymaplestudios.com/v/privacy-agreement.html)，[本地原文](nongame/content-reelshort-official-policy.txt)：列 Unityads；广告位置、可见时长、点击/响应等类别 | 官方开发者政策将 Unityads 列为广告伙伴 | 精确 SDK 版本、每个字段已传、视频观看记录流入 Unity、使用引擎/Vector |
| Winwalk（计步奖励） | [政策](https://www.winwalk.app/privacy-policy)，[原文](nongame/life-winwalk.txt)：Unity Ads 在 Advertising, surveys and rewards 类别 | 有明确非游戏生活服务广告伙伴披露 | Google Fit/步数进入 Unity；政策还明确 Google 用户数据不对第三方分享 |
| WeWard（步行/购物奖励） | [政策](https://www.wewardapp.com/legal/privacy-policy)，[原文](nongame/life-weward-correct.txt)：广告共享类别和 Unity/ironSource 等名单 | 有经同意的广告/效果衡量共享声明 | 每个伙伴收到完整字段表、所有定位/浏览数据可训练、广告网络接入等于 Unity 引擎 |

来源：[NG04](EVIDENCE_INDEX.md#ng04)。未取得上述 App 的 APK，没有准确 SDK 版本/实际调用和生产请求证明。不是“已验证3款当前二进制全部正常发送”的结论。

**WeWard 的排除条款很重要：**政策将某些位置数据用于地图分区、奖励和防欺诈，明确不用于广告、不共享广告伙伴、不出售；非商家域名不保留，相关导航数据不出售、不用于广告定向/模型训练。其广告共享表同时提到年龄等总体类别，**不能写成 Unity/AppLovin 每家均收到年龄**；AppLovin 自身公开模型说明还排除年龄/性别等 protected characteristics。应按接收方规则和实际路由核实，而不是把政策整张表复制成广告 payload。

## 2. Unity Ads / LevelPlay 可以脱离引擎运行

【官方公开证实】[Android 原生初始化文档](nongame/unity-ads-android-native.raw)提供原生 Java/Activity 的 `UnityAds.initialize` 与监听器。它不是只有 Unity C# 游戏才能调用的接口。

【SDK代码证实】复用已取得 Unity Ads4.17/4.18.1、LevelPlay9.3/9.4/9.5的[代码摘录](vector/CODE_EVIDENCE.json)：请求包含广告机会、广告位、设备/会话、TCF/developerConsent、广告格式/中介上下文；operative event 有广告tracking token等，队列及工作任务分别可定位。`LevelPlayAdInfo` 有network/revenue/precision/country等。

这证明原生非游戏 App 具有同类广告数据接口；**不证明某非游戏 App 向 Unity 发送了它的编辑内容、搜索全文、通讯录、步数、收据或全部消费历史**。广告生命周期与应用内容行为是不同数据流。[VG05](EVIDENCE_INDEX.md#vg05)

## 3. Runtime 与更广义 Developer Data

| 来源 | 可以是什么 | 必须满足的边界 |
|---|---|---|
| Unity Engine Runtime | 【官方公开证实】运行诊断/引擎上下文；不限于游戏用途的 Unity 产品 | 要使用对应 Unity Runtime；配置与云链接/版本/Diagnostics条件仍适用。非引擎 App 的 Ads SDK 事件不是引擎 Runtime |
| Unity Analytics | 【官方公开证实】标准事件、开发者声明的custom events、transaction/transactionFailed | 业务事件须注册、实现并允许采集，非游戏也不能自动推定已埋点 |
| Unity IAP / D2C | 【官方公开证实】购买交易、账单等对应服务信息 | 真实商品/订阅购买与虚拟奖励分开；收集/使用条件及服务角色需单列 |
| 外部 Firebase/BigQuery | 【官方公开证实】开发者拥有的数据，链接后可作为 Developer Data，并采集source-specific identifiers | 明确的链接和Collection/Usage Settings；外部数据不因此变成引擎自动观察 |
| MMP 安装后事件 | 【官方公开证实】授权安装、会话、真实购买/广告收入 | advertiser Game ID、partner共享和事件映射；不依赖本体使用Unity引擎 |

资料：[Developer Data外部接入](nongame/unity-ddf-external.raw)、[自定义事件](nongame/unity-analytics-correct.txt)、[交易事件](nongame/unity-analytics-revenue.txt)、[既有MMP链](24_Unity与AppLovin技术对比.md)、[NG08](EVIDENCE_INDEX.md#ng08)。

【合理推断】使用 Unity 的非游戏应用，在合法配置后可以记录参与时长、功能动作、购物或订阅事件；这属于可实现的业务埋点，不是系统自动理解所有用户行为。Analytics 的事件支持和 REST 接口也不证明任意外部应用事件会被接收并用于 Vector。

【官方公开证实】交易文档明确 `transactionFailed` 不贡献收入指标；Unity IAP4.2+会自动发送对应交易事件，手动再发会重复计算。订阅首次购买/续费/退款等不能只靠“有 transaction API”推断全部被正确覆盖。**没有把广告观看奖励或预测LTV伪装成IAP。**

### 授权默认值复核

【官方公开证实】Developer Data的 Collection 与 Usage 分开；Additional Recommended Data、跨开发者组合/建模选项不因未配置就全开。End-user consent中的 `ads_intent` 与 `analytics_intent` 不同。6000.3官方绑定只有接口层证据，native collector→Vector训练仍无完整原文链。

【官方公开证实】关闭 Diagnostics 不会关闭通过其他产品/外部链接独立收集的所有数据；这一点已按最新配置文档在 [25](25_Unity_Runtime数据优势调查.md)说明。不能建议用一个开关管理所有Ads/MMP/Analytics隐私状态。

【无法确认】本轮非游戏样本中，没有取得 Unity 引擎版本与 Developer Data授权配置、Runtime接收日志、Vector训练使用的可核验配对。**已证明非游戏广告伙伴，尚未证明非游戏 Runtime→Vector 实例。**

## 4. Exchange：实际公开的交易字段

【官方公开证实】[Unity Exchange bid requests](nongame/unity-exchange-bid-fields.raw)，保留原始Markdown与行号。字段协议包括：

- `imp`/video/banner：广告尺寸/格式、可支持API、底价/币种、placement等。
- `app`：bundle、name、storeurl、publisher；文档明确**某些合约禁止时不传应用信息**。
- `device`：UA、OS/型号、网络/IP、语言等，条件化 `ifa/lmt` 等；geo有协议定义/示例，不能把示例坐标当实际GPS采集证据。
- `regs`/隐私及归因扩展：例如COPPA、SKAdNetwork相关对象；具体字段出现仍受集成和权限约束。未声称已完全审计所有GDPR/GPP扩展。

【官方公开证实】先前[Exchange流程](vector/doc-get-started.html)为广告请求→DSP bid request→第一价格拍卖→缓存→展示通知/trackers。**bid request参与者可见的上下文，不等于所有其他网络用户数据库或完整业务内容。**也不能由协议能力断言任一目标广告主实际参与某次交易。

【官方公开证实】Unity Exchange的 [RampID美加公告](vector/exchange-rampid.txt)提供实际商业身份互通能力证据，需要双方支持；不是仅从广告ID推测身份服务。但没有本轮样本启用、匹配成功或Vector使用RampID的证据。

## 5. Unity 与 AppLovin：政策中的具体合作角色

本轮未找到单独猜测的 advertising-partners URL，但在[Unity正式隐私政策](https://unity.com/legal/game-player-and-app-user-privacy-policy)本体取得完整内容：[快照](nongame/unity-policy.txt)，[定位摘录](nongame/SOURCE_EXCERPTS.json)。

【官方公开证实】其“third-party partners”段列 `AppLovin (FKA MoPub)`，并明确伙伴可独立于Unity或与其合作收集数据、结合跨时间信息，用于profile及个性化广告；中介段另列 `Applovin`，原文写：**“mediation product shares your Personal Data to the bidding partners identified below.”**

可支持的分层结论：

| 角色 | 证据判断 |
|---|---|
| Unity为供给/中介，AppLovin作为参与需求/竞价伙伴 | 【官方公开证实】名单加数据共享用途声明；不是只有公司Logo |
| 两家同时向广告主销售获客 | 【官方公开证实】两家现有产品文档，竞争关系与交易合作可共存 |
| 某次Unity请求实际发送给AppLovin、并产生win/loss | 【无法确认】没有授权bid log/流量记录；不能从名单证明当前逐笔交易 |
| Unity向AppLovin同步完整电商订单/Runtime、供Axon训练 | 【无法确认】声明未给出这条逐字段业务链 |
| AppLovin把其他竞价者用户数据/出价喂Axon | 【官方公开证实】AppLovin官方模型说明明确否认采集/摄入此类数据；不能拿Unity名单反向推定它发生 |

名单包含历史名称，抓取日期不等于每个伙伴仍有实时交易。**政策已说明允许/存在的共享场景；它不是某个用户的传输抓包或模型训练证据。**[NG08](EVIDENCE_INDEX.md#ng08) [NG09](EVIDENCE_INDEX.md#ng09)

## 6. 另一个明确但不同的跨应用入口

【官方公开证实】同一Unity政策产品清单描述 `Unity Player Sign In` 可提供“persistent ID across projects or games/apps”；还列 Web Offerwall、Unity Rewards App、Unity IAP5.4+等入口。因此不能笼统说 Unity 没有跨应用账户或奖励业务。

【无法确认】用户实际采用该登录、哪些开发者共享了同一用户、该账户标识是否进入广告模型、Offerwall/Rewards具体样本当前SDK和字段路由。**账户跨项目能力、广告ID归因、RampID身份互通、Vector训练是四个不同命题。**本轮没有登录任何账号、采集标识或测试受众。
