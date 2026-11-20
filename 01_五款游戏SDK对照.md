# SDK 实际接入与实现边界

标记规则：**业务链**＝已找到业务入口/回调至 SDK API；**框架能力**＝处理器或包装器存在但生产选择未知；**打包**＝只确认类/组件；**未发现**＝本轮指定 DEX 命名空间未检出，不能排除混淆或原生实现。所有“调用”均指静态可达代码，不表示已观察到服务端接收。

## 主矩阵

| 组件 | Car Race 1.348.2 | Meowdoku 1.25.1 | Rotate Rings 1.2.4 | Amaze GO! | Jewel Coloring 1.24.1 |
|---|---|---|---|---|---|
| Adjust | 业务链：场景挂载、初始化、campaign、事件/收入 | 未发现标准包 | 未发现标准包 | 无样本 | 业务链：归因 JNI、AdWorth 事件、ILRD |
| AppsFlyer | 本轮未建立业务链 | 业务链，6.14.2 | 业务链，6.17.5 | 无样本 | 未发现标准包 |
| Play Install Referrer | SDK 读取实现 | 包含 12 类，AppsFlyer 归因生态 | 包含 12 类、读取实现 | 无样本 | 包含 12 类，Adjust 生态 |
| TikTok Business | 启动初始化 + ILRD | 包含 1.6.1；Analyze 平台包装器与 GRT 接收端，生产路由需配置 | 1.7.1，初始化开关、收入回调直接调用 | 无样本 | **不能认作标准 Business SDK**：仅 2 个 `com.tiktok` 工具类；业务桥使用另一路实现 |
| Firebase Analytics | 22.4.0，业务事件/收入 | 22.1.2，多平台 GRT 与包装器 | 22.4.0，业务事件/收入 | 无样本 | 23.2.0，RedFirebaseAnalytics |
| 远程配置 / 实验 | Firebase fetch→activate；A/B 能力，线上实验未知 | Learnings ABCenter、UserTag、GRT 配置及游戏 AB 分支 | Hurelax/HsAbTest + 收入策略 JSON；Firebase RC 组件 | 无样本 | AdWorth 本地/配置驱动，具体生产配置缺失 |
| Meta | 广告适配器；未建立独立业务 App Events 主链 | 明确的 `facebook` GRT 接收平台；具体事件需路由 | Meta 初始化包装器；**uploadDataFB 是 Firebase**；另有 Meta S2S 意图 | 无样本 | App Events 包装器、IAA 事件与 AdWorth 状态桥 |
| Metica | 当前广告场景 provider 初始化 | 未发现标准包 | 未发现标准包 | 无样本 | 未发现标准包 |
| MAX / AdMob / ironSource / Unity Ads | MAX 生态 + Metica；多网络适配 | Learnings 广告框架 + 多网络；具体供给份额未知 | Hurelax MAX 收入业务链 + 多网络 | 无样本 | Bulldog/原生广告层 + 多网络桥 |
| AppMetrica | 打包，独立业务 activate 未证实 | 7.14.2，2173 类；独立业务 activate 未证实 | 本轮标准包未检出 | 无样本 | 8.3.0，2243 类；独立业务 activate 未证实 |
| ThinkingData | 未建立业务链 | 未建立业务链 | 业务链，归因 ID 联结、事件/异常/拟 S2S 元数据 | 无样本 | 未建立业务链 |
| Branch | 本轮标准 DEX 包未检出/未建立链 | 标准包未检出 | 标准包未检出 | 无样本 | 标准包未检出 |

