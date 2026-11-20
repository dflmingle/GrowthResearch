# 本地MVP真实测试报告

本系统是自主的本地合成工程MVP，不是Axon/Vector逆向复现，不证明真实自然人身份、生产模型消费或LTV增益。仅使用Python标准库和SQLite；未启动MAX/LevelPlay、外部身份接口、广告网络或真实用户数据。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 00—78、76程序与既有研究证据不修改，主索引/证据图也不追加。

正式代码对应运行：`results/run-003`；seed=760078。标准unittest实际执行40项（20项原验收＋20项回归），131条断言，0失败、0错误。网络socket/DNS/连接在整个测试期间被禁用；不是向真实服务发送请求后的结果。

原20行需求从server-identity-reference复制，SHA记录于RUN_MANIFEST；映射保留原test/expected/rules原文，没有降低预期。[逐项矩阵](ACCEPTANCE_MAPPING_RESULTS.csv)、[实际日志](results/run-003/UNITTEST.log)、[全部案例](results/run-003/ALL_CASE_RESULTS.json)。

| ID | 原始验收 | 真实执行 | 断言数 | 逐项输入/预期/实际 |
|---|---|---|---|---|
| V01 | 同值不同issuer/app/namespace | PASS | 3 | [记录](results/run-003/cases/V01/EXPECTATIONS_AND_ACTUALS.json) |
| V02 | pairwise sector | PASS | 5 | [记录](results/run-003/cases/V02/EXPECTATIONS_AND_ACTUALS.json) |
| V03 | 账号认证与重放 | PASS | 6 | [记录](results/run-003/cases/V03/EXPECTATIONS_AND_ACTUALS.json) |
| V04 | 账号共享 | PASS | 4 | [记录](results/run-003/cases/V04/EXPECTATIONS_AND_ACTUALS.json) |
| V05 | 未校准高分 | PASS | 3 | [记录](results/run-003/cases/V05/EXPECTATIONS_AND_ACTUALS.json) |
| V06 | 桥接冲突 | PASS | 2 | [记录](results/run-003/cases/V06/EXPECTATIONS_AND_ACTUALS.json) |
| V07 | 删桥拆分 | PASS | 5 | [记录](results/run-003/cases/V07/EXPECTATIONS_AND_ACTUALS.json) |
| V08 | 图关系回填 | PASS | 2 | [记录](results/run-003/cases/V08/EXPECTATIONS_AND_ACTUALS.json) |
| V09 | 事件幂等与attempt | PASS | 4 | [记录](results/run-003/cases/V09/EXPECTATIONS_AND_ACTUALS.json) |
| V10 | 请求多候选多回调 | PASS | 3 | [记录](results/run-003/cases/V10/EXPECTATIONS_AND_ACTUALS.json) |
| V11 | 迟到退款和收入 | PASS | 4 | [记录](results/run-003/cases/V11/EXPECTATIONS_AND_ACTUALS.json) |
| V12 | 缺失与零 | PASS | 2 | [记录](results/run-003/cases/V12/EXPECTATIONS_AND_ACTUALS.json) |
| V13 | Feast后端时间语义 | PASS | 7 | [记录](results/run-003/cases/V13/EXPECTATIONS_AND_ACTUALS.json) |
| V14 | 读旧缓存 | PASS | 3 | [记录](results/run-003/cases/V14/EXPECTATIONS_AND_ACTUALS.json) |
| V15 | 部分删除回执 | PASS | 9 | [记录](results/run-003/cases/V15/EXPECTATIONS_AND_ACTUALS.json) |
| V16 | 备份重放 | PASS | 4 | [记录](results/run-003/cases/V16/EXPECTATIONS_AND_ACTUALS.json) |
| V17 | 训练影响 | PASS | 3 | [记录](results/run-003/cases/V17/EXPECTATIONS_AND_ACTUALS.json) |
| V18 | 接收缺失/模型默认 | PASS | 5 | [记录](results/run-003/cases/V18/EXPECTATIONS_AND_ACTUALS.json) |
| V19 | 产品不一致 | PASS | 3 | [记录](results/run-003/cases/V19/EXPECTATIONS_AND_ACTUALS.json) |
| V20 | 真实来源与引用权限缺失 | PASS | 5 | [记录](results/run-003/cases/V20/EXPECTATIONS_AND_ACTUALS.json) |

## 用户十项必测的覆盖

| 要求 | 测试 |
|---|---|
| 单账号多设备 | V04 |
| 多账号共用设备且不串收入 | V04、R11 |
| 多应用实例关联 | R03及V04 |
| 标识重置 | R02 |
| 关系冲突 | V06、R01 |
| 错误关系撤销/拆分 | V07 |
| 同意撤销 | V14、R20 |
| 删除传播与恢复后不复活 | V15、V16、R14 |
| 派生特征失效/到期 | V07、V14、R17 |
| 预测时间点防泄漏 | V08、V11、R06；V13为后端准入契约 |

## 回归与证据限制

回归还覆盖auth nonce备份恢复、直接伪造账号边、错误实体粒度、经济冲突、混币、审计篡改、产品/模型/时间引用不一致、删除不误伤另一个账号、合成数据不能获准LTV实验、恶形证据fail-closed、socket确实禁用及SQLite事务失败回滚。

V13只验证自有适配器准入条件及本地时序逻辑；没有安装/运行Feast。V17只注册“合成已训模型引用”用于测试未知状态，没有真的训练或遗忘模型。V18–V20的来源/复核/引用权字段是本地fixture声明，仅检验审计判定器不跳级；不证明真实权利方真实性。R09故意破坏测试库审计链，预期verify=false，是通过的反例，不是正式运行数据损坏。

日志和结果是本轮真实执行产生；数据完全合成，所以PASS只证明指定工程行为。未报告真实匹配准确率、错误合并总体率、延迟SLA或LTV收益。复现命令见README。测试环境/版本/源SHA在RUN_MANIFEST，结果目录只新增不覆盖；开发期和旧run也保留。
