# 自主身份图谱本地MVP

本系统是自主的本地合成工程MVP，不是Axon/Vector逆向复现，不证明真实自然人身份、生产模型消费或LTV增益。仅使用Python标准库和SQLite；未启动MAX/LevelPlay、外部身份接口、广告网络或真实用户数据。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 00—78、76程序与既有研究证据不修改，主索引/证据图也不追加。

已实现七组件，并执行原20项验收及20项反例回归。当前正式结果：[SUMMARY](results/run-003/SUMMARY.json)，40项测试、131条断言，失败0、错误0。更早run保留，不用其PASS替代当前代码结果。

## 运行

Python3.10+，无第三方Python依赖，不需要pip或网络。Windows PowerShell：

```powershell
Set-Location D:\GrowthResearch\identity-graph-mvp
python -X utf8 run_tests.py --seed 760078
python -X utf8 -m identity_mvp demo --output demo/my-run --seed 760078
python -X utf8 generate_synthetic_data.py --seed 760078 --output fixtures/my-input.json
python -X utf8 verify_delivery.py
```

本机实际使用`C:\Users\89trillion\anaconda3\python.exe`。run_tests默认选择新的results/run-NNN；也可`--output results/my-run`。输出目录存在会拒绝覆盖。demo同样要求新目录。测试由标准unittest执行；runner增加断网、逐案例日志与验收映射，不是假PASS生成器。

## 源码与交付

- [七组件源码](identity_mvp/system.py)、[固定种子合成世界](identity_mvp/fixtures.py)、[CLI](identity_mvp/__main__.py)、[数据生成器](generate_synthetic_data.py)。
- [数据表Schema](identity_mvp/schema.sql)、[独立权限/删除控制Schema](identity_mvp/control_schema.sql)、[数据契约和模型边界](DATABASE_CONTRACTS.md)。
- [组件与14条规则映射](ARCHITECTURE.md)、[20项自动化验收映射](ACCEPTANCE_MAPPING_RESULTS.csv)、[自动化用例](tests/test_acceptance.py)。
- [真实执行测试报告](TEST_REPORT.md)、[失败与风险](FAILURES_AND_RISKS.md)、[后续LTV准入](LTV_FEATURE_ADMISSION.md)、[历史保全与交付核验](DELIVERY_VERIFICATION.json)。

每个`results/run-003/cases/Vxx`或Rxx目录包含INPUT.json（固定种子、完整合成操作与返回/异常）、EXPECTATIONS_AND_ACTUALS.json、RESULT.json、AUDIT_LOG.json，以及实际SQLite测试数据库。RUN_MANIFEST记录Python/SQLite、源文件SHA256、原验收矩阵SHA256和禁止联网条件；UNITTEST.log为实际unittest日志。R18显式验证socket被阻断，R19以SQLite触发器注入写入失败并验证回滚。

仅demo包含数据流演示，合成金额不是模型效果。`consume_local`只是实际读取特征并记录校验和的本地探针，不是LTV模型、实时竞价或真实广告决策。
