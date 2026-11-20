# MAX 13.2.0 / 13.6.2 / 13.6.3 / 13.6.4 事件协议差分

2026-11-18。使用已取得匹配官方AAR和四款原包，不下载新SDK。以官方JAR反编译+`javap -c -s`和原包DEX方法相互定位，未执行SDK。

## 1. 比较结果

**【官方 SDK 代码证实】**

| 项目 | 13.2.0 / Meow | 13.6.2 / Rotate | 13.6.3 / Jewel | 13.6.4 / Car |
|---|---|---|---|---|
| 旧式`4.0/pix` | 有 | 有 | 有 | 有 |
| 结构化`v1/app` | 所查EventService无 | 有 | 有 | 有 |
| `axon_events`默认表 | 无 | `z4.A0` | `c5.A0` | `c5.B0` |
| 默认结构化事件集合 | 无 | 42名称 | 同13.6.2 | 同13.6.2 |
| 非匹配名称 | 旧式顶层/子事件 | 旧式顶层/子事件 | 同左 | 同左 |
| 结构化`dedupe_id` | 无该分支 | 可选options字段 | 同左 | 同左 |
| 结构化`visitInfo` | 无该分支 | 有 | 有 | 有 |
| 独立可选`AppLovinUserData` | 所查接口无 | 所查接口无 | 所查接口无 | 新增，事件/广告请求可消费 |
| 既有自定义ID→`cuid` | 有 | 有 | 有 | 有 |
| SDK自动landing默认协议 | 旧 | 旧 | 旧 | 旧 |

