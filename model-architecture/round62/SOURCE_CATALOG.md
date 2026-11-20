# 62号冷启动证据目录

本轮11条限定主张：新增作者/关联发布溯源，复用已核验原文检验A/B/C/D，不能按主张数量解释研究突破。

<a id="ct62s01"></a>
## CT62S01 · Unity / Vector cross-game article authorship

- 原文URL：https://unity.com/blog/d7-vs-d28-iap-roas-campaigns
- 日期：2026-06-25；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[model-architecture/public/unity-d7-d28.txt:L123](../../model-architecture/public/unity-d7-d28.txt)；L123—L130
- SHA256：`9aca03187f001a9cdfcbb4e4386d8e81b66791007dd571e55f90cb68d271688a`
- 短摘录：Senior Content Marketing Manager
- 【官方公开证实】 原文及JSON-LD确认作者Daniel Godley、2026-06-25及内容营销职务；无可见作者工程论文/演讲引用
- 范围：文章身份/证据类型，不否定官方用途声明
- 限制：作者职务本身既不证明技术主张错误，也不使其成为独立部署审计；未发现引用不证明外部材料不存在

<a id="ct62s02"></a>
## CT62S02 · Unity / Cross-game use at bid decision

- 原文URL：https://unity.com/blog/d7-vs-d28-iap-roas-campaigns
- 日期：2026-06-25; cited data period 2024-04 to 2025-02；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[model-architecture/public/unity-d7-d28.txt:L208](../../model-architecture/public/unity-d7-d28.txt)；L208—L223
- SHA256：`9aca03187f001a9cdfcbb4e4386d8e81b66791007dd571e55f90cb68d271688a`
- 短摘录：cross-game behavioral patterns and aggregate cohort insights
- 【官方公开证实】 官方将跨游戏行为模式/聚合cohort洞察与bid-time玩家区分连接；未区分统计、共享参数或个人历史
- 范围：Vector D7/D28 IAP用途；B有明确聚合洞察陈述，C/D未定
- 限制：样本比较来自2024-04至2025-02；不能证明2026模型消融或个人级join，也不能指定embedding

复用原对象：MA60S17；旧记录不变。

<a id="ct62s03"></a>
## CT62S03 · Unity / Linked ROAS onboarding announcement

- 原文URL：https://unity.com/blog/uads-march-updates
- 日期：2026-03-06；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[model-architecture/round62/public/unity-march-linked.txt:L123](../../model-architecture/round62/public/unity-march-linked.txt)；L123—L150
- SHA256：`43db735b820a14c9a06186969b01330c26b99c2adcd745d48ace01406820e188`
- 短摘录：data enablement and validation steps
- 【官方公开证实】 原文章链接的官方发布仍要求数据准备/验证，并保留Learning到Live门槛；简化开户不等于无数据学习
- 范围：2026-03-06 Vector ROAS onboarding，作者Danielle Shevchuk/产品营销
- 限制：不是模型论文，也没有公开B/C/D实现；Homa案例不能补迁移因果

原始HTTP：[model-architecture/round62/public/unity-march-linked.raw](../../model-architecture/round62/public/unity-march-linked.raw)；SHA256 `d8ff3015be7130e59969bd1d997db4c95a01cf25a5306ee2aebdef2fb0343710`。

<a id="ct62s04"></a>
## CT62S04 · Unity / Same-app cross-source prelaunch learning

- 原文URL：https://docs.unity.com/en-us/grow/acquire/campaigns/roas/roas-campaign-best-practices.md
- 日期：2026-03-05；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[vector/doc-roas-campaign-best-practices.txt:L36](../../vector/doc-roas-campaign-best-practices.txt)；L36—L70
- SHA256：`181a6cffe4f8921bda559c2a0cc0571e8d61bf352dc8e400c05b5553ad63955f`
- 短摘录：at least two weeks before you create your new ROAS campaign
- 【官方公开证实】 同目标App可在新活动前提供SDK和未归因事件帮助训练；无需等待这些样本来自本平台付费安装
- 范围：机制A；预启动数据不计入学习退出门槛
- 限制：不等于跨游戏个人数据、模型共享或无自身历史时已能准确预测；非自动历史回填

复用原对象：MA60S14；旧记录不变。

<a id="ct62s05"></a>
## CT62S05 · Unity / No prerequisite install campaign

- 原文URL：https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md
- 日期：2026-05-21；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[vector/doc-intro-to-roas-campaigns.txt:L91](../../vector/doc-intro-to-roas-campaigns.txt)；L91—L95
- SHA256：`dbf6ca7e80360e22e49243ab7ab487dc1d4ce433a15310a1dc8b8160d3b1aa61`
- 短摘录：without first running an Install campaign
- 【官方公开证实】 官方明确可直接启动ROAS不必先跑Install campaign，但仍在Learning收集相关post-install数据
- 范围：新活动/新网络冷启动，不是零数据高精度保证
- 限制：不能取消该文成熟及样本阈值，也不证明全新游戏直接有优质价值识别

<a id="ct62s06"></a>
## CT62S06 · Unity / Unattributed source scope

