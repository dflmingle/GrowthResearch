# 61＋63原始证据增量目录

旧MA60对象和矩阵行不改；本轮只新增更精确的事件、预算和决策边界。文档行为不等于生产代码或独立观测。

<a id="rv61s01"></a>
## RV61S01 · Unity / Post-install event data

- 原文：https://docs.unity.com/en-us/grow/acquire/partner-integration/app-data/post-install-event-data.md
- 位置：[model-architecture/round61-63/public/u-appdata-direct.txt:L10](../../model-architecture/round61-63/public/u-appdata-direct.txt)；L10—L28
- 日期：2026-11-18；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`4736a5f5569acd229cfe310d84e689f0d7d7a52be38210b343d0403834929a5f`
- 短摘录：Post-install event data informs Unity's models
- 主张：【官方公开证实】正式数据契约把session/purchase/ad_revenue/level_complete与相应目标分开，并建议额外事件数据
- 适用范围：Unity Ads UA MMP事件契约，不是逐行训练label
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：收到事件种类不证明所有字段实际用于每个模型；level_complete不是收入

原始HTTP响应：[model-architecture/round61-63/public/u-appdata-direct.raw](../../model-architecture/round61-63/public/u-appdata-direct.raw)；SHA256 `e7365de537bb9448d6a7ed321f43830c6fa4e3485e5e539586b40da4407993e4`。

<a id="rv61s02"></a>
## RV61S02 · Unity / Post-install data loss

- 原文：https://docs.unity.com/en-us/grow/acquire/partner-integration/app-data/post-install-event-data.md
- 位置：[model-architecture/round61-63/public/u-appdata-direct.txt:L38](../../model-architecture/round61-63/public/u-appdata-direct.txt)；L38—L59
- 日期：2026-11-18；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`4736a5f5569acd229cfe310d84e689f0d7d7a52be38210b343d0403834929a5f`
- 短摘录：your servers can't retroactively send data from events
- 主张：【官方公开证实】官方警告错误集成会丢失事件且不能靠服务器retroactive发送补回；MMP事件种类和订阅支持有条件
- 适用范围：Unity所述MMP集成，不扩展为所有收入平台的绝对限制
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：该产品契约不证明一般技术上无法补数，或所有MMP永不支持backfill；不等于训练标签迟到窗口

原始HTTP响应：[model-architecture/round61-63/public/u-appdata-direct.raw](../../model-architecture/round61-63/public/u-appdata-direct.raw)；SHA256 `e7365de537bb9448d6a7ed321f43830c6fa4e3485e5e539586b40da4407993e4`。

<a id="rv61s03"></a>
## RV61S03 · Unity / Revenue event mapping

- 原文：https://docs.unity.com/en-us/grow/acquire/partner-integration/integration-best-practices.md
- 位置：[model-architecture/round61-63/public/u-integration-best.txt:L60](../../model-architecture/round61-63/public/u-integration-best.txt)；L60—L88
- 日期：2026-02-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`dd07456e6a4f607a3bbcaa70aadd1eb0f5c78f570cc7786c3ac5085d6727a3ba`
- 短摘录：Sending ad revenue as a different event type can cause campaign optimization to stop working
- 主张：【官方公开证实】Unity明确IAA要走专用收入通道；不支持时不能伪装purchase，否则可能破坏优化
- 适用范围：Adjust及除Singular外所述集成契约
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：此处不能推断具体损失函数；真正Hybrid组合目标不等于混淆事件语义

原始HTTP响应：[model-architecture/round61-63/public/u-integration-best.raw](../../model-architecture/round61-63/public/u-integration-best.raw)；SHA256 `3d54d826d0b5ea50a3d91e2319c012c5270f65db436fe671ed1c5a3c98d4868a`。

<a id="rv61s04"></a>
## RV61S04 · Unity / Singular mapping exception

- 原文：https://docs.unity.com/en-us/grow/acquire/partner-integration/integration-best-practices.md
- 位置：[model-architecture/round61-63/public/u-integration-best.txt:L107](../../model-architecture/round61-63/public/u-integration-best.txt)；L107—L124
- 日期：2026-02-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`dd07456e6a4f607a3bbcaa70aadd1eb0f5c78f570cc7786c3ac5085d6727a3ba`
- 短摘录：Singular is the only MMP that supports sending ad revenue and in-app purchase events together
- 主张：【官方公开证实】Unity文档对Singular给出__REVENUE__*及Send all ad monetization events的特定例外
- 适用范围：Unity-Singular partner配置，仅限文档表述
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：不证明任意MMP可混报；例外不允许把代理value当收入；不证明游戏已启用

