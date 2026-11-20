# 实际测试报告

本轮Python3/NumPy本地执行，无新安装依赖。当前正式运行results/run-002；run-001是保留的失败，不纳入正式结果。原代码与协议SHA256见[RUN_MANIFEST](results/run-002/RUN_MANIFEST.json)。后添加的summarize.py、verify_delivery.py、run_unit_tests.py、check_preservation.py属于报告/验收工具，不参与已冻结实验的训练计算。

|验收层|结果|原始材料|
|---|---|---|
|时序、标签、预处理、隔离回归|11/11通过|[UNITTEST.log](results/unit-tests/UNITTEST.log)|
|原MVP实际生命周期与质量探针|17/17通过|[ENGINE_PROBES.json](results/run-002/ENGINE_PROBES.json)|
|全图谱不可用回退|90/90组预测差≤1e-8|[CONTROL_EQUIVALENCE.json](results/run-002/CONTROL_EQUIVALENCE.json)|
|合成世界完整执行|2世界×5种子×3窗口×12变体，360结果行|[MODEL_METRICS.csv](results/run-002/MODEL_METRICS.csv)|
|预测输出|32400行，2700个独立世界/窗口/测试安装标签|[PREDICTIONS.csv](results/run-002/PREDICTIONS.csv)|
|特征时间与权限|3600条实际查询逐行检查|[TIME_PERMISSION_AUDIT.csv](results/run-002/TIME_PERMISSION_AUDIT.csv)|
|独立交付验收|56568项检查、失败0|[DELIVERY_VERIFICATION.json](DELIVERY_VERIFICATION.json)|
|历史保护|2845文件无变化|[PRESERVATION_BASELINE.json](PRESERVATION_BASELINE.json)|

验收器包含代码/协议哈希、历史文件、现金流标签与退款重算、成熟窗口、owner隔离、共享设备拒绝、图谱金额回算、各模型相同样本和4次alpha预算、实际训练中位数/标准化重算、参数重建预测与所有报告指标重算。检查数量含逐行重复断言，不能解释为56568种独立测试场景。

完整逐阶段日志：[RUN_LOG.jsonl](results/run-002/RUN_LOG.jsonl)；控制台记录：[stdout](results/run-002_stdout.log)。每个graphs分片保存原始SQLite、特征快照、MVP审计记录；data目录保存合成真值、现金流、实际特征、反证输入、标签成熟和非法注入拒绝结果。

复现命令见[README](README.md)。新实验必须使用新输出目录，正式旧结果不会被覆盖。运行器在成功后才更新LATEST_RUN；统计汇总不重新拟合模型。没有因测试指标不理想更改协议、删极端样本或增加模型搜索。
