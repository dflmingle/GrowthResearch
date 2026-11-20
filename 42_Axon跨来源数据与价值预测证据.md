# Axon：跨来源数据、用户表示与价值预测

2026-11-19。**已证“允许的数据类别→预测用途→价值出价”；仍缺“哪条历史→哪一用户表示→哪个训练样本”的内部血缘。**证据关系图A01—A20。

## 1. 官方直接确认的训练输入及边界

Axon官方说明明确使用设备/网络信息、App/广告/其他数字属性互动、伙伴共享数据、广告主自愿共享用户数据，以及自身收到的MAX赢/输标通知；持续训练优化并按特定广告主价值决定出价。隐私政策还披露跨App/设备信息收集与结合、过去App或网站行为用于广告相关性。**【官方公开证实】**这是模型用途层证据，超过“仅收集SDK字段”，但没有列出每个具体feature及join键。[S01](nongame/applovin-axon-about.txt)（原文L58—73） [S02](nongame/applovin-axon-about.txt)（原文L54—60） [S03](nongame/applovin-axon-about.txt)（原文L72—73） [S04](nongame/applovin-policy-direct.txt)（原文L124—138）

**反面边界有明确新证据。**2026-09-16 Adam Foroughi的官方文章直接写：Ad Review不据此建立用户/设备档案，不把该数据输入Axon或其他AppLovin模型；其他网络的广告输出不用于其训练，并移除用户级journey展示。Axon说明另排除其他bidder的出价/用户数据、敏感信息、受保护类别和儿童数据。**【官方明确排除】**不能因MAX能看到候选/广告审查信息，便认定Axon学习了全行业用户级广告输出。该排除针对来源和用途；不否定广告主合法授权的实际广告收入反馈。[S24](prediction-system/applovin-excluded-rival-data.txt)（原文L14—17） [S01](nongame/applovin-axon-about.txt)（原文L58—73）

## 2. 身份与历史关联：可证到哪一层

| 层 | 原始依据 | 判定 |
|---|---|---|
| 获取标识 | MAX13.6.4 `sdk.m.a(Map,boolean)`、`t7` | 【SDK代码证实】GAID、AppSet、CUID分别受可用性/配置约束；Android字段名idfa/idfv不能当苹果标识 |
| 同一请求共封装 | collector与CUID manager | 【SDK代码证实】可构成关联输入，不证明后台已join；AppSet和发行商ID受作用域限制 |
| 过去跨属性行为→模型总体用途 | Axon说明、隐私政策 | 【官方公开证实】类别用途；具体来源集合、历史长度、跨设备置信度未披露 |
| 用户表示→Axon特征表 | ML招聘 | 【间接技术线索】有工程方向，缺实际部署/数据血缘 |
| 电商身份+订单→高价值新客 | 订单历史官方指南 | 【官方公开证实】电商客户建模；不能跨成手游IAA模型默认训练 |

[S32](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java)（原文L1328—1366） [S33](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/t7.java)（原文L1—96） [S04](nongame/applovin-policy-direct.txt)（原文L124—138） [S11](nongame/doc-order-history.txt)（原文L13—26）。详细Pixel/CAPI静态路径复用[31号](31_AppLovin设备身份图谱.md)，本轮不重跑身份采集。

## 3. 本轮新增：用户表示和特征基础设施招聘

公开Greenhouse API取得45条职位，官方原始JSON保存在[prediction-system/applovin-public-jobs.raw](prediction-system/applovin-public-jobs.raw)，职位更新时间均按API字段记录，不能当初次发布日期。

