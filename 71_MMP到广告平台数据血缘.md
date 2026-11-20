# 71号：MMP到广告平台的数据血缘

2026-11-20。**已证的是SDK字段构造、MMP官方处理契约与后台可配置的伙伴转发；没有证明四款游戏的后台配置、平台实收或训练列。** 金额被MMP记录、金额归因给来源、金额转给广告网络、金额被模型使用，是四种结论。

## 字段链矩阵

| 原始事件 | MMP字段/入口 | partner配置 | 对外事件或字段 | 平台接收 | 训练标签边界 |
|---|---|---|---|---|---|
| MAX公共收入回调 | AdjustAdRevenue：source、revenue、currency、network、unit、placement | Adjust账户广告收入权限；另启用具体伙伴共享 | `/ad_revenue`先到Adjust；不是直接送Axon/Vector | 所有实际接收UNKNOWN | 可能支持IAA统计；不能仅凭API称训练标签 |
| MAX本地收入广播 | `id`、合并后的revenue等Bundle字段 | 本地订阅topic；再由具体MMP实现转发 | SDK广播有serve ID契约，实际MMP保留/映射未知 | UNKNOWN | ID基础赋值有覆盖边界；未证明经济去重 |
| Rotate广告收入业务调用 | `AFAdRevenueData(network,APPLOVIN_MAX,USD,d)`，附app_version_code | AppsFlyer广告收入处理/目标伙伴设置 | `logAdRevenue`；另有ad_revenue2/4业务事件 | UNKNOWN | 所查调用未带MAX event_id/opportunityId；不能按金额时间认定同一账本行 |
| 真实IAP交易 | AF `af_purchase`、`af_revenue`、`af_currency`或购买连接器；Adjust收入event | 验单、退款、毛/净额口径；映射和收入开关 | Unity `purchase`；Axon checkout仅允许真实直接付款 | UNKNOWN | 必须区别金额API与验单成功交易 |
| 代理value/达标事件 | 自定义事件参数；预测值必须独立命名 | 明确事件映射；不得冒充购买 | Unity level_complete类或普通postinstall，取决于契约 | UNKNOWN | 可作辅助行为，不能当真实IAA/IAP金额 |
| 自然量/跨渠道安装和事件 | MMP归因分类、install时间、事件时间 | all-source及收入/事件授权 | Unity attributed/unattributed/organic；Axon按选定来源 | UNKNOWN | 没有开启、历史完整和成熟窗口就不能声称冷启动训练已发生 |
| 自定义关联参数 | Adjust callback_params / partner_params；AF additionalParameters | 目的渠道独立；伙伴字段映射/共享范围 | 自有回调参数与网络伙伴参数不是同一出口 | UNKNOWN | 自定义键不是保留的训练列或去重主键 |

逐行来源：L71S01/03/04/06/07/08、L71C07—14、XS43、CGS42—52、L71D01。[机器可读矩阵](lineage71/FIELD_LINEAGE.csv)补充时间、精度、join和未证状态。

## MAX→Adjust：补齐到包构造，不跨越接收边界

Adjust官方例子明确从**同一MaxAd**读取金额、网络、广告位、placement（L71S03）。新源码核验：

`AdjustAdRevenue`字段→`PackageBuilder.getAdRevenueParameters`→`ActivityKind.AD_REVENUE`、path=`/ad_revenue`→`ActivityHandler.trackAdRevenueI`排队并调`sendFirstPackage`（L71C07—10）。

序列化金额用`addDoubleWithoutRounding`；这避免该处显式小数舍入，不能恢复此前业务float转换造成的精度损失。`created_at`来自SDK处理时的`now`，不能当成MAX原始展示时间。示例和类型没有专用serve ID或precision字段；开发者可另加参数，但本轮未见目标游戏完成对应ID赋值。

Jewel既有方法把float金额转double并传USD、网络、单元、可选placement→Adjust；这只是既有业务静态证据，**不能将本轮5.8.1公共源码直接当成Jewel内嵌版本完全等价证明**。Rotate的XS43也不能证明网络已送达。

## 去重：有通用能力，不是广告收入全局恰好一次

L71C11—14：一般`AdjustEvent`显式提供deduplicationId才经过`shouldProcessEventI`；未提供则放行；历史ID是有上限并会淘汰的列表，0可禁用记忆。官方文档默认缓存10个，可配置（L71S05）。

专用`AdjustAdRevenue`没有相同成员，所查`trackAdRevenueI`没有调用该一般事件去重方法。因此不能将IAP/一般事件去重能力套到ILRD收入，更不能据此证明SDK、S2S、日报镜像已合并。本报告**不声称Adjust服务器没有其他去重**，服务器规则未知。

AppsFlyer官方说明：ROI360用户若将`af_revenue`手动事件与购买连接器/广告收入API叠加，可能重复报告收入（L71S07）；新`logAdRevenue`上线时应移除旧AdRevenue connector（L71S06）。这支持重复计账风险，不证明Rotate已发生重复：其自定义`event_revenue`是否变成保留收入字段、哪些事件被共享，必须单独核验，不能把名称相似或多次调用直接相加。

## partner参数到底送给谁

Adjust源码将callback_params与partner_params分别构造（L71C09）。官方将前者定位为开发者自有回调/BI，后者用于已配置外部伙伴（L71S04）。**加一个callback参数不等于广告网络收到它。**

Axon伙伴文档给出更具体的映射：SDK parameter→Partner parameter；未设置重命名映射时按SDK名称转发，并列出`{partner_parameters}`、`{revenue_usd}`、`{is_organic}`、`{match_type}`等（L71D01）。这证明配置契约，不证明任何任意键会被Axon接受为训练输入，也不免除共享授权与隐私限制。

## Axon和Unity不能套用同一收入映射

Axon的AppsFlyer指南将真实直接付款映射checkout、Values & revenue；明确排除IAA、预测LTV等成为这条购买收入流（CGS49/52）。**这不表示Axon完全不使用IAA；表示不能把IAA塞进checkout，并把此文当IAA标签契约。** Adjust通用in-app revenue选项同样不能自动证明专用ad revenue向Axon的字段映射。

Unity官方则明确`af_ad_revenue→ad_revenue`、`af_purchase→purchase`，要求可用账户权限、广告收入共享、事件映射、values & revenue、来源范围和窗口（CGS44/45/46）。广告收入映射成其他类型可能破坏优化。文档同时涵盖收入导入与对外postback两个配置方向，不能把“拉到AppsFlyer”当“已转给Unity”。

all-source开关是授权范围，不是实际历史文件；Lifetime窗口不是任意历史补传承诺。L71S08明确错误集成导致的事件损失不能通过事后补传恢复；Adjust S2S广告收入另有28天时效（L71S10），两者不能混成同一产品规则。

## 归因和标签仍缺什么

需要分别记录原始展示时刻、SDK构造时刻、MMP接收时刻、伙伴转发/接收时刻、安装时间、标签成熟水位。IAA必须保留precision及错误/未知值；IAP必须保留交易验单、币种、退款及净额口径；代理value必须独立列。

当前无实际接收日志，无经济唯一主键映射，无成熟完整cohort；因此不报告训练行数、D28标签覆盖率或真实ROAS。最小补证是**脱敏的配置导出＋同一经济事件跨系统schema/对账规则**，无需真实用户标识。

原始URL、片段、版本和哈希见[来源目录](lineage71/SOURCE_CATALOG.md)。
