# 76号：双App本地mock与独立证据判定

这是**Python命令行双App mock**，源App、目标App、mock服务、审计器作为不同进程运行，以本地JSON文件通信。不生成Android/iOS安装包，不接入生产SDK，不建立HTTP服务，也不请求广告或身份商。

只需Python标准库，已在Python3.12.7/Windows验收；固定默认种子`760031`。没有文献/SDK扫描，也没有扩大75号统计模拟。所有标识为程序内`mock-*`fixture，时间为显式整数逻辑时钟。

## 直接运行

在`D:\GrowthResearch\engineering76`运行，替换为本机Python命令即可：

```powershell
python -X utf8 run_demo.py --output D:\GrowthResearch\engineering76\results\my-demo --seed 760031
python -X utf8 run_acceptance.py --output D:\GrowthResearch\engineering76\results\my-acceptance --seed 760031
```

输出目录必须不存在，防止覆盖历史。**不要用已存在的`demo`、`acceptance-v1/v2/v3`作新运行目录。** 正式证据对应`results/acceptance-v3`；前两个验收版本和最初demo保留为开发背景，不拿旧PASS验证新代码。

从研究根目录检查最终交付与历史保留：

```powershell
python -X utf8 engineering76/validate.py
```

标准库单元测试（默认临时目录；正式验收额外保留每测试的日志与状态）：

```powershell
python -X utf8 -m unittest discover -s tests -v
```

独立审计器可只接收公开packet，完全不需要service root或private truth：

```powershell
python -X utf8 -m mock76.auditor --input results/acceptance-v3/auditor_isolated/packet.json --output results/audit-review.json
```

最后一条的输出文件如已存在会原子更新；要保留旧审核请另取文件名。运行器则拒绝整个结果目录覆盖。

## 代码与边界

| 文件 | 作用 |
|---|---|
| `mock76/app_source.py` | App S独立进程，严格源事件schema，仅mock类别/标识，输出本地事件封装 |
| `mock76/app_target.py` | App T独立进程，固定上下文schema；只有明确的bridge fixture才可夹带源类别，并检查作用域/逻辑时间 |
| `mock76/service.py` | 本地接收/去重、延迟可用、epoch重置、用途权限、D0/D1/LEAK与决策证据链 |
| `mock76/auditor.py` | 不导入service，不接受route truth；交叉核对时间/权限/来源/读取/决策，返回有界局部链、不可识别或证据无效 |
| `mock76/io.py` | JSON原子写、序号+前项hash链；一致性检测，不声称数字签名/第三方证明 |
| `mock76/safety.py` | App/service/auditor禁止socket及子进程；运行器只实现本地Python子模块启动，不包含外部客户端或SDK |
| `build_acceptance.py` | 从75原CSV逐行保留全部56行，生成固定验收契约和scope边界 |
| `run_acceptance.py` | 执行56行主/证据削弱对照、13项进程回归、40项单元；捕获命令、stdout/stderr、所有本地IPC |
| `tests/test_engine.py` | 时间边界、撤权、缓存、重置、反例、schema、审计完整性等40项回归 |

进程分离和盲化是**代码/数据输入层的独立性**，不是Windows用户/ACL隔离；同一OS用户仍可能读private目录。本审计器未读它，孤立packet测试已验证。Python audit hook是语言层防误联网，不是OS防火墙或抵抗恶意本地代码的安全沙箱；运行器有受控启动本地子进程的能力。工程没有网络客户端、远端URL、真实SDK或身份资料。新增任意第三方代码前必须重新审查，不能沿用本报告作为保证。

## 路由和判定

- D0：只用固定基础上下文，无个体源历史查询。完整本地日志最多证明该次instrumented run未读源历史，仍不能区分H0与H3的训练来源。
- D1：用途允许且`event_time <= received_at <= available_at <= prediction_time`、epoch有效时，从同设备S历史取值，记录lookup→history_read→非空feature_read→decision。
- LEAK：明确的本地桥接把源值放入T当前上下文，记录context_bridge→target context→current-context feature_read。不会被判为广告平台身份解析。
- 相同类别/分数/素材可由D1和LEAK产生。只提供外部响应的视图必为`UNIDENTIFIABLE`，不按分数猜route。
- hash/序号篡改、跨设备伪造、未来来源等为`INVALID_EVIDENCE`；缺失来源/读取、截断、只见响应为`UNIDENTIFIABLE`；完整有效本地链为`IDENTIFIED_LOCAL_CHAIN`。后者不等于厂商E5/E6。

撤权后不查缓存；旧bridge用途失效时先剥离源字段再写目标请求日志。重置只在mock epoch下清除可用事件，不恢复旧新标识。**审计日志仍保留合成fixture历史，不能称真实隐私删除系统或模型遗忘实现。** 重装只用安装实例mock变更，不操作真实OS或ID。

## 日志与结果

正式目录`results/acceptance-v3`：

- `SUMMARY.json`、`UNITTEST.json/txt`、`MATRIX_RESULTS.csv`、`REGRESSION_RESULTS.json`：验收结论。
- `CASES.json`、`matrix_cases/BB75M001..056.json`：原行、输入、判定、证据削弱、必要时derived反例及实际假设边界。
- `process_runs/*/ipc/`：源/目标App与服务全部文件消息；`process_transcript.jsonl`捕获每次子进程命令和退出信息。
- `process_runs/*/audit/ledger.jsonl`与packet/verdict：完整逻辑时钟证据序列及独立审计输出。
- `process_runs/*/private/`：fixture路由/状态，仅发生器真值；不传入判定器。
- `unit_cases/`：40项测试结束时保留的本地服务状态/ledger；异常断言和审计篡改逻辑可由固定代码重放，原始未篡改ledger保留。
- `CODE_AT_RUN.json`：验收时实际代码SHA256；`MANIFEST.json`：结果文件哈希，最终完整性校验会核对。

矩阵的H2/人/家庭行也执行，但只验证“不应升级”的可识别性边界；本工程**没有实现真实跨设备、人/家庭解析或成熟价值增益模型**。受众/maintained/derived是本地契约fixture，不是调用LiveRamp。

详细结果见[测试报告](TEST_REPORT.md)和根目录76号总结。
