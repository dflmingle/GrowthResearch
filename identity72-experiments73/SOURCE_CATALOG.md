# 72身份审计＋73实验：来源目录

UTC:2026-11-20T05:27:46.711048+00:00。与此前72数据访问专题并存，全部历史报告保留。

## 静态调用链

| ID | 组件版本 | 原始位置 | 能证层级 |
|---|---|---|---|
| IG72C01 / MAX-GAID | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/v.java:87 | E1，生产匹配/入模未证 |
| IG72C02 / MAX-AppSet-start | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/i1.java:1 | E1，生产匹配/入模未证 |
| IG72C03 / MAX-AppSet-result | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/i1$a.java:1 | E1，生产匹配/入模未证 |
| IG72C04 / MAX-device-payload | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java:1328 | E1,E2，生产匹配/入模未证 |
| IG72C05 / MAX-app-payload | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java:884 | E1,E2，生产匹配/入模未证 |
| IG72C06 / MAX-user-normalization | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/r7.java:24 | E1，生产匹配/入模未证 |
| IG72C07 / MAX-structured-device | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/y6.java:1 | E1，生产匹配/入模未证 |
| IG72C08 / MAX-cuid-manager | AppLovin/MAX 13.6.4 | identity-graph/sdk/max-13.6.4/java/com/applovin/impl/t7.java:1 | E1，生产匹配/入模未证 |
| IG72C09 / AXON-appset-result | AppLovin/Axon 1.3.4 | identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/g0.java:1 | E1，生产匹配/入模未证 |
| IG72C10 / UPA-oauth-start | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/PlayerAccountServiceInternal.cs:63 | E1,E2，生产匹配/入模未证 |
| IG72C11 / UPA-oauth-request | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/PlayerAccountServiceInternal.cs:154 | E1,E2，生产匹配/入模未证 |
| IG72C12 / UPA-oauth-result | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/PlayerAccountServiceInternal.cs:229 | E1,E2，生产匹配/入模未证 |
| IG72C13 / UPA-id-claims | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/Models/IdToken.cs:1 | E1，生产匹配/入模未证 |
| IG72C14 / UGS-external-link | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.External.cs:327 | E1,E2，生产匹配/入模未证 |
| IG72C15 / UGS-project-context | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Network/AuthenticationNetworkClient.cs:110 | E1,E2，生产匹配/入模未证 |
| IG72C16 / UGS-token-scope | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Security/AccessToken.cs:1 | E1，生产匹配/入模未证 |
| IG72C17 / UGS-unity-id | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/PlayerInfo.cs:185 | E1，生产匹配/入模未证 |
| IG72C18 / UGS-identity-model | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Identity.cs:1 | E1，生产匹配/入模未证 |
| IG72C19 / UGS-network-endpoints | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Network/AuthenticationNetworkClient.cs:15 | E1，生产匹配/入模未证 |
| IG72C20 / AXON-user-normalization | AppLovin/Axon 1.3.4 | identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/l3.java:25 | E1，生产匹配/入模未证 |
| IG72C21 / UNITY-ads-privacy | Unity/Ads 4.18.1 | vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java:20 | E1,E2，生产匹配/入模未证 |
| IG72C22 / UNITY-ads-identity-repository | Unity/Ads 4.17.0 | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidDeviceInfoRepository.kt:20 | E1，生产匹配/入模未证 |
| IG72C23 / UNITY-ads-idfi-auid | Unity/Ads 4.17.0 | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt:213 | E1，生产匹配/入模未证 |
| IG72C24 / UNITY-ads-analytics-source | Unity/Ads 4.17.0 | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidAnalyticsDataSource.kt:1 | E1，生产匹配/入模未证 |
| IG72C25 / UNITY-ads-initialization-identities | Unity/Ads 4.17.0 | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetInitializationRequestPayload.kt:26 | E1,E2，生产匹配/入模未证 |
| IG72C26 / UNITY-ads-shared-privacy | Unity/Ads 4.17.0 | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt:18 | E1,E2，生产匹配/入模未证 |
| IG72C27 / UNITY-ads-PII-gates | Unity/Ads 4.17.0 | ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt:20 | E1,E2，生产匹配/入模未证 |
| IG72C28 / UGS-PlayerId-token | Unity Authentication/Player Accounts 3.9.0 package | identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs:434 | E1，生产匹配/入模未证 |

## 官方契约与数据发布者

