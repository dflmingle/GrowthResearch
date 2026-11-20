# Unity Core 身份提供者与生命周期

2026-11-19。新增官方 Core 1.19.0 并验过 registry SHA1 与本地 SHA256。复用 Analytics 6.3.0、IAP 5.5.1、Authentication 3.9.0；未安装到任何游戏或读取实际 ID。[原包及来源](core-insights/PACKAGE_PROVENANCE.json)、[55段源码定位及哈希](core-insights/CODE_CATALOG.md)。

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

初始化先创建安装提供者，随后获取项目配置，最后在初始化成功时注册服务组件。更换环境/初始化选项的 `FreeOptionsDependantComponents` 不清空安装提供者。证据：[C53S01](core-insights/CODE_CATALOG.md#c53s01)、[C53S02](core-insights/CODE_CATALOG.md#c53s02)、[C53S03](core-insights/CODE_CATALOG.md#c53s03)、[C53S04](core-insights/CODE_CATALOG.md#c53s04)、[C53S06](core-insights/CODE_CATALOG.md#c53s06)、[C53S12](core-insights/CODE_CATALOG.md#c53s12)、[C53S16](core-insights/CODE_CATALOG.md#c53s16)。

### 不同接口何时同值

以下为**源码分支推导**，A/B/E是符号，不是真实标识，也不是设备实验。

| 已有 UnityInstallationId | Engine 返回值 | Analytics 安装ID | IAP 安装ID | 能否建立等号 |
|---|---|---|---|---|
| 空 | 非空 E | 首次复制 E 并保存 | E | 该次初始化条件下同源/同值，之后需存储和引擎值均未变化 |
| A | B | A，提前返回 | B | 不保证相等；没有强制同步或覆盖旧 A |
| A | 空 | A | 空/缺失 | 不相等，不应以旧 A 填充为已证行为 |
| 空 | 空 | legacy Analytics，次选 Ads，最后 GUID | 空 | 只是 fallback；不得将其当通常新安装分支 |

`InstallationId.CreateIdentifier` 中 legacy `unity.cloud_userid` 和 `unityads-idfi` 的写回发生在 engine 为空的后续分支。engine 非空时在写入 `UnityInstallationId` 后就返回，**不会继续把值写给两个 legacy SDK**。fallback EngineImplementation 正常会生成非空 GUID，所以不能把 legacy 桥画成所有新安装必经路径。[C53S02](core-insights/CODE_CATALOG.md#c53s02)、[C53S03](core-insights/CODE_CATALOG.md#c53s03)、[C53S09](core-insights/CODE_CATALOG.md#c53s09)、[C53S10](core-insights/CODE_CATALOG.md#c53s10)。

这补充了48号原先的“未核实提供者”，也找到了此前旧 `unity.cloud_userid` 问题的条件式读写桥。**不是**发现所有 Unity Ads、新 Analytics 与 Core 始终共享 ID。

## ExternalUserId 的真实生命周期

【SDK代码证实】同时满足 `ENABLE_UNITY_CLOUD_IDENTIFIERS` 和 `UNITY_SUPPORTS_IDENTIFIERS_USER_ID` 才使用引擎分支；否则是内存字段。版本定义精确为：

- `[6000.0.78f1,6000.1.0a1)`
- `[6000.3.18f1,6000.4.0a1)`
- `[6000.5.2f1,6000.6.0a1)`
- `6000.6.0a8` 及按 Unity versionDefine 规则满足该下界的版本

还要满足平台引擎符号；不能简化成“6000.6以上才有”，也不能仅凭版本认定所有平台启用。[C53S05](core-insights/CODE_CATALOG.md#c53s05)、[C53S07](core-insights/CODE_CATALOG.md#c53s07)。

引擎分支 getter/setter 均代理 `Identifiers.userId`；监听引擎 userIdChanged 再通知消费者。公开绑定把 null 归一为空串，超过1024字符抛错，相同值不再次通知。Core 静态重置时移除旧订阅、重建包装器；fallback Dispose 清内存值；引擎分支 Dispose 不清除原生 userId。新分支跨会话持久性由 Core 注释和公开引擎绑定明确说明；原生存储位置、卸载/备份恢复后的行为与跨设备同步不可见。[C53S05](core-insights/CODE_CATALOG.md#c53s05)、[C53S08](core-insights/CODE_CATALOG.md#c53s08)、[C53S36](core-insights/CODE_CATALOG.md#c53s36)。

初始化兼容项 `com.unity.services.core.analytics-user-id` 只在 ExternalUserId 为空时写入。它是开发者命名空间输入，不是 Auth PlayerId 的自动别名。原始位置 `CorePackageInitializer.InitializeExternalUserId`:L255—272，见[C53S54](core-insights/CODE_CATALOG.md#c53s54)。

## PlayerId、存储和重置

【SDK代码证实】Authentication 的缓存键前缀为 `CloudProjectId.Profile.unity.services.authentication.`，其中 `player_id` 保存服务器返回的 token Subject。SignOut 默认保留该 PlayerId；`SignOut(true)` 才清除凭据和玩家ID；登出状态切 profile 会 Refresh 对应缓存。因此“退出登录后还带 PlayerId”并不自动说明匿名追踪绕过，必须核对调用选项及业务实现。[C53S13](core-insights/CODE_CATALOG.md#c53s13)、[C53S14](core-insights/CODE_CATALOG.md#c53s14)、[C53S15](core-insights/CODE_CATALOG.md#c53s15)、[C53S16](core-insights/CODE_CATALOG.md#c53s16)。

| 维度 | 源码可证范围 | 仍不能证明 |
|---|---|---|
| 应用/安装 | fallback安装键在当前应用 PlayerPrefs；Android旧Ads键在当前 Activity 的 MODE_PRIVATE SharedPreferences | 一个全设备/全发行商统一ID；卸载重装必然重新生成（备份恢复需另证） |
| 项目/环境 | 安装键本身不带项目/环境；Auth缓存显式带项目/profile；Analytics collect URL带项目/环境 | 同工程换项目就自动重置所有安装ID；组织级跨项目Auth合并 |
| 账号 | PlayerId来自Auth Subject；ExternalUserId由开发者设置 | 两者相等或自动账号绑定；第三方身份提供者与Unity广告用户的服务器join |
| 内存/磁盘/原生 | 两个fallback安装类各有内存缓存及不同磁盘键；新引擎 getter到 extern | 原生 installationId 的生成/重置算法、后端跨设备解析 |

Android存储证据：[C53S11](core-insights/CODE_CATALOG.md#c53s11)。这些安装类没有公开的“统一清除全部身份”方法；源码也没有跟随广告拒绝而删除安装键的路径。此处仅描述提供者，不据此下隐私合规结论。

## Analytics 与 IAP 实际消费者

Analytics6.3：`IInstallationId → IdentityManager.InstallId`；`UserId = 非空ExternalId，否则InstallId`；PlayerId独立动态读取。IAP5.5.1：`IEngineInstallationId → PlayerData → Insights.UnityIdentities.UnityInstallationId`；ExternalUserId、PlayerId各自独立字段。[C53S17](core-insights/CODE_CATALOG.md#c53s17)、[C53S18](core-insights/CODE_CATALOG.md#c53s18)、[C53S20](core-insights/CODE_CATALOG.md#c53s20)、[C53S21](core-insights/CODE_CATALOG.md#c53s21)、[C53S24](core-insights/CODE_CATALOG.md#c53s24)。

Analytics标准事件额外写 installationID/unityPlayerID；所有这两种构造路径共用 userID/sessionID/eventUUID 头。**不能把标准事件的身份字段自动写成每个 custom event 都有。** [C53S19](core-insights/CODE_CATALOG.md#c53s19)。

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
