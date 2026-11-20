# 静态代码证据目录

所有SDK均未初始化；源码、反编译视图和目标游戏调用分别标记。包哈希与文件哈希分开保存。

## XS01 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L97—172；方法：`PlayerData.CreatePlayerIdentityAsync`。
- 文件SHA256：`13233ab6ea00e470aaba64f2c3d5bb966a71d5d2ed117c0aacc3c3dc52619528`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Consent + remote allowlist -> optional advertising/Firebase IDs -> PlayerIdentity。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS02 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L176—229；方法：`PlayerData.FetchEnabledFirebaseIdsAsync`。
- 文件SHA256：`13233ab6ea00e470aaba64f2c3d5bb966a71d5d2ed117c0aacc3c3dc52619528`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Explicit Firebase getter assignment, allowed attributes and caches。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS03 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L60—124；方法：`FirebaseAnalyticsClient.FetchAppInstanceIdAsync/FetchSessionIdValueAsync`。
- 文件SHA256：`5f6d98d742761dd0e2213e57a7b33834439d6a48c7cedb635f9a76301e648b08`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：JNI calls FirebaseAnalytics.getAppInstanceId/getSessionId; missing provider -> null。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS04 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs):L44—91；方法：`ConnectionsSettingsClient.CachedEnabledAttributes/FetchAndCacheAsync`。
- 文件SHA256：`ab0cc755e98a056ac539775b72e3c539d82fbb207f2feea41ef0f7d68c222650`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：session-global allowlist, empty until successful async fetch, retries on later miss。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS05 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs):L104—186；方法：`ConnectionsSettingsClient.FetchEnabledAttributesAsync/ParseEnabledAttributes/PostAsync`。
- 文件SHA256：`ab0cc755e98a056ac539775b72e3c539d82fbb207f2feea41ef0f7d68c222650`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：project/install context -> endpoint; true attributeOverride entries -> allowlist; timeout10。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS06 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs):L38—56；方法：`CoreRegistryHelper properties`。
- 文件SHA256：`212bfdbd42cc46be3de42704ef19e6739aa66563e331df6d685902ea5e3bf7c0`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Explicit IPlayerId/IExternalUserId component getters, not equal by field name。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS07 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs):L58—97；方法：`GooglePlayStoreExtendedPurchaseService.SendPurchasePaidEvent/SendPurchaseFulfilledEvent`。
- 文件SHA256：`21622106306172a42b6ab04227c9b3a2632fe07257adf0db7c783f39e7bf1493`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Concrete purchase callbacks -> separate paid/fulfilled events and store receipt payload。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS08 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L92—146；方法：`PurchaseEventEmitter.SendPurchasePaidEvent/SendPurchaseFulfilledEvent`。
- 文件SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Separate lifecycle variants; awaiting identity; Forward per cart item。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS09 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L190—239；方法：`PurchaseEventEmitter.Forward/ForwardGateway/ForwardModule`。
- 文件SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：protobuf bytes -> conditional EngineDiagnostics module OR HTTP gateway; schema headers; not observed send。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS10 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L243—287；方法：`PurchaseEventEmitter.BuildEnvelope`。
- 文件SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：UUID, UTC, Firebase session/app, project/environment, consent, identities, order。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS11 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L363—378；方法：`PurchaseEventEmitter.MapIdentity`。
- 文件SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：UGS PlayerId, external UserId, AnalyticsId and platform IDs explicitly co-packaged。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS12 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L404—426；方法：`PurchaseEventEmitter.BuildSku`。
- 文件SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：metadata price * 1e6, currency, quantity; catalog price not guaranteed final settlement。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS13 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39—94；方法：`PurchaseEventProtobufWriter.SerializeIaps`。
- 文件SHA256：`4ba0c2a596d7b8218ec45034b4c6d75aec20da89fb9e1157e964c355c9e656cd`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Firebase session explicitly serialized tag4; event IDs and schema envelope。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS14 · com.unity.purchasing 5.4.0

