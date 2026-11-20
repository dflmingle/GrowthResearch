# 71号：MAX经济展示与收入关联

2026-11-20。范围：复用70号MAX13.6.4证据，仅为新定位的CommunicatorService定点解析一个类，不重新扫描版本、不运行SDK。

**本轮补齐“响应ID→本地MMP收入广播”的字段级连接，但没有补齐收入账本唯一性或生产MMP消费。另一个重要发现：70号的load内部处理现在可追踪到收入广播，虽然该方法没有调用公共onAdRevenuePaid。** 所有结论是静态能力和官方契约，不是四款游戏的运行记录。

## 新连接及覆盖优先级

```text
完整响应.event_id → 每个候选c3.T()
  ├→ 成功加载赢家跟踪 → 下一请求.previous_loaded_request_id
  ├→ MaxAdWaterfallInfoImpl.eventId → SDK遥测.ad_event_id
  └→ SDK l.u()返回CommunicatorService k
       → k.a(c3): Bundle.id = c3.T()
       → putAll(ad_values)                 [可能覆盖同名键]
       → k.b(c3): putAll(revenue_parameters)[可能再次覆盖同名键]
       → country_code
       → 本地topic=max_revenue_events
       → MMP订阅者                           [实际订阅/转发未知]
```

新代码：L71C01—04、22。[k.java](lineage71/java/com/applovin/impl/sdk/k.java) L177—182、L274—297；`c3.y/S/T`见L71C03。SDK `l.u()`返回类型通过原JAR的javap签名核对，[签名](lineage71/max-sdk-l.signatures.txt)。旧响应/赢家链为CL70C18—27。

关键限制：基础Bundle明确赋值`id=c3.T()`，但两次`putAll`在后，公开代码没有排除服务器下发同名`id`。因此**不能无条件写“广播最终id恒等响应event_id”**。需要服务器schema禁止碰撞，或授权的脱敏配置样本证明该次无覆盖。对`revenue`等键也必须按实际合并顺序解析。

`k.b(topic)`要求功能开关开启，且topic位于配置列表或有订阅者；发布还涉及配置选择的消息保留策略。**本地发布不是网络发送，发布也不证明某MMP已订阅。** 本轮没有分析为MMP自动去重的机制，也没有这种运行证据。

## 一个event_id能对应多少候选

CL70C18—21证明V2路径把同一完整响应传给多个ads条目，每个候选的`T()`读该完整响应。故**可为一对多**；具体数量由响应ads数组决定，本项目没有生产响应，不能报实际数量。赢家记录只表示成功加载/选择，不是已经展示或计费。

AppLovin官方MMP广播文档将`id`定义为“Unique internal ID for the serve”（L71S01），这提供了接口语义，却没有给出数据库唯一约束、候选→展示的基数或重试账本规则。它与“候选共享完整响应ID”的代码并不自动矛盾：候选不等于实际serve；也不能反过来用文案证明每个候选各有一个经济展示ID。

`MaxAdWaterfallInfo`公开接口没有`getEventId`，实现类有该getter（L71C06、CL70C25/26）。不能要求普通集成必然取得该实现字段；也不能因此断言所有其他可配置接口都取不到关联值。

## 五个收入阶段不是五笔收入

| 路径 | 所查触发条件 | 公共onAdRevenuePaid | 本地max_revenue_events | 经济含义边界 |
|---|---|---|---|---|
| raw impression | `revenue_event`后缀mimp | 条件调用 | 经同一`u().b(c3)` | WILL_DISPLAY路径，不是结算证明 |
| viewability | 后缀vimp | 条件调用 | 同上 | 与可见性检测有关，不应新增一笔独立收入 |
| adapter impression | 后缀cimp | 条件调用 | 同上 | 网络适配器展示通知 |
| click | 后缀click | 条件调用 | 同上 | 不能把收入回调统一定时为展示瞬间 |
| load | 后缀load | **所查方法没有** | **现在已追踪到条件发布** | 可早于实际展示；不是已实现经济收入证明 |

证据：CL70C28、37、38和新L71C02；MAX `MediationServiceImpl` L409—465、L596—614、L683—697。70号“load仅内部处理”的结论保留历史，本报告补出该内部调用的本地广播目的地。

对同一个未变化的字符串，这五个不同后缀不能同时成立，因此不能声称每个对象一定产生五次收入回调。但是互斥选择阶段也**不是全局恰好一次契约**：没有证明重复底层回调、重载、消息保留/订阅、S2S/SDK镜像及业务重发都已经济去重。允许存在路径级防重，不以局部未见防重断言整个SDK没有防重。

## 对外经济ID有三套语义，不能按名称拼接

| 接口 | 可证字段 | 可以确认 | 不能确认 |
|---|---|---|---|
| 本地MMP广播 | `id` | 官方serve ID；基础值来自`T()`；有覆盖边界 | 最终值、MMP实际保留、跨接口唯一性 |
| 账户启用的S2S展示收入 | `{EVENT_ID}`、`{EVENT_TOKEN}`、`{TS}`、`{PRECISION}` | 官方独立事件UUID与签名/时间宏契约 | 与SDK `id`/响应event_id相等 |
| 日级非聚合报表 | impression时间、金额、广告位等 | 每展示行；金额USD六位小数；UTC日终8小时后可取 | 所示schema没有强制event ID，不可仅按时间金额无损join |

L71S02：S2S需账户/支持团队开启；GET、可能延迟数分钟、5秒超时、**无重试**。这与客户端g6任务不是同一个产品/传输路径，不能混用重试结论。本轮仅读文档，没有调用收入报表、下载用户数据或验证签名。

官方`EVENT_ID`示例为36字符UUID，广播`id`示例是另一种格式；**示例差异不证明生产永不相等，更不证明存在映射**。当前只能将该边标UNKNOWN。

## MMP桥接与标签风险

Adjust官方示例：同一`MaxAd.getRevenue()`、network、adUnit、placement→`AdjustAdRevenue("applovin_max_sdk")`→`trackAdRevenue`（L71S03）。示例没有传serve ID或precision。新L71C07—10继续证明对象字段如何序列化到`/ad_revenue`及排队；这不是生产送达。

金额精度分级不能抹掉：13.6.4 API注释与现行在线文档对`undefined`的解释不同，按版本保留（L71C05、L71S11）。`exact`仅表示实时竞价结果，**不等于财务已结算净收入**；0可能未就绪，-1错误需按具体接口处理，不能统统作为真实零收入。

最小补证：无真实用户标识的字段字典，说明响应event_id、广播最终id、S2S EVENT_ID、MMP收入事件ID如何映射；去重粒度、迟到/修正规则和precision保留方式。没有这些，不应把任何请求ID当作收入账本主键。

原件、版本、原包SHA256、精确源码行与六层状态见[证据目录](lineage71/SOURCE_CATALOG.md)及[代码证据](lineage71/CODE_EVIDENCE.json)。本轮完成的是客户端条件关联，平台实收与训练列仍UNKNOWN。
