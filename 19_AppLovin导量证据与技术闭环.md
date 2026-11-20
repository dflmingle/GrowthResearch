# AppLovin 导量证据与技术闭环：本轮结论

2026-11-18。总入口：[14 SDK清单](14_第三方SDK全量清单.md)、[15 MAX/Axon](15_AppLovin_MAX与Axon技术分析.md)、[16 MMP](16_Adjust_AppsFlyer归因与Postback.md)、[17 身份](17_第三方身份图谱技术调查.md)、[18 游戏差分](18_游戏与SDK差分分析.md)。

## 1. 实际给五款导量了吗

**【无法确认】目前没有产品级可靠证据。**既未取得可核验的目标游戏×AppLovin广告记录，也未取得授权MMP归因/partner配置/postback日志。Meow的`applovin_int`枚举、四款MAX/适配器、其他产品Oakever/iKame素材资源路径，都不能完成这个证明。Amaze没有样本。[13](13_AppLovin真实投放证据.md) [AX04](EVIDENCE_INDEX.md#ax04)

**【实际游戏代码证实】**可以证明的是四款具备广告变现、价值事件和MMP客户端链；**【官方 SDK 代码证实】**能还原客户端事件封装、标识字段、队列和公开Axon事件分支；**【官方文档证实】**MMP到AppLovin的后台共享/映射方式可还原。闭环中缺的是**目标游戏实际获客记录、共享开关、事件映射、送达及目标配置**，不是缺一份通用流程图。

## 2. 流量可能来自哪里

**【官方文档证实】**AppLovin公开库存覆盖Puzzle、Match&Sort、Casual&Action、Words&Cards等合作移动游戏，以关卡间和奖励场景的全屏video/playable为重要形式；当前官网称多数库存视频化。tracking macros支持展示应用/placement、campaign、创意集、国家及event ID。[AX02](EVIDENCE_INDEX.md#ax02) [AX05](EVIDENCE_INDEX.md#ax05)

**【无法确认】**五款具体广告在哪个应用、哪个国家、哪天展示；不可由本游戏适配器清单认定流量来自对应网络，也不可由MAX收入倒推AppLovin预算。

## 3. 哪些信号能进入，哪些已证明进入

| 信号 | 平台能力 | 目标游戏实际证据 |
|---|---|---|
| 安装、打开、归因媒体/campaign | 【官方文档证实】MMP tracking与partner共享 | 【实际游戏代码证实】四款MMP入口/结果消费；【无法确认】实际AppLovin安装或送达 |
| 关卡、教程、参与时长 | 【官方文档证实】CPE、postinstall映射；【官方 SDK 代码证实】13.6.4事件表 | 【实际游戏代码证实】部分规则→Adjust/AF；【无法确认】被AppLovin接收或选为目标 |
| 广告展示价值 | 【官方文档证实】MAX与IAA/Blended产品关联；【官方 SDK 代码证实】ILRD及precision | 【实际游戏代码证实】Car/Jewel→Adjust、Rotate→AF等；【无法确认】目标游戏AppLovin侧的IAA配置 |
| 真实内购 | 【官方文档证实】checkout金额及币种 | 客户端IAP接口不等于已发生购买或partner送达 |
| Car国家阈值 | 【实际游戏代码证实】Firebase-only已定位路径 | 【无法确认】AppLovin没有已建立路由 |
| Meow时间窗×活跃/深度 | 【实际游戏代码证实】指定平台GRT行为；收入规则生产配置未知 | 【无法确认】AF共享和选用状态 |
| Rotate国家×安装年龄/收益 | 【实际游戏代码证实】AF/Firebase业务链，标准ILRD独立 | 【无法确认】AppLovin partner和价值字段映射 |
| Jewel AdWorth | 【实际游戏代码证实】90默认规则，Firebase/Meta/Adjust分发；31表不全被引用 | 【无法确认】未证明输出给AppLovin；Meta代理purchase不能当AppLovin真实内购 |

证据：[12 信号矩阵](12_Axon身份与价值优化信号.md)、[TP03–TP05](EVIDENCE_INDEX.md#tp03)、[C03](EVIDENCE_INDEX.md#c03)、[M01](EVIDENCE_INDEX.md#m01)、[R02](EVIDENCE_INDEX.md#r02)、[D01](EVIDENCE_INDEX.md#d01)。

**没有一项目标游戏特有价值事件已取得“AppLovin服务端实际收到并用于优化”的证明。**静态调用、SDK通用发送能力、MMP映射文档是三个不同证据层；本轮没有伪造事件去验证生产端点。

## 4. 身份如何关联

**【实际游戏代码证实】**Meow AdUuid→MAX，Rotate ThinkingData distinctId→MAX，AF CUID与游戏分析ID有单应用链；Car Metica初始化可传MAX用户ID。**【官方 SDK 代码证实】**AppLovin13.6.4具备可选user_data规范化/哈希和设备上下文字段。**【无法确认】**五款联系方式匹配、跨应用合并、相似人群实际建立或商业图谱供应商启用。[17](17_第三方身份图谱技术调查.md)

**【官方文档证实】**AppLovin政策披露跨应用/设备与MMP数据及AI个性化；它没有给出这五款的逐条生产事实，也不能替代受众操作日志。SDK中`Liveramp CMP`、可选UID2或InMobi UnifiedID类存在不等于已用商业图谱。[I08](EVIDENCE_INDEX.md#i08) [AX03](EVIDENCE_INDEX.md#ax03)

## 5. 谁提供了什么

- **【官方 SDK 代码证实】**网络SDK/适配器提供广告载入展示、竞价token接口、收入回调与隐私选项；Adjust/AF提供标识、归因客户端、事件/广告收入包、缓存和任务队列。
- **【实际游戏代码证实】**Zego国家阈值、Learnings/GRT、Hurelax国家安装年龄策略、Bulldog/AdWorth构成额外的业务/框架价值加工层。它们不是MAX或MMP默认统一算法；法律所有权不能单凭类名确定。
- **【官方文档证实】**AppLovin提供竞价/定向/素材选择和IAA/IAP/Blended等优化产品。
- **【无法确认】**Axon训练标签处理、特征权重、预测模型、身份join、反作弊及目标游戏后台预算/ROAS不在已取得客户端证据内。

## 6. 最值得我们实现的部分

**【合理推断 / 建议】**先实现少量可解释的早期行为事件、真实ILRD与精度字段、金额口径和幂等键，再用授权MMP partner配置把正确语义的事件共享给获客平台；广告价值代理与真实IAP严格分开。对国家/安装年龄门槛做自有数据验证和holdout，不照抄其他游戏金额或默认未使用的来源权重。无需先建立跨应用身份图谱。

**【官方文档证实】**尤其不要把AdWorth或预测LTV伪装成AppLovincheckout：当前官方指南明确不接收这类收入。SDK `purchase` API可调用不等于这种业务映射符合平台定义。[AX01](EVIDENCE_INDEX.md#ax01)

## 7. 本轮验证范围

发行包、源码、请求状态、许可证与SHA256见[14](14_第三方SDK全量清单.md)；API比较明确限定为声明匹配。没有修改原包、工程、手机或存档。没有授权后台就无法完成生产闭环证明；新增证据将先从脱敏campaign/归因和postback导出入手，不以继续随机录像或SDK字符串堆砌代替。
