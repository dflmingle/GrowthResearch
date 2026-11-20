# 75号黑盒设计与合成验证

本目录不访问网络、身份服务、SDK或真实广告系统。只复用72—74的契约/代码证据并运行独立合成设计验证。

- `HISTORY_BEFORE.json`与两个before文件：开始前00—74及主图/索引基线，只读。
- `READING_LOG.json`、`REUSED_EVIDENCE.json`：先前报告复核与31个旧证据对象逐哈希复用；不重新扫描SDK。
- `HYPOTHESES.json`、`IDENTIFIABILITY_MATRIX.json`：训练来源/在线通路两轴，56条可识别性判断。
- `PREREGISTRATION.md`、`CONFIG.json`、`simulate.py`：执行前冻结方案、固定seed750031和完整参数；19情景，无真实模型训练。
- `results/REPLICATE_RESULTS.csv`：5700条重复统计；`DESIGN_SUMMARY.csv`：19情景和Monte Carlo区间。
- `results/OBSERVATIONS/replicate0_all.csv`：每情景第0重复的99840条外部观测；其他重复可按冻结代码重建，不声称全部原始逐机会数据都已落盘。
- `results/TRUTH/replicate0_generator.csv`：对应生成器真值；不假装现实黑盒可以观察。
- `results/OBSERVATIONS/EQUIVALENT_WORLDS.csv`与TRUTH配对JSON：三组逐行相同输出、不同内部机制的反例。
- `results/VALUE_SCALE_COUNTEREXAMPLE.json`：仅见赢家不识别绝对价值尺度。
- `results/RUN.json`：协议/参数/代码哈希与运行时间。
- `admission.py`、`ADMISSION_AND_INTERPRETATION_CHECKS.json`：12项本地权限与反误判fixture；当前L2未获权。
- `EXPERIMENT_READINESS.json`：当前L0/离线与前瞻L1/L2准入，不充当执行许可。
- `VALIDATION.json`、`ARTIFACT_MANIFEST.json`：历史文件、图前缀、来源与统计结果/文档一致性。

Python使用numpy1.26.4、pandas2.2.2、scipy1.13.1；`simulate.py`无需sklearn且没有训练步骤。验证命令（根目录运行）：

```powershell
python -X utf8 blackbox75/validate.py
```

复现实验时复制本目录到独立副本，将副本的旧results归档，不改本目录原始结果。脚本拒绝覆盖；在副本运行：

```powershell
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
python -X utf8 simulate.py
```

参数/协议改变必须另建版本，不能换种子挑好结果。`build_matrix.py`、`write_sim_report.py`、`update_graph.py`仅生成本轮衍生文件，不改00—74；运行会更新本轮文件，已完成后只需validate。L2假设用例分支只是本地配置检查，不具有外部调用实现或实际授权。