- 原文URL：https://docs.unity.com/en-us/grow/acquire/partner-integration/attribution/introduction.md
- 日期：2026-11-18；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[model-architecture/round62/public/unity-acquire-attribution.txt:L26](../../model-architecture/round62/public/unity-acquire-attribution.txt)；L26—L36
- SHA256：`07b36ec7e2a866122e265c0308c3861682468b0da1df9e0cb27cafb8341c6083`
- 短摘录：Unity counts organic installs as **Unattributed**
- 【官方公开证实】 此MMP契约的unattributed是目标App来自其他广告网络/自然量，不是跨游戏个人历史的同义词
- 范围：机制A来源分类；不把文章泛称跨游戏数据与该字段自动判等
- 限制：只定义来源；不说明训练样本混合权重或join成功

原始HTTP：[model-architecture/round62/public/unity-acquire-attribution.raw](../../model-architecture/round62/public/unity-acquire-attribution.raw)；SHA256 `64d20fd3e139d358d631d3388d257ee87932a4842cd4d6a6a45ac54de619e973`。

<a id="ct62s07"></a>
## CT62S07 · AppLovin / Axon public training categories

- 原文URL：https://legal.applovin.com/about-applovins-axon-ai/
- 日期：not stated; snapshot date is not publication date；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[nongame/applovin-axon-about.txt:L60](../../nongame/applovin-axon-about.txt)；L60—L73
- SHA256：`450c55b0b8ef263c41d312af1399433984762753c0f70ed5f94722eba5946cd7`
- 短摘录：As more advertisers use our performance-based advertising solutions, the models improve through additional data
- 【官方公开证实】 缓存官方说明称额外广告主数据/洞察改善模型，持续训练使用允许的互动与广告主自愿数据；未披露跨游戏学习契约
- 范围：一般系统级数据学习声明，不特指B/C/D；此次刷新403，使用保留旧官方快照
- 限制：不证明统一权重、跨游戏feature store、每用户历史或新游戏冷启动提升；不获取受限页面

复用原对象：MA60S02；旧记录不变。

<a id="ct62s08"></a>
## CT62S08 · AppLovin / Advertiser-owned all-source sharing

- 原文URL：https://help.adjust.com/en/partner-setup/applovin
- 日期：page date not stated; cached/reviewed 2026-11-19；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[axon/adjust-applovin.txt:L113](../../axon/adjust-applovin.txt)；L113—L127
- SHA256：`95962bafc284b1d3abf4e0db17095e205504d1c737529b85e109ac0c05d72984`
- 短摘录：Data from all attribution sources
- 【官方公开证实】 Axon partner可选择全部来源或只Axon来源，session/revenue/事件映射须配置；最直接支持A可用
- 范围：同一广告主App归因来源；文档说may optimize，不保证某游戏生产学习
- 限制：不是将别的游戏个人行为授权给本游戏；没有明确跨游戏参数/统计/个人特征契约

复用原对象：CGS50；旧记录不变。

<a id="ct62s09"></a>
## CT62S09 · AppLovin / Cross-category prospective gaming benefit

- 原文URL：https://www.applovin.com/en/blog/introducing-applovin-ads
- 日期：2025-10-01; metadata modified 2026-07-15；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[model-architecture/public/al-introducing.txt:L47](../../model-architecture/public/al-introducing.txt)；L47—L50
- SHA256：`da5e38340c85e2fa6b6f17a08fbe11514c7b4b0f512c375006a1e8fafe8df87b`
- 短摘录：the incremental data will materially improve
- 【官方公开证实】 官方预期更多广告主数据将改善游戏伙伴效果；前瞻承诺不等于明确跨游戏共享实现
- 范围：系统增长方向与未来受益，不是游戏个人级轨迹授权
- 限制：will/believe不能升级实际部署；无法区分聚合/参数共享/个人历史贡献

复用原对象：MA60S04；旧记录不变。

<a id="ct62s10"></a>
## CT62S10 · Unity / Developer Data privacy gating

- 原文URL：https://docs.unity.com/en-us/cloud/developer-data-framework/end-user-consent.md
- 日期：not stated; snapshot date is not publication date；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[vector/ddf-end-user-consent.txt:L20](../../vector/ddf-end-user-consent.txt)；L20—L38
- SHA256：`ea304dbc17e8077ee3baf00e01c0294d6bde940a3616d7fb0abc2c1df98b2d31`
- 短摘录：ads_intent = denied
- 【官方公开证实】 Developer Data个性化广告用途及广告专用标识受ads_intent约束；未知状态默认denied
- 范围：排除默认无限收集/训练个人广告历史；不是全部SDK统一闸门
- 限制：无广告ID不证明完全无关联；B/C也需合法训练用途，聚合不能洗白未经授权原始数据

复用原对象：MA60S23；旧记录不变。

<a id="ct62s11"></a>
## CT62S11 · AppLovin / Ad Review data exclusion

- 原文URL：https://www.applovin.com/en/blog/catch-bad-ads-not-data
- 日期：2026-09-16；查阅：2026-11-19T10:48:25.769680+00:00
- 本地：[prediction-system/applovin-excluded-rival-data.txt:L14](../../prediction-system/applovin-excluded-rival-data.txt)；L14—L17
- SHA256：`fd07f9c935dad89f911dd2544760d3c69a50d5b826a13c53a89dd2858ef4b534`
- 短摘录：do not feed it into Axon
- 【官方公开证实】 官方排除Ad Review输出建用户/设备档案或供给Axon；不能用广告审查观察来补跨游戏D
- 范围：特定数据来源/用途排除；不否定允许的广告主收入反馈
- 限制：不排除Axon用其他合法来源的B/C/D；只能否定该来源链

复用原对象：MA60S08；旧记录不变。