| 职位/原始定位 | 实际文字 | 可得结论与禁止推断 |
|---|---|---|
| Software Engineer, Machine Learning；`jobs[id=4712559006].content` | user signals、representation learning、ranking/retrieval、embeddings、feature interaction、multi-task learning、离线/在线增量实验 | 【间接技术线索】广告平台研究方向；没有明确Axon模型名称/版本，不证明某种Embedding生产部署 |
| ML Data Infrastructure Engineer；`4716524006` | model training and feature serving、从raw ingestion到feature delivery、reproducibility/traceability；Spark/Flink及feature store为技能项 | 【间接技术线索】团队职责包含训练/服务数据链；不能据此写已采用某厂牌feature store或训练频率 |
| Measurement Data Scientist；`4705264006` | platform/3rd-party/internal attribution、MMM/MTA/incrementality/RCT/GeoLift | 【间接技术线索】存在测量需求；不证明当前投放报告都经过增量校正 |

[S25](prediction-system/applovin-job-4712559006-clean.txt)（原文L6—21） [S26](prediction-system/applovin-job-4716524006-clean.txt)（原文L8—23） [S27](prediction-system/applovin-job-4705264006-clean.txt)（原文L8—23）。更新时间2026-11-05；本次公开获取2026-11-19。

## 4. 真实收入与代理价值不能混用

MAX `onAdRevenuePaid()`提供金额与precision：`exact`来自实时拍卖，`estimated`、`publisher_defined`质量不同，不能统称最终财务结算收入。官方支持ILRD共享给MMP，Ad ROAS产品要求live app、MAX、MMP、素材和目标。**【SDK/API证实】【官方公开证实】**由此能支持IAA价值优化产品链；**【无法确认】**具体ILRD行进入何训练表、窗口、loss、退款/无效流量回溯及数据缺失处理。[S05](axon/gaming-apps.txt)（原文L71—80） [S06](axon/max-ilrd.txt)（原文L124—147） [S07](axon/max-ilrd.txt)（原文L188—201）

IAP指南只接受用户真实支付；明确排除广告收入、预测收入和预测LTV。Adjust/AF需要伙伴共享、来源范围、事件映射，AF指南中的checkout不能拿来装IAA或GRT/AdWorth代理金额。**MMP接收某事件≠AppLovin收到≠已用于训练。**[S08](axon/doc-in-app-purchase-revenue-sharing.txt)（原文L14—28） [S09](axon/doc-adjust.txt)（原文L39—73） [S10](axon/doc-appsflyer.txt)（原文L177—224）

## 5. 专利、论文与工程文章的证据上限

取得US20130159103A1 *Advertisement Selection Based on Mobile Applications*：优先权2011-12-16、公开2013-06-20，发明人Adam Foroughi、John Krystynak、Andrew Karam、Furqan Rydhan、Matthew Bornski。文中描述已安装App列表、特征及使用级别辅助广告选择。**【专利间接线索】**只是早期构想，不证明现代Axon调用安装列表，也不能覆盖现代权限限制。Google Patents页面标注Abandoned并声明法律状态非法律结论；本报告不作法律有效性判断。[S31](prediction-system/applovin-historical-patent.txt)（原文L387—398）

没有取得可明确归属现代Axon的生产模型论文/技术会议完整实现。已有ESMM/MMoE等[公开论文](ltv/fetches-model-literature.json)只能提供行业路线，不可归属Axon。公开招聘把表示学习作为方向，也不能补成论文中的MMoE具体架构。

## 6. 目标游戏与下一条关键证据

四款游戏的MAX变现、MMP收入链及本地价值规则已有静态证据；仍未建立“具体游戏价值规则→MAX EventService→结构化Axon”的显式业务链，也未取得伙伴postback送达/训练用途日志。**【无法确认】**这不否定服务器集成，却禁止把游戏规则图直接连到Axon训练。[S39](20_Axon实际事件调用链.md)（原文L8—15） [S40](10_买量优化机制最终对比.md)（原文L9—17）

最值得获取：**经授权、脱敏且带字段血缘的MMP/MAX收入→Axon训练用途说明或技术案例**，同时给出安装前特征时间、水位及幂等规则。仅增加SDK字段无法补这个断点。
