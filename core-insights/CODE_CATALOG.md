# 53—55 原始代码证据目录

仅静态读取官方发行包与固定提交公开绑定；未运行 SDK，未读取设备标识，未发送生产事件。

<a id="c53s01"></a>
## C53S01 · CorePackageInitializer.InitializeComponents/InitializeInstallationId

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Registration/CorePackageInitializer.cs:L111](sdk/core/1.19.0/extracted/package/Runtime/Registration/CorePackageInitializer.cs) · Core 1.19.0

Core registers two separate installation providers; initializes installation before project configuration.

文件 SHA256：`24c3a53b70441d17086579c1e3b5d817d3a10a18f6e4fb8ca693dc69b15901f1`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s02"></a>
## C53S02 · InstallationId.CreateIdentifier/GetOrCreateIdentifier

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/InstallationId.cs:L7](sdk/core/1.19.0/extracted/package/Runtime/Device/InstallationId.cs) · Core 1.19.0

Existing UnityInstallationId wins; otherwise copy engine ID; legacy fallback only when engine ID empty.

文件 SHA256：`ba2264ac6de4bbd1aca18070d4bb2d175acd2fc51caebec9f1a2949489eb3624`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s03"></a>
## C53S03 · EngineInstallationId.GetOrCreateIdentifier/CreateIdentifier

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/EngineInstallationId.cs:L7](sdk/core/1.19.0/extracted/package/Runtime/Device/EngineInstallationId.cs) · Core 1.19.0

Engine API under compile symbol; otherwise unity_connect.installation_id or new GUID.

文件 SHA256：`962581c4c64176efe335d4a56e7b360721a8864c16c3c2d6a30a44235ed9d430`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s04"></a>
## C53S04 · UnityEngineIdentifier.UserId

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityEngineIdentifier.cs:L5](sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityEngineIdentifier.cs) · Core 1.19.0

Explicit wrapper reads injected IEngineInstallationId; setter is no-op.

文件 SHA256：`3b0cb173f073056778398552d9d107e95efe83a45aabd943c03c0f23ddaa0bbd`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s05"></a>
## C53S05 · ExternalUserIdProperty.UserId/Dispose

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Core/ExternalUserIdProperty.cs:L8](sdk/core/1.19.0/extracted/package/Runtime/Core/ExternalUserIdProperty.cs) · Core 1.19.0

Conditional native userId alias vs memory-only fallback; subscription disposed.

文件 SHA256：`fbc52928798c9259f6d6900d3155b945d83d8c0194991fe2d00c4e40cb82f707`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s06"></a>
## C53S06 · ExternalUserId.UserId/UserIdChanged

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Configuration/ExternalUserId.cs:L6](sdk/core/1.19.0/extracted/package/Runtime/Configuration/ExternalUserId.cs) · Core 1.19.0

IExternalUserId resolves shared UnityServices.ExternalUserIdProperty.

文件 SHA256：`e7a50c127e866f15b344de5c2f4531fb3bb3911ec031ce59cbacd4effba33bef`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s07"></a>
## C53S07 · versionDefines

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Core/Unity.Services.Core.asmdef:L1](sdk/core/1.19.0/extracted/package/Runtime/Core/Unity.Services.Core.asmdef) · Core 1.19.0

Exact version intervals for UNITY_SUPPORTS_IDENTIFIERS_USER_ID; platform flag separately required.

文件 SHA256：`cf756830cc494eb0037e38a3519ce0c20bf0fd017cd8d72d69a8c0d517be80ab`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s08"></a>
## C53S08 · UnityServices.ExternalUserId/ResetStaticsOnLoad

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Core/UnityServices.cs:L79](sdk/core/1.19.0/extracted/package/Runtime/Core/UnityServices.cs) · Core 1.19.0

Native branch persistence is documented; fallback memory; reset disposes/replaces property.

文件 SHA256：`40f4b962fb731287dc5fbdd2e44daf29fbccbcee226989a0a782159ea7898638`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s09"></a>
## C53S09 · UnityAdsIdentifier.UserId

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityAdsIdentifier.cs:L3](sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityAdsIdentifier.cs) · Core 1.19.0

Legacy Ads IDFI uses application private preferences, not GAID.