- 原文：[cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/PlayerData.cs](../cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/PlayerData.cs):L88—152；方法：`PlayerData.CreatePlayerIdentityAsync (older)`。
- 文件SHA256：`dff9e5b11c33faed112e95ca0876819ae78152ea72ab093cdf3f04a063cdd790`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.4.0/purchasing-5.4.0.tgz](../cross-sdk/packages/purchasing/5.4.0/purchasing-5.4.0.tgz)；SHA256：`f66ac4f26ef96346b34c63c920512d6e981430712a2d5092544bc66cb7a278ef`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.4.0.tgz。
- 结论范围：Firebase fetches commented out; mere fields did not establish live bridge。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS15 · com.unity.purchasing 5.4.0

- 原文：[cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs](../cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39—91；方法：`SerializeIaps (older)`。
- 文件SHA256：`71e824506e3bd8b6b1b80e06a1d254337277ff9ee4571a1a76db7bf7dd3aed37`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.4.0/purchasing-5.4.0.tgz](../cross-sdk/packages/purchasing/5.4.0/purchasing-5.4.0.tgz)；SHA256：`f66ac4f26ef96346b34c63c920512d6e981430712a2d5092544bc66cb7a278ef`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.4.0.tgz。
- 结论范围：Firebase session field4 not written in selected older release。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS16 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md](../cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L2—13；方法：`Official package CHANGELOG 5.5.1`。
- 文件SHA256：`e9e1ccf5647901070585f96e97a8daaa861aaf558032f9794f956ac2594b1131`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Official acknowledgement of missing Firebase session serialization fix。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS17 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md](../cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L88—100；方法：`Official package CHANGELOG 5.4.3`。
- 文件SHA256：`e9e1ccf5647901070585f96e97a8daaa861aaf558032f9794f956ac2594b1131`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Google Analytics ID authorization and engine Insights route evolution。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS18 · com.unity.services.analytics 6.3.0

- 原文：[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs):L49—106；方法：`AnalyticsService.Initialize`。
- 文件SHA256：`b94ec18f62aef3c3dc5baf99b85805b3ecd33b713693ce26ffe2c698c78992d5`。
- 独立SDK包：[cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz](../cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz)；SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；来源：https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz。
- 结论范围：Authentication/Core components -> IdentityManager -> BufferX/Dispatcher; registers Analytics IDs。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS19 · com.unity.services.analytics 6.3.0

- 原文：[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs):L42—87；方法：`IdentityManager constructor/Initialize`。
- 文件SHA256：`836cfa2da1f65e331103708136d00c4619f219a5d64669c7e1ab8395f76617c1`。
- 独立SDK包：[cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz](../cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz)；SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；来源：https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz。
- 结论范围：External UserId preferred else installation ID; UGS PlayerId separate property。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS20 · com.unity.services.analytics 6.3.0

- 原文：[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs):L373—395；方法：`BufferX event header writing`。
- 文件SHA256：`fdd07ac22a44caa6f208c5771d7bad0b115482344417b1dbbb2ab3167df859a4`。
- 独立SDK包：[cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz](../cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz)；SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；来源：https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz。
- 结论范围：Distinct player ID included in event payload, not automatically equal UserId。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS21 · com.unity.services.analytics 6.3.0

- 原文：[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/Dispatcher.cs](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/Dispatcher.cs):L93—158；方法：`Dispatcher.UploadCompleted`。
- 文件SHA256：`f055baf9d67ecd522042a012e33265270b13e1e707771c559ba51dc896727205`。
- 独立SDK包：[cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz](../cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz)；SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；来源：https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz。
- 结论范围：2xx and4xx both discard; network/5xx retain and flush disk; client ACK != training ACK。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS22 · com.unity.services.analytics 6.3.0

- 原文：[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/ConsentManager.cs](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/ConsentManager.cs):L51—104；方法：`ConsentManager.DataFrameworkConsentChanged`。
- 文件SHA256：`dce8647f1541b36008c67948784fab0133d9c12d33c903a19bb23533df430050`。
- 独立SDK包：[cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz](../cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz)；SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；来源：https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz。
- 结论范围：AnalyticsIntent handling; legacy flow cannot mix; not equivalent AdsIntent。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS23 · com.unity.services.analytics 6.3.0

- 原文：[cross-sdk/packages/services.analytics/6.3.0/extracted/package/CHANGELOG.md](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/CHANGELOG.md):L48—62；方法：`Official Analytics changelog6.1.0`。
- 文件SHA256：`a21895a1e783872637e7ca9d59a27efba3f952965cd5446255bc12d16eed7984`。
- 独立SDK包：[cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz](../cross-sdk/packages/services.analytics/6.3.0/services.analytics-6.3.0.tgz)；SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；来源：https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz。
- 结论范围：DDF integration and conditional automatic start; no unconditional collection。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS24 · Google/FirebaseRemoteConfig 24.0.1

- 原文：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/ConfigFetchHttpClient.java](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/ConfigFetchHttpClient.java):L321—363；方法：`ConfigFetchHttpClient.createFetchRequestBody`。
- 文件SHA256：`8f980968694d78eb401055ff06061c5ccffed300e6ce2e15262cbf5591ccaa7d`。
- 独立SDK包：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar)；SHA256：`1462c064e9b8b35ca7174e18c05b3cb7bc1f9121a5dd58c5d02cd18d8e8a4ea7`；来源：https://dl.google.com/dl/android/maven2/com/google/firebase/firebase-config/24.0.1/firebase-config-24.0.1.aar。
- 结论范围：FID not Analytics app instance ID; includes Analytics user properties/custom signals。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS25 · Google/FirebaseRemoteConfig 24.0.1

