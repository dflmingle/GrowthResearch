# 跨SDK身份关联与字段映射

2026-11-19。只将明确读取、赋值、转换或共享契约列为已证关联。**本轮最重要的新证据是Unity IAP→Firebase/UGS组件的实际读取及共封装，仍未证明统一跨应用身份图谱。**

| 输入→输出 | 证据 | 作用域与条件 |
|---|---|---|
| ID01 Authentication IPlayerId.PlayerId → Analytics IdentityManager.PlayerId -> unityPlayerID | 【SDK代码证实】[XS18](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs):L49；[XS19](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs):L42；[XS20](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs):L373 | UGS项目玩家，不等于Analytics UserId |
| ID02 Core IExternalUserId.UserId → Analytics UserId; fallback InstallId | 【SDK代码证实】[XS18](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs):L49；[XS19](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs):L42 | 开发者控制的命名空间；不是自动跨发行商ID |
| ID03 FirebaseAnalytics.getAppInstanceId() → IAP pps.UnityAppInstanceId -> Insights.PlayerIdentity.AppInstanceId | 【SDK代码证实】[XS01](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L97；[XS02](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L176；[XS03](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L60；[XS11](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L363 | 5.5.1; ads consent +远程允许 +Firebase可用 |
| ID04 FirebaseAnalytics.getSessionId() → IAP FirebaseSessionId -> protobuf tag4 | 【SDK代码证实】[XS03](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L60；[XS10](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L243；[XS13](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39 | 会话标识；5.4.0不能据字段存在声称已发送 |
| ID05 FirebaseApp.getOptions().getApplicationId() → IAP FirebaseAppId -> protobuf tag100 | 【SDK代码证实】[XS41](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L127；[XS13](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39 | 项目/App标识，不是用户身份 |
| ID06 IAP CoreRegistry IPlayerId / IExternalUserId / AnalyticsService.GetAnalyticsUserID → Insights PlayerId / UserId / AnalyticsId | 【SDK代码证实】[XS06](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs):L38；[XS01](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L97；[XS11](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L363 | 可同包出现，不代表这些字符串彼此相等 |
| ID07 MAX adapter serverParameters.event_id → Google networkExtras.placement_req_id | 【SDK代码证实】[XS30](cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java):L494 | 广告请求关联，不是人或跨App用户 |
| ID08 MAX consent / doNotSell → Unity gdpr.consent / privacy.consent | 【SDK代码证实】[XS28](cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java):L101；[XS29](cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java):L268 | 配置缺失不自动当已同意；不证明实际初始化 |
| ID09 official Facebook app signed AttributionIdProvider.aid → Adjust DeviceInfo.fbAttributionId -> PackageBuilder.fb_id | 【SDK代码证实】[XS34](ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/DeviceInfo.java):L440；[XS44](ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/PackageBuilder.java):L276 | 不是Facebook账号ID，也不是Meta AppEvents匿名ID |
| ID10 Developer Singular customUserId → SingularInstance.saveCustomUserId | 【SDK代码证实】[XS39](cross-sdk/java/singular-1217/com/singular/sdk/Singular.java):L382 | 未证明任何目标游戏或其他MMP设置同值 |

## 生成、持久化及重置边界

- UGS Analytics的`UserId`优先开发者ExternalId，否则安装ID；持久化`UnityAnalyticsUserId`用于识别本地变化，旧`UnityAnalyticsInstallationId`有迁移逻辑。`PlayerId`单独从Authentication读取。改ExternalId会进入身份变化处理，不代表自动跨设备合并。
- IAP的事件UUID是`Guid.NewGuid`，交易ID来自订单；Firebase Session ID表示会话，Firebase App ID表示应用，不能代替用户键。IAP会缓存非空Firebase结果，App/Session/Instance ID的生命周期以相应提供者为准，不由缓存自动延长。
- MAX用户ID、AF CUID、Rotate ThinkingData ID、Car Metica ID的已有明确桥接复用[21号](21_MAX用户ID与身份数据流.md)；这些不是本轮新发现，也不能据同属发行商扩为统一账户。
- GAID、AppSet、苹果IDFV作用域、重置和授权限制复用[31](31_AppLovin设备身份图谱.md)/[32](32_Unity身份互通与RampID.md)。本轮仅静态分析，无真实标识。

## 刻意不建立的等号

| 容易误判的字段 | 本轮结论 |
|---|---|
| Firebase RC `INSTANCE_ID`与Firebase Analytics App Instance ID | RC来源是FirebaseInstallations的FID；不能因名字相似判等 |
| Analytics `IInstallationId`与IAP `IEngineInstallationId` | 两处所读接口不同；未审计Core具体提供者，不直接认定同值 |
| 新UGS Analytics UserId与旧`unity.cloud_userid` | Unity Ads4.17读取的是旧PlayerPrefs键；未建立新SDK写该键的路径 |
| MAX cuid、UPA、RampID、GAID | 均不同输入及scope；没有跨者服务器join证据 |
| MAX `event_id`、Axon `dedupe_id`、IAP `EventUuid`、交易ID | 广告请求、事件去重和订单身份分别处理，不能当同一键 |
| Facebook Provider `aid`与GAID/Meta账号 | 不同来源，不因值名/长度相似关联 |

详细逐字段证据及原包SHA256见[机器映射表](cross-sdk/IDENTITY_MAPPINGS.json)和[代码目录](cross-sdk/CODE_CATALOG.md)。