| ID | URL | SHA256 | 等级/边界 |
|---|---|---|---|
| IG72S01 | https://developer.android.com/identity/app-set-id | `0cc8467649d695ddd7f62c6b5c870f2fae77c53005f0532b6e6dad4f1025be84` | E3；Google App Set ID scope/reset and permitted usage;not global personal identity |
| IG72S02 | https://docs.unity.com/en-us/authentication/unity-player-accounts.md | `855d1cbba7a24d89ac84026f09045a14c9449b43d73cf902cb2a27e41f646154` | E3,E4；Explicit org-scoped account persistence across games/devices;not Vector consumption |
| IG72S03 | https://docs.unity.com/en-us/authentication/identity-management.md | `0eceb6f88c8b4aacd70ba8b04f276abd1fddc02dcd8c86e268828373b099fbcf` | E3,E4；Link/unlink external identities,conflict constraints;not automatic unconsented merge |
| IG72S04 | https://liveramp.com/our-platform/rampid | `90390b9360436b654f34684b1dc04cadb0ff257e7e1ff0c99d0f42ec7cc735e3` | E3,E4；Commercial identity resolution/activation product;not measured Unity match rate |
| IG72S05 | https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming | `e2124f8e22357e85d8934c612f24483367a154bf7b25a42fbabe59c5746fc818` | E3,E4；US/Canada Exchange RampID activation requires receiving partner support;not confirmed Vector input |
| IG72S06 | https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api | `a4360a00852221596f3688d073411a4f45c69c5f63b26be3f60c4742db66e93a` | E3；Merchant customer/click/contact/transaction inputs,not observed game cross-business join |
| IG72S07 | https://www.applovin.com/privacy/ | `3277dda04bb545a07d4c8e2b6f0c58daaf113815004d6ec5d34066a64402701c` | E3；Privacy scope is not a particular production identity mapping |
| IG72S08 | https://www.wurl.com/ | `37cb7c7be2a963d33a956909c9057080952b0f5a7a4f88d6a59076bcb1937601` | E3；CTV advertising/content business;not evidence of personal game training join |
| IG72S09 | https://unifiedid.com/docs/intro | `8ae279d0e4e11e1da20ea6943fc299f4763b3bacf33631a5ebe6892249535adf` | E3,E4；Explicit analytics/identity service contract;not proof of Axon/Vector integration |
| IG72S10 | https://docs.mixpanel.com/docs/tracking-methods/id-management/identifying-users-simplified | `f742e6571f65c67b3e67beb9812e5cf8da338c8a2b0018d460a44347a36f4e6f` | E3,E4；Explicit analytics/identity service contract;not proof of Axon/Vector integration |
| IG72S11 | https://amplitude.com/docs/data/sources/instrument-track-unique-users | `83efce369ac87a519df80bcf399a9798ebeadca10ae2808fed694256b671c227` | E3,E4；Explicit analytics/identity service contract;not proof of Axon/Vector integration |
| IG72S12 | https://help.branch.io/developers-hub/docs/android-advanced-features | `2af44325e9998ce8a51e313447c1457fa0503cd210055e8f69dfcee00fe45653` | E3,E4；Explicit analytics/identity service contract;not proof of Axon/Vector integration |
| IG72S13 | https://firebase.google.com/docs/analytics/userid | `9e2a36fac098765d3c923650a36e4ca90bb286b3afd6e696a49026bb3ada042d` | E3,E4；Explicit analytics/identity service contract;not proof of Axon/Vector integration |
| EX73S01 | https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/ | `0ac075ca9c576a6eadb7db2681e934032a85ed54713d88d429f9ee933086e9a8` | 数据准入证据，非平台身份等级；Real sampled displayed impressions,30-day conversion label;noncommercial restricted;no training |
| EX73S02 | https://zenodo.org/api/records/13932202 | `1095d994b901e5c668fb50dd7448d62c242bd2998638e369a08a8bcb29bafb4b` | 数据准入证据，非平台身份等级；Official synthetic matching dataset Apache2.0 metadata |
| EX73S03 | https://www.amazon.science/publications/bpid-a-benchmark-for-personal-identity-deduplication | `40074c59dfc3fe119230ee62a50e7b217e93c75a82ac43e8a733715da2b927da` | 数据准入证据，非平台身份等级；Original publisher confirms synthetic profiles not real individuals |
| EX73S04 | https://www.kaggle.com/competitions/talkingdata-mobile-user-demographics/data | `fecedce96d38e3031993aa5ac9107a282524eb774e3e92caeb212afa3da7d81d` | 数据准入证据，非平台身份等级；HTML shell only;no accepted competition rules/files |
| EX73S05 | https://www.kaggle.com/competitions/talkingdata-mobile-user-demographics/rules | `332b4df05bae1b165ff0d083ae4a439cf96f32751d0c3c30fd35dea308898aac` | 数据准入证据，非平台身份等级；Rules shell only;not licence to train |

全部精确摘录和源文件哈希见CODE_EVIDENCE、PIXEL_EVIDENCE、SOURCE_EVIDENCE；原始AAR/JAR哈希见ARCHIVE_INVENTORY，原分析JAR哈希见代码对象。既有图对象复用见REUSED_EVIDENCE；不将E1/E2提升为E5/E6。

BPID完整ZIP58,115,842字节，发布MD5及ZIP CRC核验见BPID_ARCHIVE_AUDIT。论文与原作者明确synthetic，只有匹配数据有人工标签；1M blocking记录无实体簇真值。本地未输出档案值，未关联外部身份。

TalkingData只取得Kaggle网页壳，未登录、未接受竞赛规则，未下载镜像。Criteo CC BY-NC-SA4.0用途资格未确认，仅读字段/许可，未下载原始行、未训练。三份数据从不互相join。

PREREGISTRATION在实验前保存；结果B/D是两种不同的合成实验，不是实际设备图谱、LTV或ROAS。所有结果文件和脚本哈希将在验证清单留存。
