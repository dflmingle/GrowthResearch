# 76号工程测试报告

2026-11-20。正式结果：`results/acceptance-v3`，seed760031，Python3.12.7，全部离线。该版本按最新代码运行，历史v1/v2和初始demo未删除。

| 测试层 | 结果 | 验证目标 |
|---|---|---|
| 75号矩阵主验收 | **56/56 PASS** | 原56行ID及全部字段保留，每行观察级别、必需/禁止声明及假设边界均断言 |
| 证据削弱对照 | 按观察级别逐行执行并通过 | 去掉受众/匹配scope或实际读取日志时，不能升级结论；feature/score返回不可识别 |
| derived反例 | 7个match行全部执行并通过 | 返回derived不标existing maintained匹配；confidence仅cascade标签 |
| 独立进程回归 | **13/13 PASS** | 三route、广告等价、只见响应、时点/权限/reset、独立packet审计、固定seed重放、socket/子进程禁用 |
| 单元测试 | **40/40 PASS，0 skip** | 接收/可用边界、迟到、事件去重、缓存撤权、schema、epoch、篡改/缺失审计、无真标签停止等 |

主case数可记为56+13+40=109；削弱/derived对照包含在56行文件里，不冒称新的独立用户或统计重复。没有扩大75号统计模拟，没有新模型训练、真实广告或身份解析。

## 实际观察到的工程行为

完整instrumented trace下，D1得到`SAME_DEVICE_HISTORY_READ`，LEAK得到`CONTEXT_LEAKAGE`。同seed下两者response完全相同；只给response的审计都为`UNIDENTIFIABLE`。这验证工程能区分来源证据，不是证明任何厂商路由。

D0日志完整且未读历史时，返回`NO_INDIVIDUAL_HISTORY_READ_OBSERVED`，保留H0/H3训练来源不可识别。source/target用途关闭为`GATE_BLOCKED`且不发生lookup；未来available_at、重置后旧epoch和其他device不能产生合法同设备读取。`available_at==prediction_time`允许，迟到接收但预测前可用也允许；source事件当时未获许可，之后补grant仍不能回填权限。

完整hash链不够：即使重新计算hash，伪造未来来源、错误device/epoch、实际读取缺失或模型版本不符仍拒绝。仅记录logged但`actual_read=false`不能升级入模。截断log或缺读取来源返回不可识别；明确矛盾/篡改返回证据无效。

“独立审计”测试复制公开packet到无private truth的输入目录，启动单独auditor进程；结果与原packet一致。审计器不导入service，不接受隐藏route键。它仍依赖本地日志生产者的instrumentation真实，不是第三方签名/生产证明。

socket动态探针在创建socket时被拒绝，App侧启动子进程探针被拒绝；运行器只启动工程内Python模块。该检查没有连接任何外部地址。代码和依赖均为标准库，无广告SDK、网络监听或浏览器。

## 矩阵转译的实际覆盖与不覆盖

56=7个假设/子假设×8种观察。O1—3只见素材/频率/广告主类别，均不可识别；O4/O5提供本地有界受众/服务状态，不等于模型；O6/O7只有完整局部trace才能确认局部实际读取；O8无真实标签，固定STOP。H1在有效同设备trace下只能说“本地同设备链”，不能证明系统全局不存在D2。

H2_account/H2_person/HH是待证问题，工程没有伪造其正向实现，只验收当前证据不能识别它们。H0/H3行不从无读取或相同输出推断训练来源。没有为凑56条把同一个“PASS”复制，而是每行保存原契约、不同观察输入、弱化输入、判定和禁止跳级条件；来源文字仍供人工复核，自动case不代表原自然语言全部条件均已在真实环境验证。

## 开发修正与证据新鲜度

开发时发现旧bridge在撤权后仍可能夹带上下文，已在目标App加入时点/epoch检查，服务在拒绝用途时先剥离源字段再记目标请求；增加对应回归。权限预约顺序改按effective_at/version评估，不能因较晚提交早生效grant覆盖未来撤权。审计还核查来源读取时点的权限，不只看最终预测时刻。

v1通过35单元、v2通过40单元；v3进一步保留每单元完整服务日志并补App进程禁用探针。**本报告只引用v3的当前代码哈希与结果**，不会用旧PASS代替新验证。固定种子重放比较整个ledger（不含绝对输出路径的进程启动记录），内容完全一致。

## 不能从PASS得出的结论

不能推出Axon/Vector使用图谱、person matching成功、任何真实值入模、独立预测增益或真实买量收益。CLI进程不是手机二进制，也没有Windows用户隔离、真实OS广告ID重置或生产隐私删除。hash链只检测内容一致性，恶意生产者可重写整条自洽历史，需外部信任/签名和实际接收材料才可能用于真实证据。

机器报告：[SUMMARY](results/acceptance-v3/SUMMARY.json)、[矩阵结果](results/acceptance-v3/MATRIX_RESULTS.csv)、[回归](results/acceptance-v3/REGRESSION_RESULTS.json)、[单元日志](results/acceptance-v3/UNITTEST.txt)、[运行代码SHA](results/acceptance-v3/CODE_AT_RUN.json)。历史保留/全图检查见[VALIDATION](VALIDATION.json)。
