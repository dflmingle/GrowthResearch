"""Evidence-bounded revenue/distribution and bid-constraint synthesis."""
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent

r61='''# 收入标签与价值分布预测：Axon / Vector

2026-11-19。复用60号MA60原始证据，新增16项更具体的数据/预算契约及静态核验；不重复SDK清单，不修改00—60。**结论：Axon公开承认未来多日价值分布预测，但尚不能证明显式概率分布输出或风险敏感决策；Vector对D7/D28收入目标及反馈窗口更具体，但内部标签构造仍未公开。** 本轮没有恢复生产模型网络、损失函数或训练数据集，也没有目标四款的实际训练记录。

本轮来源/原包/日期/行号/哈希：[RV61目录](model-architecture/round61-63/SOURCE_CATALOG.md)；[原始片段](model-architecture/round61-63/SOURCE_EVIDENCE.json)；全量增量[CLAIM_MATRIX](model-architecture/CLAIM_MATRIX.csv)。旧MA60编号及行保持不变。

## 1. Axon“未来价值分布”可确认到哪一层

| 问题 | 直接证据 | 可证结论与未证边界 |
|---|---|---|
| 预测什么 | CEO原文列ad engagement、CTR、app/site engagement、conversion likelihood、payment probability、purchase size、repeat behavior；随后称“predict expected value distributions many days into the future” | 【官方公开证实】多阶段行为及未来多日价值是官方描述的预测对象。**原段重点是向游戏玩家展示非游戏offer的估值**，不能直接定义成每名安装者的D28 IAA标签。[MA60S01](model-architecture/SOURCE_CATALOG.md#ma60s01) |
| 时间窗口 | 原文many days；手游产品区分IAA/IAP/Blended | 【官方公开证实】多日和产品收入目标；【无法确认】Axon该句的统一D7/D28、是否自然日/滚动天、无限生命周期或任务特定窗口。不能把Unity窗口移植过来。[MA60S09](model-architecture/SOURCE_CATALOG.md#ma60s09)、[RV61S12](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s12) |
| 训练标签 | 设备/互动、自身胜负、广告主自愿数据持续训练；IAP只允许真实支付；MAX与IAA/Blended产品有明确关系 | 【官方公开证实】数据类别、收入语义和训练用途；【无法确认】逐行label定义、经济展示/订单去重、退款回滚、成熟/迟到/汇率/权重。[MA60S02](model-architecture/SOURCE_CATALOG.md#ma60s02)、[MA60S10](model-architecture/SOURCE_CATALOG.md#ma60s10) |
| 是否概率分布 | 原文仅expected value distributions；招聘涉及multi-task/representation | **【无法确认】**无法从复数distributions区分“跨用户/目标的预测价值分布”和“每用户条件概率分布F(R|x)”；没有PDF/PMF、分位数、方差、置信区间、分布参数或proper scoring loss。招聘不补这一层。[MA60S06](model-architecture/SOURCE_CATALOG.md#ma60s06) |
| 是否分阶段预测 | 原文列多个概率/金额对象 | 【官方公开证实】列出了这些预测对象；【无法确认】独立pInstall/pPurchase head、金额条件模型、乘法结构、多任务共享层。可以有多个模型或直接预测最终展示价值 |
| 决策用途 | 原文real-time capital allocation；另有each impression按return goals出价 | 【官方公开证实】价值预测与实时资源/出价用途连接；【无法确认】是否用方差/CVaR/下分位数作风险调整或预算探索。[MA60S01/04](model-architecture/SOURCE_CATALOG.md#ma60s01) |

**为什么可能强调分布？【合理推断】**相同期望可来自大量小额收入或少数大额收入，兑现时间与波动也可能不同；完整分布有能力支持风险和预算决策。但这是解释“分布为何可能有用”的通用理论，**不是Axon披露了以上分布建模、量化了不确定性或已按风险出价**。第3节与H-A表将这种可行性和厂商事实分开。

## 2. Vector D7/D28：目标更具体，样本内部仍未知

【官方公开证实】D7广告收入目标预测安装后7天IAA，D28目标预测28天IAA；IAP目标预测相应窗口购买价值；Hybrid优化组合收入。国家tROAS和campaign类型/窗口可配置，模型根据目标动态竞价。**这是窗口内收入，不是无限期LTV。**[MA60S13/15/16](model-architecture/SOURCE_CATALOG.md#ma60s13)、[ROAS原文](vector/doc-intro-to-roas-campaigns.txt)、[RV61S10](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s10)

| 标签环节 | Vector已证材料 | 精确边界 |
|---|---|---|
| IAA与IAP来源 | 正式post-install契约分purchase/ad_revenue；与session/level_complete分别定义 | 【官方公开证实】收入事件与行为事件分开；不证明每条已接收或用于训练。[RV61S01](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s01) |
| 事件映射 | 非Singular集成须分IAA/IAP，IAA不支持时不能映射purchase；否则优化可能停止工作 | 【官方公开证实】事件语义影响优化；不公开哪个loss或内部标签列。Singular特定配置例外不能推广。[RV61S03/04](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s03) |
| 自然量/其他渠道 | 全来源含organic；预启动至少两周SDK+对应unattributed数据可以帮助训练 | 【官方公开证实】同一广告主跨来源样本与冷启动用途；不能当网络自身付费安装，也不证明全量历史可回填。[MA60S14](model-architecture/SOURCE_CATALOG.md#ma60s14) |
| 成熟窗口 | 文档例子D0 Jan1→Jan3、D7→Jan10、D28→Jan31；D28退出学习门槛使用D7成熟数据 | 【官方公开证实】产品所需成熟期/门槛；不能认定D28模型只用D7标签或D28结果已成熟，亦不能从例子恢复每事件迟到截断。[MA60S15](model-architecture/SOURCE_CATALOG.md#ma60s15) |
| 迟到/数据缺失 | 新取得的post-install文档明确错误集成可导致数据丢失，服务器不能retroactively补发 | 【官方公开证实】该集成下的补数限制；Lifetime窗口不承诺自动回填。**不是证明所有平台技术上不可能backfill，也不是训练迟到水位策略。**[RV61S02](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s02) |
| 反馈使用 | 官方称post-install数据inform models；产品有安装/收入门槛 | 已有训练用途陈述，**没有**完整收入账本→零值补齐→样本权重→loss→更新作业的公开代码 |
| 联合预测 | Hybrid组合收入、IAP/ad behavior correlations | 不等于确认联合loss、单共享模型或独立pPurchase/pAdRevenue头；也不说明按安装条件训练与展示条件训练如何组合 |

## 3. 单用户收入与单次展示价值不是同一变量

**以下仅为研究者独立构造的定义/数学例子，不是Axon或Vector模型。**

- 定义候选标签`Y_h = 窗口h内合资格、去重并按明确会计口径处理的IAA + IAP`。真实落地须另定日历/时区、收入precision、FX、税费、退款和接收水位；本式不替任何平台作这些决定。
- 对安装者的条件价值`E[Y_h | install, x_bid]`和每次展示价值`E[V_h | x_bid]`不同。**仅当所计价值必须经安装产生、且所有相关分支已被恰当处理时**，可用全期望写`E[V_h|x] = P(install|impression,x) × E[Y_h|install,x]`。这不是厂商采用两个head的证据；网站转化/再营销等还可能需要其他路径。
- 原始`Y_h`是观测收入，`预测Y_h`是模型输出；GRT/AdWorth达标或加权value是代理；一个API叫purchase不能改变经济事件真实性。

**合成数学例子：**A有10%概率产生8美元、其余0；B有1%概率产生80美元、其余0。两者安装后期望均0.8美元，但方差分别5.76与63.36。一个只消费均值且风险中性的决策可以给两者相同报价；风险/预算/探索策略也可以区分。**不能由“distributions”推断Axon就是这两点混合、采用该方差或压低B报价。**计算可复核于[math_examples.py](model-architecture/round61-63/math_examples.py)与[结果](model-architecture/round61-63/MATH_EXAMPLES.json)。它只验证算术，不测任何真实平台。

## 4. 零收入、长尾、退款和重复：证据逐层限定

| 问题 | Axon / AppLovin | Vector / Unity | 仍缺的材料 |
|---|---|---|---|
| 零收入玩家 | 全来源安装/打开有共享契约，但不证明零收入label行、negative sampling或缺失补0 | 安装门槛与购买/收入门槛分开，也不等于训练集已补全零值 | canonical install universe、完整性水位、zero vs missing定义及采样权重 |
| 极高值/长尾 | 多日分布措辞没有披露clipping、log变换、零膨胀模型或tail loss | D28覆盖迟付价值，但无尾部处理实现 | 特征/label变换及反变换、截断阈值、校准/尾部检验 |
| 退款/负收入 | IAP语义只接受真实支付，但原文没有给手游训练退款处理 | IAP遥测可含购买多阶段和metadata价格，不能当退款后净收入label | 订单状态/退款/拒付S2S契约、更新版本与训练重算 |
| 负金额SDK边界 | **【SDK代码证实】**独立Adjust5.8.1 `checkRevenue`拒绝负金额赋值，零不被此比较拒绝 | 这是MMP API约束，不能外推成Unity退款不支持 | 不得用`setRevenue(-x)`臆造通用退款链；是否有专用服务端退款契约另查。[RV61S14](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s14) |
| 事件去重 | 网站文档：同事件共享dedupe_id；≤30秒merge，>5分钟后到副本drop；30秒—5分钟未明确 | MMP映射/SDK EventUUID不足以证明训练exactly-once | AppLovin该条只适用于所述网站Pixel/site-to-site/SDK集成，**不套手游IAA/MMP**；需经济展示/订单级统一幂等契约。[RV61S13](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s13) |
| 同一收入多SDK上报 | Rotate已证同double入AFAdRevenueData和ad_revenue2/4；其他游戏有多平台分发 | SDK副本是上报，不是多笔经济收入 | backend收入源优先级、去重键及聚合对账；没有则不能相加。[49号](49_行为价值事件端到端调用链.md) |
| 迟到成熟 | Axon统一窗口/迟到队列未知 | Unity有成熟例子和补发限制，但训练水位、最终标签修订未知 | event_time/available_at/received_at、late watermark与修订表 |
| 未安装机会 | 未公开全机会训练样本与归因失败/负例定义 | CVR术语可见，但训练样本构建未知 | impression universe、view/click链及可观测安装标记/隐私缺失，不只安装者导出 |

**【合理推断】**只看安装者可以研究条件收入，但不能估计全量机会的安装概率，也不能证明真实竞价收益；未观测收入不能直接置0。安装/归因选择及隐私可见性会改变样本分布。两家如何处理这种偏差仍【无法确认】，不能替它们补IPS、反事实学习或延迟反馈算法。

## 5. Axon四个竞争假设：没有唯一胜者

| 假设 | 必要条件 | 支持证据 | 反证/限制与无法区分处 | 下一份关键材料 |
|---|---|---|---|---|
| H-A1 单点LTV | 特征到一个均值/标量；目标窗口/金额口径明确 | 每展示价值/return goal披露与之兼容 | “分布”措辞使纯粹只输出单点的完整系统描述不充分，但均值head/均值竞价可与分布内部表示共存；不能据文案排除A1 | 线上serving输出schema：均值、量纲、预测条件、窗口 |
| H-A2 多阶段概率与金额 | 多阶段标签及概率/金额条件定义，或多模型组合 | CEO明确列CTR、转化/支付概率、购买额/复购 | 列多个对象≠独立heads或乘积；直接预测展示价值也可符合 | 模型图、任务/标签定义及最终输出映射 |
| H-A3 显式分布 | 每机会/用户条件分布参数、分位数或样本，及适当训练目标 | “expected value distributions”是最直接措辞 | distribution也可指跨人群/目标的值分布；未披露PDF/quantile/loss；本轮仍不能证明显式概率输出 | 带随机变量/条件定义的技术论文、serving分布字段和校准 |
| H-A4 分布+风险/预算 | 分布/不确定性输出实际参与risk/预算/探索控制 | 实时资本配置、ROAS/全局预算建议与之相容 | 均值+pacing已可产生同样宏观行为；没有风险阈值、方差/CVaR或uncertainty-use证据 | 预测输出→控制器的生产接口/消融：固定均值改变方差是否改价 |

这些假设可以共存；不能用“资本配置”认定A4，用multi-task招聘认定A2，或从分布一词唯一选A3。完整八假设（含Vector）见[竞争性检验](model-architecture/round61-63/COMPETING_HYPOTHESES.md)。

## 6. 本轮证据进展与搜索上限

**新增辨识力在数据契约和预算行为，不在生产模型网络。**已补具体事件类别/错误映射反证、Unity集成补发限制、网站去重时间范围、独立MMP负收入校验。没有取得Axon条件概率分布/训练loss或Vector零值/长尾/退款标签实现。

直接查官方现有导航和正式文档；旧Unity post-install链接跳向不可访问的内部地址后停止，改用文档新canonical公开路径成功取得；旧IAA/IAP/Hybrid路径失效/跳转不作为反证。AppLovin HTTP200软404明确排除。不再反复同类广搜，不访问生产接口。[获取台账](model-architecture/round61-63/ACQUISITION_LEDGER.json)

下一步优先要**匿名化canonical标签规范（含零值、退款、重复与成熟修订）以及serving输出schema**，而非继续从SDK字段猜测分布架构。
'''

