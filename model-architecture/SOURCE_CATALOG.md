# 模型架构证据来源目录

本轮为60号第一轮；公开产品声明、SDK可见路径、招聘/专利分别分级。官方发布不等于独立验证生产实现。所有quote均与本地原文逐字核验。

<a id="ma60s01"></a>
## MA60S01 · AppLovin / Axon 2

- 原始URL：https://www.applovin.com/en/blog/applovin-business-model
- 原始文件：[model-architecture/public/al-business.txt:L31](../model-architecture/public/al-business.txt)；范围L31—L34
- 日期：2026-02-02; metadata modified 2026-07-28；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`b38323d5cd83d75adf8f803c86c39bcc45878ec21df56fabe9dc28282020c72b`
- 短摘录：> These models now predict expected value distributions many days into the future
- 主张：【官方公开证实】 官方称Axon2已于2023-04推出，预测互动/转化/支付/金额/复购，并预测未来多日的价值分布用于实时资本配置
- 产品范围：Axon2；原段重点解释游戏玩家对非游戏offer的价值评估，不证明每种手游目标都有相同预测头
- 部署证据：vendor states rollout April 2023 and current prediction; not independently audited
- 限制/反证：CEO署名产品/商业解释，不公开概率分布族、独立heads、loss、参数量、特征表或四款游戏使用。

原始HTTP文件：[model-architecture/public/al-business.raw](../model-architecture/public/al-business.raw)；SHA256 `fb38e804c2bf2807a94797ba3cc0167c7f7f03a68b92b4d369d9238c490bdae1`。

<a id="ma60s02"></a>
## MA60S02 · AppLovin / Axon

- 原始URL：https://legal.applovin.com/about-applovins-axon-ai/
- 原始文件：[nongame/applovin-axon-about.txt:L54](../nongame/applovin-axon-about.txt)；范围L54—L73
- 日期：not stated; snapshot date is not publication date；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`450c55b0b8ef263c41d312af1399433984762753c0f70ed5f94722eba5946cd7`
- 短摘录：> train and optimize on a continual basis
- 主张：【官方公开证实】 官方明确模型持续训练优化的数据类别、广告主特定展示价值出价及排除项
- 产品范围：Axon总体，不是特定游戏字段血缘
- 部署证据：vendor describes current model data use and bidding
- 限制/反证：不公开每字段join、模型结构、训练频率；排除其他bidder出价/用户数据、敏感/受保护/儿童数据。

复用既有证据：S01；保持旧对象不变。

<a id="ma60s03"></a>
## MA60S03 · AppLovin / AppLovin AppsFlyer partner

- 原始URL：https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/appsflyer
- 原始文件：[axon/doc-appsflyer.txt:L183](../axon/doc-appsflyer.txt)；范围L183—L241
- 日期：page date not stated; cached/reviewed 2026-11-19；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`dc1dfd019060e41b50e9570dcdce70452500ecba72a358d7f01dca2b2cf70b30`
- 短摘录：> All media sources, including organic
- 主张：【官方公开证实】 all-source含organic事件共享，landing/checkout/postinstall和金额口径有不同配置
- 产品范围：MMP后台契约，非MAX EventService直发
- 部署证据：supported integration; target-game activation unknown
- 限制/反证：未证后台启用或训练；checkout明确排除广告收入/预测LTV。

复用既有证据：CGS49；保持旧对象不变。

<a id="ma60s04"></a>
## MA60S04 · AppLovin / AppLovin Ads / Axon

- 原始URL：https://www.applovin.com/en/blog/introducing-applovin-ads
- 原始文件：[model-architecture/public/al-introducing.txt:L27](../model-architecture/public/al-introducing.txt)；范围L27—L50
- 日期：2025-10-01; metadata modified 2026-07-15；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`da5e38340c85e2fa6b6f17a08fbe11514c7b4b0f512c375006a1e8fafe8df87b`
- 短摘录：> the incremental data will materially improve AppLovin Ads
- 主张：【官方公开证实】 官方称实时评估展示并按return goals出价；前瞻声明更多广告主的增量数据将改善游戏伙伴效果
- 产品范围：平台扩展方向；不是游戏/电商逐字段共享契约
- 部署证据：real-time bidding present tense; cross-category benefit is forward-looking will/believe
- 限制/反证：不能据此认定电商订单默认进入某手游模型或单一共享网络；无独立数据消融。