文件 SHA256：`bc440fd6a573be811fea221dc255d60ffdb68b64baa90bd1cfeb47f7b3145f7c`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s10"></a>
## C53S10 · UnityAnalyticsIdentifier.UserId

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityAnalyticsIdentifier.cs:L6](sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityAnalyticsIdentifier.cs) · Core 1.19.0

Legacy unity.cloud_userid read/write fallback.

文件 SHA256：`162bd2223eed3acced6d656777f156e7c7ab73736d88ffb184e6ada36aaffdec`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s11"></a>
## C53S11 · AndroidUtils.GetSharedPreferences/SharedPreferencesPutString

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/AndroidUtils.cs:L7](sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/AndroidUtils.cs) · Core 1.19.0

current Activity context; MODE_PRIVATE; not shared cross-app storage.

文件 SHA256：`082f1b9c35543bd5ad87c5397b95d3e184af3694b35b11a6e5e2db9bc43fbde7`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s12"></a>
## C53S12 · AuthenticationPackageInitializer.InitializeService

[identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Core/AuthenticationPackageInitializer.cs:L77](../identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Core/AuthenticationPackageInitializer.cs) · Authentication 3.9.0

PlayerIdComponent registered by Authentication, not Core; Engine ID also used by network client.

文件 SHA256：`aa3003a5b1262208e1e215befdce2c8305eab6a28d66e4e7c16035add16afc72`。

原包 SHA256：`bf9efe33dc39a09756ee3defd0d621366a05a926793104a10c5d49c9582d4dde`；[官方来源](https://download.packages.unity.com/com.unity.services.authentication/-/com.unity.services.authentication-3.9.0.tgz)。

<a id="c53s13"></a>
## C53S13 · PlayerIdComponent

[identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Components/PlayerIdComponent.cs:L6](../identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Components/PlayerIdComponent.cs) · Authentication 3.9.0

player_id cache; Clear/Refresh/set and change callback.

文件 SHA256：`04b0a7cb4ab848c628403782449f951ecac89166130d8c737d1fcf34c2e119e2`。

原包 SHA256：`bf9efe33dc39a09756ee3defd0d621366a05a926793104a10c5d49c9582d4dde`；[官方来源](https://download.packages.unity.com/com.unity.services.authentication/-/com.unity.services.authentication-3.9.0.tgz)。

<a id="c53s14"></a>
## C53S14 · AuthenticationCache.Prefix/GetKey

[identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Utilities/Cache/AuthenticationCache.cs:L7](../identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Utilities/Cache/AuthenticationCache.cs) · Authentication 3.9.0

Cache prefix is CloudProjectId.Profile; not global account/device scope.

文件 SHA256：`4d4d53d95c14e8fa12fb7fcfbaaceb3c63ed17e364cd850c5989f74995984553`。

原包 SHA256：`bf9efe33dc39a09756ee3defd0d621366a05a926793104a10c5d49c9582d4dde`；[官方来源](https://download.packages.unity.com/com.unity.services.authentication/-/com.unity.services.authentication-3.9.0.tgz)。

<a id="c53s15"></a>
## C53S15 · AuthenticationServiceInternal.SignOut/SwitchProfile

[identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs:L224](../identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs) · Authentication 3.9.0

SignOut clears PlayerId only if clearCredentials; profile switch refreshes cache.

文件 SHA256：`700da3842fc1b7842a33bf3e06bf172d2e98e47ce6cf5c6c2e0fa3ee6a40520f`。

原包 SHA256：`bf9efe33dc39a09756ee3defd0d621366a05a926793104a10c5d49c9582d4dde`；[官方来源](https://download.packages.unity.com/com.unity.services.authentication/-/com.unity.services.authentication-3.9.0.tgz)。

<a id="c53s16"></a>
## C53S16 · AuthenticationServiceInternal sign-in completion

[identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs:L425](../identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs) · Authentication 3.9.0

PlayerId assigned from decoded token Subject, distinct from engine installation ID.

文件 SHA256：`700da3842fc1b7842a33bf3e06bf172d2e98e47ce6cf5c6c2e0fa3ee6a40520f`。

原包 SHA256：`bf9efe33dc39a09756ee3defd0d621366a05a926793104a10c5d49c9582d4dde`；[官方来源](https://download.packages.unity.com/com.unity.services.authentication/-/com.unity.services.authentication-3.9.0.tgz)。

<a id="c53s17"></a>
## C53S17 · AnalyticsService.Initialize

[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs:L49](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs) · Analytics 6.3.0

IInstallationId/IPlayerId/IExternalUserId consumers and project/environment collect URL.

文件 SHA256：`b94ec18f62aef3c3dc5baf99b85805b3ecd33b713693ce26ffe2c698c78992d5`。

原包 SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；[官方来源](https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz)。

<a id="c53s18"></a>
## C53S18 · IdentityManager constructor/Initialize/ExternalUserIdChanged

[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs:L22](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs) · Analytics 6.3.0

InstallId captured; UserId external-first; PlayerId live read; local migration and identity change.

文件 SHA256：`836cfa2da1f65e331103708136d00c4619f219a5d64669c7e1ab8395f76617c1`。

原包 SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；[官方来源](https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz)。

<a id="c53s19"></a>
## C53S19 · BufferX.PushStandardEventStart/PushCommonEventStart

[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs:L366](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs) · Analytics 6.3.0

Standard-event installationID/playerID vs common userID/sessionID/eventUUID; not every custom event contains every ID.

文件 SHA256：`fdd07ac22a44caa6f208c5771d7bad0b115482344417b1dbbb2ab3167df859a4`。

原包 SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；[官方来源](https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz)。

<a id="c53s20"></a>
## C53S20 · CoreRegistryHelper.InstallationId/Resolve

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs:L27](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs) · IAP 5.5.1

IAP InstallationId property explicitly resolves IEngineInstallationId; optional player/external components.

文件 SHA256：`212bfdbd42cc46be3de42704ef19e6739aa66563e331df6d685902ea5e3bf7c0`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s21"></a>
## C53S21 · PlayerData.CreatePlayerIdentityAsync/FetchEnabledFirebaseIdsAsync

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs:L90](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs) · IAP 5.5.1

AdsIntent/allowlist gated GAID/IDFA/Firebase; IDFV independent; session preference; per-instance caches.

文件 SHA256：`13233ab6ea00e470aaba64f2c3d5bb966a71d5d2ed117c0aacc3c3dc52619528`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s22"></a>
## C53S22 · PurchaseEventEmitter.Send*Event

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs:L44](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs) · IAP 5.5.1

Intent/paid/failed/fulfilled/payment options SDK callbacks; fire-and-forget.

文件 SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s23"></a>
## C53S23 · PurchaseEventEmitter.Forward/ForwardModule/ForwardGateway

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs:L188](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs) · IAP 5.5.1

Compile-time exclusive routes; protobuf POST vs base64 LogEvent(1000); no per-event ACK/retry in wrapper.

文件 SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s24"></a>
## C53S24 · PurchaseEventEmitter.BuildEnvelope/MapIdentity/BuildSku

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs:L243](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs) · IAP 5.5.1