r63='''# 预测价值到实时竞价与预算约束

2026-11-19。**本轮将“按价值动态出价”推进到可核验的国家/预算/探索与交付约束；没有恢复Axon或Vector真实报价公式。**Unity正式预算文档提供的行为比招聘线索更直接，但不等于公开pacing控制器源码；Axon也只能确认产品目标及部分预算建议。收入/分布边界见[61号](61_收入标签与价值分布预测.md)。

四层证据严格区分：①官方明确披露的用途/产品行为；②工程招聘等间接线索；③研究者通用理论/独立数学模型；④厂商内部未知。第一层仍是厂商公开陈述，不是本研究观测生产部署。

## 1. 两家的已证决策链和断点

```mermaid
flowchart LR
 A[合法广告机会/上下文] -->|SDK代码证实 56号 外层构造| C[SDK token/请求]
 C -.->|无法确认 逐字段server join与feature| P[价值预测]
 L[真实安装后收入] -->|官方契约61号 需授权| F[MMP或平台反馈入口]
 F -.->|无法确认 canonical label与训练作业| P
 P -->|官方披露 MA60 Axon价值/Vector D28| D[动态需求侧出价]
 T[国家tROAS/预算] -->|官方用途 RV61S05-12| D
 D -->|协议 RV61S15-16| X[有效性/底价/时限/第一价格]
 X -->|协议及SDK| I[加载后实际展示/计费]
 I -.->|用途已披露 逐条更新未知| P
```

MAX/LevelPlay的媒体变现拍卖、Exchange的DSP接口、Axon/Vector广告主优化是不同层。即使本地看到请求/CPM/胜负，也不能把供给侧价格选择当需求侧LTV模型源码。

## 2. 目标ROAS、国家和预算：哪些已是明确用途

| 环节 | Axon / AppLovin | Vector / Unity | 内部仍未知 |
|---|---|---|---|
| 价值→出价 | 【官方公开证实】对特定广告主的展示价值、return goals、多日价值分布与实时资本配置[MA60S01/02/04](model-architecture/SOURCE_CATALOG.md#ma60s01) | 【官方公开证实】按预测收入和目标ROAS动态竞价；降低目标可提高CPI及量，不能保证达标[原ROAS文档](vector/doc-intro-to-roas-campaigns.txt) | pInstall/LTV是否拆分，系数、目标约束求解、价格上限、收入净额/税费口径 |
| 国家/campaign | 官方建议支持的国家、合乎盈利目标的goal，以及跨国global预算[RV61S12](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s12) | 按国家设ROAS goal，campaign设置类型/窗口/预算/归因[RV61S10](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s10) | 目标游戏配置、国家预算是否改变训练权重或表示、模型选择 |
| 预算层级 | 有global预算和足够目标转化的运营建议，未取得完整Axon控制器说明 | **组织余额为0暂停；campaign/日预算分层；日预算平均目标并throttle**[RV61S05](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s05) | Axon实际pacing；Unity每bid概率门控/乘子/控制频率；不是所有预算硬保证 |
| ROAS自动竞价 | 未取得同口径细则，不能照搬Unity | **CPI计费ROAS活动自动使用Automated bidding**；按日调节/周级补偿，预算改变约7日适应[RV61S07](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s07) | 不能把安装量最大化描述直接套到全部ROAS目标；也不能外推全部计费模式同一控制器 |
| pacing | return goal及预算建议不证明分布风险控制 | **7日滚动预算**，超支/欠支后续补偿，并非严格日cap；国家组实时按赢标/转化分配[RV61S06/09](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s06) | 7日是预算管理窗口，不是D7收入标签；UTC日状态和周级管理不是同一时间概念 |
| 探索/冷启动 | 至少15–20目标转化/日是稳定表现建议，非模型训练阈值[RV61S12](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s12) | 正式文档说探索campaign/creatives，建议campaign预算至少日预算5倍；另有预启动全来源训练[RV61S08](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s08)、MA60S14 | UCB/Thompson/RL、初始模型、exploration rate、分布不确定性是否驱动探索 |

**文档边界和歧义也保留：**Unity budget intro称campaign/day预算可选，而best practices称启用日预算需设置campaign预算；应按实际dashboard/计费条件核对，不能自编统一规则。intro一方面解释达到Daily/Geo Cap暂停，另一方面允许超支；因此“有capped状态”不等于“发票绝不超过目标”。[RV61S05–09](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s05)

## 3. 第一价格、bid shading、频控、时延和不确定性

| 机制 | 层级①官方用途/协议 | 层级②间接线索 | 层级③理论可能性 | 层级④内部未知 |
|---|---|---|---|---|
| 第一价格 | MAX统一拍卖及Unity Exchange公开first-price；有效报价/底价/创意/timeout影响资格[RV61S15/16](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s15) | — | 先过滤再在有效集合选赢家 | 不代表每次Axon/Vector请求都走同一Exchange路径或同一fee/净价算法 |
| bid shading | 无取得两家实际shading算法的直接披露 | Vector岗位bid landscape forecasting、survival analysis方向[MA60S20](model-architecture/SOURCE_CATALOG.md#ma60s20) | 第一价格可优化报价而非总报完整估值 | 不可由第一价格反推已shading；赢标价反馈也不证明Axon摄入竞争者报价 |
| 时延 | Unity Exchange：waterfall seat TMAX最高1000ms，bidding由mediation配置并扣50ms；当次请求预算为准[RV61S16](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s16) | Vector Gamer AI招聘低延迟online inference[MA60S18](model-architecture/SOURCE_CATALOG.md#ma60s18) | timeout下可能少候选或fallback | 该tmax不是Vector模型推断SLA，不能扣完即称模型有950ms；未得线上P99/feature-fetch预算 |
| 频次 | 客户端会话/展示计数和token状态已证；不构成获客频控策略[56号](56_安装前竞价信号与Token血缘.md) | 无能补齐实际策略的新材料 | 可限制用户/广告/时间窗内重复曝光 | 未取得Axon/Vector特定frequency cap、重置键、状态范围或与价值调价的连接 |
| 不确定性 | Axon distributions措辞，无方差/分位数；Vector无本轮取得的显式不确定性决策说明 | 强化学习等岗位技能不够 | 风险折扣、置信下界或探索上界均可 | 没证据唯一选风险厌恶、风险中性、risk-seeking或UCB；A4仍未知 |
| 冷启动fallback | Unity预启动数据/学习阶段与探索资金有文档 | Axon表示研发、Vector建模职责 | population prior/context模型/迁移等 | 没公开新App/新创意/无广告ID时选哪模型、共享哪些权重 |

**第一价格≠第二价；预算pacing≠bid shading；市场价格预测≠玩家LTV预测；时延约束≠某种模型架构。**Axon排除竞争者bid/user数据、Ad Review不入模型的官方边界仍有效；不因为Exchange宏/中介可见性就升级训练用途。[MA60S02/08](model-architecture/SOURCE_CATALOG.md#ma60s02)

## 4. 独立数学候选：只说明可行机制

**本节全部公式、参数和结果均为研究者独立构造，不是Axon/Vector报价公式，也不是平台精度/ROAS实验。**

设一次展示的安装概率为`p`，安装后窗口真实收入条件均值预测为`mu`，目标ROAS为`tau > 0`。在“收入必须经该次可归因安装产生、统一收支口径、忽略费用/退款不确定性”的理想假设下：

`v_impression = p × mu`

`示例可承受CPM = 1000 × p × mu / tau`

它来自期望价值与目标比值，不证明平台真的拆成p和mu。真实系统可直接预测展示价值，也可能有其他转化路径。**`tau`是目标值，不是保证实际ROI；广告主CPI计费、交易所CPM、发布者净ILRD也不是一笔相同的价格。**

合成算例：`p=0.02, mu=$0.80, tau=1.20`，每展示预测价值$0.016，示例CPM上限$13.333。若只有`mu`增至$1.00，同样假设下变$16.667；若目标提高至1.50且mu仍0.80，则降为$10.667。更高估值可能赢更多库存，**不保证真实收入兑现或成本不同比例上涨**。[可运行算术](model-architecture/round61-63/math_examples.py)

**另一个研究者构造的竞价问题：**选择报价`b_i`以最大化一段时间内`sum(P(win|b_i,x_i) × E[value|x_i])`，同时满足总期望花费≤预算、目标ROAS和资格/时限/频次约束。第一价格简化支出可写`P(win|b_i,x_i) × b_i/1000`，但真实费用、计费及结算口径另定。这个候选问题能容纳shading/pacing/探索，**并不能证明两家实际求解它或具有某种risk项**。

均值相同而尾部不同的两个分布可得到相同风险中性估值；要证明H-A4，必须看到“固定均值改变不确定性→实际改价”的授权生产接口或对照，不可从宏观预算平滑反推风险模型。

## 5. Vector四个竞争假设

| 假设 | 必要条件 | 支持证据 | 反证/无法区分处 | 下一份关键材料 |
|---|---|---|---|---|
| H-V1 同游戏历史学习 | 同广告主App收入/安装/事件，时间与来源明确 | 预启动unattributed/organic/跨渠道共享帮助训练是直接官方用途MA60S14 | 支持V1存在，不说明它足以解释全部表现；无标签数据集/权重 | 同App训练样本字典和cold-start holdout |
| H-V2 跨游戏聚合统计迁移 | 跨游戏分组/统计/合法用途契约；不必个人级ID | MA60S17明确cross-game patterns和aggregate cohort insights用于bid-time | supports用途而非实施公式；无法区分只统计迁移、参数共享或二者 | cohort/聚合表schema、覆盖、时间和禁用统计消融 |
| H-V3 跨游戏共享表示 | 跨游戏共享参数/embedding/训练任务/应用条件 | 玩家/游戏关联文案、rich data建模岗位与之相容 | **无直接生产共享网络证据**；V2或单游戏条件模型也能符合文案 | 模型图、共享层/版本和跨游戏迁移消融 |
| H-V4 合法个人级历史关联 | 允许跨应用作用域的标识/授权join、事件时序、门控、特征路径 | 合法广告ID/受限PII及跨游戏行为用途与之相容 | 同包ID不等于匹配；AppInstance/AppSet/账号scope不同；aggregate机制不需要个人图谱；未证该特征进入Vector | 去标识数据血缘、join作用域与匹配质量、禁用个人历史对照及隐私fallback |

V1—V4可能共存。**当前证据不能唯一选择V2/V3/V4，也不能声称个人图谱是Vector优势前提。**同游戏跨来源、共享统计、共享参数和共享个人历史分别记录；不把Unity链条推成Axon实现。[完整八假设](model-architecture/round61-63/COMPETING_HYPOTHESES.md)

## 6. 如何区分数据优势、模型优势和出价策略优势

| 候选优势 | 能辨识的对照 | 不能代替的证据 |
|---|---|---|
| 数据覆盖/质量 | 同一模型版本、出价策略和机会集合，仅合法输入/标签完整性变化；按国家/隐私覆盖/成熟cohort分层 | SDK字段数量、全来源开关存在或更多下载量 |
| 模型 | 固定数据快照/可用时间、任务、机会/验证集/预算，用不同模型做时间外校准、tail/Top-value识别与授权在线对照 | 招聘、参数量营销、预测目标更长、Beta ARPU增加 |
| 出价/预算策略 | 固定预测分数与库存/预算，比较控制器；记录价格、win/timeout、花费时间/国家分配和成熟回报 | 仅看到ROAS改善或国家预算被重新分配 |
| 库存/预算/素材 | 固定上述因素，分层或随机测试素材、市场组合/边际库存 | 增加预算后总收入涨或均值ROAS变化 |
| 归因口径 | 独立收支对账并固定窗口、来源、成熟度；有条件做随机/地域holdout | 归因报表变好不能单独证明新增现金利润 |

这些为【合理推断/实验设计】，本轮未取得真实机会日志/选择概率或实验授权，不报告因果增益、模型准确率或真实平台ROAS。官方测量文章自身也区分归因/MTA/MMM/增量[MA60S27](model-architecture/SOURCE_CATALOG.md#ma60s27)。

## 7. 不改玩法也能越过盈亏线的最有力解释

**【合理推断】**游戏玩法决定部分价值，但获客买到谁、付什么价、收入如何兑现及归因怎么计量也会改变单位经济。更完整的真实收入反馈、较长目标窗口、合法历史样本、对高价值机会更好排序，或预算移向更合适的国家/时段/素材，均可能在玩法不变时改变买入cohort的真实LTV与CPI。若原来接近盈亏线，有限改善足以改变贡献符号。

独立合成例：同口径净D28 LTV=$0.54、CPI=$0.60、其他变动成本暂设0，贡献-$0.06。玩法不变而用户选择使净LTV=$0.66且CPI仍$0.60，或LTV仍$0.54但CPI=$0.48，都会变+$0.06。**只是会计可能性，不是这四款或任何平台实测收益。**更高预测也可能只是过估导致涨价；扩量后的边际人群更贵/价值更低，可能使效果消失。

MAX/LevelPlay提高同类用户的填充/eCPM/展示收益属于变现改善，需与买来更高LTV玩家分开。前后切SDK、换目标、换素材/国家和加预算同时发生的报表，不能区分原因。

四款已有收入/代理事件可提供合法可配置的反馈入口，但Car的Firebase-only阈值、Meow GRT线上规则、Rotate多路收入去重和Jewel AdWorth代理均有断点，不能直接称Axon/Vector输入；也没有新的独立投放/增长因果证据。[49号](49_行为价值事件端到端调用链.md)、[58号](58_Axon_Vector完整买量反馈闭环.md)

## 8. 当前结论与三个真正值得追的断点

1. **标签：**真实IAA/IAP经济事件→去重/验真/退款/零值/成熟标签。最小材料是canonical label规范＋授权脱敏MMP投递与收入cohort对账，不能只给SDK字段。
2. **分布/表示：**Axon serving输出究竟是均值、多个条件预测还是显式分布；Vector跨游戏模式究竟来自统计、共享参数还是合法个人历史。最小材料是官方模型/特征schema及真正消融，不是更多产品介绍。
3. **控制器/效果：**输出如何经预算、风险、探索/频控/时延成为报价；固定分数后的策略对照才能区分模型与出价改善。最小材料是授权决策日志/控制器契约和同预算成熟收益实验。

本轮没有新增生产模型架构、风险调价或bid-shading实现证据；**有新增正式预算/事件契约，所以将“pacing只有招聘线索”收窄为“Unity已有部分行为公开，但具体实现仍未知”**。旧报告保持当时证据状态，不覆盖原文；关系图新增补充边并保留未知边。
'''

