# 数据许可、可下载性与真实标签审计

2026-11-19。本轮检查9个候选，**3个已实际取得并核验的数据发行物允许开展受限通用研究**：UCI Online Retail、官方仓库Open Bandit小样本、KuaiRand-Pure。没有一个同时满足本项目手游D7/D28真实收入、全安装分母、多游戏或真实竞价收益的准入要求。另一个下载成功的是代码包，不算收入数据集。

## 1. 实际取得与可用范围

| 编号 | 下载与许可证据 | 当前准入边界 |
|---|---|---|
| DS65-01 | UCI352官方页CC BY4；23715478字节ZIP、541909行Excel，原包SHA256见[ASSET_VERIFICATION](audit/ASSET_VERIFICATION.json) | 可做已观察零售客户的未来发票金额预测；Quantity×UnitPrice为GBP，不是IAA/IAP、验真银行到账或游戏净LTV。允许使用需署名，不作个人识别或跨源join |
| DS65-03 | ZOZO官方st-tech/zr-obp仓库含obd样本，项目明示Apache2；实际下载random/all/all.csv、10000行，见[样本核验](audit/OBD_SAMPLE_VERIFICATION.json) | 准入**仓库发行样本**，保留许可/版权及修改说明；不把代码许可证外推外部26M全量ZIP。可做点击/策略OPE，不是收入或竞价 |
| DS65-04 | Zenodo官方发行47432272字节tar.gz实际可下载；内置[LICENSE](audit/KUAI_DATA_LICENSE.txt)为CC BY-SA4，仓库亦为SA4 | portal元数据写CC BY4，**不据此丢弃归档内ShareAlike条件**；本轮采用内置较严格条款，保留出处、修改说明及适用再分发要求。只做非货币行为研究，无游戏收入 |

公开匿名化键仅在本数据集内分组；不得反查、跨数据集匹配或重建自然人身份。本轮结构审计不导出用户行值、账号/广告ID或评论者姓名；下载的研究数据保留发布方匿名键，不是访问真实账号。原始公开发行物只读保存，审计输出是schema/聚合质量而非个人画像。

## 2. 三个只有看真实文件才发现的风险

1. **UCI metadata不替代数据质量。**API称has_missing_values=no，但实际CustomerID缺135080行，Description缺1454行；完全相同行5268条，非正单价2517条、非正数量10624条。相同行不一定是重复经济事件，缺少行幂等键时不得盲删；取消/负数不是自动清洗成0，需定义退款和发票口径。不得悄悄只留付费高价值者。
2. **OBD文档与文件字段有版本差异。**README称`action_prob`，实际为`propensity_score`；本样本2019-11-24—30，仅38点击，p=0.0125。不能伪造真实金额或声称稳定的模型增益；静态用户/视频统计的available_at未证，默认排除以免未来泄漏。
3. **KuaiRand的portal许可和包内许可不同。**实际归档LICENSE和6份CSV表头已核；保留SA义务。`play_time_ms`、`is_click`、`long_view`都是参与信号；tab/policy不是不同游戏。曝光后的playtime不能当同次曝光前特征，汇总statistic表也不能未经as-of审计入模。

## 3. 没有通过的候选

| 编号 | 真实取得了什么 | 停止原因 |
|---|---|---|
| DS65-02 Online Retail II | 官方元数据/许可与下载链接；未下载二进制 | 与352同一商家且时间重叠；不提供跨游戏，也不能当独立复制验证。为避免重复下载，本轮未取另一个大包 |
| DS65-05/06 Criteo | 官方完整数据定义与CC BY-NC-SA4条款、公开链接；未下载数据 | 当前商业增长研发不能擅自视为非商业用途，暂停下载/训练；Attribution的cost/cpo还明确是transformed，不是真实币种；二者无手游IAA/IAP标签。不是“许可不明”，而是用途限制明确但当前适用未获确认 |
| DS65-07 iPinYou | 作者整合仓库README/代码LICENSE；原UCL公开地址连接超时 | 代码Apache不自动授权原竞赛数据；原数据未取得，不绕过访问限制，也不从二手镜像推定数据许可 |
| DS65-08 mobile_games_LTV | 第三方仓库声称2100万游戏事件、代码/分析文档；根目录无已核验原始数据和数据许可 | GitHub公开不是数据授权，README效果不是本地真实样本；未取作者个人文档或联系作者，不算可用游戏数据 |
| DS65-09 Zenodo游戏预测框架 | 下载189171字节代码ZIP；README L13—19明确商业月度估计不可再分发、包内code only；有两游戏公共事件日历 | **MIT只授权代码，日历CC BY4不提供收入标签**。标题/摘要看似多游戏收入可复现，实际商业panel缺失；即使有月度总额也不是用户D28安装标签。见[缺口原文](audit/GAME_CODE_DATA_GAP.json)与[README](audit/GAME_FRAMEWORK_README.md) |

本轮候选搜索使用官方UCI/Criteo/ZOZO仓库、Zenodo/DataCite API和公开仓库；Bing宽查询返回无关词典结果，不算覆盖完整。候选数量和成功下载量都不是研究质量；**可执行手游价值预测数据集数仍为0**。未登录Kaggle/商业情报后台，未绕过登录、挑战、支付或权限。

## 4. 保留与再分发

原始数据包位于audit目录，不修改，不向报告附个人行；公开分享衍生数据前按具体许可复核署名、NOTICE/修改及SA条款，不直接把本地全部audit目录推送到外部。许可不授予再识别、商标或额外隐私权；本轮不执行真实广告或归因请求。

逐候选字段和准入结论见[DATASET_CATALOG.csv](DATASET_CATALOG.csv)，E0—E4见[EXPERIMENT_ADMISSION_MATRIX.csv](EXPERIMENT_ADMISSION_MATRIX.csv)。本轮没有训练模型、报告增益或把合成数据替代真实标签。
