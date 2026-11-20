# 数据准入与STOP检查器设计 v1

本文件仅定义未来独立、离线、默认拒绝的检查器；**没有实现或运行真实数据检查器**，不连接平台、不自动补字段、不修改原MVP/76号/lab。`verify_design.py`只验证本轮文档、引用和历史完整性，不能输出真实数据GO。

## 双阶段与职责分离

阶段A只接收不含个人值的授权文件索引、schema、覆盖/时间证明和scope manifest。授权未完成时不打开行文件，也不读取“先看一眼”的样本。文件是否匿名不能替代处理许可。阶段A通过最多是`GO_CONTROLLED_INSPECTION_SCOPED`，不是训练准入。

阶段B须由权利方或获授权复核人在批准的环境执行，读取最小必要记录和支撑原件；研究者可仅拿到聚合结论、哈希承诺和缺失列表。只有所有拟开展任务的门槛实际通过并签认，才能出具范围化准入。解析/训练/导出/公开引用许可分别检查；没有公开引用许可不发布受限事实。

人工权利判断与机械一致性检查分开。工具不能凭合同文件存在判断签署者有权，不能凭self-reported=true或hash链判定真实生产接收。缺陷修复可能要求权利方新证据，而非研究者填默认值。

## 闸门

|Gate|验证输入/规则|缺失|明确不符|实际通过仅支持|
|---|---|---|---|---|
|RA00 权利/目的|P0有权签认、主体、全源/目标用途、时间/地区/人员/处理与披露范围|STOP_AUTHORIZATION，不导入行|STOP_OUT_OF_SCOPE|指定范围受控审查|
|RA01 来源/真实性|P9原件、签认权限、独立复核、转换/缺失清单|HOLD_PROVENANCE，执行STOP|STOP_INVALID_PROVENANCE|来源可复核，不是模型效果|
|RA02 粒度/namespace|P1/P2实体类型、issuer/scope/epoch、typed关系/重装定义|HOLD_SCOPE，相关任务STOP|STOP_GRAIN_OR_KEY_CONFLICT|account/device作用域；不自动person|
|RA03 真实经济语义|P4真实交易/ILRD，币种、精度、现金流/修订、归属/去重|HOLD_AMOUNT，收入任务STOP|STOP_PROXY_OR_DOUBLE_COUNT|指定经济口径金额|
|RA04 分母/观察|P1全安装；P5入退样/缺采/完整窗口和全源水位|HOLD_OBSERVATION，训练STOP|STOP_FALSE_ZERO|有限窗口内可区分零与缺失|
|RA05 时间因果|P2/P3/P6真实observed、received、available、物化和读取时间；误差区间/DAG|HOLD_TIME，相关特征与实验STOP|STOP_LEAKAGE|当时可用，不证明信息有用|
|RA06 关系合法性/质量|解析用途许可、当时有效关系、独立P8真值/质量和拒识阈值|HOLD_LINK_TRUTH，图谱收益STOP|STOP_UNAUTHORIZED_OR_FALSE_SCOPE|指定粒度的匹配质量可评估|
|RA07 生命周期|P7历史/当前同意或合法依据、撤销/删除/缓存/snapshot/sink、保留政策|HOLD_LIFECYCLE，相关消费STOP|STOP_REVOKED_OR_DELETED_USE|消费合法范围；不证模型遗忘|
|RA08 标签成熟|D1/D7/D30现金流发生窗、到账水位、修订语义、L≤7天及覆盖证明|HOLD_MATURITY，训练STOP|STOP_IMMATURE_OR_REVISED_LABELS|对应标签可用于指定阶段|
|RA09 时间/实体隔离|绝对窗口、权利方审计簇分区、无跨阶段关系、独立保管测试|HOLD_SPLIT，训练STOP|STOP_OWNER_OR_TIME_LEAK|独立测试设计可执行|
|RA10 冻结/功效/公平|版本化协议、日期/字段/种子、delta_min/先导方差、资源/容量、全部对照同rows/labels|HOLD_PROTOCOL_OR_POWER，训练STOP|STOP_TEST_TUNING_OR_UNFAIR_COMPARISON|仅预注册的检验范围|
|RA11 审计/输出|每门证据定位/复核人、完整样本流图、未确认sink、负结果、批准的聚合披露|HOLD_AUDIT，报告真实效果STOP|STOP_INCOMPLETE_OR_UNQUOTABLE_REPORT|可引用的范围化结果|