UUID/time; identity mappings; metadata price * 1e6; quantity separate; UnityAdsIdfi not assigned.

文件 SHA256：`dd21045ac9c2cf64abdaf45b3f38253866383f64c40dc1ff7534d1b296dc48e2`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s25"></a>
## C53S25 · PurchaseEventProtobufWriter complete serializer

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs:L14](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs) · IAP 5.5.1

Exact emitted field numbers/wire forms and submessages; no original .proto bundled.

文件 SHA256：`4ba0c2a596d7b8218ec45034b4c6d75aec20da89fb9e1157e964c355c9e656cd`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s26"></a>
## C53S26 · IAPSDKEvent and lifecycle variants

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/IAPSDKEvent.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/IAPSDKEvent.cs) · IAP 5.5.1

Envelope and enum definitions; six oneof alternatives, not six revenue events.

文件 SHA256：`def4208c4a2350e5fa172964ad25b876df7586df64883953a4f8e272cfc17079`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s27"></a>
## C53S27 · PlayerIdentity

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/PlayerIdentity.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/PlayerIdentity.cs) · IAP 5.5.1

Optional identity DTO fields; schema presence alone does not populate them.

文件 SHA256：`364d17441408e6b38a8f978ae24cb64945dbc9975f6aa0253db9cfea2e5b1917`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s28"></a>
## C53S28 · ConnectionsSettingsClient.CachedEnabledAttributes/ParseEnabledAttributes/PostAsync

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs:L15](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs) · IAP 5.5.1