原始HTTP响应：[model-architecture/round61-63/public/u-integration-best.raw](../../model-architecture/round61-63/public/u-integration-best.raw)；SHA256 `3d54d826d0b5ea50a3d91e2319c012c5270f65db436fe671ed1c5a3c98d4868a`。

<a id="rv61s05"></a>
## RV61S05 · Unity / Budget hierarchy/throttling

- 原文：https://docs.unity.com/en-us/grow/acquire/budgets/introduction.md
- 位置：[model-architecture/round61-63/public/u-budget-intro.txt:L20](../../model-architecture/round61-63/public/u-budget-intro.txt)；L20—L61
- 日期：2026-06-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`a1d66a7f7e97bad3473058ee8af40fa74f12864c559d2d17ca5d0c71bece5447`
- 短摘录：use the target budget to throttle your campaign
- 主张：【官方公开证实】公开组织/活动/日预算分层；日预算为目标/平均值，接近限制会throttle且可超支，UTC重置
- 适用范围：Unity UA预算行为，非特定模型公式
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：预算不是逐请求硬上限；不公开控制器系数或每bid multiplier；部分设置页与总览需核对具体产品

原始HTTP响应：[model-architecture/round61-63/public/u-budget-intro.raw](../../model-architecture/round61-63/public/u-budget-intro.raw)；SHA256 `62852d018f59d3e1595ccdf402ac252765c32ebe402b138147a940d4ceb4e090`。

<a id="rv61s06"></a>
## RV61S06 · Unity / Multi-country allocation

- 原文：https://docs.unity.com/en-us/grow/acquire/budgets/introduction.md
- 位置：[model-architecture/round61-63/public/u-budget-intro.txt:L63](../../model-architecture/round61-63/public/u-budget-intro.txt)；L63—L86
- 日期：2026-06-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`a1d66a7f7e97bad3473058ee8af40fa74f12864c559d2d17ca5d0c71bece5447`
- 短摘录：distributes spend across the countries in each group in real time
- 主张：【官方公开证实】公开国家组预算实时按赢标/转化分配；Daily/Geo Capped会暂停全部或部分交付
- 适用范围：全部campaign types公开预算产品行为
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：按performance分配不等于每次按D28预测值排序，也不证明共享模型参数

原始HTTP响应：[model-architecture/round61-63/public/u-budget-intro.raw](../../model-architecture/round61-63/public/u-budget-intro.raw)；SHA256 `62852d018f59d3e1595ccdf402ac252765c32ebe402b138147a940d4ceb4e090`。

<a id="rv61s07"></a>
## RV61S07 · Unity / ROAS automated bidding

- 原文：https://docs.unity.com/en-us/grow/acquire/budgets/best-practices.md
- 位置：[model-architecture/round61-63/public/u-budget-best.txt:L14](../../model-architecture/round61-63/public/u-budget-best.txt)；L14—L32
- 日期：2026-06-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`62b99d6cfe8c443333cdd4c530a023a62a08ec4358886da132f5f8ea2ec27c75`
- 短摘录：with CPI billing, the campaign automatically uses Automated bidding
- 主张：【官方公开证实】官方明确CPI计费ROAS自动使用Automated bidding，并描述按日调整/周级预算和约7日适应
- 适用范围：Unity ROAS+CPI billing预算策略
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：限定计费和产品条件；不把安装量自动竞价目标外推为所有ROAS策略；不是生产源码

原始HTTP响应：[model-architecture/round61-63/public/u-budget-best.raw](../../model-architecture/round61-63/public/u-budget-best.raw)；SHA256 `379a058238b1fdf60bdfa3f4191cee2d828fa8fabc8d74cfa9d7fafb97b923f4`。

<a id="rv61s08"></a>
## RV61S08 · Unity / Exploration budget

- 原文：https://docs.unity.com/en-us/grow/acquire/budgets/best-practices.md
- 位置：[model-architecture/round61-63/public/u-budget-best.txt:L34](../../model-architecture/round61-63/public/u-budget-best.txt)；L34—L40
- 日期：2026-06-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`62b99d6cfe8c443333cdd4c530a023a62a08ec4358886da132f5f8ea2ec27c75`
- 短摘录：explore your campaign and creatives
- 主张：【官方公开证实】官方明确先探索campaign/creatives，建议campaign预算至少为日预算5倍以提供探索资金
- 适用范围：Unity UA预算建议；产品条件见原文
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：5倍是运营建议不是模型样本阈值；不证明UCB/Thompson/RL或用方差调价