原始比较表：[protocol-matrix.json](axon/deep/protocol-matrix.json)；官方输入哈希/版本沿用[TP01](EVIDENCE_INDEX.md#tp01)，本轮原包方法位置见[XD01](EVIDENCE_INDEX.md#xd01)、[XD03](EVIDENCE_INDEX.md#xd03)。**只能说明这些已选版本之间的变化，不能声称13.6.2就是Axon协议首次发布。**

## 2. 进入新分支需要什么

**【官方 SDK 代码证实】**三版13.6.x的`EventServiceImpl.trackEvent(String,Map,Map)`顺序为：

1. 名称空：报错/返回，测试或特定SDK条件可抛异常。
2. 查生效`axon_events`集合，名称匹配则走结构化分支。
3. 否则走legacy分支；legacy再根据top_level_events决定顶层event或`postinstall/sub_event`。
4. 结构化分支校验可选`items`必须为List且成员是Map；不合法则记录错误且不提交网络任务。
5. 任务在调度器中执行，构建请求后交持久postback管理器；初始化/URL/尝试次数等还可阻止实际派发。

不是“新版SDK启动就自动上报默认表里的所有事件”。默认表42名称包含关卡/教程、广告机会/查看/点击、经济/购买、社交/账户等；没有业务调用就没有对应游戏事件。默认`landing`与`app_open`也不是同一个名称：前者来自SDK初始化且属于旧式顶层名单，后者只是新表的一项。[XD03](EVIDENCE_INDEX.md#xd03)

**【官方 SDK 代码证实】**`core.c(config)`从SettingsManager读取当前配置，`SettingsManager.a(JSONObject)`可按已注册key更新并保存，列表由逗号拆分。包内表不是生产快照；远端设置可能改分流和字段开关。**【无法确认】**本轮未请求或读取任何用户的在线SDK配置，不能断言实际表仍为默认。[XD07](EVIDENCE_INDEX.md#xd07)

## 3. 载荷与去重

**【官方 SDK 代码证实】**13.6.2/13.6.3的结构化payload有：

- `id/name/data/timestamp`：事件对象生成标识/时间、调用参数。
- `app_info/device_info`：SDK collector快照，`app_info`可按条件含`cuid`。
- `dedupe_id`：只在第三参数options里存在有效可转换值时加入，不是SDK为所有业务自动生成的统一幂等键。
- `axon`：连接事件key、eventId、SDK版本、平台等；其中`visitInfo`取app_info中的首次安装时间、上次启动时间、启动计数及当前启动时间。

13.6.4在此基础上可加独立`user_data`，legacy事件也增加该可选数据分支。`send_user_data`默认true但对象默认未由`setUserIdentifier`创建；需显式传入AppLovinUserData且规范化后有有效内容。广告请求`a6.e(JSONObject)`同样检查配置和对象。[XD03](EVIDENCE_INDEX.md#xd03) [XD07](EVIDENCE_INDEX.md#xd07)

**【无法确认】**字段`dedupe_id`、调试缓存或本地once都不能证明服务端去重、账户匹配成功、事件金额被用作训练标签。客户端能构建某字段不等于广告主后台已授权使用。

## 4. visitInfo与用户ID不是同一回事

**【官方 SDK 代码证实】**`firstVisitTs←ia_v2`、`lastVisitTs←last_launch_ms`、`visitCount←app_launch_count`、`currentVisitStartTs←alts_ms`，表示SDK应用访问上下文，不是游戏关卡时长、玩家实际有效操作分钟或未来LTV。未证明SDK以此生成特定游戏的高价值分层。[XD03](EVIDENCE_INDEX.md#xd03)

`cuid`来自独立用户管理器、受`qq3`控制，持久项受`pui`控制；`user_data`来自另一个对象。它们可以在同一包出现，但设置其中一个不会自动填另一个。详见[21](21_MAX用户ID与身份数据流.md)。

## 5. 队列、磁盘与网络

**【官方 SDK 代码证实】**四版通用链为：事件任务→`network.d`描述请求→`network.b`内存待发/in-flight/待重试集合→PostbackServiceImpl→TaskDispatchPostback→网络执行/回调。`network.c`负责`persistent_postback_cache.json`的pb数组序列化/反序列化；默认持久开关`spp=true`。缓存有上限及重试次数，成功移除、失败等后续调度，不是无限重试。[XD04](EVIDENCE_INDEX.md#xd04)

新版结构化主URL默认由`eete=https://b.applovin.com/`加`v1/app`构成；旧协议默认`https://rt.applovin.com/4.0/pix`及其备用。**本轮只读常量，没有向这些生产URL发送请求。**具体HTTP封装可能按配置处理query/body、编码、压缩和备用端点；逻辑Map不是网络抓包。

本轮将四版网络任务、持久回调、请求类和JVM指令保留为证据。调试`getTrackedAxonEvents`的最多20条deque与持久postback队列是两种结构：前者不能充当送达日志。[XD04](EVIDENCE_INDEX.md#xd04)

## 6. 结构化分支在目标游戏中“可达”到什么程度

| 游戏 | API/分支存在 | 已找到的上游 | 实际业务到v1/app结论 |
|---|---|---|---|
| Car | 是 | 通用MaxUnity与Metica桥；SDK自动事件 | 【无法确认】可从桥传匹配名称，但没有具体游戏行为的已证实调用 |
| Rotate | 是 | SDK自身生命周期/隐私等 | 【无法确认】没有游戏显式名称匹配链 |
| Jewel | 是 | SDK自身；AdWorth另走其他平台 | 【无法确认】未证明AdWorth→MAX；native/热更未知 |
| Meow | 否，所查EventService无此分支 | SDK自动旧事件，GRT另走MMP | 【实际游戏代码证实】不能把本版旧事件写成v1/app直发；不排除MMP服务端向AppLovin回传 |

“有API可达性”不是“运行时业务触发可达性”，更不是“网络成功”。本轮没有对SDK发模拟事件来填补这个缺口。[20](20_Axon实际事件调用链.md)

## 7. 仍不能从客户端恢复的部分

**【无法确认】**实际收到的事件/有效配置、MMP partner postback映射、campaign优化目标、Axon训练标签、身份join、预测模型与预算。公开投放调查也未取得目标游戏的可核验素材/日期/媒体记录；参见[XD08](EVIDENCE_INDEX.md#xd08)。本轮新增的是协议差分和本地数据流证据，不是生产投放证明。
