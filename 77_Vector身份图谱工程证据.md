# 77号：Vector身份图谱工程证据

2026-11-20。**核对3份明确属于Vector的官方工程岗位，其中2份已由旧证据覆盖，真正新增1份数据基础设施岗位；没有找到Vector生产价值模型读取个人跨App/跨设备身份解析结果的直接证据。C_graph和独立增益D仍UNKNOWN。** 不将岗位别名重新计算为新成果。

## Vector工程团队材料与别名去重

官方Unity careers页面的Next.js公开载荷列出129个职位，随后只读取3个相关Workday岗位。普通可见正文为空不代表岗位不存在；原始HTML内有JobPosting JSON-LD，描述及datePosted已保存，未登录、申请或调用身份接口。

| 证据 | 团队及日期 | 原文短摘录 | 正确结论 |
|---|---|---|---|
| 复用S30/MA60S19 / PE77C06，JOBREQ-2616596 | Vector Ads Modeling；2026-09-28 | Leverage rich user data and large-scale compute to validate models rapidly. | 用户行为建模/广告推荐研发职责明确对应Vector；未定义身份图谱输入 |
| PE77S04 / PE77C07，JOBREQ-2616462 | Vector Data Infrastructure；2026-11-13 | our platform also supports large-scale model training, feature generation, and experimentation workflows that power production ML systems. | 官方描述支持production ML的训练/特征平台；未给出身份输入列、join或消费模型 |
| 复用S28/MA60S20 / PE77C08，JOBREQ-2616286 | Vector Bidding Science / Vector AI org；2026-09-28 | ...bidding and pacing algorithms that automatically maximize advertisers’ returns. | 明确竞价/pacing团队和在线A/B职责；不是图谱特征已部署或收益证明 |

本轮HTML快照采集均为2026-11-20。PE77S03/05在实体去重时发现与旧CXS接口归档是同一JOBREQ，属于两次重复获取的执行偏差；保留快照但不计新增，主矩阵引用旧ID。字段datePosted不是模型上线日期。岗位用“productionalize research”“will develop”表述任务，不能直接写成已上线实现。Data Infrastructure对现有平台的陈述可作为官方团队架构描述，但不能升级为某项图谱特征生产消费。来源URL、正文位置及SHA256见[目录](production77/SOURCE_CATALOG.md)和[矩阵](77_生产身份图谱工程证据矩阵.csv)。

## 与既有用途披露如何连接

MA60S17（官方D7/D28文章，2026-06-25）已有原文：

> It uses both attributed data and unattributed data, like cross-game behavioral patterns and aggregate cohort insights, to distinguish between these player types at the moment of bid decision.

这确实说明Vector的跨游戏/cohort知识和bid-time用途，不能说完全没有用途证据。但cross-game behavioral patterns未定义为同一自然人记录；aggregate cohort insights明确也相容于非个人机制。新岗位的rich user data没有补充这些数据怎样关联、何时可用或具体由哪个线上模型读取。

不能把三岗位串起来便声称“身份解析服务→特征库→Vector报价器”已经恢复。训练数据基础设施、广告排序和竞价优化本来就可以由上下文、同App历史、聚合先验和共享参数驱动。

## 最近的身份组件线索属于Exchange，不属于Vector

IG72S05为2026-04-02官方Unity Exchange/RampID整合公告，明确美加库存的身份受众激活可用性及接收方支持条件。本轮复用，不重做伙伴名单。它比双方拥有相似ID字段更强，但实际接收产品是Exchange；没有Exchange→Vector特征表、模型版本及实际读取的桥接材料。

仍继承74号反误判：返回RampID可能只是derived输出，不代表已有实体匹配；maintained/derived必须区分；matchConfidence不是自动校准概率；月活设备数不是匹配人数。即使接收成功，也可能只支持第三方DSP受众激活，而非Vector价值预测。岗位未排除这一解释。

## 新专利：与身份图谱的实质距离

PE77S06 / PE77C11，US12353873B2，标题为Methods circuits devices systems and functionally associated machine executable code for recommendation and distribution of digital content。

- 发明人：Arnon Harish、Sagi Ben Basat；申请号US17/301,134。
- Google公报所列优先权2015-08-11、申请2021-03-26、授权/公开2025-07-08。
- Current Assignee同时列IronSource Ltd和Unity Technologies SF，Original Assignee列Unity Technologies SF；事件表记录2021-12-09向IRONSOURCE LTD.转让。保留原始元数据，不凭此重建产品整合史或作法律意见。
- 状态显示Active，Google明确提示状态/权利人可能不准确，本研究未独立法律核验。
- 共20项权利要求；独立项1为系统、7为方法、12为计算机可读介质。权利要求正文围绕OS版本变化、应用inventory及附加信息来产生适配应用推荐。

设备监测/应用列表提供的是**专利方案中的设备上下文**，不说明跨设备个人图谱；也没有Vector、LTV输入列或生产模型消费。不能因专利属于相关公司且含device/recommendation就认定其为Vector身份架构。另一个窄查询命中的Polyspatial application interaction属于空间交互，未进入正证据矩阵。

## 判断

Vector最接近价值模型的工程材料是既有Ads Modeling的用户行为建模职责和新增Data Infrastructure的production ML特征管道描述；最接近身份组件的是既有Exchange/RampID合作。**两端都存在范围内的正证据，中间“Exchange/解析结果→Vector实际接收→当时模型读特征”仍缺失，不能拼接补齐。** 不排除个人机制，也无法排除聚合/共享参数解释。当前停止公开架构扩搜。
