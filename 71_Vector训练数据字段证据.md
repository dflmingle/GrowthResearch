# 71号：Vector训练数据字段证据

2026-11-20。**Unity公开资料已直接说明多类post-install事件影响模型和优化campaign，并明确预启动SDK数据/未归因postback可帮助训练；仍没有公开物理训练表、逐字段消费、去重或个人级跨游戏join。** 比Axon披露更细，不等于效果更强。

## 字段与用途必须分层

| 来源层 | 字段/数据类别 | 已证用途或契约 | 仍缺什么 |
|---|---|---|---|
| Unity Ads Token | tokenId、tokenNumber及已核验上下文；CGS01/02 | 客户端竞价信号构造 | opaque token服务端展开及特征列 |
| Ads operative事件 | eventId、impressionOpportunityId、trackingToken、eventType、additionalData、可选sid、设备/会话上下文 | L71C16/21明确构造，L71C18/19持久化传输 | 类型语义/金额、接收、标签消费 |
| MMP session | app打开/session事件 | 官方Retention产品关联；L71S08 | 实际接收行及物理特征列 |
| MMP purchase | 真实购买金额、币种、安装/事件时间；映射purchase | IAP/Hybrid/Payer产品关联；L71S08、CGS44/46/48 | 退款、验单、成熟窗口和去重的实际实现 |
| MMP ad_revenue | 广告收入金额及对应事件 | Ad Revenue/Hybrid ROAS关联；L71S08、CGS44/46 | 是否保留ILRD粒度、precision、经济展示主键 |
| milestone | level_complete等 | 里程碑/事件优化；L71S08 | 不能变成收入金额，无实际后台映射证据 |
| 自定义postback参数 | gamer_id、game_id、install_ts、event、value/currency或revenue_usd、归因标记等 | CGS48的旧自定义接口契约 | 并非所有当前MMP接口都同schema；不代表收齐或入模 |
| 未归因/自然量/跨渠道 | SDK data及post-install postbacks，来源分类 | CGS42/43：预启动至少两周可帮助模型训练；all-source建议 | 每广告主实际开启、授权、覆盖与训练采样 |
| 跨游戏行为/聚合cohort | 官方D7/D28技术产品文章类别 | MA60S17：bid decision时的优化信息 | 聚合先验、共享表示、个人历史三者仍不可辨识 |

新官方文档[Post-install event data](https://docs.unity.com/en-us/grow/acquire/partner-integration/app-data/post-install-event-data.md)，标注更新2026-11-18，原文短摘：**“Post-install event data informs Unity's models”**。L71S08保留原始Markdown、采集时间及SHA256。它比泛泛SDK介绍更直接证明事件类别→模型用途，但**不是训练列契约**。

## MMP映射不是一个统一开关

AppsFlyer：Unity集成激活、正确Game ID、来源范围、postback窗口、事件映射、数值与收入选项分别配置；IAA需要相应账户能力和收入共享。`af_ad_revenue→ad_revenue`与`af_purchase→purchase`不能互换。Advanced Privacy影响可共享数据；文档说明不能当作绕过同意的指令（CGS44/45）。

Adjust：事件映射和收入共享独立；不支持专用广告收入共享时不得伪装成其他类型发送（CGS46）。没有本项目四游戏的控制台导出，因此任何启用结论都UNKNOWN。

L71S08新增的明确限制：错误集成会丢事件，服务器不能事后补传这些事件。故“Lifetime窗口”不保证新接入平台可取得任意过去收入。Adjust S2S本身另有28天时效（L71S10），不可将它当作Unity标签窗口。

## D7/D28与真实标签的边界

官方ROAS产品和文章支持D7/D28收入目标、预测和优化用途；不公开每行采用的是成熟累计值、部分窗口外推、概率分布、退款后净值还是不同任务输出。不能把目标D28直接理解成所有训练样本都已成熟28天。

要构造可验证标签，至少需要安装cohort分母、零收入的观察完整性、原始事件及可用时间、金额币种/precision、重复/退款修正规则、成熟水位。这是研究准入要求，**不是宣称Unity内部就按该schema实现**。

## 广告事件与真实收入尚未接通

本轮确认机会/事件token快照及重试边界，但没有证据将operative additionalData解释成IAA收入，更没有明确连接到IAP/Analytics/Insights。相同公司、同SDK工程或名称近似不是join契约。

受限能力仍可能帮助优化：同App历史数据、跨游戏聚合统计、共享模型参数都可在不关联个人跨App身份时成立。公开“cross-game patterns/cohort”不能唯一确定哪种生产实现；个人级路径仍受授权、标识作用域及平台限制。

## 最小补证与停止判断

最小材料：一份Unity/MMP授权的字段级例子，说明`原始IAA/IAP→MMP postback字段→Unity接收→归因安装/去重键→D7/D28目标列→训练/推断版本`，并列哪些特征在bid_time前已可用。可以只有schema、无个人数据。

公开材料可证明产品级消费和客户端构造，但不能观察生产训练表。没有该材料，停止从token、事件名或招聘关键词推断更细模型；不报告Vector相对Axon的精度/ROAS优势。

全部原件、精确片段、原包哈希见[来源目录](lineage71/SOURCE_CATALOG.md)、[代码证据](lineage71/CODE_EVIDENCE.json)。