缺失和明确失败均阻止相应执行，但原因分开。HOLD表示等可补证输入，不表示允许边训练边补材料；STOP表示本轮执行禁止或当前源不适配。N/A仅在确实不适用且有权复核人签认时成立，例如IAP-only任务的IAA字段不要求；若任务仍名为总收入则不能N/A。

## 范围化判定

`GO_METADATA_REVIEW_ONLY`仅允许现有公开/合法元数据整理；`GO_CONTROLLED_INSPECTION_SCOPED`要求RA00通过后才能受控查验；`GO_SAME_APP_REVENUE_SCOPED`与`GO_RELATION_QUALITY_SCOPED`分别要求各自完整门槛；`GO_GRAPH_FEATURE_EVALUATION_SCOPED`必须全部RA00—RA11通过。来源只有同App收入时不能给图谱任务GO；没有P8真值不能从收益反推匹配准确率。

如果部分安装没有可用关系，RA06/07合格的设计可以把这些行的图谱列编码missing并保留同一M0/M1/M2样本；这不等于把一个根本没有合法解析用途或质量审计的数据源放行为图谱实验。无权读关系时根本不查询，不能先读再mask。

拟议输出包括`package_ref/task_ref/schema_version/environment`、处理/引用范围、`gate_results`、每项`evidence_refs/reviewer/verified_at`、`missing_fields/unknowns/contradictions`、允许/禁止操作、样本分母和排除理由、合格标签/关系粒度、snapshot/manifest哈希、失效时点。没有证据的状态UNKNOWN，不能用null/空串/false相互替代。`complete_schema`不得自动变成`verified_facts`。

## 拒绝与反证用例（未来验收设计，未执行）

|输入改变|预期|原因|
|---|---|---|
|schema完整但无签署授权|STOP_AUTHORIZATION|不接收真实行|
|账号边声称person，未有独立依据|STOP_GRAIN_OR_KEY_CONFLICT|账号不是自然人|
|返回derived RampID，声称已有个人匹配|RELATION_UNRESOLVED|返回键不证匹配成功|
|事件早、available在预测后|STOP_LEAKAGE|发生早不代表可用早|
|关系在预测后才确认，强行回填valid_from|STOP_LEAKAGE|有效时间不替代known_at|
|COMPLETE缺证，无购买直接填0|STOP_FALSE_ZERO|缺失不是零|
|请求ID被当经济展示主键，多回调累加|STOP_PROXY_OR_DOUBLE_COUNT|经济事实未去重|
|标签窗口够长但水位未到/退款口径未知|STOP_IMMATURE_OR_REVISED_LABELS|跨度不是成熟证明|
|撤销生效后读缓存/无删除sink确认|STOP_REVOKED_OR_DELETED_USE或HOLD_LIFECYCLE|取决于明确违规或仍未知|
|置信分数高但无独立真值|HOLD_LINK_TRUTH|score不等于准确率|
|同一审计簇跨train/test|STOP_OWNER_OR_TIME_LEAK|隔离失败|
|只导出成功匹配/正收入样本|HOLD_OBSERVATION/STOP_FALSE_ZERO|选择偏差与分母不明|
|只给特征库查询日志，无模型输入读取|READ_UNRESOLVED|不是C_graph正证据|
|Exchange接收冒称Vector，沙箱冒称生产active|SCOPE_UNRESOLVED/STOP|产品、环境不可升级|
|修改测试后阈值或缩短窗口凑数|STOP_TEST_TUNING_OR_UNFAIR_COMPARISON|需新独立时期|

本轮只设计这些验收，不制造真实生产日志，不运行更多合成效果实验。当前所有来源的真实图谱增益任务均STOP；原因和可恢复输入逐行保留于[矩阵](01_真实数据来源及授权可行性矩阵.csv)。