【代码证实】类清单、包内属性与调用定位：[S01](EVIDENCE_INDEX.md#s01)、[V01](EVIDENCE_INDEX.md#v01)、[C01–C06](EVIDENCE_INDEX.md#c01)、[M01–M05](EVIDENCE_INDEX.md#m01)、[R01–R05](EVIDENCE_INDEX.md#r01)、[J01–J03](EVIDENCE_INDEX.md#j01)。AppsFlyer 两个版本来自原始 DEX 版本字符串和包装器证据；Rotate 包装器的 `6.2.3` 是未初始化 fallback，不能当作实际安装版本。

未给出版本的组件不以适配器版本、HTTP API 版本、数据库版本替代主 SDK 版本。完整可定位的 BuildConfig 字段在 [SDK_VERSION_EVIDENCE.json](SDK_VERSION_EVIDENCE.json)，其中大量条目是**适配器**版本。Google Play Billing 分别可确认 Car Race 9.0.0、Meowdoku/Rotate 8.1.0、Jewel 9.0.0；它们也不证明实际付费收入。

## 初始化、归因字段和事件入口

### Car Race

【代码证实】加载场景挂有启用的 `ZegoAdjust` 和 `ZegoAd_Metica`；`Start → InitAdjust`、归因回调获取 Campaign 并缓存，超时/重试配置 30 秒/1 秒。Adjust 数据结构支持 network/adgroup/creative/cost，但不能把结构字段全部当成业务分层输入。`GetCampaignType` 有名称子串分类，已发现 caller 是调试器，未证明它决定玩法或广告。[C01–C02](EVIDENCE_INDEX.md#c01)

【代码证实】`ZegoTikTok.Bootstrap` 为 BeforeSceneLoad 入口；`Report → Payload.Build → Send` 进入 TikTok SDK。Firebase 初始化、Tracker、IAA 和广告 provider 收入方法有实际 API 调用。Metica 当前 provider 与独立 MAX 备用 provider 必须区分。[C05–C06](EVIDENCE_INDEX.md#c05)

### Meowdoku

【代码证实】`launcher.gd → UniKit.initialize`，Godot plugin 桥调用 Learnings 模块；`ModuleManager.initModules → GrtModule.init → LearningsGRT.init`。AppsFlyer 初始化设置统一 UUID、conversion listener、deferred link、start。conversion callback 整理 `af_status`、`media_source`、`campaign_id`（回退 `af_c_id`）、`campaign_name`。[M02–M04](EVIDENCE_INDEX.md#m02)

【代码证实】普通 `Tracker._send → UniKitManager.send_event → UniKitAnalyzeModule` 未显式指定平台时只路由 `learnings`；专用 GRT 关卡/分钟事件明确路由四平台。不能说所有 UI/玩法事件都发给 AppsFlyer、Meta 和 Firebase。[M01](EVIDENCE_INDEX.md#m01)

【代码证实】TikTok 包装器初始化调用 `disableRetentionLogging/disableAutoIapTrack/disableAutoEnhancedDataPostbackEvent`；收入事件名 `impressionLevelAdRevenue` 走 TTAdRevenueEvent，其他事件走普通 TTBaseEvent。是否收到该事件取决于实际路由配置，不能把 SDK 自动能力当作游戏默认全开。[M03](EVIDENCE_INDEX.md#m03)

### Rotate Rings

【代码证实】`App.initDataSDK → GlDataManager`，AppsFlyer adapter `g8.a` 设置 customer ID 和 ThinkingData distinct ID；conversion callback 把结果交业务 listener。`SDKManager.handleAdRevenue` 先回传标准 AppsFlyer ILRD，再调度 `lambda$handleAdRevenue$4 → SDKKeybehaviors$evenue.upload_revenue`。TikTok 的 TTAdRevenueEvent 也在后者直接调用。[R01–R03](EVIDENCE_INDEX.md#r01)

【代码证实】`ta.b.getInfo` 向规则上下文提供 country、media_source、install_time、appversion、is_new_user。`va.f` 接收 `is_af_purchase/revenue_info` 配置；`ta.c.offline_af_points` 是可关闭 AppsFlyer 事件的名单，默认空。生产返回值未获取。[R05](EVIDENCE_INDEX.md#r05)

### Jewel Coloring

【代码证实】Adjust attribution listener `n0.k.onAttributionChanged` 将 network/campaign/creative/costAmount 传给自定义 `AdSourceUtils.receiveAdjustAdSource`；虽在 `com.facebook.appevents` 命名空间中，该桥与原生游戏联通，不能误认为官方 Meta 默认逻辑。`AdWorthEventUtils._read` 读规则并初始化 Adjust 映射；发送层进入 `common.platform.sendAdjustAWEEvent`。[J01–J03](EVIDENCE_INDEX.md#j01)

【代码证实】`sendAdjustAdRevenue` 传金额/币种/广告网络/unit/placement；`sendFacebookIAAEvent` 使用 Meta ad impression value；RedFirebase 包装器可发送事件和 purchase。包含 `sendEventUserAdWorthTest11111...55555` 测试方法，**未证明生产调用，不把其中 DONATE/CONTACT 算作真实增长事件**。[J02](EVIDENCE_INDEX.md#j02)

## 缓存、去重、失败、隐私边界

| 层次 | 已查到的实现 | 未能证明的事情 |
|---|---|---|
| Car 业务 | attribution 获取重试；PlayerPrefs 保存收入 cache；广告不可用/超时/skip/回调分支 | SDK 服务端确认、用户重装/跨设备去重、生产回传成功率 |
| Meow 业务 | GameState 为 GRT 事件持久化 once 标记；隐私未同意时 AnalyzeModule 明确丢弃；GRT 版本化本地配置缓存 | 写 once 标记不能保证送达；拒绝隐私后不能声称事件一定补发 |
| Meow SDK 包装器 | BaseAnalyze 有初始化前内存列表；`init` 的反编译顺序是先 drain 后置 isInit，需谨慎看待非空队列重入风险 | 不能直接称其可靠离线持久队列/恰好一次；本轮未运行该边界 |
| Rotate 业务 | once 标志、收入 cache/循环索引；关闭名单；conversion 失败统计与上限分支；初始化超时兜底 | 标志写入与服务器接收非事务；所有事件没有统一 impression ID 去重证明 |
| Jewel 业务 | network available 才执行时间点事件；发出后减去 intervalUSD 或清零并更新时间戳 | 这一层没有确认服务端 ACK/精确重试；其他底层队列不能由此排除 |
| SDK 内部 | 本轮额外导出 Adjust PackageHandler 与 TikTok logger/storage 方法体，见 [Q01](EVIDENCE_INDEX.md#q01) | 库内排队能力不能替代游戏自身金额口径和生产送达观测 |

【代码证实】见 [C04](EVIDENCE_INDEX.md#c04)、[M04–M05](EVIDENCE_INDEX.md#m04)、[R04–R05](EVIDENCE_INDEX.md#r04)、[J05](EVIDENCE_INDEX.md#j05)。本轮不发送事件验证、不修改客户端配置，也不对线上隐私合规作无运行证据的总体判断。

【代码证实】额外检查到的SDK内部机制是具体的：Jewel内Adjust `PackageHandler.addPackage` 将任务交给scheduler，`addI` 更新packageQueue并写盘；`sendFirstI` 检查paused与原子isSending，附带retry_count/等待时间后交给sender；`sendNextI` 更新队列并写盘、调度后续发送。Rotate内TikTok `TTAppEventStorage.persist` 先检查SDK全局激活开关，再导出事件队列、合并磁盘数据；`readFromDisk/saveToDisk`均有方法体。它们说明库有异步/持久化机制，**不证明游戏产生的每个事件都进入该队列，也不证明端到端恰好一次**。[Q01](EVIDENCE_INDEX.md#q01)