h='''# 八个架构假设的竞争性检验（61＋63增量）

这些假设可能共存；支持用途≠唯一识别生产架构。下表引用旧MA60或本轮RV61证据，不覆盖60号假设文件。

| 假设 | 必要数据/实现 | 当前支持 | 反证或限制 | 无法区分 | 下一份关键材料 |
|---|---|---|---|---|---|
| H-A1 单点LTV | 标量预测、单位/窗口/条件清楚 | MA60S01/02/04的预期价值、目标出价可兼容 | distributions使纯单点完整叙述不够，但不是对均值输出的否定 | 内部显式分布也可能只把均值给bidder | 线上输出schema及消费字段 |
| H-A2 多阶段概率与金额 | 每阶段标签/概率、条件金额及组合 | MA60S01列互动、转化、支付、金额、重复行为 | 列多对象不证明独立head/乘积，多任务招聘非部署 | 多模型、直接价值回归、联合模型均可能 | 模型图、任务/标签定义和映射 |
| H-A3 显式分布 | 条件概率分布/参数/quantile/采样及训练目标 | MA60S01 expected value distributions | 原文无随机变量/条件/分布参数；可泛指人群值分布 | 标量集合与每用户概率分布无法区分 | 分布输出和校准、loss定义 |
| H-A4 分布加风险/预算 | 分布/方差等被策略消费，有预算/效用约束 | 实时资本配置和RV61S12预算建议兼容 | 均值+pacing也解释宏观行为；无risk-use公开接口 | 是否风险中性、折扣或探索不可定 | 固定均值、改变不确定性的授权策略对照 |
| H-V1 同游戏历史 | 同App全来源安装/收入与可用时间 | MA60S14明确预启动训练用途 | 不说明所有流量/目标游戏实际启用或权重 | 可与V2/3/4并存 | 同App训练数据字典/来源holdout |
| H-V2 聚合迁移 | cohort特征/聚合统计及作用域 | MA60S17直接披露bid-time aggregate cohort insights/cross-game patterns | 无具体表/聚合隐私/覆盖与增量 | 统计共享可以没有个人级ID | 表schema及禁用聚合消融 |
| H-V3 共享表示 | 跨游戏共享参数/表示/任务及训练 | MA60S17/21和Modeling职位兼容 | 无部署网络/embedding证据 | V2或每游戏条件模型同样符合文案 | 共享层模型图、参数迁移消融 |
| H-V4 合法个人历史 | 标识作用域/权限、跨App join和安装前水位 | SDK受限标识和cross-game用途兼容 | 没有join结果与特征血缘；aggregate不需要个人图谱 | 设备级/账号级/统计级混合未能区分 | 授权去标识join血缘、隐私fallback及特征消融 |

可证明同游戏跨来源学习，并不证明跨游戏个人历史；可证明聚合数据用途，也不证明共享参数。以上对Axon和Vector分别成立，不能相互补证。
'''