原始HTTP文件：[model-architecture/public/al-introducing.raw](../model-architecture/public/al-introducing.raw)；SHA256 `1eb877f32b6a6125fe48ad009e88eb08b0ddf86159cf6e3b8118f5260d895de8`。

<a id="ma60s05"></a>
## MA60S05 · AppLovin / Discovery / Prospecting

- 原始URL：https://www.applovin.com/en/blog/discovery-campaigns
- 原始文件：[model-architecture/public/al-discovery.txt:L21](../model-architecture/public/al-discovery.txt)；范围L21—L36
- 日期：2026-02-25; metadata modified 2026-07-28；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`ad681c6d28df9f79efa11fdfb1c479c221537d9dc44954d2ab997c6829a819aa`
- 短摘录：> uses the same historical purchase data
- 主张：【官方公开证实】 电商Discovery与Prospecting使用同一历史购买数据，区别新访客/新买家目标
- 产品范围：电商获客，不自动适用于手游IAA
- 部署证据：official product launch and setup instructions
- 限制/反证：可证历史购买作为产品输入，未公开身份join、模型、gaming迁移或线上增量。

原始HTTP文件：[model-architecture/public/al-discovery.raw](../model-architecture/public/al-discovery.raw)；SHA256 `b2bcf539a14d492b29d94b30c93db909f36b92ca5b8fd023b4b9ff2aa0074fc1`。

<a id="ma60s06"></a>
## MA60S06 · AppLovin / Advertising platform research

- 原始URL：https://boards.greenhouse.io/applovin/jobs/4712559006?gh_jid=4712559006
- 原始文件：[prediction-system/applovin-job-4712559006-clean.txt:L8](../prediction-system/applovin-job-4712559006-clean.txt)；范围L8—L21
- 日期：updated_at=2026-11-05T14:45:29-05:00；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`8e343eb570d116a28cd6f5b73780858b9d27e1c54ac47f2a4b4e4e9fc792794d`
- 短摘录：> representation learning, feature interaction, and multi-task learning
- 主张：【间接技术线索】 招聘职责涉及用户表示、ranking/retrieval、feature interaction和multi-task learning
- 产品范围：AppLovin广告平台招聘，未明确Axon版本
- 部署证据：research/development duties, not architecture deployment proof
- 限制/反证：explore/develop及技能不证明已部署embedding/MMoE/Transformer或跨App用户图谱。

复用既有证据：S25；保持旧对象不变。

<a id="ma60s07"></a>
## MA60S07 · AppLovin / ML data infrastructure

- 原始URL：https://boards.greenhouse.io/applovin/jobs/4716524006?gh_jid=4716524006
- 原始文件：[prediction-system/applovin-job-4716524006-clean.txt:L8](../prediction-system/applovin-job-4716524006-clean.txt)；范围L8—L21
- 日期：updated_at=2026-11-05T14:45:29-05:00；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`f2459b7bc84a91b24a6d66fdefcc35b22d097b82bd4aac3dfb475cc5f957a688`
- 短摘录：> model training and feature serving
- 主张：【间接技术线索】 职责涉及model training和feature serving数据管道、traceability；feature store是加分项
- 产品范围：AppLovin ML平台职责，非Axon专属源码
- 部署证据：team engineering duties; concrete system implementation unknown
- 限制/反证：不能据此确定已部署某feature store、Spark/Flink链路、更新周期或真实数据源。

复用既有证据：S26；保持旧对象不变。

<a id="ma60s08"></a>
## MA60S08 · AppLovin / Ad Review vs Axon

