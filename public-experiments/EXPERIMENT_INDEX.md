# 公开数据独立实验索引

历史入口：[65号准入](../65_公开扩量证据与模型实验可行性审计.md)、[66号实验](../66_UCI用户未来消费金额预测实验.md)。


## 67：独立未来时间，零售发票，不是手游LTV

- [报告](../67_用户价值预测独立时间验证.md)、[预注册](../67_独立实验协议.md)
- [复现代码](round67/run67.py)、[实际运行](round67/RUN_MANIFEST.json)、[冻结66重建](round67/FROZEN66_RECONSTRUCTION.json)
- [结果与CI](../67_模型对照结果.csv)、[配对比较](round67/PAIRED_COMPARISONS.csv)、[校准](../67_预测校准分析.csv)、[分层](../67_分层预测误差.csv)
- 结论：原M2对历史日均MAE复制；两阶段/校准无确认整体优势；跨游戏与广告ROAS不获准入。外部游戏线保持STOP。


67号补充：[周×消费层描述诊断](round67/WEEK_BY_TIER_DIAGNOSTIC.csv)、[固定重建一致性](round67/WEEK_TIER_DIAGNOSTIC_MANIFEST.json)。未调参，原运行结果保留；尾层仍不稳定，未新增模型优势结论。


## 68：独立新数据审计，训练STOP

- [报告](../68_全新公开数据源调查.md)、[17候选](../68_DATASET_CATALOG.csv)、[准入矩阵](../68_EXPERIMENT_ADMISSION_MATRIX.csv)
- [跨产品方案与恢复条件](../68_CROSS_PRODUCT_TRANSFER_READINESS.md)、[源证据](round68/SOURCE_CATALOG.md)
- 已取得Complete Journey和REES46两商店原件，未满足两产品完整金额/零值门槛；无训练、无旧UCI使用、无平台/手游外推。


## 69：原始来源、字段和观察完整性，训练STOP

- [最终准入](../69_实验准入最终判断.md)、[CJ处理血缘](../69_CompleteJourney原始数据与观察覆盖审计.md)
- [Jewelry字段](../69_REES46Jewelry字段语义审计.md)、[电子异常](../69_REES46Electronics缺失与异常审计.md)
- 官方历史原包恢复字段、公开代码揭示人工日历；真实零/覆盖与金额口径仍未通过，未训练/未使用UCI。