- 原文：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/RemoteConfigComponent.java](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/RemoteConfigComponent.java):L172—188；方法：`RemoteConfigComponent.get`。
- 文件SHA256：`cd88f0d114d7a52ef0f4f68dbff5c8c21126a2d94da4e9f5cdad95bbc29bc570`。
- 独立SDK包：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar)；SHA256：`1462c064e9b8b35ca7174e18c05b3cb7bc1f9121a5dd58c5d02cd18d8e8a4ea7`；来源：https://dl.google.com/dl/android/maven2/com/google/firebase/firebase-config/24.0.1/firebase-config-24.0.1.aar。
- 结论范围：value-read listener wired to personalization.logArmActive。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS26 · Google/FirebaseRemoteConfig 24.0.1

- 原文：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/Personalization.java](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/Personalization.java):L63—108；方法：`Personalization.logArmActive`。
- 文件SHA256：`e36c9b23c7ad6e274c1220d58625a31c11e3cde7b90d7ed355546a9b6aad2077`。
- 独立SDK包：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar)；SHA256：`1462c064e9b8b35ca7174e18c05b3cb7bc1f9121a5dd58c5d02cd18d8e8a4ea7`；来源：https://dl.google.com/dl/android/maven2/com/google/firebase/firebase-config/24.0.1/firebase-config-24.0.1.aar。
- 结论范围：assignment + internal choice event to Analytics; choice-level in-memory dedup。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS27 · Google/FirebaseRemoteConfig 24.0.1

- 原文：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/FirebaseRemoteConfig.java](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/FirebaseRemoteConfig.java):L688—710；方法：`FirebaseRemoteConfig.updateAbtWithActivatedExperiments`。
- 文件SHA256：`4cc14b2344ea1713e4958a0a61c199a7df8ef9d426c5dbdda0e639e93631837c`。
- 独立SDK包：[ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar](../ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/firebase-config-24.0.1.aar)；SHA256：`1462c064e9b8b35ca7174e18c05b3cb7bc1f9121a5dd58c5d02cd18d8e8a4ea7`；来源：https://dl.google.com/dl/android/maven2/com/google/firebase/firebase-config/24.0.1/firebase-config-24.0.1.aar。
- 结论范围：activated experiments -> FirebaseABTesting.replaceAllExperiments, optional provider。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS28 · AppLovin/Adapter-unityads-adapter 4.18.1.0

- 原文：[cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java](../cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java):L101—113；方法：`UnityAdsMediationAdapter.collectSignal`。
- 文件SHA256：`185fb359ddedf6c2bc29ac9c69beadfe41d7c31ad4f9b2c995ebcf923b46b555`。
- 独立SDK包：[ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.18.1.0/unityads-adapter-4.18.1.0.aar](../ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.18.1.0/unityads-adapter-4.18.1.0.aar)；SHA256：`f0c7f2474b214a75315b97ce360711db3e06fe3402e54a344cba8f34a71ee275`；来源：https://repo.maven.apache.org/maven2/com/applovin/mediation/unityads-adapter/4.18.1.0/unityads-adapter-4.18.1.0.aar。
- 结论范围：Privacy first -> Unity token -> MAX callback; token not a global user ID。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS29 · AppLovin/Adapter-unityads-adapter 4.18.1.0