Fail-closed per-session allowlist and project/install request; not event-level ACK.

文件 SHA256：`ab0cc755e98a056ac539775b72e3c539d82fbb207f2feea41ef0f7d68c222650`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s29"></a>
## C53S29 · FirebaseAnalyticsClient getters

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs:L60](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs) · IAP 5.5.1

Firebase Analytics AppInstanceId/SessionId and Firebase App options ApplicationId; not FirebaseInstallations FID.

文件 SHA256：`5f6d98d742761dd0e2213e57a7b33834439d6a48c7cedb635f9a76301e648b08`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s30"></a>
## C53S30 · SessionEventEmitter.SendAuthenticationCompleteEvent/BuildEnvelope

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/SessionEventEmitter.cs:L18](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/SessionEventEmitter.cs) · IAP 5.5.1

SignedIn creates a real DTO/writer path; no store/order; not a purchase label.

文件 SHA256：`cb767cbd16c677edc31b6c3cf961cf71fb9cf40442955ae1389a2a82e18d007f`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s31"></a>
## C53S31 · IapCoreInitializeCallback.InitializeSessionEvents/PrefetchConnectionsSettings

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/IapCoreInitializeCallback.cs:L24](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/IapCoreInitializeCallback.cs) · IAP 5.5.1

Conditional Authentication.SignedIn subscription and reset cleanup; allowlist prefetch.

文件 SHA256：`8c89d3499dd2abcf2c309fdca651b2ae948d5d80900514323c8475d2b2951636`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s32"></a>
## C53S32 · ImpressionScope

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Insights/ImpressionScope.cs:L8](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Insights/ImpressionScope.cs) · IAP 5.5.1

impression_id is AsyncLocal purchase-journey GUID, not an ad impression ID.

文件 SHA256：`978ff968ccc2fd9fb619c0d194192540787c60d5d08b6855ed75149cdecde3fd`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s33"></a>
## C53S33 · RequiresInsights assembly declaration

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Editor/AssemblyInfo.cs:L9](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Editor/AssemblyInfo.cs) · IAP 5.5.1

Conditional package requirement registration.

文件 SHA256：`f6ac95676134cc249838ba7cc54c2f44bc4bb06eb36918ba3c874a7f57b94217`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s34"></a>
## C53S34 · versionDefines

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Unity.Purchasing.Stores.asmdef:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Unity.Purchasing.Stores.asmdef) · IAP 5.5.1

Exact SDK feature/Insights compile-time version definitions.

文件 SHA256：`cf2008c9919bbe978fea96ca874600cd8a37e00b7cc5bbb6d25948057bdb02d1`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s35"></a>
## C53S35 · EngineDiagnostics.LogEvent/IsEventAllowed/SetBlockedEventTypes

[core-insights/EngineDiagnostics-6000-7.raw:L14](EngineDiagnostics-6000-7.raw) · Runtime pinned public branch or dated document

Pinned 6000.7 C# boundary; native queue/receiver/ACK not public.

文件 SHA256：`6eff26a09b592e746a4a31321ae6f7a83cd9751bbb6b97f7a60f7c4afed9d353`。

[公开来源](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/2f32630a2ce9ba2e692c9968c96ed39418d4ea2c/Modules/Insights/EngineDiagnostics.bindings.cs)。

<a id="c53s36"></a>
## C53S36 · Identifiers.installationId/userId

[core-insights/Identifiers-6000-7.raw:L13](Identifiers-6000-7.raw) · Runtime pinned public branch or dated document

Native installation getter/userID setter; 1024-char limit; persistence documented but native store invisible.

文件 SHA256：`098bfa4ac5fae954471e7729672ac63dd54cd0b2276693254a6405534ce2e7fe`。

[公开来源](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/2f32630a2ce9ba2e692c9968c96ed39418d4ea2c/Modules/Identifiers/Identifiers.bindings.cs)。

<a id="c53s37"></a>
## C53S37 · RequiresInsightsAttribute/CollectionRequirement

[core-insights/RequiresInsights-6000-7.raw:L11](RequiresInsights-6000-7.raw) · Runtime pinned public branch or dated document