readme='''# 61＋63增量证据

交付：[61收入标签与分布](../../61_收入标签与价值分布预测.md)、[63价值到竞价与预算](../../63_预测价值到实时竞价与预算约束.md)。

- SOURCE_CATALOG.md / SOURCE_EVIDENCE.json：16项原文/源码的精确位置、哈希、日期及限制。
- COMPETING_HYPOTHESES.md：Axon四项＋Vector四项，不唯一选模。
- ACQUISITION_LEDGER.json / public/：官方文档GET与失败/软404记录，不执行广告API。
- CLAIM_MATRIX.before.csv：更新前28行原始矩阵；主矩阵只追加本轮16行。
- EVIDENCE_GRAPH.before.json / after.json：旧对象不变；新增边只补充证据层级，不升级生产观察。
- math_examples.py / MATH_EXAMPLES.json：仅研究者独立数学算例，不是厂商算法或真实效果。
- VALIDATION.json：引用/哈希/历史对象/数学算术核验，不证明线上模型。

无新SDK下载、无SDK执行、无生产广告/转化事件、无真实用户标识。保留00—60、prediction-validation和全部旧证据；不制作62/64最终报告。
'''

for p,body in [(R/'61_收入标签与价值分布预测.md',r61),(R/'63_预测价值到实时竞价与预算约束.md',r63),
                (O/'COMPETING_HYPOTHESES.md',h),(O/'README.md',readme)]:
    if p.exists():raise FileExistsError(p)
    p.write_text(body,encoding='utf-8')
print('Reports61/63 and eight-hypothesis comparison written; no historical reports changed.')