- 原文：[cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java](../cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java):L268—284；方法：`UnityAdsMediationAdapter.updatePrivacyConsent`。
- 文件SHA256：`185fb359ddedf6c2bc29ac9c69beadfe41d7c31ad4f9b2c995ebcf923b46b555`。
- 独立SDK包：[ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.18.1.0/unityads-adapter-4.18.1.0.aar](../ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.18.1.0/unityads-adapter-4.18.1.0.aar)；SHA256：`f0c7f2474b214a75315b97ce360711db3e06fe3402e54a344cba8f34a71ee275`；来源：https://repo.maven.apache.org/maven2/com/applovin/mediation/unityads-adapter/4.18.1.0/unityads-adapter-4.18.1.0.aar。
- 结论范围：MAX consent and do-not-sell explicitly converted to Unity metadata。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS30 · AppLovin/Adapter-google-adapter 25.4.0.0

- 原文：[cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java](../cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java):L494—516；方法：`GoogleMediationAdapter ad request builder`。
- 文件SHA256：`1c92c2355638352e7ca74f0349b9860be3d8928259b4a46ada2e01b5918e42de`。
- 独立SDK包：[ThirdPartySDKs/AppLovin/Adapter-google-adapter/25.4.0.0/google-adapter-25.4.0.0.aar](../ThirdPartySDKs/AppLovin/Adapter-google-adapter/25.4.0.0/google-adapter-25.4.0.0.aar)；SHA256：`5b540214c1121410d72e8e1f757ad83a265f092f16850aec1507af255bac953b`；来源：https://repo.maven.apache.org/maven2/com/applovin/mediation/google-adapter/25.4.0.0/google-adapter-25.4.0.0.aar。
- 结论范围：MAX event_id -> Google placement_req_id; consent npa/rdp; request ID is not user ID。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS31 · AppLovin/MAX 13.7.0

- 原文：[cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java](../cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java):L181—195；方法：`EventServiceImpl.trackEvent`。
- 文件SHA256：`029ccc2c1f00a616b4ee50d444f7990fc47498954b57bf9ef55397de58fad9a1`。
- 独立SDK包：[ThirdPartySDKs/AppLovin/MAX/13.7.0/applovin-sdk-13.7.0.aar](../ThirdPartySDKs/AppLovin/MAX/13.7.0/applovin-sdk-13.7.0.aar)；SHA256：`58d01ce77af9786b4b2d393534a057738bae7fb65f9bb02de7264646b1c6a563`；来源：https://repo.maven.apache.org/maven2/com/applovin/applovin-sdk/13.7.0/applovin-sdk-13.7.0.aar。
- 结论范围：Remote-resolvable axon_events determines protocol; not every name generated automatically。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS32 · AppLovin/MAX 13.7.0

- 原文：[cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java](../cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java):L245—293；方法：`EventServiceImpl structured payload`。
- 文件SHA256：`029ccc2c1f00a616b4ee50d444f7990fc47498954b57bf9ef55397de58fad9a1`。
- 独立SDK包：[ThirdPartySDKs/AppLovin/MAX/13.7.0/applovin-sdk-13.7.0.aar](../ThirdPartySDKs/AppLovin/MAX/13.7.0/applovin-sdk-13.7.0.aar)；SHA256：`58d01ce77af9786b4b2d393534a057738bae7fb65f9bb02de7264646b1c6a563`；来源：https://repo.maven.apache.org/maven2/com/applovin/applovin-sdk/13.7.0/applovin-sdk-13.7.0.aar。
- 结论范围：event data + optional dedupe/user_data + visitInfo; familiar 13.6.4 path persists。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS33 · AppLovin/MAX 13.7.0