Package requirement kept even if Engine Diagnostics project setting disabled; unsupported platforms excluded.

文件 SHA256：`93be105c5b44424c04f94e908f9338d3aabe5a26ace23e981809544f863af11c`。

[公开来源](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/2f32630a2ce9ba2e692c9968c96ed39418d4ea2c/Modules/InsightsEditor/RequiresInsightsAttribute.cs)。

<a id="c53s38"></a>
## C53S38 · Identifiers 6000.6 binding

[core-insights/Identifiers-6000-6.raw:L10](Identifiers-6000-6.raw) · Runtime pinned public branch or dated document

Separate pinned 6000.6 branch, not assumed identical to target-engine patch.

文件 SHA256：`9b509943e9d80e9bc3cc256e586f24b1f7768430e681dc1afd5237dc45c20c98`。

[公开来源](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/dea82c432a5c6c695472ffc5996ccc8057f9971f/Modules/Identifiers/Identifiers.bindings.cs)。

<a id="c53s39"></a>
## C53S39 · EngineDiagnostics 6000.6 binding

[core-insights/EngineDiagnostics-6000-6.raw:L11](EngineDiagnostics-6000-6.raw) · Runtime pinned public branch or dated document

Public native interface exists before IAP new routing gate; availability != chosen SDK route.

文件 SHA256：`a86051b88e40b26ba73f1339a77d3fd41eea18e118a34311e8e7efdb5df59236`。

[公开来源](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/dea82c432a5c6c695472ffc5996ccc8057f9971f/Modules/Insights/EngineDiagnostics.bindings.cs)。

<a id="c53s40"></a>
## C53S40 · Unity IAP privacy overview

[core-insights/iap-privacy-overview.txt:L24](iap-privacy-overview.txt) · Document pinned public branch or dated document

Default purchase telemetry; optional consent-gated IDs; IAP operation and revenue reporting; 6000.7 Insights; retention and roles.

文件 SHA256：`6c4801c3003109a6e4065feda446b51e574571c3937b4b421a935b15d104802c`。

[公开来源](https://docs.unity.com/en-us/iap/privacy-and-consent/overview.md)。

<a id="c53s41"></a>
## C53S41 · Core 1.19.0 official changelog

[core-insights/sdk/core/1.19.0/extracted/package/CHANGELOG.md:L1](sdk/core/1.19.0/extracted/package/CHANGELOG.md) · Core 1.19.0

Official ExternalUserId engine delegation release statement.

文件 SHA256：`2a771b1b0f171c141fc91e4039149228c8d974edfc5e9073e7d75e002948afbe`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s42"></a>
## C53S42 · IAP 5.5.1/5.4.x official changelog

[cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md) · IAP 5.5.1

Firebase session serialization fix and Core1.19 dependency; optional connections restrictions.

文件 SHA256：`e9e1ccf5647901070585f96e97a8daaa861aaf558032f9794f956ac2594b1131`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s43"></a>
## C53S43 · SessionManager.StartNewSession

[cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/SessionManager.cs:L12](../cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/SessionManager.cs) · Analytics 6.3.0

Analytics session is generated GUID; no equality to IAP unity_connect.session_id.

文件 SHA256：`f23185d1779a154e5c4c5ab157040855b95bce4b6db46de8c0cb58bc11d47180`。

原包 SHA256：`bc1f64b7c3432aa7209ed37d0db5a53e3044507d77326845069de891d57b8910`；[官方来源](https://download.packages.unity.com/com.unity.services.analytics/-/com.unity.services.analytics-6.3.0.tgz)。

<a id="c53s44"></a>
## C53S44 · GooglePlayStoreExtendedPurchaseService.Send*Event

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs:L45](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs) · IAP 5.5.1

Actual SDK purchase service overrides invoke emitter.

文件 SHA256：`21622106306172a42b6ab04227c9b3a2632fe07257adf0db7c783f39e7bf1493`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s45"></a>
## C53S45 · AppInstallInfo.GetInstallTimestamp/FetchInstallTimestamp

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/AppInstallInfo.cs:L24](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/AppInstallInfo.cs) · IAP 5.5.1

Android firstInstallTime ms -> UTC; iOS directory time approximation; null other platforms.

