# 自主身份图谱：合成LTV特征实验

此目录是独立实验框架，只使用本地合成身份、安装、行为、净收入和退款。复用相邻 `identity-graph-mvp` 的实际图谱查询与隐私规则，不修改原MVP、76号程序及00—78历史成果，不更新主证据索引或证据图。

**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。合成预测差异不是真实LTV收益，也不是厂商生产证据。**

## 运行

Python 3.10+，本机已安装NumPy 1.26.4；其BSD许可及附带声明完整保留在[依赖目录](dependencies/AUDIT.json)。无需安装包或联网。Windows PowerShell：

```powershell
Set-Location D:\GrowthResearch\identity-graph-ltv-lab
C:\Users\89trillion\anaconda3\python.exe -X utf8 -m unittest test_lab -v
C:\Users\89trillion\anaconda3\python.exe -X utf8 run_experiment.py --output results/my-new-run
C:\Users\89trillion\anaconda3\python.exe -X utf8 summarize.py
C:\Users\89trillion\anaconda3\python.exe -X utf8 verify_delivery.py
```

实验拒绝覆盖已有run。`LATEST_RUN.txt`只在完整成功后更新；报告生成器和验收器读取该指针。不要重跑`prepare.py`：它仅在本轮运行前冻结历史SHA256及预注册协议，已有协议会拒绝覆盖。新运行数值应按固定种子复现；绝对路径、运行时间和外部文件元数据不要求逐字节相同。

## 代码与产物

- [冻结协议](PREREGISTRATION.json)；[完整性基线](PRESERVATION_BASELINE.json)。
- [数据生成](lab/generator.py)、[原MVP适配器](lab/adapter.py)、[事件调度与真实本地查询](lab/extraction.py)。
- [模型及指标](lab/model.py)、[实际生命周期探针](lab/counterexamples.py)、[实验入口](run_experiment.py)、[回归测试](test_lab.py)。
- [模型对照](MODEL_COMPARISON.md)、[十项反证](COUNTEREXAMPLES.md)、[时间与权限审计](TIME_PERMISSION_AUDIT.md)。
- [本轮总结](EXPERIMENT_SUMMARY.md)、[实际测试报告](TEST_REPORT.md)。
- [失败与限制](FAILURES_AND_RISKS.md)、[真实数据准入](REAL_DATA_ADMISSION.md)、[交付核验](DELIVERY_VERIFICATION.json)。

当前正式运行`results/run-002`；首轮`run-001`的真实失败保留，详见失败报告。每次运行包含SQLite数据库、完整MVP审计链、决策时特征快照、合成真值与现金流账本、全部模型参数/验证试验、所有测试预测、校准与分组误差、配对区间和逐阶段日志。合成真值文件单独保存，不进入特征矩阵。

## 实验契约

两个独立世界、各5个种子、每组360个安装，共3600个。按安装时间将180/90/90分成训练/验证/测试，owner严格隔离，标签在下一阶段预测前成熟。预测发生在安装6小时；D1/D7/D30标签按安装起有限窗口净现金流计算，包含窗口内退款。

M0上下文，M1加本应用早期行为，M2加经过时间、权限和关系质量检查的观察历史金额与可用位。三者相同样本、标签和切分，每个模型4次alpha试验；训练预算按试验次数可比，输入列数不同。仅在验证集选参数；所有预处理只用训练集。

运行期间Python socket/DNS/connection入口被阻断。导入MVP时禁止生成字节码。只在本目录的合成数据库设置SQLite MEMORY journal和synchronous=OFF，以缩短逐事件审计的磁盘开销；这不是故障恢复、崩溃一致性或生产数据库耐久性测试。各个shard是独立世界分区，不跨shard查询身份。
