# 77号：Axon身份图谱工程证据

2026-11-20。**没有取得Axon生产价值模型实际读取跨App或跨设备身份图谱特征的直接工程证据；本轮C_graph升级为零。** 有官方岗位说明用户表示、模型训练/服务和竞价基础设施，也有既有Axon标识/历史行为类别用途披露。这些正证据成立，但没有闭合“解析组件→实际接收产品→价值模型读取”。不据此判断图谱不存在。

## 判定范围与原有起点

沿用74号：A是能力/契约，B是特定产品接收，C_id是标识/历史类别用途，C_graph是具体身份解析结果或关联历史进入指定价值模型，D是固定条件下身份独立增益。75号证明仅观察广告变化不能识别个人图谱；76号本地审计验证了检查时间、权限、实际读取及决策引用的方法，不能当厂商生产日志。

本轮只核对岗位、专利、技术论文/文章及整合架构。未重扫SDK、重搜隐私政策、整理伙伴名单或进行实验；完整矩阵含原URL、日期、摘录、文件哈希、实体粒度及未证环节。

## 最接近的工程线索仍是已有用户表示岗位

S25/MA60S06为同一官方Software Engineer ML岗位4712559006，原文件第7—21行描述user signals、representation learning、ranking、retrieval及从特征开发到production的职责：

> Develop and improve user signals, features, and representations used by large-scale machine learning models for advertising and recommendation.

这明确连接“用户信号/表示研发”与“广告推荐模型职责”，比普通AI宣传具体。但user不提供设备/账号/人/家庭的粒度定义；岗位未指定identity resolver、跨设备join、映射namespace、输入列或Axon价值模型版本。第一方历史、设备内互动、上下文embedding和群体共享参数同样相容。岗位任务也不是某特征已经上线的运行证明。PE77C01明确标REUSED，没有重复下载这份正文。

S26/MA60S07（4716524006）涉及model training、feature serving以及raw ingestion到feature delivery，说明数据基础设施职责，不说明谁做身份解析。不能将两份岗位拼接为“已知图谱通过feature store进入Axon”。

## 本轮两份新增岗位提供了什么

| 新证据 | 原文与具体范围 | 能支持什么 | 不能支持什么 |
|---|---|---|---|
| PE77S01 / PE77C03，ML Infrastructure Engineer 4655740006 | high throughput and low latency to our bidding ecosystem；training、serving、online models | 官方团队描述竞价模型交付基础设施 | 没有解析组件、跨App接收列或Axon专属消费记录 |
| PE77S02 / PE77C04，Data Scientist – Analytics 4705263006 | petabyte-scale datasets across our ad and app ecosystem；模型稳定性/校准评估 | 生态数据分析与模型评估职责 | across ecosystem不等于按个人join，DAU也不定义身份粒度 |

两岗位发布者均为AppLovin官方Greenhouse；API的first_published分别为2026-02-18与2026-08-13，updated_at均为2026-11-05；采集日2026-11-20。日期是招聘元数据，不能回填为架构上线日。原文、完整时间及SHA256见[原始目录](production77/SOURCE_CATALOG.md)。两份是新URL、旧主题的补充，生产图谱结论未升级。

## 专利和整合材料的边界

已有US20130159103A1（S31/MA60S11/12），优先权2011-12-16、公开2013-06-20，Google档案状态为Abandoned。其应用列表→用户profile→广告选择是历史方案；不能当现代Axon图谱部署或价值模型输入。未重复获取，也不从过时实施例推导当前合法可用字段。

本轮AppLovin assignee及identity graph窄查询没有新增相关公报；查询覆盖有限，不证明其他专利不存在。云客户候选页返回soft404，猜测的Adjust收购完成URL404，均未收入技术证据。收购事实即使成立，也不自动给出Adjust身份结果流入Axon价值特征的映射。

既有IV74S09明确Axon广告因素可包含广告ID、设备与互动/购买历史。这是C_id官方用途披露，不因缺少图谱证据而抹去；本轮仅复用范围判断，未重搜隐私材料。广告ID被使用可以只是设备键，不等于自然人跨设备实体或图谱特征。

## Axon剩余断点及结论

尚缺合法可引用的：解析服务/版本、输出namespace及实体粒度、Axon实际接收、特征组与当时available_at、模型版本及实际读取trace。若要证明优势，还要身份开关对照中固定数据量、模型容量和竞价控制器；当前没有D层结果。

因此最强工程线索仍是“用户表示→广告模型研发职责”，新增的是竞价服务及评估职责。**没有生产身份图谱读取证据，没有独立增益证据。** 停止同义搜索；待具体一手架构文档或授权匿名审计包出现再恢复。完整竞争解释见[缺口报告](77_关键证据缺口与竞争解释.md)。