- 原文：[cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java](../cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java):L46—80；方法：`EventServiceImpl scheduler/postback builder`。
- 文件SHA256：`029ccc2c1f00a616b4ee50d444f7990fc47498954b57bf9ef55397de58fad9a1`。
- 独立SDK包：[ThirdPartySDKs/AppLovin/MAX/13.7.0/applovin-sdk-13.7.0.aar](../ThirdPartySDKs/AppLovin/MAX/13.7.0/applovin-sdk-13.7.0.aar)；SHA256：`58d01ce77af9786b4b2d393534a057738bae7fb65f9bb02de7264646b1c6a563`；来源：https://repo.maven.apache.org/maven2/com/applovin/applovin-sdk/13.7.0/applovin-sdk-13.7.0.aar。
- 结论范围：actual request construction code; not observed production request。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS34 · Adjust/Android 5.8.1

- 原文：[ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/DeviceInfo.java](../ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/DeviceInfo.java):L440—487；方法：`DeviceInfo.getFacebookAttributionId`。
- 文件SHA256：`34f4dae64b17cd417cfe87d84d80df05d696f6214c67289557bf5c3ce95835e0`。
- 独立SDK包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar](../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar)；SHA256：`98caabf85f07a6859767465c90394ee1e097c5da12f7bb967ea8f01f2272b84e`；来源：https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1.aar。
- 结论范围：official Facebook signature check -> exported attribution provider; no account login identity inferred。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS35 · Adjust/Android 5.8.1

- 原文：[ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/ActivityHandler.java](../ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/ActivityHandler.java):L2352—2404；方法：`ActivityHandler.processRemoteTriggersI`。
- 文件SHA256：`8b2ae7cae4dee5d3e0a1209f7ab9017571060e806151b304511edf620a3cab44`。
- 独立SDK包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar](../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar)；SHA256：`98caabf85f07a6859767465c90394ee1e097c5da12f7bb967ea8f01f2272b84e`；来源：https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1.aar。
- 结论范围：backend remote_triggers label/payload -> registered main-thread callback。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS36 · Adjust/Android 5.8.1

- 原文：[ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/ActivityHandler.java](../ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/ActivityHandler.java):L3503—3520；方法：`ActivityHandler.shouldProcessEventI`。
- 文件SHA256：`8b2ae7cae4dee5d3e0a1209f7ab9017571060e806151b304511edf620a3cab44`。
- 独立SDK包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar](../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar)；SHA256：`98caabf85f07a6859767465c90394ee1e097c5da12f7bb967ea8f01f2272b84e`；来源：https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1.aar。
- 结论范围：optional finite local event dedup, not global exact-once。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS37 · Adjust/Android 5.8.1

- 原文：[cross-sdk/adjust-changelog.raw](../cross-sdk/adjust-changelog.raw):L1—36；方法：`Adjust official CHANGELOG`。
- 文件SHA256：`eee45a63cc6c42b6d294e5f4adc18447382ddd6f1f27d4832bbfcb9f8645f996`。
- 独立SDK包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar](../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar)；SHA256：`98caabf85f07a6859767465c90394ee1e097c5da12f7bb967ea8f01f2272b84e`；来源：https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1.aar。
- 结论范围：5.6 remote triggers;5.7 sharing settings;5.8 disableDeviceIdsReading。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS38 · Singular Android 12.17.0

- 原文：[cross-sdk/java/singular-1217/com/singular/sdk/Singular.java](../cross-sdk/java/singular-1217/com/singular/sdk/Singular.java):L261—305；方法：`Singular.eventJSON/customRevenue`。
- 文件SHA256：`89c0115a1bf00d05c67fc376da9a3ecc2ba39cb2b259311eae941fe57f653529`。
- 独立SDK包：[cross-sdk/packages/singular/12.17.0/singular_sdk-12.17.0.aar](../cross-sdk/packages/singular/12.17.0/singular_sdk-12.17.0.aar)；SHA256：`fc126a348b9b9fb9bb56425a8210da41dc98a660930b2e8467b58615adfc7924`；来源：https://maven.singular.net/com/singular/sdk/singular_sdk/12.17.0/singular_sdk-12.17.0.aar。
- 结论范围：generic event -> SingularInstance.logEvent; caller-supplied revenue flag not verified purchase。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS39 · Singular Android 12.17.0