文件 SHA256：`3a48f3b9a678a42251c9764340d8089551191edce7cbc4d75c1115e542e53f4b`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s46"></a>
## C53S46 · PaymentOption enum

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Insights/PaymentOption.cs:L5](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Insights/PaymentOption.cs) · IAP 5.5.1

Payment options wire values including Webshop; not proof each provider used.

文件 SHA256：`0829a7d1c2767a282e21a13df0a2cb23127a1c5895b07a14405a3ec3f063e592`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s47"></a>
## C53S47 · ConsentState/DataCollectionMode

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/Consent.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/Consent.cs) · IAP 5.5.1

Proto consent enum differs from UnityConsent API ordinal values; explicit mapping required.

文件 SHA256：`c4a3555fe3d15c5a9318db03af4b065f57600bb10fe478673e6a07b9ebe495fa`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s48"></a>
## C53S48 · DeviceInfo

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/DeviceInfo.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/DeviceInfo.cs) · IAP 5.5.1

Complete public device-info model; byte quantities and boot-time source require native provider context.

文件 SHA256：`6d2353a9dd853071d161c44800240ca00d7526247c2c28f6d051b85d4a6b6775`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s49"></a>
## C53S49 · OrderData/Sku/Store/ProductType

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/OrderData.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/OrderData.cs) · IAP 5.5.1

Complete public SKU/order schema types and enum values.

文件 SHA256：`7ef440861bfed28c8cd73c0bd1d887f4301018b57b52e730b180db2164451138`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s50"></a>
## C53S50 · StorePayload/OwnershipType

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/StorePayload.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/StorePayload.cs) · IAP 5.5.1

Store-specific transaction evidence fields and ownership enumeration.

文件 SHA256：`26f4f7a0d722d5d5694cea36762f34ceb4c897d81c2ec8532771d2ddcaa3e069`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s51"></a>
## C53S51 · EventType.IapSdk

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/EventType.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/EventType.cs) · IAP 5.5.1

IAP producer type is 1000, distinct from lifecycle oneof field numbers.

文件 SHA256：`368f88db3b71c3b90d0106028ef957c93d3a3e6ea48ed0e18c9b352e1a4b2de0`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s52"></a>
## C53S52 · Reporting

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/Reporting.cs:L1](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/Reporting.cs) · IAP 5.5.1

Platform and bundle ID; application context, not individual identity.

文件 SHA256：`90a41cab56feb496de906a607636f48aec8ea090b523d82c9a23c3984dfb729b`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s53"></a>
## C53S53 · PlayerData session preference and optional Analytics getter

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs:L23](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs) · IAP 5.5.1

IAP reads engine session preference; Analytics ID getter optional and handles uninitialized services.

文件 SHA256：`13233ab6ea00e470aaba64f2c3d5bb966a71d5d2ed117c0aacc3c3dc52619528`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。

<a id="c53s54"></a>
## C53S54 · CorePackageInitializer.InitializeExternalUserId

[core-insights/sdk/core/1.19.0/extracted/package/Runtime/Registration/CorePackageInitializer.cs:L255](sdk/core/1.19.0/extracted/package/Runtime/Registration/CorePackageInitializer.cs) · Core 1.19.0

Compatibility analytics-user-id option only fills empty ExternalUserId.

文件 SHA256：`24c3a53b70441d17086579c1e3b5d817d3a10a18f6e4fb8ca693dc69b15901f1`。

原包 SHA256：`cc62fb2eb916a5592bb5a5e31260f5bed7c71a6e5d495e4cfc206c319a9fe2a9`；[官方来源](https://download.packages.unity.com/com.unity.services.core/-/com.unity.services.core-1.19.0.tgz)。

<a id="c53s55"></a>
## C53S55 · PurchaseService.Purchase/InvokePurchasePendingEvent

[cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/PurchaseService.cs:L250](../cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/PurchaseService.cs) · IAP 5.5.1

Real SDK entry starts a purchase journey and intent; pending callback reports paid.

文件 SHA256：`38c1257d07cc7d485e267fce0b1ee54f74fde4f90d4e28ca73492e68d7ef61a9`。

原包 SHA256：`cf382958920ef886c51998988153ac55d6682fbd79d79cfb34362d7973ca9403`；[官方来源](https://download.packages.unity.com/com.unity.purchasing/-/com.unity.purchasing-5.5.1.tgz)。