- 原始URL：https://www.applovin.com/en/blog/catch-bad-ads-not-data
- 原始文件：[prediction-system/applovin-excluded-rival-data.txt:L14](../prediction-system/applovin-excluded-rival-data.txt)；范围L14—L17
- 日期：2026-09-16；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`fd07f9c935dad89f911dd2544760d3c69a50d5b826a13c53a89dd2858ef4b534`
- 短摘录：> Axon
- 主张：【官方公开证实】 官方明确Ad Review不建立用户/设备画像，不供给Axon或其他模型
- 产品范围：Ad Review数据用途排除，不排除广告主授权的自身收入反馈
- 部署证据：explicit official exclusion
- 限制/反证：禁止由MAX适配器或其他网络广告输出推断竞争者用户/报价进入Axon。

复用既有证据：S24；保持旧对象不变。

<a id="ma60s09"></a>
## MA60S09 · AppLovin / Ad ROAS / Blended ROAS

- 原始URL：https://www.applovin.com/en/gaming-apps
- 原始文件：[axon/gaming-apps.txt:L20](../axon/gaming-apps.txt)；范围L20—L40
- 日期：publication date not stated; local official snapshot reused 2026-11-19；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`26948f476ee7859902deeb7a9ceb7d23083fbadf511076a550d3b0f51798d46e`
- 短摘录：> maximizing player lifetime ad revenue
- 主张：【官方公开证实】 产品明确以玩家长期广告收入/IAP/Hybrid价值优化，并将MAX变现与获客关联
- 产品范围：游戏获客目标与产品关系
- 部署证据：officially offered product, not per-game selected objective
- 限制/反证：不公开IAA窗口、每行训练表、收入精度处理或实际效果。

复用既有证据：CGS54；保持旧对象不变。

<a id="ma60s10"></a>
## MA60S10 · AppLovin / IAP revenue sharing

- 原始URL：https://support.applovin.com/en/growth/promoting-your-apps/troubleshooting/in-app-purchase-revenue-sharing
- 原始文件：[axon/doc-in-app-purchase-revenue-sharing.txt:L13](../axon/doc-in-app-purchase-revenue-sharing.txt)；范围L13—L26
- 日期：page date not stated; cached/reviewed 2026-11-19；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`2aa160152e20bf5afcf6cee0f7bf76de6cde0878978f8a515a63e6041457f366`
- 短摘录：> Predicted revenue or predicted LTV
- 主张：【官方公开证实】 IAP/checkout只允许真实用户支付，排除IAA、预测收入和预测LTV
- 产品范围：AppLovin IAP共享口径，不是IAA通道
- 部署证据：documented revenue contract
- 限制/反证：代理value不能伪装真实purchase；该契约不证明后台验单/退款处理。

复用既有证据：CGS52；保持旧对象不变。

<a id="ma60s11"></a>
## MA60S11 · AppLovin / Historical patent metadata

- 原始URL：https://patents.google.com/patent/US20130159103A1/en
- 原始文件：[prediction-system/applovin-historical-patent.txt:L28](../prediction-system/applovin-historical-patent.txt)；范围L28—L84
- 日期：priority 2011-12-16; publication 2013-06-20；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`59b7c77b5765fd53b0e2dbb78b46778db4e717d6da75cffd0760c2dc798698f7`
- 短摘录：> 2011-12-16
- 主张：【间接技术线索】 US20130159103A1优先权2011-12-16；申请人Applovin Corp；Google Patents列Abandoned
- 产品范围：2011/2013专利构想，不是现代Axon部署
- 部署证据：patent publication only; no deployment or current legal opinion
- 限制/反证：Google状态非法律意见；现代权限/数据排除不被早期专利覆盖。

复用既有证据：S31；保持旧对象不变。

<a id="ma60s12"></a>
## MA60S12 · AppLovin / Historical patent claims

- 原始URL：https://patents.google.com/patent/US20130159103A1/en
- 原始文件：[prediction-system/applovin-historical-patent.txt:L1595](../prediction-system/applovin-historical-patent.txt)；范围L1595—L1721
- 日期：priority 2011-12-16; publication 2013-06-20；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`59b7c77b5765fd53b0e2dbb78b46778db4e717d6da75cffd0760c2dc798698f7`
- 短摘录：> A computer-implemented process to generate a user profile
- 主张：【间接技术线索】 42项公开权利要求；独立1/15/29覆盖由App存在/身份/使用及特征产生用户画像的流程/系统/存储介质
- 产品范围：US20130159103A1权利要求范围
- 部署证据：published claim text, not granted/deployed Axon design
- 限制/反证：专利demographics等示例不能套用当前Axon；无LTV训练网络/label/实时CPM公式证据。

