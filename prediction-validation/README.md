# 独立价值预测验证：第一轮

**当前结论：没有核实到合法可用的真实用户/cohort数据。真实训练停止；本轮完成56号审计、数据契约、可运行的输入/标签/时间检查框架及合成fixture测试。没有拟合新模型或生成57—60真实结果。**

这不是Axon/Vector的恢复实现，也不通过SDK字段假装拥有真实数据。已有`../ltv/model`、`../auction/model`和`../vector/model`保持原样，历史结果均按原合成性质保留，不重复运行或升格为真实证据。

## 目录

- `data_contracts/`：封闭JSON Schema、字段字典、接入/授权/标签/时间规则、特征白名单。
- `src/`：资产盘点、语义校验、经济事件去重与标签构造、特征时点门控及synthetic-only runner。
- `tests/`：仅合成数据的拒绝/边界测试。
- `experiments/protocol.json`：M0—M5及未来消融/指标/时间外验证的预登记设计，尚未执行。
- `results/asset_audit.json`：现有数据资产审计；`round56_smoke_v2/`为当前合成会计/门控试跑，v1结果保留；无模型效果数字。

## 运行

在本目录执行（Python3.12，依赖jsonschema；本轮复用本地已安装版本，无需联网）：

```powershell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 -m src.run --synthetic-smoke --run-id my_new_local_run
```

run-id必须全新；已有结果目录会被拒绝，避免覆盖历史。测试的schema及源码哈希、Python/依赖版本见`results/DELIVERABLE_VALIDATION.json`和`results/TEST_RESULTS.json`。

合成fixture只有3个安装者和4个已展示机会，用于核对跨SDK收入副本、paid/fulfilled、退款、零收入者、精确窗口边界、时间泄漏和隐私门控。样本根本不足以作预测效力、置信区间、身份增益或ROAS结论；这些字段在结果中为null。

## 真实数据能力边界

当前语义验证函数可检查符合合同的离线bundle，但不会自行证明授权，不包含真实训练执行入口。`real_training_allowed`始终为false。授权须按[data_contracts/README.md](data_contracts/README.md)在运营方/授权隔离环境另行核实。

最小可推进数据：单游戏全体安装者（含零收入）+所有者预聚合且带当时可用时间的D0行为/代理值+成熟D7/D28净IAA和已验单净IAP/退款血缘。仅用导出内随机行键。它可先做M3—M5和剩余LTV验证，**不能**估P(install)或还原全量竞价收益。安装前和跨App研究还需要真实bid时刻、合法历史快照及独立join授权；不默认具备。
