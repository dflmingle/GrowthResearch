# Axon / Vector模型架构公开证据：第60号第一轮

2026-11-19。**可以还原两家公开声称的“输入类别→价值目标→竞价用途”，还不能还原其生产模型的网络、损失函数、参数共享或训练数据集。** 本轮取得比SDK字段更接近决策用途的材料，但不将官方产品/CEO陈述当作独立部署审计。按执行顺序，本轮完成60号与证据基础文件，尚未制作61—64号的最终研究结论。

原始URL、日期、短摘录、SHA256、位置、适用产品、部署措辞、反证及未知点逐行保存于[CLAIM_MATRIX.csv](model-architecture/CLAIM_MATRIX.csv)；可读来源：[SOURCE_CATALOG.md](model-architecture/SOURCE_CATALOG.md)；完整原文片段：[SOURCE_EVIDENCE.json](model-architecture/SOURCE_EVIDENCE.json)。28条主张分别绑定原文件，复用既有SDK证据，不重新下载SDK。

## 1. Axon目前最强的五组架构证据

| 优先级 | 原始证据与短摘录 | 真正证明什么 | 不能证明什么 |
|---|---|---|---|
| A1 | 【官方公开证实】Adam Foroughi，2026-02-02，*The AppLovin business model*：“predict expected value distributions many days into the future”；列出ad engagement、CTR、conversion、payment probability、purchase size、repeat behavior。[MA60S01](model-architecture/SOURCE_CATALOG.md#ma60s01) | 官方明确称Axon2已于2023-04推出，当前预测未来多日价值分布并用于实时资本配置；不是只有安装量 | 列举预测量不证明分别有独立head、乘法结构、联合loss或某分布族。原段重点解释游戏玩家对非游戏offer的评估，不能全部套成手游IAA实现 |
| A2 | 【官方公开证实】Axon官方说明：“train and optimize on a continual basis”，使用设备/网络、App/广告等互动、MAX胜负通知及广告主选择共享的数据。[MA60S02](model-architecture/SOURCE_CATALOG.md#ma60s02) | 明确涉及训练输入类别和持续优化，而非仅SDK能采集；按对特定广告主的展示价值出价 | 不公开每字段join、跨游戏表示、训练批次/频率。明确排除其他bidder出价/用户数据及敏感/受保护/儿童数据 |
| A3 | 【官方公开证实】2025-10-01 CEO文章：“evaluates each impression in real time and bids based on your return goals”。[MA60S04](model-architecture/SOURCE_CATALOG.md#ma60s04) | 明确涉及在线推断/决策用途：单次展示与广告主return goal关联；目标价值而非仅CTR | 未给pInstall/条件LTV拆解、CPM公式、pacing或bid shading；“实际按目标行动”不等于承诺每个广告主盈利 |
| A4 | 【官方公开证实】2026-02-25技术人员署名的Discovery发布文：“uses the same historical purchase data”；可在后台选择新访客/新买家目标。[MA60S05](model-architecture/SOURCE_CATALOG.md#ma60s05) | 历史真实购买是一个明确产品输入，目标定义不同可改变获客优化。另有全来源/organic MMP共享契约[MA60S03](model-architecture/SOURCE_CATALOG.md#ma60s03) | Discovery属于电商；未公开该数据具体是排除名单、训练标签、特征或组合，也未证明它进入手游IAA模型。不能用电商能力补游戏训练断点 |
| A5 | 【间接技术线索】ML岗位明确提user representations、ranking/retrieval、multi-task learning；数据基础设施岗位职责提model training/feature serving和traceability。[MA60S06](model-architecture/SOURCE_CATALOG.md#ma60s06)、[MA60S07](model-architecture/SOURCE_CATALOG.md#ma60s07) | 有针对性地支持“广告平台存在表示、训练与在线特征工程研发”的轮廓，比行业通用猜测具体 | 职位未指定Axon模型版本；explore/develop及preferred skill不是已部署MMoE/Transformer/feature store证据。A5弱于A1—A3的产品用途直接陈述 |

**新增跨业务边界：**2025-10-01文章明确说更多广告主的“incremental data will materially improve”广告效果并“driving better results for our gaming partners”。这是官方预期方向，更新了“完全没有公开跨业务受益表述”的说法；但使用will/believe，**仍不是电商订单默认混入手游训练的生产血缘证明**。新来源和旧未知边并存，不覆盖历史记录。[MA60S04](model-architecture/SOURCE_CATALOG.md#ma60s04)

## 2. Vector目前最强的五组架构证据

| 优先级 | 原始证据与短摘录 | 真正证明什么 | 不能证明什么 |
|---|---|---|---|
| V1 | 【官方公开证实】2026-06-25，*D7 or D28 IAP ROAS campaigns?*：“cross-game behavioral patterns and aggregate cohort insights”，在“moment of bid decision”区分玩家类型。[MA60S17](model-architecture/SOURCE_CATALOG.md#ma60s17) | **官方明确把跨游戏行为模式、聚合cohort洞察与bid-time玩家区分连接起来**；比只说收集Runtime数据更具体 | 未给行为字段、窗口、ID、表示、特征表、隐私分支；无法区分参数迁移、聚合统计、个人级历史的具体贡献。营销作者的产品用途陈述不是生产架构论文 |
| V2 | 【官方公开证实】2026-05-21 D28发布：“predicts each user’s likely ad revenue over 28 days”，按国家D28 ROAS目标动态调价；Hybrid用28天组合收入。[MA60S13](model-architecture/SOURCE_CATALOG.md#ma60s13) | 明确预测目标、时间窗口及对出价的作用；支持IAA与IAP共同价值目标 | 不证明独立收入heads、未来无限LTV、预测误差或真实计费公式。组合目标不等于多任务网络 |
| V3 | 【官方公开证实】ROAS best practices：预启动至少两周SDK数据+对应unattributed postbacks“helps to train the machine learning models”，且不计入学习阈值。[MA60S14](model-architecture/SOURCE_CATALOG.md#ma60s14) | 这是**明确训练用途**，不是仅能发事件；同一广告主自然/跨渠道用户可提供冷启动学习样本 | 不等于跨广告主个人级共享；不证明全部历史自动回填或样本权重。学习阈值是产品退出门槛，非训练集大小[MA60S15](model-architecture/SOURCE_CATALOG.md#ma60s15) |
| V4 | 【官方公开证实】Vector页面明确IAP与ad behavior的correlations、game DNA和real player behavior；2026-06 IAP文章说明购买预测和D7/D28动态竞价。[MA60S21](model-architecture/SOURCE_CATALOG.md#ma60s21)、[MA60S16](model-architecture/SOURCE_CATALOG.md#ma60s16) | 产品公开声称使用玩家/游戏关联及两类变现行为关系，且窗口会改变目标玩家 | 相关性建模不证明多任务损失、shared embedding或个人图谱；game DNA不是已公开字段规范 |
| V5 | 【间接技术线索】Vector Gamer AI职位明确负责ad ranking/bidding和online model inference；Bidding Science职责提pacing、bid landscape forecasting和A/B。[MA60S18](model-architecture/SOURCE_CATALOG.md#ma60s18)、[MA60S20](model-architecture/SOURCE_CATALOG.md#ma60s20) | 明确归属Vector的推断与竞价团队分工，可支持实时服务层和竞价约束层分开研究 | 虽有当前生产职责描述，仍是招聘材料；Triton、RL、control theory、survival analysis不能升级成实际部署事实 |

**V1的用词需要精确：**本文中的attributed/unattributed及cross-game patterns属于产品叙述，不应把“unattributed”机械等同于“已经取得跨App个人画像”。MMP文档的unattributed指未归因给Unity，可包含其他渠道/自然量；两种语境不能直接拼成同一字段血缘。

## 3. 哪些真正触及训练或推断，哪些仍只是线索

| 层级 | 已取得材料 | 可用结论 |
|---|---|---|
| 明确训练输入/用途 | Axon官方持续训练类别；Unity预启动unattributed数据帮助训练 | 【官方公开证实】存在该产品级数据用途；不证明目标游戏或逐字段样本 |
| 明确推断目标/决策用途 | Axon未来多日价值分布/实时展示return goal；Vector D28收入预测/动态调价；Vector跨游戏模式用于bid decision | 【官方公开证实】用途连接比SDK字段更强；仍是厂商披露，非本研究独立生产观测 |
| 工程组织和方向 | AppLovin表示/训练数据工程岗位；Vector Modeling/Gamer AI/Bidding Science | 【间接技术线索】支持架构分层研究；不指定模型实现 |
| 可见客户端路径 | Unity Ads Token历史外层；IAP Insights gateway/native；MMP身份/收入契约 | 【SDK代码证实/官方公开证实】数据可构造或配置共享；不证明这些字段进生产训练[MA60S24–MA60S26](model-architecture/SOURCE_CATALOG.md#ma60s24) |
| 效果/商业叙述 | CEO规模/利润表述、D28 beta聚合结果、素材和预算建议 | 厂商案例/主张，不用于恢复架构或评判两家优劣 |
| 网络结构/损失函数/参数共享 | 没有取得可核验的现代Axon/Vector生产实现论文或白皮书 | 【无法确认】不能将MMoE、ESMM、Transformer、用户Embedding、RL或图神经网络写成厂商事实 |

**不是“官方文章=纯营销”，也不是“官方文章=架构已恢复”。**本轮保留具体可证用途，同时明确哪些是产品作者或CEO的陈述，哪些是代码、配置、招聘、专利以及独立审计。

## 4. 专利与会议材料的审计边界

核验既有原文US20130159103A1 *Advertisement Selection Based on Mobile Applications*：申请人/原始受让人Applovin Corp；发明人Adam Foroughi、John Krystynak、Andrew Karam、Furqan Rydhan、Matthew Bornski；优先权2011-12-16、申请2012-12-14、公开2013-06-20。Google Patents索引为Abandoned，状态/受让人均附非法律结论警示。[MA60S11](model-architecture/SOURCE_CATALOG.md#ma60s11)

42项公开权利要求中，独立1/15/29分别覆盖流程、系统、计算机可读介质：App存在/身份/使用情况及App特征→用户画像；从属项增加广告选择/存储等。**不覆盖一个已证现代Axon LTV训练网络。**专利里的demographics/安装App检测只是当时方案，不能越过现代权限，尤其不能覆盖当前Axon排除年龄/性别等受保护特征的说明。[MA60S12](model-architecture/SOURCE_CATALOG.md#ma60s12)、[MA60S02](model-architecture/SOURCE_CATALOG.md#ma60s02)；结构化专利记录：[PATENT_RECORDS.json](model-architecture/PATENT_RECORDS.json)。

本轮未取得可核验的Unity/Vector专属LTV模型专利，也没有取得可归属现代Axon/Vector的GDC/会议完整模型实现。**这表示本轮检索没有取得，不是证明不存在。**公开搜索的Google HTTP200实际上为JS壳；部分Bing结果为空或无关，Yahoo403、DuckDuckGo202挑战均停止，不绕过。随后使用官方sitemap发现署名文章。失败/无关结果不算支持证据。[ACQUISITION_LEDGER.json](model-architecture/ACQUISITION_LEDGER.json)

## 5. 主动反证与五个未知点

- **数据供给不是无限。**Axon明确排除竞争者bid/user数据，Ad Review也明确不供给Axon；不能从中介拥有信息推断训练可用。[MA60S02](model-architecture/SOURCE_CATALOG.md#ma60s02)、[MA60S08](model-architecture/SOURCE_CATALOG.md#ma60s08)
- **购买不等于代理金额。**AppLovin checkout排除IAA和预测LTV；IAP metadata价格、AdWorth/GRT或reward到账不自动构成真实训练收入。[MA60S10](model-architecture/SOURCE_CATALOG.md#ma60s10)、既有53—59号
- **数据用途受门控。**Unity Developer Data的ads_intent默认denied；IAP/Runtime可见接口仍止于gateway/native，不证明训练集接入。[MA60S23](model-architecture/SOURCE_CATALOG.md#ma60s23)、[MA60S24](model-architecture/SOURCE_CATALOG.md#ma60s24)
- **跨游戏用途不等于个人图谱。**V1支持模式/聚合洞察用于bid-time；不证明依赖相同个人ID，也不证明跨游戏shared embedding。AppLovin跨业务受益表述是前瞻，不证明已训练。
- **统计不能跨期升级。**Unity新文章38% IAP观察引自2024-04—2025-02内部比较，不能当2026 Vector模型改进的因果结果；D28 beta也缺完整随机化/成本/置信区间。AppLovin测量文章明确归因/MTA/MMM/增量是不同量。[MA60S17](model-architecture/SOURCE_CATALOG.md#ma60s17)、[MA60S27](model-architecture/SOURCE_CATALOG.md#ma60s27)

五个最关键未知点：①逐行真实收入如何去重/验真/退款/成熟为训练标签；②bid前特征的具体字典、时间水位与合法join；③跨游戏参数迁移、聚合统计和个人级历史各自贡献；④概率/价值输出如何经不确定性、预算、底价/竞价规则成为CPM；⑤这些机制在目标四款实际启用及其增量效果。

## 6. 最有证据支持的两家轮廓

**Axon：**广告主目标＋允许的设备/互动/自愿数据→持续学习的预测系统→对特定广告主的未来展示价值→实时出价；多日价值分布有官方明确陈述。用户表示、训练/feature serving工程有间接线索。**未知：**共享参数/身份实现、具体IAA标签、模型网络与实际出价约束。电商历史购买和未来跨业务受益不得补成手游已部署。

**Vector：**授权SDK/MMP全来源数据＋公开声称的玩家/游戏及跨游戏模式/聚合洞察→收入目标与成熟cohort学习→D7/D28购买/IAA/Hybrid预测→动态出价；有明确训练用途及bid-time用途披露。Gamer AI推断和Bidding Science团队分工有间接线索。**未知：**字段级Runtime/Insights训练映射、个人级join、共享网络与loss、pacing生产实现。

共同机制是按目标价值选择及定价，而非只买最便宜安装；可能差异是公开披露的输入来源、时间窗口和工程分工，**不能由此判断谁掌握更多有效特征或谁模型更准**。四款游戏都缺实际campaign/postback/训练与运营实验，不能声称因两家平台而增长。

## 7. 下一轮优先级与停止点

1. **先61：收入到训练标签。**现有MMP字段只能证明接口，最值得查零收入安装者、退款、重复事件、迟到和成熟窗口的正式契约。没有真实标签定义，无法解释何谓高价值。
2. **再63：价值到报价。**Axon多日价值分布及Vector动态出价已提供明确锚点；重点找官方阈值、频控、预算/时延约束的生产说明，不能以通用乘法公式代替。
3. **再62：跨游戏机制。**V1值得追踪到具体数据字典/授权技术材料，区分共享参数、聚合统计、个人ID和同App跨来源。无进一步公开证据就保留竞争假设。
4. **最后64：四款解释。**只有前述证据与四款实际启用相接，才能从可行机制推进到产品解释；运营因果仍需授权对照。

最值得继续追踪的三个断点及所需材料见[EVIDENCE_GAPS.md](model-architecture/EVIDENCE_GAPS.md)。**本轮止于60号先行结论，不提前制作61—64号最终报告，也不把未知段填成行业通用架构。**