复用既有证据：S31；保持旧对象不变。

<a id="ma60s13"></a>
## MA60S13 · Unity / Vector D28 IAA / Hybrid

- 原始URL：https://unity.com/blog/d28-roas
- 原始文件：[vector/d28-blog.txt:L15](../vector/d28-blog.txt)；范围L15—L43
- 日期：2026-05-21；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`3fb6008feba929fde7ab919c45e9bae687457b219545a4289e6a57c90e983e68`
- 短摘录：> predicts each user’s likely ad revenue over 28 days
- 主张：【官方公开证实】 官方明确预测每用户28天广告收入并按国家tROAS动态出价；Hybrid优化组合28天收入
- 产品范围：2026-05 D28 IAA/Hybrid产品，不是无限生命周期
- 部署证据：official product launch and closed-beta aggregate results
- 限制/反证：未公开预测头/收入样本构造；配对beta非本研究随机实验，不能量化架构贡献。

复用既有证据：S22；保持旧对象不变。

<a id="ma60s14"></a>
## MA60S14 · Unity / Unity Ads ROAS learning

- 原始URL：https://docs.unity.com/en-us/grow/acquire/campaigns/roas/roas-campaign-best-practices.md
- 原始文件：[vector/doc-roas-campaign-best-practices.txt:L36](../vector/doc-roas-campaign-best-practices.txt)；范围L36—L70
- 日期：2026-03-05；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`181a6cffe4f8921bda559c2a0cc0571e8d61bf352dc8e400c05b5553ad63955f`
- 短摘录：> helps to train the machine learning models
- 主张：【官方公开证实】 官方明确预启动至少两周SDK数据及未归因事件有助训练，未计入学习阈值；建议全来源和Lifetime窗口
- 产品范围：同一广告主App跨来源样本；非跨广告主个人轨迹
- 部署证据：explicit training-purpose contract; no target-game activation
- 限制/反证：未给逐字段训练血缘、样本权重、回填范围或增益；自然量与付费分布可不同。

复用既有证据：CGS42；保持旧对象不变。

<a id="ma60s15"></a>
## MA60S15 · Unity / Unity Ads ROAS cohorts

- 原始URL：https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md
- 原始文件：[vector/doc-intro-to-roas-campaigns.txt:L79](../vector/doc-intro-to-roas-campaigns.txt)；范围L79—L116
- 日期：2026-05-21；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`dbf6ca7e80360e22e49243ab7ab487dc1d4ce433a15310a1dc8b8160d3b1aa61`
- 短摘录：> 75 unique, D7 matured purchasers
- 主张：【官方公开证实】 成熟cohort与IAA/IAP/Hybrid学习门槛公开；D28退出门槛用D7成熟数据
- 产品范围：ROAS学习退出条件，不是模型全部训练样本或D28已成熟
- 部署证据：documented optimization product behavior
- 限制/反证：零收入负例采样、迟到/退款/去重/损失函数未知。

复用既有证据：CGS47；保持旧对象不变。

<a id="ma60s16"></a>
## MA60S16 · Unity / Vector IAP D7 / D28

- 原始URL：https://unity.com/blog/d7-vs-d28-iap-roas-campaigns
- 原始文件：[model-architecture/public/unity-d7-d28.txt:L145](../model-architecture/public/unity-d7-d28.txt)；范围L145—L176
- 日期：2026-06-25; sitemap lastmod 2026-10-26；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`9aca03187f001a9cdfcbb4e4386d8e81b66791007dd571e55f90cb68d271688a`
- 短摘录：> use machine learning to predict which users are most likely to make purchases
- 主张：【官方公开证实】 官方说明IAP optimizers预测购买/价值并动态出价，D7/D28窗口学习速度不同
- 产品范围：D7/D28 IAP产品级预测说明
- 部署证据：present-tense product description; architecture not disclosed
- 限制/反证：不证明独立pPurchase head或多任务共享层；D28不等于无限LTV。

