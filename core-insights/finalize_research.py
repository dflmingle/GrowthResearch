"""Write reports and append evidence without upgrading old unknown edges."""
from pathlib import Path
import json, hashlib, datetime, re, copy

R=Path(__file__).resolve().parent.parent
O=R/'core-insights'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p): return json.loads(p.read_text('utf-8'))
def put(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
sources=load(O/'CODE_EVIDENCE.json')
S={s['id']:s for s in sources}
BASE_SOURCES={s['id']:s for s in load(O/'EVIDENCE_GRAPH.before53.json')['sources']}
packages=load(O/'PACKAGE_PROVENANCE.json')
proto=load(O/'PROTOCOL_SCHEMA.json')
def cite(n):
    k=f'C53S{n:02d}'
    return f'[{k}](core-insights/CODE_CATALOG.md#{k.lower()})'

report53=f'''# Unity Core 身份提供者与生命周期

2026-11-19。新增官方 Core 1.19.0 并验过 registry SHA1 与本地 SHA256。复用 Analytics 6.3.0、IAP 5.5.1、Authentication 3.9.0；未安装到任何游戏或读取实际 ID。[原包及来源](core-insights/PACKAGE_PROVENANCE.json)、[{len(sources)}段源码定位及哈希](core-insights/CODE_CATALOG.md)。

## 结论与适用版本

【SDK代码证实】**两个安装接口是不同实现；新安装可通过显式复制得到同值，已有安装不保证同值。ExternalUserId 在满足编译条件时是真正的引擎 userId 桥；PlayerId 则由 Authentication 注册，并非 Core 自动生成的设备 ID。** 以下全部是独立 SDK 的条件化实现证据，不是四款目标游戏已使用这些版本、生产实际同值或跨应用身份的证明。

IAP 5.5.1 与 Authentication 3.9.0 的 package.json 都依赖 Core 1.19.0；Analytics 6.3.0 声明 Core 1.16.0。把三者与 Core 1.19.0 对照说明接口兼容下的调用关系，不能声称所有 Analytics 6.3.0 工程都会解析到 1.19.0，也没有观察目标工程锁文件或实际运行。包依赖见[原包记录](core-insights/PACKAGE_PROVENANCE.json)。

## 提供者、注册、优先级

| 接口 | 实际实现与注册 | 值来源、存储与消费者 |
|---|---|---|
| IInstallationId | CorePackageInitializer 初始化 InstallationId 并注册该实例 | 先读 PlayerPrefs `UnityInstallationId`；非空直接返回；否则读注入的 EngineInstallationId 并复制保存；仅当该值为空，才考虑 legacy Analytics、legacy Ads、GUID。Analytics6.3 IdentityManager 消费此接口 |
| IEngineInstallationId | 独立 EngineInstallationId 实例；同时注入 InstallationId | 有 `ENABLE_UNITY_CLOUD_IDENTIFIERS` 时调用 `Identifiers.installationId`；否则读 `unity_connect.installation_id`，为空则生成 GUID 保存。IAP CoreRegistryHelper 消费的是这个接口 |
| IExternalUserId | Core 注册 ExternalUserId 包装器 | getter 与事件代理到同一个 `UnityServices.ExternalUserIdProperty`；值来自开发者输入或兼容初始化选项；新引擎分支代理 Identifiers.userId |
| IPlayerId | Authentication 初始化并注册 PlayerIdComponent | 从项目/profile作用域缓存读取；登录完成后由解码 access token 的 Subject 赋值。Analytics/IAP 都可读取，缺少包时不能假定存在 |

初始化先创建安装提供者，随后获取项目配置，最后在初始化成功时注册服务组件。更换环境/初始化选项的 `FreeOptionsDependantComponents` 不清空安装提供者。证据：{cite(1)}、{cite(2)}、{cite(3)}、{cite(4)}、{cite(6)}、{cite(12)}、{cite(16)}。

### 不同接口何时同值

以下为**源码分支推导**，A/B/E是符号，不是真实标识，也不是设备实验。

| 已有 UnityInstallationId | Engine 返回值 | Analytics 安装ID | IAP 安装ID | 能否建立等号 |
|---|---|---|---|---|
| 空 | 非空 E | 首次复制 E 并保存 | E | 该次初始化条件下同源/同值，之后需存储和引擎值均未变化 |
| A | B | A，提前返回 | B | 不保证相等；没有强制同步或覆盖旧 A |
| A | 空 | A | 空/缺失 | 不相等，不应以旧 A 填充为已证行为 |
| 空 | 空 | legacy Analytics，次选 Ads，最后 GUID | 空 | 只是 fallback；不得将其当通常新安装分支 |

`InstallationId.CreateIdentifier` 中 legacy `unity.cloud_userid` 和 `unityads-idfi` 的写回发生在 engine 为空的后续分支。engine 非空时在写入 `UnityInstallationId` 后就返回，**不会继续把值写给两个 legacy SDK**。fallback EngineImplementation 正常会生成非空 GUID，所以不能把 legacy 桥画成所有新安装必经路径。{cite(2)}、{cite(3)}、{cite(9)}、{cite(10)}。

这补充了48号原先的“未核实提供者”，也找到了此前旧 `unity.cloud_userid` 问题的条件式读写桥。**不是**发现所有 Unity Ads、新 Analytics 与 Core 始终共享 ID。

## ExternalUserId 的真实生命周期

【SDK代码证实】同时满足 `ENABLE_UNITY_CLOUD_IDENTIFIERS` 和 `UNITY_SUPPORTS_IDENTIFIERS_USER_ID` 才使用引擎分支；否则是内存字段。版本定义精确为：

- `[6000.0.78f1,6000.1.0a1)`
- `[6000.3.18f1,6000.4.0a1)`
- `[6000.5.2f1,6000.6.0a1)`
- `6000.6.0a8` 及按 Unity versionDefine 规则满足该下界的版本

还要满足平台引擎符号；不能简化成“6000.6以上才有”，也不能仅凭版本认定所有平台启用。{cite(5)}、{cite(7)}。

引擎分支 getter/setter 均代理 `Identifiers.userId`；监听引擎 userIdChanged 再通知消费者。公开绑定把 null 归一为空串，超过1024字符抛错，相同值不再次通知。Core 静态重置时移除旧订阅、重建包装器；fallback Dispose 清内存值；引擎分支 Dispose 不清除原生 userId。新分支跨会话持久性由 Core 注释和公开引擎绑定明确说明；原生存储位置、卸载/备份恢复后的行为与跨设备同步不可见。{cite(5)}、{cite(8)}、{cite(36)}。

初始化兼容项 `com.unity.services.core.analytics-user-id` 只在 ExternalUserId 为空时写入。它是开发者命名空间输入，不是 Auth PlayerId 的自动别名。原始位置 `CorePackageInitializer.InitializeExternalUserId`:L255—272，见{cite(54)}。

## PlayerId、存储和重置

【SDK代码证实】Authentication 的缓存键前缀为 `CloudProjectId.Profile.unity.services.authentication.`，其中 `player_id` 保存服务器返回的 token Subject。SignOut 默认保留该 PlayerId；`SignOut(true)` 才清除凭据和玩家ID；登出状态切 profile 会 Refresh 对应缓存。因此“退出登录后还带 PlayerId”并不自动说明匿名追踪绕过，必须核对调用选项及业务实现。{cite(13)}、{cite(14)}、{cite(15)}、{cite(16)}。

| 维度 | 源码可证范围 | 仍不能证明 |
|---|---|---|
| 应用/安装 | fallback安装键在当前应用 PlayerPrefs；Android旧Ads键在当前 Activity 的 MODE_PRIVATE SharedPreferences | 一个全设备/全发行商统一ID；卸载重装必然重新生成（备份恢复需另证） |
| 项目/环境 | 安装键本身不带项目/环境；Auth缓存显式带项目/profile；Analytics collect URL带项目/环境 | 同工程换项目就自动重置所有安装ID；组织级跨项目Auth合并 |
| 账号 | PlayerId来自Auth Subject；ExternalUserId由开发者设置 | 两者相等或自动账号绑定；第三方身份提供者与Unity广告用户的服务器join |
| 内存/磁盘/原生 | 两个fallback安装类各有内存缓存及不同磁盘键；新引擎 getter到 extern | 原生 installationId 的生成/重置算法、后端跨设备解析 |

Android存储证据：{cite(11)}。这些安装类没有公开的“统一清除全部身份”方法；源码也没有跟随广告拒绝而删除安装键的路径。此处仅描述提供者，不据此下隐私合规结论。

## Analytics 与 IAP 实际消费者

Analytics6.3：`IInstallationId → IdentityManager.InstallId`；`UserId = 非空ExternalId，否则InstallId`；PlayerId独立动态读取。IAP5.5.1：`IEngineInstallationId → PlayerData → Insights.UnityIdentities.UnityInstallationId`；ExternalUserId、PlayerId各自独立字段。{cite(17)}、{cite(18)}、{cite(20)}、{cite(21)}、{cite(24)}。

Analytics标准事件额外写 installationID/unityPlayerID；所有这两种构造路径共用 userID/sessionID/eventUUID 头。**不能把标准事件的身份字段自动写成每个 custom event 都有。** {cite(19)}。

同一默认 CoreRegistry、同一个具体 provider、同一个读取时刻，才能依据 getter 建立“读取相同提供者”的条件结论。IAP helper 用 CoreRegistry.Instance，Analytics 的 Initialize 接收 registry 参数；多实例、异步读值、运行中改ID均要求另核对。没有实测值，不写“运行时已验证相等”。

## 五级证据核验与终点

| 层级 | 本轮结论 |
|---|---|
| 相同接口类型 | 两SDK的ExternalUserId/PlayerId接口相同；安装接口不同 |
| 相同提供者实现 | 默认注册路径下的具体实现已定位；安装实现分别是InstallationId与EngineInstallationId |
| 相同底层存储 | ExternalUserId新分支确实代理同一原生API；两个fallback安装键不同；有条件复制，不是同一键 |
| 相同运行时返回值 | 未采集；只证明明确初态下的分支推导，不是任意生产状态 |
| 相同跨应用身份 | 未证实。应用私有存储与项目/profile命名空间不能自动升级为跨App图谱 |

【无法确认】原生标识存储/重置细节、生产SDK解析版本、目标游戏实际设置、服务器ID命名空间与join。继续验证需要对应构建的锁文件/编译符号、开发者授权的匿名化提供者测试，以及服务端身份映射契约；无需也不应收集真实用户标识。
'''

report54=f'''# Unity Insights 事件协议与接收边界

2026-11-19。独立 IAP5.5.1 官方包，SHA256 `{packages['IAP']['sha256']}`。Core1.19与Analytics6.3消费者已对照，所有证据为静态；没有初始化SDK或发生产请求。[原包](core-insights/PACKAGE_PROVENANCE.json)、[代码目录](core-insights/CODE_CATALOG.md)。

## 可证实的数据链

【SDK代码证实】购买生命周期→商店服务override→PurchaseEventEmitter→PlayerData→DTO→protobuf writer→**编译时二选一**：HTTP gateway，或 `EngineDiagnostics.LogEvent(1000, base64)`。本轮终点是公开 C#→native 接口或 SDK 的 HTTP 请求构造；没有生产送达、服务端接收或训练血缘证据。{cite(22)}、{cite(23)}、{cite(24)}、{cite(25)}、{cite(44)}。

```mermaid
flowchart LR
 BUY[SDK购买阶段] -->|SDK代码| EM[PurchaseEventEmitter]
 AUTH[Authentication SignedIn] -->|条件订阅 SDK代码| SE[SessionEventEmitter]
 IDS[Core及可选Firebase身份] -->|读取与门控代码| EM
 EM -->|DTO与writer| PB[protobuf IAPSDKEvent]
 SE -->|相同writer与Forward| PB
 PB -->|编译条件不满足| GW[HTTP gateway请求构造]
 PB -->|两个编译符号满足| NAT[base64 LogEvent 类型1000]
 GW -.->|未观察生产送达| SERVER[Unity接收与内部处理]
 NAT -.->|原生队列及网络实现未知| SERVER
 SERVER -.->|事件级血缘未知| V[Vector训练集]
```

实线仅代表可读源码连接；虚线为未证生产或内部连接。官方泛化用途与某个字段实际用于训练分开。

## 协议版本与完整字段边界

【SDK代码证实】Gateway设置 `Content-Type/Accept: application/x-protobuf`，`X-Tenant: iapSdk`，`X-Schema-Name: insights.producers.iapsdk.v1alpha1.IAPSDKEvent`，`X-Schema-Version: 1`，`X-Proto-Sdk-Version: 1`，`X-SDK-Release-Version: IAPVersion.Current`。schema namespace的v1alpha1、schema版本、SDK版本、Unity版本均不是Vector模型版本。{cite(23)}。

原包没有注释提到的 `Schemas~/.../*.proto` 文件。本报告与[PROTOCOL_SCHEMA.json](core-insights/PROTOCOL_SCHEMA.json)是**依据实际writer及DTO恢复的发送侧描述**，没有声称取得规范原始proto、服务器reserved/options或接收端校验规则。以下覆盖全部已见68处字段写入（其中oneof分支另列）及Timestamp的2个内层字段。{cite(25)}—{cite(27)}、{cite(47)}—{cite(52)}。

### IAPSDKEvent 顶层

| tag | 字段 | 类型与语义 |
|---|---|---|
| 1 | Timestamp | protobuf.Timestamp；BuildEnvelope时的UTC，不是支付平台结算时间 |
| 2 | EventUuid | string；每次BuildEnvelope新GUID，非玩家ID |
| 3 | SessionId | string；IAP读取unity_connect.session_id |
| 4 | FirebaseSessionId | string；允许时读取Firebase Analytics session |
| 5 / 6 | ProjectId / EnvironmentId | string；Core项目/环境 |
| 7 / 8 | IapSdkVersion / EngineVersion | string；组件版本，不是模型版本 |
| 9 / 10 | AdsIntent / AnalyticsIntent | ConsentState enum；显式转换，不照抄UnityConsent枚举序号 |
| 11 | UnityIdentities | PlayerIdentity message |
| 12 | DeviceInfo | DeviceInfo message |
| 13 | Reporting | Reporting message |
| 14 | InstallationTimestamp | Timestamp；Android firstInstallTime；iOS目录创建时间近似 |
| 15 | Store | Store enum |
| 16 | Order | OrderData message |
| 17 / 18 / 19 / 20 | intent / paid / failed / fulfilled | oneof：空message / StorePayload / failure / StorePayload |
| 21 | ApplicationVersion | string；应用版本 |
| 22 / 23 | auth complete / payment options shown | oneof：空message / options message |
| 24 | ImpressionId | string；**购买旅程ID**，见下文 |
| 100 | FirebaseAppId | string；Firebase application配置ID，不是用户ID |
| 101 | InstallMode | string；Android store/dev_release/adhoc/enterprise/editor等映射，其他平台缺省 |

### 所有嵌套message字段

| message | tag→字段（发送侧类型） |
|---|---|
| PlayerIdentity | 1 UnityInstallationId；2 PlayerId；3 UserId；4 AnalyticsId；5 Idfa；6 Gaid；7 Idfv；8 UnityAdsIdfi；9 AppInstanceId；均string |
| DeviceInfo | 1 SystemLanguage string；2 LocaleList repeated string；3 Model string；4 SystemBootTime string；5 OsVersion string；6 TotalSpace uint64 |
| Reporting | 1 Platform string；2 AppBundleId string |
| OrderData | 1 Sku message；2 StoreTransactionId string |
| Sku | 1 SkuId string；2 ProductType enum；3 LocalizedTitle string；4 LocalizedDescription string；5 LocalizedPriceString string；6 PriceMicro int64可空；7 IsoCurrencyCode string；8 Quantity int64；9 CatalogListingId string；10 UnitySku string |
| paid/fulfilled的StorePayload | oneof：1 AppStorePayload；2 GooglePlayPayload |
| AppStorePayload | 1 AppReceipt；2 JwsRepresentation；3 OriginalTransactionId；4 AppAccountToken，均string；5 OwnershipType enum |
| GooglePlayPayload | 1 OriginalJson string；2 Signature string |
| PurchaseFailed | 1 FailureReason enum；2 FailureMessage string |
| PaymentOptionsShown | 1 OptionsShown repeated enum（writer逐项unpacked写，包含0）；2 OptionsDefaultProvider string |
| Timestamp | 1 seconds int64；2 nanos int32；.NET ticks×100并不代表时钟有纳秒精度 |

完整enum编号如下，来自发行包DTO，不由字段名称推测：
'''
for name, values in proto['enums'].items():
    report54 += '\n- `'+name+'`：'+'；'.join(f'{k}={v}' for k,v in values.items())+'。\n'
report54+=f'''
除nullable消息/可空PriceMicro及重复enum的特定写法，writer按proto3省略空字符串、默认0和未设置对象；线型仅0(varint)/2(LEN)。6个事件variant互斥；`DataCollectionMode`虽有枚举定义，没有在该顶层writer中序列化。`UnityAdsIdfi`虽有tag8，`MapIdentity`未赋值；源码注释的“Runtime可补”不是已证原生赋值。{cite(24)}、{cite(25)}、{cite(47)}。

## 触发、时间、价格及重复计收风险

| 事件 | 实际SDK触发 | 价值含义 |
|---|---|---|
| intent | Purchase入口→服务override→SendPurchaseIntentStartEvent | 意图；可带商品metadata，不能视为购买收入 |
| paid | PendingOrder→SendPurchasePaidEvent | 支付阶段报告；仍需验单/折扣/退款与去重口径 |
| fulfilled | ConfirmedOrder→SendPurchaseFulfilledEvent | 完成/履约阶段；与paid可能同交易，不能加算第二笔收入 |
| failed | FailedOrder→SendPurchaseFailedEvent | 失败；带价格不代表成交 |
| auth complete | IapCoreInitializeCallback在Auth可用时订阅SignedIn→SessionEventEmitter | 无Store/Order的会话事件，不是仅存在默认事件表中的名称 |
| options shown | PaymentOptionProvider/UITK→SendPaymentOptionsShownEvent | 显示支付选项；不是支付 |

已追踪 GooglePlay 服务与 PurchaseService SDK调用；目标四款游戏是否实际使用5.5.1未证。登录链是本轮新补齐的实际SDK调用，而不是仅schema能力。`IAP_UNITY_AUTH_ENABLED`还受包版本编译条件影响。{cite(22)}、{cite(30)}、{cite(31)}、{cite(34)}、{cite(44)}、{cite(55)}。支付选项调用位置：`Runtime/Purchasing/PaymentOption/PaymentOptionProvider.cs`:L137，`PaymentOptionProviderUITK.cs`:L135（同一IAP原包）。

`BuildSku` 读取所选catalog listing的metadata，`PriceMicro=(long)(localizedPrice×1_000_000m)`，Quantity独立。它没有读取最终税后净额、折扣成交额、退款后收入或预测LTV。事件timestamp在异步取身份**之后**构建，不能当作精确原始点击/商店支付时间。安装时间Android来自PackageInfo.firstInstallTime毫秒转UTC；iOS来自persistentDataPath创建时间，是平台近似。{cite(24)}、{cite(45)}。

**ImpressionId重要纠正：**这里是`ImpressionScope.Shared`基于AsyncLocal的购买旅程GUID。Enter/EnterOrJoin/EnterOutcome/EnterNone限制它在购买链、结果回调、并发操作之间传播；native/UI回调可失去它，fulfilled默认取身份时也未传入旅程ID。它不是MAX/Unity Ads展示ID，更不是跨App用户ID。{cite(32)}、{cite(22)}。订单ID、EventUuid、ImpressionId分别标记订单、事件和购买旅程，不能彼此替代去重。

## 同意、远程允许列表与包要求

【SDK代码证实】广告同意不是整个PurchaseEmitter的总开关。只有AdsIntent为Granted才进入GAID/IDFA/Firebase可选读取分支；还需`ConnectionsSettingsClient.attributeOverride`对应Boolean true。缓存未就绪、缺项目/安装ID、请求失败时fail-closed不读取对应标识；下一次缓存miss可重试配置请求。Apple IDFV在源码中独立读取，不能声称与GAID使用完全同一门控。{cite(21)}、{cite(28)}。

配置请求带projectId、**IEngineInstallationId**、platform、appVersion、editorVersion、sdkVersion。session级共享allowlist有generation复位；Firebase值另有PlayerData实例内缓存。这是采集门控，不是实时模型配置，不证明生产allowlist内容。{cite(20)}、{cite(28)}。

【官方公开证实】IAP隐私说明（2026-11-05）明确：购买事件为运营服务需要，不因consent状态停发；ads consent影响广告及Firebase标识；数据用于IAP服务、交易去重与Dashboard收入报表。文档也说明6000.7+可经Insights模块。{cite(40)}。

IAP声明RequiresInsights的版本门槛是`6000.7.0a7`，并要求`ENABLE_CLOUD_SERVICES_ENGINE_DIAGNOSTICS`。公开Attribute契约明确：包级requirement可在项目Engine Diagnostics设置关闭时仍保留模块并启用该包所需采集；不支持的平台不生效。**项目诊断开关、SDK包级采集要求、广告ID同意是不同层控制。** 这不证明该游戏的构建状态。{cite(33)}、{cite(34)}、{cite(37)}。

## 两条接收路径与ACK边界

| 路径 | 最后可见实现 | 无法继续证明的部分 |
|---|---|---|
| Gateway | UnityWebRequest POST `https://prd.insights.analytics.unity3d.com/v1/ingest/producer`，protobuf及版本头，completed仅Dispose | 此wrapper无响应成功判断、事件级ACK、持久队列/重试；不能证明生产送达或exactly-once。底层HTTP内部行为不在此wrapper中恢复 |
| Runtime | 同一protobuf→Convert.ToBase64String→EngineDiagnostics.LogEvent(1000,...)，默认immediate=false | native原生队列、封装/补字段、重试、过滤、上传、ACK不可见；不把注释当实际接收实现 |

6000.6公开绑定虽有LogEvent/IsEventAllowed，但IAP5.5.1的新ForwardModule分支仍受6000.7.0a7条件限制。6000.7固定提交额外可见native推送blocked event types、managed helper及thread-safe LogEvent；IAP wrapper没有调用`IsEventAllowed/IsInitialized`，不能把managed capture hook的过滤自动解释成这个IAP调用已在C#层过滤。{cite(23)}、{cite(35)}、{cite(39)}。

UUID旁注“重试需保持相同”不是已实现重试证据；不同BuildEnvelope会生成新UUID。ConnectionsSettings的“失败后下次读取重取”仅属于配置请求，不能借给事件传输。UGS Analytics Buffer/Dispatcher是另一条路径，不能拿其缓存和ACK实现填补IAP缺口。

## Insights与Vector：明确连接及断点

【官方公开证实】2026-07-21 Unity keynote说D2C及IAP SDK采集的购买数据“can help enrich Unity Vector models to find future players”。原句：[S21本地位置](vector/unity-2026-keynote.txt):L120、[官方页面](https://unity.com/blog/unite-seoul-keynote-2026-recap)。这证明官方公开的产品用途关联，**没有识别该protobuf生产者、字段、授权项目、处理后标签、训练任务或实际覆盖率**。

【无法确认】`Insights ingest/LogEvent → 服务端标准化 → 身份join → 去重/退款 → Vector feature/label` 的逐事件血缘；也未证IAP全部默认数据跨业务用于广告训练。IAP隐私页面证实的运营/报表用途不能替代这条证据。研究已到公开客户端末端，停止靠“Insights/Vector/身份字段”命名猜测模型。

进一步只接受授权且匿名化的：生产build/schema路由、接收ACK与payload映射、package requirement/同意配置快照、identity join契约、交易去重及退款规则、训练dataset列血缘/成熟窗口，以及特征或标签消融。无需生产测试事件，也不需要真实用户标识。
'''

# Field-level lineage: each row retains provider, conditions, wire and limits.
rows=[]
def row(field, origin, provider, condition, consumer, serial, transport, receiver, purpose, unknown, ids, scope, request=True):
    rows.append(dict(field=field,field_source=origin,provider=provider,read_conditions=condition,
        consumer_sdk=consumer,serialization=serial,transport_module=transport,known_receiver=receiver,
        proven_use=purpose,unproven_use=unknown,source_ids=ids,scope=scope,
        evidence_records=[dict(id=i,path=(S.get(i) or BASE_SOURCES[i])['path'],sha256=(S.get(i) or BASE_SOURCES[i])['sha256'],
            version=(S.get(i) or BASE_SOURCES[i]).get('version'),start_line=(S.get(i) or BASE_SOURCES[i]).get('start_line'),
            end_line=(S.get(i) or BASE_SOURCES[i]).get('end_line'),
            official_package=(S.get(i) or BASE_SOURCES[i]).get('official_package')) for i in ids],
        package_provenance=[packages[k] for k in ('Core','IAP','Analytics','Authentication') if any(S.get(i,{}).get('sdk')==k for i in ids)],
        privacy_conditions=condition,six_layers=dict(sdk_capability=True,actual_game_business_callsite=False,
            request_construction_code=request,production_successful_send=False,server_received=False,server_model_training=False),
        evidence_level='【SDK代码证实】',production_status='not observed; false means unproven, not proven absence'))
T='IAP Forward: compile-time gateway protobuf POST or base64 native LogEvent(1000)'
RX='Unity Insights gateway address or native EngineDiagnostics API; production receipt unobserved'
U='Server join/training use and target-game production enablement unknown'
row('UGS installation identity','PlayerPrefs UnityInstallationId; copy engine only if local empty','InstallationId:IInstallationId','Core initialized; existing-key priority','Analytics6.3.0','IdentityManager.InstallId; standard installationID; fallback userID','Analytics buffer/dispatcher','project/environment collect URL','Single-app installation fallback for analytics',U,['C53S01','C53S02','C53S17','C53S18','C53S19'],'application local; key not project-prefixed')
row('Engine installation identity','Identifiers.installationId OR unity_connect.installation_id GUID','EngineInstallationId:IEngineInstallationId','platform compile branch; Core component available','IAP5.5.1','UnityIdentities[11].UnityInstallationId[1]',T,RX,'Install context in IAP telemetry',U,['C53S03','C53S20','C53S21','C53S24','C53S25'],'engine per-game install; native storage/reset unknown')
row('External developer user ID','UnityServices.ExternalUserId / native Identifiers.userId / compatibility option','ExternalUserId:IExternalUserId','native branch requires both symbols; fallback memory','Analytics6.3.0 + IAP5.5.1','Analytics userID preferred; IAP identities[11].UserId[3]','Analytics dispatcher or '+T,'Analytics collect / '+RX,'Explicit developer identity input',U,['C53S05','C53S06','C53S07','C53S08','C53S18','C53S20','C53S24','C53S25'],'developer-controlled namespace; not automatic account graph')
row('UGS PlayerId','Auth cache then decoded access token Subject','Authentication PlayerIdComponent:IPlayerId','Authentication package/component present; profile and credentials state','Analytics6.3.0 + IAP5.5.1','Analytics standard unityPlayerID; IAP identities[11].PlayerId[2]','Analytics dispatcher or '+T,'Analytics collect / '+RX,'Project/profile player context',U,['C53S12','C53S13','C53S14','C53S15','C53S16','C53S19','C53S20','C53S24','C53S25'],'project+profile cache; not organization-wide automatic identity')
row('Analytics UserId read by IAP','AnalyticsService.Instance.GetAnalyticsUserID','IdentityManager external-first, installation fallback','Analytics symbols and service initialized; failure optional null','IAP5.5.1','identities[11].AnalyticsId[4]',T,RX,'Common envelope with separate Auth/engine IDs',U,['C53S18','C53S53','C53S24','C53S25'],'analytics logical user; may differ from both installation IDs')
row('GAID','GoogleAdvertisingIdClient getter','Android advertising ID provider','AdsIntent granted AND remote gaid allowlist; platform/provider privacy limits','IAP5.5.1','identities[11].Gaid[6]',T,RX,'Optional advertising-ID context',U,['C53S21','C53S25','C53S28'],'advertising identity; reset/permission limited')
row('IDFA','native Apple FetchAdvertisingIdentifier','Apple store native provider','AdsIntent granted AND remote idfa allowlist; ATT/provider return constraints','IAP5.5.1','identities[11].Idfa[5]',T,RX,'Optional advertising-ID context',U,['C53S21','C53S25','C53S28'],'Apple advertising ID, not IDFV')
row('IDFV','native Apple FetchVendorIdentifier','Apple vendor provider','Apple platform; independent of the AdsIntent conditional in this source','IAP5.5.1','identities[11].Idfv[7]',T,RX,'Vendor identity context',U,['C53S21','C53S25'],'vendor-scoped identity, not account/global device')
row('Firebase Analytics App Instance ID','FirebaseAnalytics.getAppInstanceId','FirebaseAnalyticsClient','AdsIntent granted AND remote app_instance_id AND Firebase available','IAP5.5.1','identities[11].AppInstanceId[9]',T,RX,'Optional Analytics-instance correlation context',U,['C53S21','C53S28','C53S29','C53S25'],'Firebase Analytics installation/instance scope; not FID')
row('Firebase Analytics Session ID','FirebaseAnalytics.getSessionId','FirebaseAnalyticsClient; PlayerData caches non-null','AdsIntent granted AND remote firebase_session_id; configured/default app conditions','IAP5.5.1','IAPSDKEvent.FirebaseSessionId[4]',T,RX,'Optional analytics-session context; 5.5.1 serialization fix',U,['C53S21','C53S29','C53S25','C53S42'],'session, not persistent user')
row('Firebase App ID','FirebaseApp options getApplicationId','FirebaseAnalyticsClient','AdsIntent granted AND remote firebase_app_id AND provider available','IAP5.5.1','IAPSDKEvent.FirebaseAppId[100]',T,RX,'Firebase application configuration context',U,['C53S21','C53S29','C53S25'],'application/project ID, not person')
row('Firebase FID','FirebaseInstallations.getId (ConfigFetchHandler L256/278)','FirebaseInstallations consumed by RemoteConfig','RC fetch prerequisites/FID token/provider privacy state','Firebase Remote Config24.0.1','ConfigFetchHttpClient INSTANCE_ID; no IAP FID assignment proven','Firebase RC HTTP fetch','Firebase RC endpoint','Configuration fetch installation context','FID=Analytics AppInstanceId or IAP FID/Vector path unproven',['XS24','XS25'],'Firebase installation identity, not Analytics instance identity')
row('Unity IAP SessionId','PlayerPrefs unity_connect.session_id','PlayerData m_SessionId','Preference available; absent allowed','IAP5.5.1','IAPSDKEvent.SessionId[3]',T,RX,'Runtime session context','Who writes native session key, equality with Analytics/Firebase session, training use unknown',['C53S53','C53S25'],'engine session preference; not player/installation')
row('UGS Analytics SessionId','SessionManager.StartNewSession Guid.NewGuid','Analytics SessionManager','new manager/session lifecycle','Analytics6.3.0','common sessionID','Analytics buffer/dispatcher','project/environment collect URL','Analytics session grouping',U,['C53S43','C53S19'],'independent generated session, no equality to IAP session')
row('IAP EventUuid','BuildEnvelope Guid.NewGuid','PurchaseEventEmitter / SessionEventEmitter','each envelope build, including lifecycle variants','IAP5.5.1','IAPSDKEvent.EventUuid[2]',T,RX,'Individual telemetry event identifier','server dedup/exactly-once, equivalence across re-built envelopes not proven',['C53S24','C53S25','C53S30'],'one event, not user or transaction')
row('Analytics Event UUID','BufferSystemCalls.GenerateGuid per event start','BufferX','Record event path and collection consent','Analytics6.3.0','common eventUUID','Analytics buffer/dispatcher','project/environment collect URL','Individual analytics event identity','Same ID as IAP event or production dedup not proven',['C53S19'],'one analytics event')
row('IAP ImpressionId','ImpressionScope AsyncLocal Journey Guid.NewGuid','ImpressionScope.Shared','journey active; callback/EnterNone may clear; fulfilled does not pass it by default','IAP5.5.1','IAPSDKEvent.ImpressionId[24]',T,RX,'Purchase journey correlation','Not advertising impression ID; not identity graph; backend success unknown',['C53S32','C53S22','C53S24','C53S25'],'purchase journey, not person or ad request')
row('UnityAdsIdfi schema field','DTO field only; MapIdentity does not assign','No established IAP emitter provider','Writer would emit if nonempty, but this business path does not populate it','IAP5.5.1','identities[11].UnityAdsIdfi[8] supported, normally absent here','No proven field movement via this emitter','Unknown actual receiver for this unpopulated field','Schema support only','Native enrichment/target enablement not proven',['C53S24','C53S25','C53S27'],'legacy install IDFI, not GAID',False)
row('MAX event_id -> Google placement_req_id','MAX adapter serverParameters event_id','GoogleMediationAdapter','selected adapter ad request path; not game-event identity','MAX Google adapter25.4.0.0','Google network extras placement_req_id','Google Mobile Ads request builder','Google ad request component','Ad-request correlation','No equivalence to userID/IAP ImpressionId/EventUuid or model join',['XS30'],'advertising request, not persistent user')
row('Product metadata PriceMicro','selected catalog listing metadata localizedPrice * 1,000,000; long cast','PurchaseEventEmitter.BuildSku','cart product/listing and metadata available; stages may include nonpurchase','IAP5.5.1','Order[16].Sku[1].PriceMicro[6]',T,RX,'Catalog/localized listed price in currency microunits','Not proved final paid/net/refund-adjusted revenue or prediction; not Vector label proof',['C53S24','C53S25','C53S49'],'one SKU listing price; quantity independent')
row('Currency and quantity','metadata.isoCurrencyCode; cartItem.Quantity','PurchaseEventEmitter.BuildSku','same catalog/cart conditions','IAP5.5.1','Order.Sku.IsoCurrencyCode[7],Quantity[8]',T,RX,'Currency code and units for purchase context','No normalization/exchange-rate/tax pipeline recovered',['C53S24','C53S25'],'native currency, integer quantity; not dollars by default')
row('Store transaction identity','order.Info.TransactionID','PendingOrder / ConfirmedOrder','paid or fulfilled path; may be same order across stages','IAP5.5.1','Order[16].StoreTransactionId[2]',T,RX,'Transaction-level reporting context','Cross-stage dedup/refunds/net revenue correctness unknown',['C53S22','C53S24','C53S25'],'store/order scope; not user or event')
row('Store verification payload','Google OriginalJson/signature or Apple receipt/JWS/original transaction/appAccountToken','Store payload mapper','store callback/payload exists; one active store variant','IAP5.5.1','paid[18] or fulfilled[20] StorePayload submessages',T,RX,'Forward store-supplied transaction evidence','Server verification success and final revenue not proven',['C53S22','C53S25','C53S50'],'transaction/store account context, not automated cross-app join')
row('Event timestamp','DateTime.UtcNow after await player identity','Purchase/Session BuildEnvelope','emitter reaches envelope construction','IAP5.5.1','Timestamp[1] seconds/nanos',T,RX,'SDK envelope creation time','Not guaranteed exact click/payment time, server ingest time or settled revenue time',['C53S22','C53S24','C53S25','C53S30'],'UTC wall-clock; encoding precision != clock accuracy')
row('Installation timestamp','Android PackageInfo.firstInstallTime ms; iOS directory creation UTC','AppInstallInfo lazy cache','platform source available; null elsewhere','IAP5.5.1','InstallationTimestamp[14]',T,RX,'Install-age context with platform limitations','Server maturity windows or historical exactness not proven',['C53S45','C53S24','C53S25'],'app install, not account creation')
row('Ads and Analytics consent states','EndUserConsent state -> ParseConsent','Unity Consent API and emitter explicit enum mapping','compile support; unspecified if unavailable','IAP5.5.1','UnityConsentStateAdsIntent[9],AnalyticsIntent[10]',T,RX,'Declared consent context; IDs separately gated','Receiving enum is not proof all downstream training/privacy policies executed',['C53S21','C53S24','C53S25','C53S47'],'per-purpose state; not one global opt-in')
row('Project/environment','Core ICloudProjectId/IEnvironmentId','CoreRegistryHelper','components available; empty permitted in envelope','IAP5.5.1','ProjectId[5],EnvironmentId[6]',T,RX,'Namespace/reporting context','No proof organization-wide join or model inclusion',['C53S20','C53S24','C53S25'],'UGS project/environment; not user')
row('AuthenticationComplete variant','AuthenticationService.SignedIn callback','IapCoreInitializeCallback -> SessionEventEmitter','IAP_UNITY_AUTH_ENABLED; subscription initialization; success callback','IAP5.5.1','oneof tag22 empty message with identity/session context',T,RX,'Login lifecycle event; no Store/Order','Not purchase or positive-revenue label; target-game delivery/training unknown',['C53S30','C53S31','C53S25'],'session/account action, no payment evidence')
put(O/'FIELD_LINEAGE.json',rows)

report55='''# 跨SDK身份与价值事件血缘最终核验

2026-11-19。本轮只补53—54能由公开客户端验证的连接，不重复SDK清单。原始发行包、固定提交、文件/原包SHA256、类/方法/行号与六层状态可交叉查看：[代码证据](core-insights/CODE_EVIDENCE.json)、[逐字段机器表](core-insights/FIELD_LINEAGE.json)、[协议描述](core-insights/PROTOCOL_SCHEMA.json)。

## 已证关联与明确不成立的等号

【SDK代码证实】新增的是Core→两个消费者的具体提供者和存储关系、ExternalUserId→引擎API的双向代理、Auth登录事件→IAP Insights的真实SDK调用、IAP购买旅程ID的生成与传播。没有证明目标四款游戏升级到这些SDK，也没有生产成功发送/接收/训练证据。

必须分开：

- 安装ID、Auth PlayerId与开发者ExternalUserId；IAP和Analytics安装值仅在特定初态可能同值。
- FirebaseInstallations FID、Firebase Analytics App Instance ID、Firebase App配置ID；不是一个ID的三种叫法。
- Analytics Session GUID、IAP读取的unity_connect.session_id、Firebase Session ID；没有自动判等路径。
- EventUuid、订单TransactionID、MAX广告请求event_id、IAP ImpressionId；后者是购买旅程ID，并非广告展示ID。
- 商品metadata价格、实际成交/净收入、预测LTV、代理value、阈值达标事件；不能混作同一种训练标签。

FID来源补充定位：Firebase RC24.0.1 `ConfigFetchHandler.java`:L256/278明确从`firebaseInstallations.getId()`取得，再交给fetch；`ConfigFetchHttpClient`:L321将其写为INSTANCE_ID。复用XS24/XS25官方源码和原包记录，不因字段名Instance就判等Firebase Analytics getter。IAP对应JNI getter见C53S29。

## 逐字段血缘表

表内“接收”指代码中的目标模块/URL，不代表生产已收到；全部目标游戏业务调用未新增证据。IAP传输缩写：**T** = 条件Gateway protobuf POST或Runtime base64 LogEvent(1000)；**R** = Unity Insights网关地址/原生接口，后端实收未知。Analytics为自己的项目/环境collect接口，不借用IAP传输结论。

| 字段 | 来源→提供者/读取条件 | 消费者与序列化位置 | 传输→已知接收方 | 已证用途；未证用途 | 原始证据 |
|---|---|---|---|---|---|
'''
for x in rows:
    refs=' / '.join(cite(int(i[-2:])) if i.startswith('C53S') else f'[{i}](cross-sdk/CODE_CATALOG.md)' for i in x['source_ids'])
    report55+=f"| {x['field']} | {x['field_source']} → {x['provider']}；{x['read_conditions']} | {x['consumer_sdk']}；{x['serialization']} | {'T→R' if x['transport_module']==T else x['transport_module']+'→'+x['known_receiver']} | {x['proven_use']}；{x['unproven_use']} | {refs} |\n"
report55+='''
## 六层证据与关系图更新

| 层级 | 本轮状态 |
|---|---|
| 1 SDK具备能力 | 源码/原包与编译条件已证 |
| 2 目标游戏实际业务调用 | 本轮没有新证据；SDK内部购买/登录回调不冒充目标游戏调用 |
| 3 请求实际构造 | 可证明“构造代码及可达条件”；没有运行采集payload。Runtime只到本地LogEvent参数，不证明native网络构造 |
| 4 生产成功发送 | 未证；HTTP completed≠成功ACK |
| 5 服务端接收 | 未证；公开隐私用途不是该次接收记录 |
| 6 服务端用于训练 | 未证事件/字段级血缘；S21仅为官方IAP/D2C→Vector产品用途披露 |

JSON中的false表示该层“未获证”，不表示证实不存在。身份读入一个envelope是明确客户端关联，但不等于接收方已完成身份join，更不等于跨应用/跨设备身份图谱。三种身份读取时刻也未承诺原子快照；不要在异步身份变化时断言同值。

本轮关系图追加细分提供者、购买旅程、登录事件、protobuf、Gateway和native边；**保留原48节点、53边、84来源逐对象不变**，包括XU07的未知训练边。前后快照与检查见[before53](core-insights/EVIDENCE_GRAPH.before53.json)、[after55](core-insights/EVIDENCE_GRAPH.after55.json)、[VALIDATION](core-insights/VALIDATION.json)。

## 关于模型输入与研究结束条件

【官方公开证实】Unity公开说IAP/D2C购买数据可帮助丰富Vector模型（原S21）。【SDK代码证实】本轮购买、登录、安装/账号/可选Firebase字段能按条件共封装。两者之间的服务端逐字段处理仍缺失。

【无法确认】哪些安装前特征与这批事件join、哪些是训练标签、如何去重/验单/退款/迟到、哪个授权项目/人群/窗口进入Vector。未新增Axon接收这些IAP事件的任何边；Unity IAP也不是AppLovin的MMP postback。

公开路径已经追到最后可见接口，按结束条件停止；不继续从字段命名猜测模型。下一份最高价值材料不是更多SDK：应是**Unity授权、匿名化的Insights producer schema→接收/标准化→Vector训练dataset列血缘**，附同意/包级requirement和项目授权条件、交易去重/退款/成熟窗口。若拿不到，则持续标记未知。

## 核验方法及边界

重新计算4个官方包SHA256；逐片段校验源文件哈希/行号/原包成员一致；核对proto顶层20个常规字段+6个oneof以及所有嵌套字段，确认原包无.proto；核对图节点/来源引用、旧对象保留、未将静态发送升级为生产ACK。检查结果写入VALIDATION.json。该验证是证据完整性审计，不是SDK运行、线上送达或模型效果测试。

没有修改任何复刻工程、APK、手机设置、真实标识或存档。本轮仅官方公开GET和本地静态分析，失败的文档地址和缺失native代码均留档。
'''

for name,content in [('53_Unity_Core身份提供者与生命周期.md',report53),('54_Unity_Insights事件协议与接收边界.md',report54),('55_跨SDK身份价值血缘最终核验.md',report55)]:
    (R/name).write_text(content,'utf-8')

gpath=R/'prediction-system/EVIDENCE_GRAPH.json'
g=load(gpath)
before=load(O/'EVIDENCE_GRAPH.before53.json')
for key in ('nodes','edges','sources'):
    original={x['id']:x for x in before[key]}
    assert all(original[x['id']]==x for x in g[key] if x['id'] in original),key
nodes=[
 ('U_core_installation','Core1.19 InstallationId / UnityInstallationId'),
 ('U_core_engine_installation','Core1.19 EngineInstallationId / native installationId or fallback key'),
 ('U_core_external','Core1.19 ExternalUserId / native userId or memory'),
 ('U_auth_player_provider','Authentication3.9 PlayerIdComponent / project-profile cache'),
 ('U_iap_journey','IAP5.5.1 AsyncLocal purchase journey (not advertising impression)'),
 ('U_iap_auth_event','IAP AuthenticationComplete triggered by SignedIn'),
 ('U_iap_proto','IAP5.5.1 protobuf producer v1alpha1'),
 ('U_iap_gateway','IAP5.5.1 HTTP gateway request builder'),
 ('U_native_insights','Unity6000.7 public EngineDiagnostics native boundary'),
]
for n,label in nodes:
    if n not in {x['id'] for x in g['nodes']}:g['nodes'].append(dict(id=n,label=label,company='Unity',stage='client_data_lineage'))
for s in sources:
    existing=next((i for i,x in enumerate(g['sources']) if x['id']==s['id']),None)
    if existing is None:g['sources'].append(s)
    else:g['sources'][existing]=s

def edge(num,src,dst,claim,ids,chain,conditions,missing,supplements,request=True,status='sdk'):
    ident=f'C53E{num:02d}'
    resolved=[S[x] for x in ids]
    e=dict(id=ident,source=src,target=dst,claim=claim,status=status,
        evidence_level='【SDK代码证实】' if status=='sdk' else '【无法确认】',source_ids=ids,
        sdk='Unity Core1.19 / IAP5.5.1 / Analytics6.3 / Authentication3.9; pinned UnityCsReference as cited',
        version='per-source exact version and source commit',
        sha256=[dict(path=s['path'],sha256=s['sha256'],official_package=s.get('official_package'),public_source=s.get('public_source')) for s in resolved],
        class_method_lines=[dict(path=s['path'],method=s['class_or_method'],start_line=s['start_line'],end_line=s['end_line']) for s in resolved],
        data_provider=src,data_receiver=dst,explicit_call_chain=chain,permission_conditions=conditions,
        six_layers=dict(sdk_capability=status=='sdk',actual_game_business_callsite=False,request_construction_code=request,
            production_successful_send=False,server_received=False,server_model_training=False),
        production_actual_proven=False,production_evidence='static only; SDK never initialized; no production request',
        observed_target_game_delivery=False,applies_to='standalone SDK code; not target-game production facts',
        supplements_original_edges=supplements,missing_evidence=missing,
        diagram_style='solid' if status=='sdk' else 'dashed',reviewed_utc=NOW)
    if ident not in {x['id'] for x in g['edges']}:g['edges'].append(e)
edge(1,'U_core_engine_installation','U_core_installation','Explicit copy only when UnityInstallationId absent; existing local value can differ',
 ['C53S01','C53S02','C53S03','C53S04'],'engine provider -> UnityEngineIdentifier -> conditional copy -> UnityInstallationId',
 'existing-key precedence; engine return must be nonempty','Actual stored values/native lifecycle/cross-app scope not observed',['XU01','XU05'],False)
edge(2,'U_core_installation','U_analytics_identity','Analytics reads IInstallationId, distinct from IAP engine interface',
 ['C53S02','C53S17','C53S18','C53S19'],'Core registry IInstallationId -> IdentityManager -> standard installationID/fallback userID',
 'same initialized registry; event/consent conditions','Runtime resolved project/version and actual event unknown',['XU01','XU02'])
edge(3,'U_core_engine_installation','U_iap_identity','IAP explicitly reads IEngineInstallationId into separate installation field',
 ['C53S03','C53S20','C53S21','C53S24','C53S25'],'CoreRegistryHelper -> PlayerData -> MapIdentity -> protobuf identities.1',
 'Core component exists; native/platform branch','Equality with Analytics installationID, delivery and server identity join unknown',['XU05','XU06'])
edge(4,'U_core_external','U_analytics_identity','ExternalUserId is engine API alias conditionally; Analytics userID uses external-first rule',
 ['C53S05','C53S06','C53S07','C53S18','C53S19','C53S36'],'Identifiers.userId OR memory -> IExternalUserId -> IdentityManager -> userID',
 'both engine support symbols for native branch; developer sets value; Analytics consent','No target-game IDs or cross-app account join observed',['XU01'])
edge(5,'U_core_external','U_iap_identity','Same interface family has explicit IAP getter and protobuf UserId assignment',
 ['C53S05','C53S06','C53S20','C53S24','C53S25'],'CoreRegistry.Instance IExternalUserId -> MapIdentity -> identities.3',
 'component available; same default registry only conditionally asserted','Atomicity/runtime same value with Analytics and production server join not proven',['XU05'])
edge(6,'U_auth_player_provider','U_analytics_identity','Authentication registers project/profile PlayerId provider consumed separately by Analytics',
 ['C53S12','C53S13','C53S14','C53S16','C53S17','C53S19'],'token Subject/cache -> IPlayerId -> standard unityPlayerID',
 'Auth component exists; standard-event branch; Analytics consent','No organization-wide identity or target-game production facts',['XU01'])
edge(7,'U_auth_player_provider','U_iap_identity','Auth PlayerId is a separate IAP identity field, not installation/external alias',
 ['C53S12','C53S20','C53S24','C53S25'],'IPlayerId.PlayerId -> MapIdentity -> identities.2',
 'Auth component available; credentials/profile state; optional null','Target games, server join, training unknown',['XU05'])
edge(8,'U_iap_journey','U_iap_proto','Purchase journey GUID is serialized as impression_id, not an advertising impression or person ID',
 ['C53S32','C53S22','C53S24','C53S25'],'AsyncLocal journey -> Current -> PlayerData -> IAPSDKEvent.24',
 'active journey; native/UI callbacks may lose context; fulfilled does not supply argument by default',
 'Server journey join/dedup and training unknown',['XU06'])
edge(9,'U_auth_player_provider','U_iap_auth_event','Real SDK SignedIn subscription constructs AuthenticationComplete context, not purchase revenue',
 ['C53S31','C53S30','C53S25'],'IapCoreInitializeCallback subscribes Auth.SignedIn -> SessionEventEmitter -> oneof22',
 'IAP_UNITY_AUTH_ENABLED; core initialized; SignedIn callback','Target-game callsite and actual delivery unknown',['XU05','XU06'])
edge(10,'U_iap_identity','U_iap_proto','Exact public serializer carries conditional IDs plus metadata price and transaction lifecycle',
 ['C53S21','C53S22','C53S24','C53S25','C53S26'],'BuildEnvelope -> protobuf writer (schema v1alpha1; headers v1)',
 'optional ID consent + remote allowlist; emitter lifecycle','Price is metadata not final net revenue; server validation and labels unknown',['XU03','XU04','XU06'])
edge(11,'U_iap_proto','U_iap_gateway','Public code constructs protobuf HTTP POST; completed only disposes',
 ['C53S23'],'Forward compile fallback -> UnityWebRequest headers/body -> SendWebRequest',
 'native module gate not met; no SDK initialization during research','No production send, success ACK, event retry or receiver evidence',['XU06'])
edge(12,'U_iap_proto','U_native_insights','Module branch passes base64 protobuf to native LogEvent type1000',
 ['C53S23','C53S33','C53S34','C53S35','C53S37','C53S51'],
 'Forward compile module -> Convert.ToBase64String -> EngineDiagnostics.LogEvent(1000)',
 'UNITY_INSIGHTS_REQUIREMENTS_API AND ENABLE_CLOUD_SERVICES_ENGINE_DIAGNOSTICS; package requirement rules',
 'Native envelope/queue/transport/retries/ACK and production delivery not public',['XU06'],False)
edge(13,'U_native_insights','U_predict','No event/field-level proof connecting native Insights receiver to Vector training',
 ['C53S35','C53S37','C53S40'],'Public SDK ends at native extern; official S21 product-purpose statement remains separate',
 'Authorized service-side lineage and purpose/privacy controls needed',
 'Need producer-to-dataset field mapping, join/consent/de-dup/refund/maturity and training records',['XU07','U07'],False,'unknown')
g['core_insights_extension']=dict(reviewed_utc=NOW,reports=[53,54,55],code_catalog='core-insights/CODE_EVIDENCE.json',
    field_lineage='core-insights/FIELD_LINEAGE.json',protocol_schema='core-insights/PROTOCOL_SCHEMA.json',
    base_graph='core-insights/EVIDENCE_GRAPH.before53.json',six_layer_semantics='False means unproven, not proven absence; static construction != observed payload')
g['reviewed_utc']=NOW
put(gpath,g)
(O/'EVIDENCE_GRAPH.after55.json').write_bytes(gpath.read_bytes())

# Append-only index section. Old reports and original evidence are retained.
index=R/'EVIDENCE_INDEX.md'
body=index.read_text('utf-8')
if True:
    if '<a id="ci53"></a>' in body:body=body.split('<a id="ci53"></a>',1)[0]
    section=['','<a id="ci53"></a>','','## CI53 · Unity Core身份提供者与Insights数据血缘（53—55）','',
        '独立官方SDK静态证据；不代表目标游戏启用、生产送达或Vector逐字段训练。', '',
        '- [53_Unity_Core身份提供者与生命周期.md](53_Unity_Core身份提供者与生命周期.md)',
        '- [54_Unity_Insights事件协议与接收边界.md](54_Unity_Insights事件协议与接收边界.md)',
        '- [55_跨SDK身份价值血缘最终核验.md](55_跨SDK身份价值血缘最终核验.md)',
        '- [原包版本/哈希/依赖](core-insights/PACKAGE_PROVENANCE.json)',
        '- [代码目录](core-insights/CODE_CATALOG.md) / [带原始片段的JSON](core-insights/CODE_EVIDENCE.json)',
        '- [逐字段血缘](core-insights/FIELD_LINEAGE.json) / [发送侧协议重建](core-insights/PROTOCOL_SCHEMA.json)',
        '- [官方公开获取记录](core-insights/ACQUISITION.json) / [固定提交绑定](core-insights/BOUNDARY_ACQUISITION.json)',
        '- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [旧图快照](core-insights/EVIDENCE_GRAPH.before53.json) / [本轮快照](core-insights/EVIDENCE_GRAPH.after55.json)',
        '- [验证结果](core-insights/VALIDATION.json)','']
    for s in sources:
        section.append(f"- **{s['id']}** [{s['class_or_method']}]({s['path']}):L{s['start_line']}；{s['sdk']} {s['version']}；原包/文件SHA256见代码目录。")
    index.write_text(body+'\n'.join(section)+'\n','utf-8')
print('Reports written; graph:',len(g['nodes']),len(g['edges']),len(g['sources']),'lineage rows',len(rows))