- 原文：[cross-sdk/java/singular-1217/com/singular/sdk/Singular.java](../cross-sdk/java/singular-1217/com/singular/sdk/Singular.java):L382—408；方法：`Singular.setCustomUserId/unsetCustomUserId`。
- 文件SHA256：`89c0115a1bf00d05c67fc376da9a3ecc2ba39cb2b259311eae941fe57f653529`。
- 独立SDK包：[cross-sdk/packages/singular/12.17.0/singular_sdk-12.17.0.aar](../cross-sdk/packages/singular/12.17.0/singular_sdk-12.17.0.aar)；SHA256：`fc126a348b9b9fb9bb56425a8210da41dc98a660930b2e8467b58615adfc7924`；来源：https://maven.singular.net/com/singular/sdk/singular_sdk/12.17.0/singular_sdk-12.17.0.aar。
- 结论范围：explicit SDK user ID setter; no target-game callsite or automatic MMP shared identity。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS40 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L188—240；方法：`PurchaseEventEmitter gateway endpoint and branch`。
- 文件SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：Literal endpoint belongs to Insights, not an explicitly named Vector training endpoint。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS41 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L127—157；方法：`FirebaseAnalyticsClient.FetchAppIdAsync`。
- 文件SHA256：`5f6d98d742761dd0e2213e57a7b33834439d6a48c7cedb635f9a76301e648b08`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：FirebaseApp options ApplicationId is app/project context, not per-user identity。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS42 · com.unity.purchasing 5.5.1

- 原文：[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/PurchaseService.cs](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/PurchaseService.cs):L314—337；方法：`PurchaseService purchase lifecycle callsite`。
- 文件SHA256：`38c1257d07cc7d485e267fce0b1ee54f74fde4f90d4e28ca73492e68d7ef61a9`。
- 独立SDK包：[cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz](../cross-sdk/packages/purchasing/5.5.1/purchasing-5.5.1.tgz)；SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；来源：https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz。
- 结论范围：SDK-internal concrete callsite, not target-game runtime observation。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

## XS43 · AppsFlyer/Android 6.17.5

- 原文：[rotate-rings/static/java/classes2.dex/g8/a.java](../rotate-rings/static/java/classes2.dex/g8/a.java):L100—126；方法：`Rotate original g8.a revenue wrapper`。
- 文件SHA256：`7c2c6b011ec46caed6c287ad292aa85aa51c16ed81fd81dcabc29ecc355c6c5a`。
- 独立SDK包：[ThirdPartySDKs/AppsFlyer/Android/6.17.5/af-android-sdk-6.17.5.aar](../ThirdPartySDKs/AppsFlyer/Android/6.17.5/af-android-sdk-6.17.5.aar)；SHA256：`af3f8e59f6ef5e0237fe7c53dd2040c0bb941688b4eb6a4c5b280143d377face`；来源：https://repo.maven.apache.org/maven2/com/appsflyer/af-android-sdk/6.17.5/af-android-sdk-6.17.5.aar。
- 结论范围：Original game USD double -> AFAdRevenueData; also ad_revenue2/ad_revenue4; consumer dedup unknown。目标游戏业务调用：True；生产发送/接收/训练：均未证实。

## XS44 · Adjust/Android 5.8.1

- 原文：[ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/PackageBuilder.java](../ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/PackageBuilder.java):L276—293；方法：`PackageBuilder session parameters`。
- 文件SHA256：`105476c7e4d3d235fcdd8146d798b55aba4761fd81505664c58a014f017f9721`。
- 独立SDK包：[ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar](../ThirdPartySDKs/Adjust/Android/5.8.1/adjust-android-5.8.1.aar)；SHA256：`98caabf85f07a6859767465c90394ee1e097c5da12f7bb967ea8f01f2272b84e`；来源：https://repo.maven.apache.org/maven2/com/adjust/sdk/adjust-android/5.8.1/adjust-android-5.8.1.aar。
- 结论范围：Explicit provider return -> fb_id request parameter; conditional null filtering。目标游戏业务调用：False；生产发送/接收/训练：均未证实。