原始HTTP文件：[model-architecture/public/unity-d7-d28.raw](../model-architecture/public/unity-d7-d28.raw)；SHA256 `92476c3495b2a740743241b3e868421c531b391b6f13037094f5f3b155f9f8c4`。

<a id="ma60s17"></a>
## MA60S17 · Unity / Vector bid-time player/game intelligence

- 原始URL：https://unity.com/blog/d7-vs-d28-iap-roas-campaigns
- 原始文件：[model-architecture/public/unity-d7-d28.txt:L208](../model-architecture/public/unity-d7-d28.txt)；范围L208—L223
- 日期：2026-06-25; cited data period 2024-04 to 2025-02；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`9aca03187f001a9cdfcbb4e4386d8e81b66791007dd571e55f90cb68d271688a`
- 短摘录：> cross-game behavioral patterns and aggregate cohort insights
- 主张：【官方公开证实】 官方明确attributed/unattributed数据，包括cross-game behavioral patterns和aggregate cohort insights，在bid decision时区分玩家类型
- 产品范围：Vector IAP D7/D28产品用途，字段/作用域不公开
- 部署证据：vendor states current bid-decision use; not independently audited
- 限制/反证：未说明参数共享/聚合统计/个人级ID各占何角色；38%统计样本期2024-04到2025-02，不是Vector因果提升实验。

原始HTTP文件：[model-architecture/public/unity-d7-d28.raw](../model-architecture/public/unity-d7-d28.raw)；SHA256 `92476c3495b2a740743241b3e868421c531b391b6f13037094f5f3b155f9f8c4`。

<a id="ma60s18"></a>
## MA60S18 · Unity / Vector Gamer AI inference

- 原始URL：https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity/job/Mountain-View-CA-USA/Staff-Backend-Engineer--ML-Inference-Systems_JOBREQ-2615964
- 原始文件：[prediction-system/unity-job-JOBREQ-2615964-clean.txt:L1](../prediction-system/unity-job-JOBREQ-2615964-clean.txt)；范围L1—L24
- 日期：startDate=2026-09-28; postedOn=Posted 30+ Days Ago；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`66b4c09347df96257c660a8bf25c993545d35ae647a3164e29c070eff41a2214`
- 短摘录：> large-scale online model inference
- 主张：【间接技术线索】 Vector Gamer AI负责广告排序/竞价，招聘陈述运行低延迟高吞吐online model inference平台
- 产品范围：明确归属Vector的团队生产职责
- 部署证据：job describes current production responsibility; implementation not independently verified
- 限制/反证：Triton仅加分项；不证明实际模型、时延SLA、特征或跨App匹配。

复用既有证据：S29；保持旧对象不变。

<a id="ma60s19"></a>
## MA60S19 · Unity / Vector Ads Modeling

- 原始URL：https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity/job/Mountain-View-CA-USA/Principal-Machine-Learning-Engineer--Ads-Modeling_JOBREQ-2616596
- 原始文件：[prediction-system/unity-job-JOBREQ-2616596-clean.txt:L1](../prediction-system/unity-job-JOBREQ-2616596-clean.txt)；范围L1—L13
- 日期：startDate=2026-09-28; postedOn=Posted 30+ Days Ago；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`882af4b6a9b94a208a6769636b8d0bd70e03cf781ffc69777dfc7c3e836400a2`
- 短摘录：> user behavior modeling
- 主张：【间接技术线索】 Vector Modeling招聘涉及用户行为建模、rich user data和research→production
- 产品范围：Vector建模团队研发方向
- 部署证据：research roadmap and candidate qualifications, not deployed architecture
- 限制/反证：不证明Embedding/Transformer/多任务/跨游戏共享网络或具体输入。

复用既有证据：S30；保持旧对象不变。

<a id="ma60s20"></a>
## MA60S20 · Unity / Vector Bidding Science