原始HTTP响应：[model-architecture/round61-63/public/u-budget-best.raw](../../model-architecture/round61-63/public/u-budget-best.raw)；SHA256 `379a058238b1fdf60bdfa3f4191cee2d828fa8fabc8d74cfa9d7fafb97b923f4`。

<a id="rv61s09"></a>
## RV61S09 · Unity / Seven-day pacing

- 原文：https://docs.unity.com/en-us/grow/acquire/budgets/best-practices.md
- 位置：[model-architecture/round61-63/public/u-budget-best.txt:L73](../../model-architecture/round61-63/public/u-budget-best.txt)；L73—L83
- 日期：2026-06-12；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`62b99d6cfe8c443333cdd4c530a023a62a08ec4358886da132f5f8ea2ec27c75`
- 短摘录：operates on a 7-day rolling window rather than enforcing hard daily limits
- 主张：【官方公开证实】预算文档明确7日滚动窗口补偿超支/欠支，含国家组预算；是可核验的pacing产品行为
- 适用范围：Unity日预算管理说明；非Vector网络架构
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：不是每自然日保证硬cap，也没有公开单次出价的pacing因子或控制算法

原始HTTP响应：[model-architecture/round61-63/public/u-budget-best.raw](../../model-architecture/round61-63/public/u-budget-best.raw)；SHA256 `379a058238b1fdf60bdfa3f4191cee2d828fa8fabc8d74cfa9d7fafb97b923f4`。

<a id="rv61s10"></a>
## RV61S10 · Unity / Country ROAS and budget setup

- 原文：https://docs.unity.com/en-us/grow/acquire/campaigns/roas/create-a-roas-campaign.md
- 位置：[model-architecture/round61-63/public/u-create-roas.txt:L16](../../model-architecture/round61-63/public/u-create-roas.txt)；L16—L42
- 日期：2026-03-05；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`b8557346f75195e7bd023602cdf5e640526c6dd611cfd7eb79092f9a9a66810f`
- 短摘录：set a [ROAS goal]
- 主张：【官方公开证实】官方配置要求选择优化类型/窗口、按国家设ROAS目标、campaign预算和归因链接
- 适用范围：Unity ROAS campaign设置
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：配置存在不证明某目标游戏已配置；不是国家用户价值训练特征已证

原始HTTP响应：[model-architecture/round61-63/public/u-create-roas.raw](../../model-architecture/round61-63/public/u-create-roas.raw)；SHA256 `54bd0f78f7978dd5da6503edb601938db7e91dbad8644ed4ae00cd57f4b7a8e4`。

<a id="rv61s11"></a>
## RV61S11 · Unity / CVR/CPI/eCPM exposure

- 原文：https://docs.unity.com/en-us/grow/acquire/bids/introduction.md
- 位置：[model-architecture/round61-63/public/u-bid-intro.txt:L20](../../model-architecture/round61-63/public/u-bid-intro.txt)；L20—L36
- 日期：2025-08-25；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`4b6955ea89691ef8ea899db0e1c0b866fc334883f5de006134b1479112768a07`
- 短摘录：determined by the CVR
- 主张：【官方公开证实】官方将展示到安装CVR与CPI连接到eCPM/曝光，列收入目标动态竞价
- 适用范围：Unity UA竞价术语与产品关系，不是报价公式
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：不证明独立pInstall神经head；表中tCPM/Target cost per install标签不一致不能自行修成真实模型

原始HTTP响应：[model-architecture/round61-63/public/u-bid-intro.raw](../../model-architecture/round61-63/public/u-bid-intro.raw)；SHA256 `232c7a2ffbe4803438a7bc5015159154115108628948ab2996407d7a35ae2e95`。

<a id="rv61s12"></a>
## RV61S12 · AppLovin / Scale and budget recommendations

- 原文：https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/scale-your-campaign
- 位置：[model-architecture/round61-63/public/al-scale-right.txt:L47](../../model-architecture/round61-63/public/al-scale-right.txt)；L47—L66
- 日期：not stated; retrieved/reviewed 2026-11-19；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`3905f03b9eba9061d9cc9a0cb7719064e1f52d937a6d5e5e1679dfae8212bfda`
- 短摘录：at least 15–20 conversions
- 主张：【官方公开证实】官方建议每天15–20目标转化、跨国单一全局预算及符合利润目标的goal；缺失conversion会影响未来campaign
- 适用范围：AppLovin apps UA运营契约
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：转化数是稳定表现建议，不是Axon训练门槛；全球预算建议不暴露pacing算法；未证明四款实际设置

