# GrowthResearch

AppLovin Axon / MAX、Unity Vector / LevelPlay 与休闲游戏获客、归因、身份及价值反馈机制研究。

本仓库整理截至 **2026-11-20、第67号研究**的报告、证据关系图、SDK发行包、静态分析工具和离线实验。完整目录见 [REPORTS.md](REPORTS.md)。

## 阅读入口

| 目的 | 入口 |
|---|---|
| 最终机制解释与游戏证据边界 | [64号最终判断](64_普通游戏盈利跃迁最终机制判断.md)、[逐案结论](model-architecture/FOUR_GAME_VERDICTS.md) |
| 架构证据与竞争性假设 | [模型研究入口](model-architecture/README.md)、[主张矩阵](model-architecture/CLAIM_MATRIX.csv) |
| 原始证据定位 | [证据索引](EVIDENCE_INDEX.md)、[机器可读证据图](prediction-system/EVIDENCE_GRAPH.json) |
| 扩量与数据可用性 | [65号审计](65_公开扩量证据与模型实验可行性审计.md)、[游戏身份表](public-evidence/GAME_IDENTITY_REGISTRY.csv) |
| 最新独立时间验证 | [67号报告](67_用户价值预测独立时间验证.md)、[拟合前协议](67_独立实验协议.md)、[结果](67_模型对照结果.csv) |
| SDK原件、版本、来源与哈希 | [SDK导航](ThirdPartySDKs/README.md)、[发行包清单](publication/SDK_ARTIFACTS.csv) |
| 复现与发布范围 | [复现说明](REPRODUCING.md)、[发布范围](publication/README.md) |

## 当前结论

- 客户端可证明SDK接口、游戏实际调用和部分请求构造；不等于生产送达、服务器接收或模型训练消费。
- MAX/LevelPlay变现接入、广告网络需求与AppDiscovery/Vector获客投放分别判断。四款游戏真实预算、成熟净收益及增长归因仍缺授权运营证据。
- 官方资料支持收入反馈、ROAS优化等产品能力；没有恢复Axon或Vector闭源模型、权重或真实报价公式。
- 第67号在新时段复现原M2相对历史日均基线的MAE优势；两阶段及校准没有全面胜出的统计支持。UCI零售发票销售额不是手游IAA/IAP，不能换算真实买量ROAS。

## 研究分组

| 编号 | 内容 |
|---|---|
| 00—22 | 游戏SDK、行为/价值事件、MMP与AppLovin调用链 |
| 23—34 | Vector增长、Runtime、非游戏数据与身份关联 |
| 35—46 | OpenRTB、竞价、预测系统证据图与服务端断点 |
| 47—59 | 跨SDK版本、Unity Core/Insights身份与价值血缘 |
| 60—64 | 架构、收入标签、跨游戏迁移、价值出价、最终因果边界 |
| 65—67 | 公开扩量、数据准入、零售消费独立时间验证 |

对象包括Car Race、Meowdoku、Rotate Rings、Jewel Coloring；精确包名以[身份登记](public-evidence/GAME_IDENTITY_REGISTRY.csv)为准。Amaze GO!缺少可验证样本时保持未知。

## 目录

- 根目录：00—67报告、汇总CSV、证据索引与清单。
- model-architecture/、prediction-system/：主张、竞争性解释、证据图及停止条件。
- ThirdPartySDKs/：官方AAR/JAR/POM、公开源码归档、历史版本及适配器。
- cross-sdk/packages/、core-insights/sdk/、identity-graph/sdk/：Unity Services、IAP、Analytics、Authentication及Singular官方包。
- auction/model/、ltv/model/、vector/model/：明确标注为合成的离线模拟器与历史结果。
- prediction-validation/：数据契约、收入会计与时点门控测试。
- public-evidence/、public-experiments/：公开来源台账、协议、66/67代码及汇总统计。
- publication/：发布清单、SDK来源/许可信息与校验结果。

## 证据边界

始终区分：**SDK能力 → 游戏调用 → 请求构造 → 生产发送成功 → 服务端接收 → 模型训练消费**。不同层不能自动推导。“合理推断”“无法确认”和负结果也是研究结果。

历史编号、文件名和字节保留；重复编号56、66对应不同专题。旧报告应结合后续核验阅读。部分引用仍指向本地原始证据，详见[发布范围](publication/README.md)。

原始游戏APK、完整游戏反编译树、手机/存档及逐客户数据未上传。第三方SDK和资料适用各自条款，本仓库未重新授予统一开源许可，见[第三方声明](THIRD_PARTY_NOTICES.md)。