- 原始URL：https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity/job/Mountain-View-CA-USA/Senior-Machine-Learning-Engineer--Vector-Bidding-Science_JOBREQ-2616286
- 原始文件：[prediction-system/unity-job-JOBREQ-2616286-clean.txt:L1](../prediction-system/unity-job-JOBREQ-2616286-clean.txt)；范围L1—L23
- 日期：startDate=2026-09-28; postedOn=Posted 30+ Days Ago；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`6daea74617f8dccd5978cd9917685cc8deb93c5801049e26d25df2e2efab0554`
- 短摘录：> bidding and pacing algorithms
- 主张：【间接技术线索】 Vector竞价团队职责涉及bidding/pacing、bid landscape forecasting与offline/online评估
- 产品范围：Vector竞价系统研发职责
- 部署证据：development duties; next-generation systems not deployment proof
- 限制/反证：RL/control theory及survival analysis属技能项，不能写成已部署算法。

复用既有证据：S28；保持旧对象不变。

<a id="ma60s21"></a>
## MA60S21 · Unity / Vector correlations and ecosystem

- 原始URL：https://unity.com/products/unity-ads/vector
- 原始文件：[vector/unity-vector-correct.txt:L10](../vector/unity-vector-correct.txt)；范围L10—L15
- 日期：page date not stated; cached/reviewed 2026-11-19；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`7c38a287f3cd15624083e4c6d4720e49de626cbc7f85e7a5483018ac2e704a61`
- 短摘录：> correlations between IAP and ad behavior
- 主张：【官方公开证实】 产品披露game DNA/real behavior、IAP和广告行为相关性及生态数据/新训练方法
- 产品范围：产品层关联建模用途，不是多任务网络结构
- 部署证据：public product claim
- 限制/反证：不证明共用embedding或跨应用个人身份；potential不等于每款引擎游戏默认供数据。

复用既有证据：CGS53；保持旧对象不变。

<a id="ma60s22"></a>
## MA60S22 · Unity / IAP / D2C to Vector

- 原始URL：https://unity.com/blog/unite-seoul-keynote-2026-recap
- 原始文件：[vector/unity-2026-keynote.txt:L120](../vector/unity-2026-keynote.txt)；范围L120—L121
- 日期：2026-07-21；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`99513962bd48ea9813178414f0ee9cd4c24d345ac536b49c43a36a7dcb530a95`
- 短摘录：> Vector
- 主张：【官方公开证实】 Unite回顾明确IAP SDK/D2C购买数据可以丰富Vector
- 产品范围：IAP/D2C产品数据用途连接，不是字段级训练表
- 部署证据：official can-help-enrich statement; per-event deployment unknown
- 限制/反证：没有因此补齐Insights native接收→训练label，四款实际启用未知。

复用既有证据：S21；保持旧对象不变。

<a id="ma60s23"></a>
## MA60S23 · Unity / Developer Data consent

- 原始URL：https://docs.unity.com/en-us/cloud/developer-data-framework/end-user-consent.md
- 原始文件：[vector/ddf-end-user-consent.txt:L14](../vector/ddf-end-user-consent.txt)；范围L14—L38
- 日期：not stated; snapshot date is not publication date；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`ea304dbc17e8077ee3baf00e01c0294d6bde940a3616d7fb0abc2c1df98b2d31`
- 短摘录：> ads_intent = denied
- 主张：【官方公开证实】 Developer Data的analytics_intent与ads_intent用途独立，默认未知状态ads_intent=denied
- 产品范围：Developer Data框架，不自动覆盖各SDK所有读操作
- 部署证据：documented consent/usage contract
- 限制/反证：可采集不等于可用于个性化广告；不能推断所有Runtime数据默认训练Vector。

复用既有证据：S20；保持旧对象不变。

<a id="ma60s24"></a>
## MA60S24 · Unity / IAP5.5.1 Insights forwarding

