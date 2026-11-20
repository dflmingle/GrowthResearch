# 71号：Unity机会ID与事件关联

2026-11-20。复用Unity Ads4.17.0完整源码链及70号4.18.1所选消费者核验，不重复下载或扫描版本。

**本轮进一步确认：operative事件构造时把当时的机会ID、trackingToken写入请求，之后持久化的是序列化请求；刷新AdObject的token，不会在所查路径中回写已经持久化的旧事件。** 这解释了客户端如何保留历史事件关联，但没有揭开原始竞价Token的服务端映射、服务器如何解析旧token或Vector训练消费。

## 各ID的生成、作用域和限制

| 标识 | 已证来源/作用域 | 能关联到哪一步 | 不能据此证明 |
|---|---|---|---|
| HeaderBiddingToken.tokenId/tokenNumber | Token构造/缓存阶段；CGS01/02 | 请求信号与其Token上下文 | 与加载UUID相等、已解码用户特征 |
| biddingAdId | MAX Unity适配器每次load新UUID；CL70C01/02 | 写load/show共同objectId | 已在原始拍卖前存在 |
| objectId→impressionOpportunityId | load读选项、UUID转ByteString；CL70C03—07 | 请求/config、AdObject、show检索 | 全局经济展示唯一性 |
| trackingToken | gateway响应提供，AdObject可变字段；CL70C08/14 | 当前广告事件携带当时token | 服务器不可变主键、永久版本映射 |
| operative eventId | 每次事件构造独立生成；L71C16 | 一个已构造请求及其持久化重试 | 一次经济展示恰好只有一个事件 |
| workId | observer另生成UUID；L71C18 | 存储键与后台工作项 | 用户ID、广告机会ID或服务端ACK |

“展示前可用”不一定“原竞价前可用”。这里的加载UUID和HB配置响应，在适配器已经取得bid response之后才出现。不能把后来的收入、trackingToken或加载结果倒灌成获取该广告机会时的已知特征。

## token刷新前后的事件

```text
AdObject(opportunity=O, trackingToken=T1)
  → GetOperativeEventApi读当前值
  → request(eventId=E1, opportunity=O, token=T1)
  → SharedFlow → UniversalRequest → bytes(workId=W1)

viewer.updateTrackingToken(T2) → AdObject.token=T2
  → 后续request(eventId=E2, opportunity=O, token=T2)

W1重试 → parse已存bytes → 仍为E1/O/T1 [所查路径]
```

L71C15/21/16：`AdObject.opportunityId`为`val`，token为`var`；API把当前ByteString传到protobuf构造器，生成新eventId。L71C17/18：repository传递构造完的request；observer保存`fullRequest.toByteArray()`，不保存可变AdObject引用。L71C19：后台工作读取旧bytes并parse后交sender，没有重新读取AdObject.token。

所以可证的是**所查持久化重试路径保留构造时的token值**；不能承诺所有并发先后、其他分支或服务器保存方式一致。回调时间、operative构造时间、外层envelope时间、网络发送时间、服务端接收时间仍是不同的时间。

## 队列不是无损账本，工作成功不等于接收成功

`OperativeEventRepository`采用SharedFlow、`DROP_OLDEST`和`tryEmit`（L71C17），不是无条件无损传输。observer只启动一次，但缓冲、生命周期、持久化失败和fallback仍有边界。

`UniversalRequestJob`在sender正常返回后删除存储项；CL70C17的sender对TTL过期直接返回，对GatewayException也可停止发送。因此工作项成功或被删除，不能升级为事件已经被收入服务或训练系统接收。真实网络发送/接收/训练状态均UNKNOWN。

原始竞价Token→markup/configurationToken→加载机会的服务端join仍止于opaque数据；本轮不解析生产token、不访问服务端接口。要推进，需要发布者给出版本化映射schema及一对多、刷新、重载、过期语义。

## opportunityId有多强的唯一性

70号代码证明加载时UUID合法性和当前仓库重复机会检查；L71C15证明对象内字段不变。`AndroidAdRepository`是本地map，完成后会移除（CL70C11；原源码可追溯）。这些只能支持**客户端加载实例/生命周期关联**，不能证明跨重启全局去重、服务器经济唯一约束或永久保留。

一个机会可产生多个eventId和多个token版本；事件ID不是玩家身份，也不是自动的收入账本主键。

## 展示、点击、完成、奖励、收入分开

L71C20的`ShowEvent`明确定义Started、Clicked、ReceivedReward、Completed和Error等变体。它证明客户端生命周期不同，**不证明每个变体都对应一个独立公开网络事件或金额字段**。

CL70C12的viewer `sendOperativeEvent`接收事件类型及base64 additionalData；L71C16可见外发事件对象包含eventId、eventType、impressionOpportunityId、trackingToken、additionalData、可选sid，以及设备/会话/活动上下文。additionalData仍不透明，不能从其存在推断真实收入。

奖励发放是游戏权益，观看完成是广告生命周期；两者都不自动等于IAA金额。IAP购买和Unity Analytics/Insights是其他事件及传输链，53—55号已标明用途断点；本轮没有发现它们与Ads operative eventId的明确赋值契约，不能按同厂商或字段同名连接。

## postback与训练边界

广告主MMP的`ad_revenue`/`purchase` postback，和流量侧Unity Ads operative事件不是同一条流。Unity官方说明前者用于ROAS等优化，并要求正确配置（L71S08、CGS42/44/46/48）；这不能证明某operative事件直接成为收入标签。

目前可直接核验：客户端机会→事件快照→持久化传输路径。未知：原竞价Token映射、旧token服务器处理、经济展示与收入去重、归因安装join、训练列和后续出价效果。需要授权的字段字典/消费血缘，无须提供真实个人标识或模型权重。

来源和原包哈希：[代码证据](lineage71/CODE_EVIDENCE.json)、[复用证据](lineage71/REUSED_EVIDENCE.json)、[端到端关系图](71_端到端训练反馈关系图.json)。
