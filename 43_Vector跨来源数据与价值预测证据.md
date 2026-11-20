# Vector：跨来源行为、收入学习与实时出价证据

2026-11-19。**相比“Unity有引擎所以掌握所有玩法”的推断，可靠证据是：玩家/游戏信息的产品用途、明确收入窗口与成熟cohort、MMP接口，以及Vector专属的建模和竞价团队说明。**

## 1. 已直接披露的数据与标签链

Vector页面写game DNA、real player behavior、ecosystem data，并推荐MMP发送attributed/unattributed installs、sessions、purchases、ad revenue及lifetime postback window。**【官方公开证实】**这是明确的数据供给建议与模型用途描述；不表示任意游戏默认开放全部数据。[S12](vector/unity-vector-correct.txt)（原文L10—17） [S13](vector/unity-vector-correct.txt)（原文L34—43）

ROAS文档明确用机器学习预测每位用户收入潜力并动态出价，支持Ad Revenue D0/D7/D28、IAP D7/D28、Hybrid D7/D28。D28当前文档仍有beta标记。D28公告明确预测28天广告收入并按国家tROAS调整报价。**【官方公开证实】**预测目标和反馈窗口，不是无限生命周期LTV，也没有公开逐样本loss。[S14](vector/doc-intro-to-roas-campaigns.txt)（原文L22—27） [S15](vector/doc-intro-to-roas-campaigns.txt)（原文L42—62） [S22](vector/d28-blog.txt)（原文L21—33）

| 学习环节 | 直接证据与限制 |
|---|---|
| 事件关联 | S2S `gamer_id/aid/ifa`、`campaign_id`、广告主`game_id`、`install_ts`、归因标记；可追踪输入接口，不证明实际join成功 |
| 收入语义 | `event=ad_revenue`或`purchase`及amount/currency；session不是收入；对增量或累计需MMP契约明确 |
| 成熟度 | 文档例子D0 1月1日→1月3日成熟，D7→1月10日，D28→1月31日；不能把窗口结束直接视为当时全部数据已到齐 |
| 学习门槛 | IAA 1000归因安装且成熟广告收入>0；D28 IAA当前表使用D7成熟收入；IAP 75位D7成熟付费者；Hybrid 1000安装+正D7广告收入+35位D7付费者 |
| 仍未知 | 内部去重键、退款回滚、事件迟到窗口、归因冲突、截尾/缺失建模及每标签权重 |

[S18](vector/doc-send-postbacks.txt)（原文L28—40） [S19](vector/doc-send-postbacks.txt)（原文L91—109） [S16](vector/doc-intro-to-roas-campaigns.txt)（原文L79—93） [S17](vector/doc-intro-to-roas-campaigns.txt)（原文L97—119）。custom S2S文档关于IDFA等存在历史/接口特定表述，不能据此推翻ATT或认定所有受限iOS请求都有IDFA。

## 2. Runtime与购买服务：两条不同证据

- **【官方公开证实】**Developer Data的collection、usage和end-user intent分别约束使用；`ads_intent=denied`限制广告专用标识及个性化用途，不能把未设置解读为全部广告授权。**【无法确认】**某Runtime事件的native采集→Vector特征/标签完整血缘。[S20](vector/ddf-end-user-consent.txt)（原文L23—39）
- **【官方公开证实】**2026-07-21 Unite Seoul回顾明确IAP SDK/D2C购买数据可丰富Vector寻找未来玩家。它比笼统“引擎数据”更具体，但仍是“can help enrich”，不能升级为四款目标游戏已启用。[S21](vector/unity-2026-keynote.txt)（原文L120—121）

Ads SDK4.17.0的`AndroidStaticDeviceInfoDataSource`、`AndroidPrivacyDeviceInfoDataSource`和shared request可追踪安装ID、LevelPlay AUID、同意与允许的PII。**【SDK代码证实】**请求构造；**【无法确认】**它们如何被转换为Vector安装前表示。[S34](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt)（原文L213—246） [S35](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt)（原文L20—58） [S36](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt)（原文L19—35）

## 3. 本轮新增：明确归属Vector的公开招聘

由Unity官方careers页面SSR发现Workday职位，再读取公开职位详情，未登录或绕过访问限制。原文JSON和`jobPostingInfo.jobDescription`定位随证据图保存；`startDate/postedOn`按原字段保留，不猜首次发布日期。

| 团队/职位 | 原文技术线索 | 可信边界 |
|---|---|---|
| Vector Bidding Science，JOBREQ-2616286 | real-time bidding、bidding/pacing algorithms、bid landscape forecasting、离线/在线A/B；RL/control theory、survival analysis为技能要求 | 【间接技术线索】业务分工和研发范围明确；不能证明已部署强化学习或某种市场价格算法 |
| Vector Gamer AI推断基础设施，JOBREQ-2615964 | 广告排序及bidding决策、低延迟高吞吐online inference；GCP/Kubernetes/Golang/监控，Triton为加分项 | 【间接技术线索】文中陈述生产职责，强于行业猜测；仍未独立验证部署，不能把Triton加分项写成已使用 |
| Vector Ads Modeling，JOBREQ-2616596 | user behavior modeling、rich user data、large-scale compute、research→production | 【间接技术线索】建模方向，未公开Embedding结构或具体跨App表示 |

[S28](prediction-system/unity-job-JOBREQ-2616286-clean.txt)（原文L1—28） [S29](prediction-system/unity-job-JOBREQ-2615964-clean.txt)（原文L1—28） [S30](prediction-system/unity-job-JOBREQ-2616596-clean.txt)（原文L1—28）。本轮将其统一放D级，不因官方发布就升级为生产架构证明。

## 4. 反证与身份隔离边界

UPA明确组织内跨游戏/设备账号；RampID明确美加Unity Exchange受众激活且双方支持。**【官方公开证实】**两项能力；**【无法确认】**UPA→RampID、UPA→Vector、RampID→Vector的训练连接。Exchange的品牌受众激活不等于Vector手游获客模型。[S37](vector/exchange-rampid.txt)（原文L13—30） [S38](identity-graph/unity-player-accounts.txt)（原文L18—29）

## 5. 效果证据不能替代因果拆分

D28公告给出2026-03-08—04-08内部closed-beta的配对D7对照，属于官方匿名化案例方法线索，非本研究独立授权实验：按游戏统计留存和ARPU改善比例；未给完整成本、样本/随机化/置信区间，不能计算统一ROAS，也不能将提升归因于Runtime或身份。[S23](vector/d28-blog.txt)（原文L43—43）

下一条最有价值证据是**带数据字典和用途开关的Runtime/IAP事件→Vector训练集血缘**，同时有“禁用这类特征”的真实消融。再取得一份SDK token字段并不能完成该证明。