- 原始URL：官方包来源见原包provenance
- 原始文件：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs:L188](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs)；范围L188—L239
- 日期：not stated; reviewed 2026-11-19；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`
- 短摘录：> Forward
- 主张：【SDK代码证实】 IAP protobuf的gateway/runtime转发分支可见，闭源native接收后的训练用途仍未知
- 产品范围：官方IAP5.5.1独立包，不是四款游戏启用证据
- 部署证据：client code only; no production invocation
- 限制/反证：不能由API存在证明收入验真、退款、送达/ACK或Vector训练。

复用既有证据：C53S23；保持旧对象不变。

<a id="ma60s25"></a>
## MA60S25 · Unity / Unity Ads4.17 prebid history

- 原始URL：官方包来源见原包provenance
- 原始文件：[ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt:L33](../ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt)；范围L33—L89
- 日期：not stated; reviewed 2026-11-19；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`eaf08c35ec940f873fe79f04701f7799cb328b90ebe34d5dc97ea2ae0ca759c1`
- 短摘录：> campaignState = campaignRepository.getCampaignState()
- 主张：【SDK代码证实】 Token外层明确写入sessionCounters、campaignState与HB seq/wins/starts
- 产品范围：4.17源码；4.18所选外层对照见既有56
- 部署证据：serialization code only, not model-feature ingestion
- 限制/反证：不能解出不透明内层或跨App轨迹；bid_time新鲜度和特征增益未知。

复用既有证据：CGS01；保持旧对象不变。

<a id="ma60s26"></a>
## MA60S26 · Unity / MMP S2S revenue association

- 原始URL：https://docs.unity.com/en-us/grow/acquire/partner-integration/custom/send-postbacks.md
- 原始文件：[vector/doc-send-postbacks.txt:L28](../vector/doc-send-postbacks.txt)；范围L28—L109
- 日期：2026-01-30；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`a4f39f6236d9d3da9f8f07f3599a656d586e15df2322b134163d1b79d652d2d2`
- 短摘录：> game_id
- 主张：【官方公开证实】 S2S公开身份、广告主/活动、安装/事件时间、归因标记与收入字段契约
- 产品范围：MMP→Unity接收契约
- 部署证据：interface capability, no observed matching/production receipt
- 限制/反证：同包ID不等于join成功；受隐私/可用性限制，publisher ID不替代advertiser ID。

复用既有证据：CGS48；保持旧对象不变。

<a id="ma60s27"></a>
## MA60S27 · AppLovin / Incrementality and measurement

- 原始URL：https://www.applovin.com/en/blog/measurement-lens
- 原始文件：[model-architecture/public/al-measurement.txt:L20](../model-architecture/public/al-measurement.txt)；范围L20—L41
- 日期：2026-06-16；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`134bf914b13efdb6623177df32d4dad90bdd76618e05f8103f341cd1a01fea3f`
- 短摘录：> not measuring the same thing
- 主张：【官方公开证实】 官方强调归因报告/MTA/MMM/增量实验不是同一量，测试受holdout和预算稳定等条件约束
- 产品范围：电商测量讨论，用于限制收益因果外推
- 部署证据：measurement-method statement; no raw experiment dataset
- 限制/反证：90% power是设计目标声明，不证明测试实际功效；不能套用四款或把相关提升当增量。

原始HTTP文件：[model-architecture/public/al-measurement.raw](../model-architecture/public/al-measurement.raw)；SHA256 `a2e5054377744af73f94121eb6f6a2593771c9615ce1b36bc60cf7f34f0836e3`。

<a id="ma60s28"></a>
## MA60S28 · AppLovin / Creative and targeting

- 原始URL：https://www.applovin.com/en/blog/silos-performance
- 原始文件：[model-architecture/public/al-silos.txt:L40](../model-architecture/public/al-silos.txt)；范围L40—L46
- 日期：2026-04-30；查阅：2026-11-19T10:26:23.399440+00:00
- SHA256：`0d97ad8496b4c0413bd26e5b17043181532a00f50d3cc0c78d8dba704ebf2d47`
- 短摘录：> Our models match the right user to the right ad relative to the conversion event
- 主张：【官方公开证实】 官方说明素材及目标转化事件影响模型匹配，限制把全部增长归因于身份/模型架构
- 产品范围：AppLovin电商品牌运营语境
- 部署证据：product/operating description, not feature-level deployment proof
- 限制/反证：女性/代际素材例子不是使用年龄/性别字段训练的证据；不得覆盖Axon明确排除项。

原始HTTP文件：[model-architecture/public/al-silos.raw](../model-architecture/public/al-silos.raw)；SHA256 `ac74cbb975a6dbc4b3de2fd3b48d9a67f189a7b50e7eebe418384dc000204fc0`。
