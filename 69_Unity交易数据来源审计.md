# Unity交易研究：真实数据与公开补充材料审计

2026-11-20。**真实研究成立，原始数据不公开；公开R代码是合成占位数据，不能拿来训练真实玩家价值模型。**

## 论文与实际取得的文件

《The Many Faces of Monetisation: Understanding the Diversity and Extremity of Player Spending in Mobile Games via Massive-scale Transactional Analysis》，David Zendle、Catherine Flick、Sebastian Deterding、Joe Cutting、Elena Petrovskaya、Anders Drachen，ACM Games: Research and Practice，2023，DOI：[10.1145/3582927](https://doi.org/10.1145/3582927)。

ACM与DMU入口返回403挑战页，本轮未绕过；通过公开PsyArXiv记录的OSF primary_file关系取得作者接受稿：[永久下载入口](https://osf.io/download/hxk8u/)。PDF SHA256：`24e89a65624536dcda43877b3a3020dddf96e1326b2e92b996459d4a2c39c4d5`，与OSF元数据给出的原文件哈希一致。

公开项目：[Distributions of Spending in Video Games](https://osf.io/du4kr/)。文件API返回两个文件，pagination next为空：

| 文件 | 实际下载/哈希 | 内容及边界 |
|---|---|---|
| Technical Appendix.docx | 13,503字节；`4f7f219a4184a3163115ec1de184aee05d56afacddb5116ec1e341eb4f428357` | 将游戏消费分布按百分位简化，用Wasserstein距离及聚类分析；不是原始交易 |
| Code for Publication.R | 10,275字节；`6a9a3a0fa95b914f12e728a87e95de7e4d1d3c6072f2980c9f21216c7f4feb38` | 注释明确generate synthetic metadata / synthetic spending data，sample生成金额；仅复现分析流程，不是69m玩家记录 |

原件：[PDF](game-industry69/sources/unity-full-paper.pdf)、[DOCX](game-industry69/sources/unity-technical-appendix.docx)、[R](game-industry69/sources/unity-analysis-code.R)。本轮只静态读取，未执行R。公开root清单不等于已穷尽所有私人材料，但已结合论文明确的数据不公开条款作准入判断。

## 论文直接证明的数据契约

| 项目 | 原文结论 | 原始位置 |
|---|---|---|
| 数据持有人与访问 | Unity提供；与高校法律协议约束；仅在Unity数据仓库内部访问；作者不能分享或帮助他人获得访问 | §2.1；提取文本815—825行 |
| 来源 | Unity IAP引擎的iOS游戏预匿名交易日志；BigQuery内聚合处理后导出R | §2.2；979—985行 |
| 入选游戏 | 观察期至少1,000位独立付费者，2,873款；不是所有Unity游戏或所有安装用户 | 984—992行 |
| 样本量 | 69,144,363个游戏内付费用户键、461,996,143笔IAP、约US$4.7bn | §2.5；1559—1563行 |
| 时间 | 2020-08-01至2022-04-16，共624天 | 1051—1052、1562—1563行 |
| 货币 | 原交易不同币种，按交易发生日期汇率换算USD | 1053—1056行 |
| 身份 | 用户在游戏内唯一，游戏之间不能关联；同一自然人可能被不同游戏重复计数 | 1057—1063、1550—1553行 |
| 收入范围 | IAP，不包含所有游戏收入；不包含广告及游戏拷贝售卖的完整收入 | 1064—1066行 |
| 许可与伦理 | 原研究按法律协议和研究伦理执行，不赋予后续第三方自动使用权 | §2.1/2.4 |

证据ID GI69S_unity_paper，行号对应[PDF提取文本](game-industry69/sources/unity-full-paper.txt)；源哈希/OSF关系见[原始证据目录](game-industry69/SOURCE_CATALOG.md)。这批是2020—2022研究数据，不能用当前IAP5.5.1新增Insights路径反写其历史采集实现。

## 可得性和申请渠道

【已核验】公开有论文、技术附录和占位代码；**没有取得真实用户级数据，也未见本次公开root文件清单含真实交易文件。** 论文提到的Unity academia-research地址本轮重定向unity.com/learn，不能当作仍有效的交易数据申请表。

【无法确认】当前是否接受外部研究申请、是否只限高校/安全研究环境、可给哪些游戏级统计、是否能开放事件时间/匿名用户表、收费与审查条件。正确下一步是向Unity权利方确认新的研究协议与最小聚合材料，而不是请求论文作者转发其无权提供的数据。仅整理申请问题，未主动联系。

可申请的最小升级：原研究明确可共享的游戏级消费分位表及处理口径；若需要预测，再询问受控环境内的匿名游戏内用户时间序列、安装时间、全安装分母/零收入、覆盖窗、退款/验单和可用时间。这是建议，不是已存在的公开API或已获得许可。

## 选择偏差与实验结论

全样本都是观察期内至少付过一次款的人。某日以后没有支付记录只表示该IAP账本未观察到支付，不能代表无IAA收入、没有活跃或永久流失。至少千名付费者的游戏筛选还排除了大量小型/冷启动产品。

如果未来依法取得相同原始数据，最多能先做**已观察付费者的游戏内未来IAP预测**，仍需固定as-of和成熟窗口。不能据此验证全安装人群pPurchase、安装概率、IAA/IAP混合LTV或安装前高价值排序。不同游戏可不依赖个人联结比较群体/共享参数，但须先取得至少两款独立游戏的同口径数据及授权；本轮不满足。

此论文证明Unity有过实际受控研究数据仓库，不证明该表、全部交易或每个匿名键被Vector训练使用；不能把论文消费分布聚类当作Vector模型结构。当前准入：文献审计GO，真实训练STOP。
