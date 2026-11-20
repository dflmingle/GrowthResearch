# Axon/Vector 与自主系统证据边界

本表直接沿用 [原六层矩阵](../axon-vector-mechanism-gap/01_Axon_Vector机制差异矩阵.csv) 的层级和 MG01—MG15 编号，只增加自主能力对照，不重评或升级厂商状态。原始来源、适用时间、缓存文件、SHA256与替代解释保留在 [原机制台账](../axon-vector-mechanism-gap/MECHANISM_EVIDENCE.csv)。本轮未刷新网页、检索 SDK/岗位/专利或获得生产材料。

A 是自主已执行能力；B 是官方公开契约/产品用途，CONFIRMED 仅指原声明在限定范围可核对；C 是厂商内部实际关系解析与模型消费。**A不推出C，B也不推出指定生产实例已执行。**

|原层级|A 自主系统|B Axon 官方/已有有界事实|B Vector 官方/邻接产品事实|C 厂商内部未知|
|---|---|---|---|---|
|L1 身份输入|IMPLEMENTED_AND_TESTED：合成namespace/typed实体、原认证回执与事件引用；MVP/E01/E02|CONFIRMED（契约/客户端范围）：MG01 Adjust→Axon可配置postback ID/上下文；MG02 Web入口；MG03旧SDK客户端能力。实际该实例收妥不由此证明|UNKNOWN（Vector逐字段接收）；MG05/06/08的CONFIRMED仅限UPA/Unity Ads/Exchange各自范围|哪些ID在指定Axon/Vector实例实际接收、作用域怎样映射仍UNKNOWN；不把字段相似视为共享|
|L2 关系解析|IMPLEMENTED_AND_TESTED：合成认证账号边、候选隔离/冲突、显式设备事实。真实概率解析未实现|UNKNOWN：MG04多ID到后端映射只有INFERRED解释，无可核验解析结果|UNKNOWN（Vector）；MG05 UPA账号链接、MG06 Exchange/RampID受众激活是邻接产品契约，不是Vector解析链|设备/账号/个人/家庭粒度、成功匹配定义、冲突处理与覆盖率UNKNOWN|
|L3 图谱更新|IMPLEMENTED_AND_TESTED：时间有效、撤边、逻辑删除、全局失效、恢复后重放独立控制库；不是生产可靠性|UNKNOWN：MG09未给Axon关系TTL、撤销/重建/删除水位执行契约|UNKNOWN：MG10；MG07 UPA unlink/冲突不升级为Vector图谱更新|指定产品如何合并/拆分、缓存与模型特征如何失效仍UNKNOWN；原客户端隐私开关不能补证|
|L4 特征服务|IMPLEMENTED_AND_TESTED：MVP受限查询、E01源/目标分区、lab device特征消费；三个范围不可混用|UNKNOWN：MG11无关系输出→图谱特征组→模型实际读取接口和记录|UNKNOWN：MG12无UPA/Exchange输出→Vector接收→指定特征消费桥|真正的feature group、graph/model版本、available_at和非默认读取记录UNKNOWN|
|L5 价值预测|IMPLEMENTED_AND_TESTED（合成lab）：M0/M1/M2及成熟金额标签；真实独立增益UNKNOWN|CONFIRMED（产品用途）：MG13官方多日价值分布/广告主价值方向；该说明的非游戏offer范围不自动扩大为所有手游|CONFIRMED（产品用途）：MG14 D7/D28、cross-game/cohort方向；具体个人身份输入仍UNKNOWN|模型结构、跨App个人历史列与聚合/共享参数贡献不能由产品宣传或自主实验推定；C_graph、D均UNKNOWN|
|L6 竞价消费|NOT_IMPLEMENTED：lab预测未接机会估值/出价控制；MVP checksum probe不算广告决策|CONFIRMED（产品用途）：MG15实时展示评估及return-goal出价；前瞻业务扩展不等于上线证据|CONFIRMED（产品用途）：MG14动态出价/bid-time intelligence|身份读取→特定inference→特定广告机会active决策trace未知；没有身份独立收益的真实对照|

## 仍然不能跳过的反证

- Adjust 的标识/事件/归因机制属于 Adjust。自主参考实现可借鉴通用契约，不能把其服务端实现或代码归属于 Axon/Vector。
- Unity Player Accounts 的组织/项目账号粒度不自动变为自然人；UPA、Unity Ads、Exchange 与 Vector 分开建模。Unity Exchange 能激活某受众不等于 Vector 接收并消费其身份特征。
- RampID返回不保证已有实体匹配成功；maintained/derived必须区分，matchConfidence不自动是校准概率。自主候选置信度保护也不证明厂商采用相同机制。
- AppLovin允许某些跨App数据用途、SDK存在ID读取/构包能力，不证明某生产模型读取个人身份图谱。Web Pixel/CAPI与手游价值任务的具体桥仍缺证。
- 无需个人关联的群体统计/共享参数是未排除的竞争解释。lab有/无植入历史信息的两种合成世界不排除现实中的这类解释。

## 厂商消费证据升级仍按78号

必须是权利方允许引用和独立复核的：解析来源/组件版本与实体粒度 → 指定接收产品/接收时间 → 特征组/graph/model版本与当时可用性 → 非空、非默认的实际读取 → 同一机会的active决策引用；同时具备合法用途、撤销/删除时点、环境范围与原件完整性。

可引用的统一链路不足，C_graph保持UNKNOWN；只有接收记录只能升级对应接收子事实。即使以后C_graph成立，D仍需独立真实消融，固定数据量、容量、时间、标签及竞价策略，并加入群体/共享参数竞争对照，不能从效果反推身份架构。

本轮新增厂商材料0、新增生产事实0、结论升级0。原生产取证STOP，未安排79号。

**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN。**