原始HTTP响应：[model-architecture/round61-63/public/al-scale-right.raw](../../model-architecture/round61-63/public/al-scale-right.raw)；SHA256 `098e05b774e0474687ebf41c332b2f0d77e4f7bd199306da283101d58faba8bf`。

<a id="rv61s13"></a>
## RV61S13 · AppLovin / Pixel/SDK/S2S deduplication

- 原文：https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/deduplicating-events
- 位置：[model-architecture/round61-63/public/al-website-dedup.txt:L13](../../model-architecture/round61-63/public/al-website-dedup.txt)；L13—L50
- 日期：not stated; retrieved/reviewed 2026-11-19；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`dba9b76e7b6372390bff441e8337954c17ff8141354d0a8bb67fe6850f5c6e33`
- 短摘录：no more than thirty seconds apart
- 主张：【官方公开证实】网站文档给同事件跨Pixel/site-to-site/SDK共享dedupe_id：30秒内merge，超过5分钟的后到副本drop
- 适用范围：AppLovin网站事件多通路去重文档，含SDK options示例
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：30秒至5分钟间行为未写清；不证明退款回滚、IAA/MMP去重或训练exactly-once；不能套到四款

原始HTTP响应：[model-architecture/round61-63/public/al-website-dedup.raw](../../model-architecture/round61-63/public/al-website-dedup.raw)；SHA256 `4f1dddcb8ff91783293f89eed082cb030dc322f3817fb52ad421656aba9c98fc`。

<a id="rv61s14"></a>
## RV61S14 · Adjust / Android5.8.1 revenue validation

- 原文：https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1-sources.jar
- 位置：[ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/AdjustEvent.java:L142](../../ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/AdjustEvent.java)；L142—L164
- 日期：not stated; retrieved/reviewed 2026-11-19；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`cc5a91b32787a9a966a44df8f1b379b45bcb2eb4443b322af7ee32960f0fd187`
- 短摘录：revenue < 0.0
- 主张：【SDK代码证实】AdjustEvent.checkRevenue对负金额返回false，零不被该比较拒绝；需非空currency
- 适用范围：独立Adjust Android5.8.1 SDK
- 部署层级：official standalone SDK code; not observed production
- 未知/反证：setRevenue不赋负金额不代表整事件必被丢弃；不证明退款永不支持/零收入玩家成为训练样本；非四款具体集成版

官方包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar](../../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar)；SHA256 `98caabf85f07a6859767465c90394ee1e097c5da12f7bb967ea8f01f2272b84e`；来源 https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1.aar。

官方包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1-sources.jar](../../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1-sources.jar)；SHA256 `dfee5dda1f80d86b1e0af56af77e04568f7929462a5fe09ffd6b75254180030b`；来源 https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1-sources.jar。

<a id="rv61s15"></a>
## RV61S15 · AppLovin / MAX unified first-price auction

- 原文：https://support.applovin.com/en/max/demand-partners/auction-dynamics
- 位置：[auction/al-dynamics.txt:L13](../../auction/al-dynamics.txt)；L13—L40
- 日期：not stated; retrieved/reviewed 2026-11-19；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`43dfae6b9630d9468767e8383d2d3f8796d3b97a9cf0345175979c9c14e430ba`
- 短摘录：unified first-price auction
- 主张：【官方公开证实】官方协议明确MAX收集有效SDK/DSP报价，与waterfall合并按最高CPM选取；render后触发billing
- 适用范围：MAX Exchange需求伙伴拍卖协议；复用已取得原文
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：供给侧机制不是Axon私有价值→报价公式；第一价格本身不证明bid shading或竞争者数据进入Axon训练

<a id="rv61s16"></a>
## RV61S16 · Unity / Exchange deadline/first-price

- 原文：https://docs.unity.com/en-us/grow/programmatic/unity-exchange/get-started.md
- 位置：[auction/unity-get-started.txt:L20](../../auction/unity-get-started.txt)；L20—L34
- 日期：2026-04-27；查阅：2026-11-19T10:38:03.055922+00:00
- 文件SHA256：`7e8f03b72a2a3bbd9005f2e542907cc630d06b5855b26ac8a28839c157ace009`
- 短摘录：50ms is deducted
- 主张：【官方公开证实】Unity Exchange公开第一价格及动态tmax；waterfall seat最高1000ms，bidding按mediation配置扣50ms
- 适用范围：Unity Exchange公开DSP协议；复用原文
- 部署层级：public behavioral contract; not independently observed production
- 未知/反证：exchange响应预算不是Vector推断SLA或SDK加载时限；不证明bid shading算法
