# 第三方 SDK 收集清单与来源验证

2026-11-18。原始发行包统一存放于 `D:/GrowthResearch/ThirdPartySDKs/<供应商>/<SDK>/<版本>/`。本轮只下载公开发行材料并静态分析，没有初始化SDK、运行广告请求或修改原包/游戏工程。

**已收集 103 个 AAR、67 个 Maven/JitPack sources JAR，覆盖 124 个有 provenance 的版本目录；另有 TikTok 两个准确标签的官方 GitHub 源码 ZIP。**原始已登记发行材料约 106.4 MiB（不含提取副本/GitHub ZIP）。其中20个目录未取得二进制，不算成功收集SDK。完整结果包括失败尝试，不是目录数量等于SDK数量。

这是一份按本轮优先级实际取得的全量清单，**不是所有适配器及传递依赖均已下载的宣称**。归因/MAX主链已深入；其余网络已收集发行包/部分源码和适配器，但没有逐个恢复全部闭源内部实现。

原包已有BuildConfig证据覆盖的**45个MAX适配器版本现均已取得AAR**（含Bigo坐标纠正）；见[ADAPTER_COVERAGE](ThirdPartySDKs/ADAPTER_COVERAGE.json)。未取得的是部分网络的独立核心或其他传递依赖，不是把适配器当作网络完整SDK。

## 来源、版本和许可如何核验

- 【官方 SDK 代码证实】匹配版本来自原包 `AppLovinSdk.getVersion()`、Adjust `Constants.CLIENT_SDK`、AF版本签名等；适配器版本另存，不能替代core版本。
- 下载来源：Maven Central、Google Maven、厂商公开Maven、官方GitHub/JitPack标签；不是二次打包站。每个版本目录保留AAR/POM/sources、提取的classes.jar、provenance、归档索引；无classes.jar的依赖壳保留其POM。
- SHA256、完整URL、UTC、HTTP状态、Last-Modified、POM许可证与依赖详见[CATALOG](ThirdPartySDKs/CATALOG.json)。下载成功不自动等于可自由再分发；闭源SDK按其EULA，公开sources也不自动等于宽松开源。
- HTTP Last-Modified是仓库对象时间，metadata lastUpdated是索引更新时间，**都不伪装成首次发布日期**。已另存Adjust GitHub release的published_at；其他没有可信日期的记为未知。
- 【无法确认】未取得AppsFlyer sources JAR；已下载的AAR可反编译。AppLovin sources JAR主要公开API，内部实现来自官方AAR反编译，不称完整源码。

## 与游戏匹配的关键版本

| 游戏 | MAX | MMP | 其他已定位版本 |
|---|---|---|---|
| Car Race | 13.6.4 | Adjust5.5.0 | Firebase22.4.0；Metica核心准确版本本轮未证实 |
| Meowdoku | 13.2.0 | AF6.14.2 | TikTok1.6.1、Firebase22.1.2、GRT1.3.2.0、UniKit2.6.1.3 |
| Rotate Rings | 13.6.2 | AF6.17.5 | TikTok1.7.1、Firebase22.4.0 |
| Jewel | 13.6.3 | Adjust5.7.0 | Firebase23.2.0；AdWorth配置内部版本不当成独立SDK发版 |
| Amaze GO! | 无包体 | 无包体 | 不从同发行商推定 |

依据：[TP01](EVIDENCE_INDEX.md#tp01)、[TP02](EVIDENCE_INDEX.md#tp02)、[V01](EVIDENCE_INDEX.md#v01)。额外下载MAX13.7/Adjust5.8.1/Metica2.5.4/FirebaseRC24.0.1只是公开参照，未匹配游戏内版本。

## 全部版本目录

下列状态中的“取得”仅证明官方发行材料已下载与校验；游戏内所有依赖版本仍应逐项看匹配证据。完整SHA256在各provenance的artifacts条目。

| 供应商 / SDK | 版本 | AAR / sources | 许可（POM原文） | 原始来源与完整哈希 |
|---|---|---|---|---|
| Adjust / Android | 5.5.0 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/Adjust/Android/5.5.0/provenance.json) |
| Adjust / Android | 5.7.0 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/Adjust/Android/5.7.0/provenance.json) |
| Adjust / Android | 5.8.1 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/Adjust/Android/5.8.1/provenance.json) |
| AppLovin / Adapter-amazon-tam-adapter | 11.0.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.0.0.0/provenance.json) |
| AppLovin / Adapter-amazon-tam-adapter | 11.1.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.1.1.0/provenance.json) |
| AppLovin / Adapter-amazon-tam-adapter | 11.3.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.3.0.0/provenance.json) |
| AppLovin / Adapter-bidmachine-adapter | 3.5.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-bidmachine-adapter/3.5.1.0/provenance.json) |
| AppLovin / Adapter-bidmachine-adapter | 3.7.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-bidmachine-adapter/3.7.1.0/provenance.json) |
| AppLovin / Adapter-bigo-adapter | 5.9.0.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/AppLovin/Adapter-bigo-adapter/5.9.0.0/provenance.json) |
| AppLovin / Adapter-bigoads-adapter | 5.9.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-bigoads-adapter/5.9.0.0/provenance.json) |
| AppLovin / Adapter-bytedance-adapter | 7.8.5.2.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-bytedance-adapter/7.8.5.2.0/provenance.json) |
| AppLovin / Adapter-bytedance-adapter | 8.1.0.3.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-bytedance-adapter/8.1.0.3.0/provenance.json) |
| AppLovin / Adapter-bytedance-adapter | 8.1.0.5.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-bytedance-adapter/8.1.0.5.0/provenance.json) |
| AppLovin / Adapter-chartboost-adapter | 9.11.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-chartboost-adapter/9.11.1.0/provenance.json) |
| AppLovin / Adapter-facebook-adapter | 6.21.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-facebook-adapter/6.21.0.0/provenance.json) |
| AppLovin / Adapter-facebook-adapter | 6.22.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-facebook-adapter/6.22.0.0/provenance.json) |
| AppLovin / Adapter-fyber-adapter | 8.4.2.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-fyber-adapter/8.4.2.0/provenance.json) |
| AppLovin / Adapter-fyber-adapter | 8.4.5.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-fyber-adapter/8.4.5.0/provenance.json) |
| AppLovin / Adapter-google-ad-manager-adapter | 25.1.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-google-ad-manager-adapter/25.1.0.0/provenance.json) |
| AppLovin / Adapter-google-ad-manager-adapter | 25.2.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-google-ad-manager-adapter/25.2.0.0/provenance.json) |
| AppLovin / Adapter-google-ad-manager-adapter | 25.4.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-google-ad-manager-adapter/25.4.0.0/provenance.json) |
| AppLovin / Adapter-google-adapter | 25.1.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-google-adapter/25.1.0.0/provenance.json) |
| AppLovin / Adapter-google-adapter | 25.2.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-google-adapter/25.2.0.0/provenance.json) |
| AppLovin / Adapter-google-adapter | 25.4.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-google-adapter/25.4.0.0/provenance.json) |
| AppLovin / Adapter-inmobi-adapter | 11.1.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-inmobi-adapter/11.1.1.0/provenance.json) |
| AppLovin / Adapter-inmobi-adapter | 11.3.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-inmobi-adapter/11.3.0.0/provenance.json) |
| AppLovin / Adapter-ironsource-adapter | 9.3.0.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-ironsource-adapter/9.3.0.0.0/provenance.json) |
| AppLovin / Adapter-ironsource-adapter | 9.4.0.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-ironsource-adapter/9.4.0.0.0/provenance.json) |
| AppLovin / Adapter-ironsource-adapter | 9.5.0.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-ironsource-adapter/9.5.0.0.0/provenance.json) |
| AppLovin / Adapter-line-adapter | 3000.0.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-line-adapter/3000.0.1.0/provenance.json) |
| AppLovin / Adapter-mintegral-adapter | 16.9.91.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-mintegral-adapter/16.9.91.0/provenance.json) |
| AppLovin / Adapter-mintegral-adapter | 17.1.51.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-mintegral-adapter/17.1.51.0/provenance.json) |
| AppLovin / Adapter-mintegral-adapter | 17.1.61.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-mintegral-adapter/17.1.61.0/provenance.json) |
| AppLovin / Adapter-moloco-adapter | 4.4.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-moloco-adapter/4.4.0.0/provenance.json) |
| AppLovin / Adapter-moloco-adapter | 4.9.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-moloco-adapter/4.9.0.0/provenance.json) |
| AppLovin / Adapter-mytarget-adapter | 5.27.4.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-mytarget-adapter/5.27.4.0/provenance.json) |
| AppLovin / Adapter-pubmatic-adapter | 4.5.2.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-pubmatic-adapter/4.5.2.0/provenance.json) |
| AppLovin / Adapter-pubmatic-adapter | 5.0.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-pubmatic-adapter/5.0.0.0/provenance.json) |
| AppLovin / Adapter-smaato-adapter | 23.0.1.1 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-smaato-adapter/23.0.1.1/provenance.json) |
| AppLovin / Adapter-smaato-adapter | 23.1.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-smaato-adapter/23.1.0.0/provenance.json) |
| AppLovin / Adapter-unityads-adapter | 4.17.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.17.0.0/provenance.json) |
| AppLovin / Adapter-unityads-adapter | 4.18.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-unityads-adapter/4.18.1.0/provenance.json) |
| AppLovin / Adapter-verve-adapter | 3.3.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-verve-adapter/3.3.0.0/provenance.json) |
| AppLovin / Adapter-verve-adapter | 3.8.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-verve-adapter/3.8.1.0/provenance.json) |
| AppLovin / Adapter-vungle-adapter | 7.6.3.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-vungle-adapter/7.6.3.0/provenance.json) |
| AppLovin / Adapter-vungle-adapter | 7.7.1.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-vungle-adapter/7.7.1.0/provenance.json) |
| AppLovin / Adapter-vungle-adapter | 7.7.6.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-vungle-adapter/7.7.6.0/provenance.json) |
| AppLovin / Adapter-yandex-adapter | 7.18.4.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-yandex-adapter/7.18.4.0/provenance.json) |
| AppLovin / Adapter-yandex-adapter | 8.1.0.0 | AAR / sources | AppLovin Corporation Mediation Adapter EULA | [provenance](ThirdPartySDKs/AppLovin/Adapter-yandex-adapter/8.1.0.0/provenance.json) |
| AppLovin / MAX | 13.2.0 | AAR / sources | AppLovin Corporation SDK EULA | [provenance](ThirdPartySDKs/AppLovin/MAX/13.2.0/provenance.json) |
| AppLovin / MAX | 13.6.2 | AAR / sources | AppLovin Corporation SDK EULA | [provenance](ThirdPartySDKs/AppLovin/MAX/13.6.2/provenance.json) |
| AppLovin / MAX | 13.6.3 | AAR / sources | AppLovin Corporation SDK EULA | [provenance](ThirdPartySDKs/AppLovin/MAX/13.6.3/provenance.json) |
| AppLovin / MAX | 13.6.4 | AAR / sources | AppLovin Corporation SDK EULA | [provenance](ThirdPartySDKs/AppLovin/MAX/13.6.4/provenance.json) |
| AppLovin / MAX | 13.7.0 | AAR / sources | AppLovin Corporation SDK EULA | [provenance](ThirdPartySDKs/AppLovin/MAX/13.7.0/provenance.json) |
| AppMetrica / Android | 7.14.2 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/AppMetrica/Android/7.14.2/provenance.json) |
| AppMetrica / Android | 8.3.0 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/AppMetrica/Android/8.3.0/provenance.json) |
| appmetrica / Dependency-analytics | 6.2.1 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/AppMetrica/Dependency-analytics/6.2.1/provenance.json) |
| AppsFlyer / Android | 6.14.2 | AAR / 无sources | Proprietary | [provenance](ThirdPartySDKs/AppsFlyer/Android/6.14.2/provenance.json) |
| AppsFlyer / Android | 6.17.5 | AAR / 无sources | Proprietary | [provenance](ThirdPartySDKs/AppsFlyer/Android/6.17.5/provenance.json) |
| bidmachine / Dependency-ads | 3.5.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/bidmachine/Dependency-ads/3.5.1/provenance.json) |
| bidmachine / Dependency-ads | 3.7.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/bidmachine/Dependency-ads/3.7.1/provenance.json) |
| bigossp / Dependency-bigo-ads | 5.9.0 | AAR / 无sources | The Apache License, Version 2.0 | [provenance](ThirdPartySDKs/bigossp/Dependency-bigo-ads/5.9.0/provenance.json) |
| chartboost / Dependency-chartboost-sdk | 9.11.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/chartboost/Dependency-chartboost-sdk/9.11.1/provenance.json) |
| fyber / Dependency-marketplace-sdk | 8.4.2 | AAR / sources | Fyber proprietary | [provenance](ThirdPartySDKs/fyber/Dependency-marketplace-sdk/8.4.2/provenance.json) |
| fyber / Dependency-marketplace-sdk | 8.4.5 | AAR / sources | Fyber proprietary | [provenance](ThirdPartySDKs/fyber/Dependency-marketplace-sdk/8.4.5/provenance.json) |
| Google / AdsIdentifier | 17.1.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/AdsIdentifier/17.1.0/provenance.json) |
| Google / AppSet | 16.0.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/AppSet/16.0.0/provenance.json) |
| google / Dependency-play-services-ads | 25.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/Dependency-play-services-ads/25.4.0/provenance.json) |
| Google / FirebaseAnalytics | 22.1.2 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/FirebaseAnalytics/22.1.2/provenance.json) |
| Google / FirebaseAnalytics | 22.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/FirebaseAnalytics/22.4.0/provenance.json) |
| Google / FirebaseAnalytics | 23.2.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/FirebaseAnalytics/23.2.0/provenance.json) |
| Google / FirebaseCommon | 23.0.0 | AAR / sources | The Apache Software License, Version 2.0 | [provenance](ThirdPartySDKs/Google/FirebaseCommon/23.0.0/provenance.json) |
| Google / FirebaseRemoteConfig | 24.0.1 | AAR / sources | The Apache Software License, Version 2.0 | [provenance](ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/provenance.json) |
| Google / InstallReferrer | 2.2 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/InstallReferrer/2.2/provenance.json) |
| Google / MeasurementAPI | 22.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MeasurementAPI/22.4.0/provenance.json) |
| Google / MeasurementBase | 22.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MeasurementBase/22.4.0/provenance.json) |
| Google / MeasurementImpl | 22.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MeasurementImpl/22.4.0/provenance.json) |
| Google / MeasurementSDK | 22.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MeasurementSDK/22.4.0/provenance.json) |
| Google / MeasurementSDKAPI | 22.4.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MeasurementSDKAPI/22.4.0/provenance.json) |
| Google / MobileAds | 25.1.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MobileAds/25.1.0/provenance.json) |
| Google / MobileAds | 25.2.0 | AAR / 无sources | Android Software Development Kit License | [provenance](ThirdPartySDKs/Google/MobileAds/25.2.0/provenance.json) |
| Google / MobileAdsBase | 25.1.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/Google/MobileAdsBase/25.1.0/provenance.json) |
| Google / MobileAdsLite | 25.1.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/Google/MobileAdsLite/25.1.0/provenance.json) |
| iabtcf / Dependency-iabtcf-decoder | 2.0.10 | 无AAR / sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/iabtcf/Dependency-iabtcf-decoder/2.0.10/provenance.json) |
| InMobi / Android | 11.1.1 | AAR / 无sources | InMobi Android Ads License | [provenance](ThirdPartySDKs/InMobi/Android/11.1.1/provenance.json) |
| InMobi / Dependency-inmobi-ads-kotlin | 11.3.0 | AAR / 无sources | InMobi Android Ads License | [provenance](ThirdPartySDKs/InMobi/Dependency-inmobi-ads-kotlin/11.3.0/provenance.json) |
| Liftoff / Dependency-vungle-ads | 7.7.6 | AAR / 无sources | Vungle SDK License | [provenance](ThirdPartySDKs/Liftoff/Dependency-vungle-ads/7.7.6/provenance.json) |
| Liftoff / Vungle | 7.6.3 | AAR / 无sources | Vungle SDK License | [provenance](ThirdPartySDKs/Liftoff/Vungle/7.6.3/provenance.json) |
| Liftoff / Vungle | 7.7.1 | AAR / 无sources | Vungle SDK License | [provenance](ThirdPartySDKs/Liftoff/Vungle/7.7.1/provenance.json) |
| linecorp / Dependency-fivead | 3.0.1 | AAR / 无sources | LINE ADS NETWORK SDK LICENSE | [provenance](ThirdPartySDKs/linecorp/Dependency-fivead/3.0.1/provenance.json) |
| Meta / AudienceNetwork | 6.22.0 | AAR / 无sources | Facebook Platform License；Apache License Version 2.0；Audience Network Beta SDK Terms | [provenance](ThirdPartySDKs/Meta/AudienceNetwork/6.22.0/provenance.json) |
| Meta / Dependency-audience-network-sdk | 6.21.0 | AAR / 无sources | Facebook Platform License；Apache License Version 2.0；Audience Network Beta SDK Terms | [provenance](ThirdPartySDKs/Meta/Dependency-audience-network-sdk/6.21.0/provenance.json) |
| Meta / FacebookCore | 18.0.3 | AAR / sources | Facebook Platform License | [provenance](ThirdPartySDKs/Meta/FacebookCore/18.0.3/provenance.json) |
| Metica / Android | 2.5.4 | AAR / 无sources | Metica Corporation SDK EULA | [provenance](ThirdPartySDKs/Metica/Android/2.5.4/provenance.json) |
| Mintegral / Android | 16.9.91 | AAR / 无sources | The Apache Software License, Version 2.0 | [provenance](ThirdPartySDKs/Mintegral/Android/16.9.91/provenance.json) |
| Mintegral / Dependency-mbridge_android_sdk | 17.1.51 | 无AAR / 无sources | The Apache Software License, Version 2.0 | [provenance](ThirdPartySDKs/Mintegral/Dependency-mbridge_android_sdk/17.1.51/provenance.json) |
| Mintegral / Dependency-mbridge_android_sdk | 17.1.61 | 无AAR / 无sources | The Apache Software License, Version 2.0 | [provenance](ThirdPartySDKs/Mintegral/Dependency-mbridge_android_sdk/17.1.61/provenance.json) |
| Moloco / Android | 4.4.0 | AAR / 无sources | Moloco Corporation SDK EULA | [provenance](ThirdPartySDKs/Moloco/Android/4.4.0/provenance.json) |
| Moloco / Dependency-moloco-sdk | 4.9.0 | AAR / 无sources | Moloco Corporation SDK EULA | [provenance](ThirdPartySDKs/Moloco/Dependency-moloco-sdk/4.9.0/provenance.json) |
| my / Dependency-mytarget-sdk | 5.27.4 | AAR / 无sources | GNU LGPL 3 | [provenance](ThirdPartySDKs/my/Dependency-mytarget-sdk/5.27.4/provenance.json) |
| Pangle / Android | 7.8.5.2 | AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/Pangle/Android/7.8.5.2/provenance.json) |
| Pangle / Android | 8.1.0.3 | AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/Pangle/Android/8.1.0.3/provenance.json) |
| Pangle / Dependency-pag-sdk | 8.1.0.5 | AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/Pangle/Dependency-pag-sdk/8.1.0.5/provenance.json) |
| pubmatic / Dependency-openwrap | 4.5.2 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/pubmatic/Dependency-openwrap/4.5.2/provenance.json) |
| pubmatic / Dependency-openwrap | 5.0.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/pubmatic/Dependency-openwrap/5.0.0/provenance.json) |
| pubnative / Dependency-hybid.sdk | 3.3.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/pubnative/Dependency-hybid.sdk/3.3.0/provenance.json) |
| pubnative / Dependency-hybid.sdk | 3.8.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/pubnative/Dependency-hybid.sdk/3.8.1/provenance.json) |
| smaato / Dependency-module-core | 23.0.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-module-core/23.0.1/provenance.json) |
| smaato / Dependency-module-core | 23.1.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-module-core/23.1.0/provenance.json) |
| smaato / Dependency-smaato-sdk | 23.0.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-smaato-sdk/23.0.1/provenance.json) |
| smaato / Dependency-smaato-sdk | 23.1.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-smaato-sdk/23.1.0/provenance.json) |
| smaato / Dependency-smaato-sdk-in-app-bidding | 23.0.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-smaato-sdk-in-app-bidding/23.0.1/provenance.json) |
| smaato / Dependency-smaato-sdk-in-app-bidding | 23.1.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-smaato-sdk-in-app-bidding/23.1.0/provenance.json) |
| smaato / Dependency-smaato-sdk-native | 23.0.1 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-smaato-sdk-native/23.0.1/provenance.json) |
| smaato / Dependency-smaato-sdk-native | 23.1.0 | 无AAR / 无sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/smaato/Dependency-smaato-sdk-native/23.1.0/provenance.json) |
| TikTok / Business | 1.6.1 | AAR / sources | POM未取得/未声明 | [provenance](ThirdPartySDKs/TikTok/Business/1.6.1/provenance.json) |
| TikTok / Business | 1.7.1 | AAR / sources | MIT License | [provenance](ThirdPartySDKs/TikTok/Business/1.7.1/provenance.json) |
| Unity / Ads | 4.17.0 | AAR / sources | Unity Ads License | [provenance](ThirdPartySDKs/Unity/Ads/4.17.0/provenance.json) |
| Unity / Ads | 4.18.1 | AAR / 无sources | Unity Ads License | [provenance](ThirdPartySDKs/Unity/Ads/4.18.1/provenance.json) |
| Unity / Dependency-mediation-sdk | 9.4.0 | AAR / 无sources | Unity LevelPlay License | [provenance](ThirdPartySDKs/Unity/Dependency-mediation-sdk/9.4.0/provenance.json) |
| Unity / LevelPlay | 9.3.0 | AAR / 无sources | Unity LevelPlay License | [provenance](ThirdPartySDKs/Unity/LevelPlay/9.3.0/provenance.json) |
| Unity / LevelPlay | 9.5.0 | AAR / 无sources | Unity LevelPlay License | [provenance](ThirdPartySDKs/Unity/LevelPlay/9.5.0/provenance.json) |
| yandex / Dependency-mobileads | 7.18.4 | AAR / sources | Terms of Use of Yandex Advertising Network | [provenance](ThirdPartySDKs/yandex/Dependency-mobileads/7.18.4/provenance.json) |
| yandex / Dependency-mobileads | 8.1.0 | AAR / sources | Terms of Use of Yandex Advertising Network | [provenance](ThirdPartySDKs/yandex/Dependency-mobileads/8.1.0/provenance.json) |

## 独立发行包缺口与嵌入组件

| 组件 | 实际获取状态 | 保留证据与限制 |
|---|---|---|
| Bulldog / AdWorth | 【实际游戏代码证实】游戏内集成样本 | Jewel原始native函数、解出的默认90规则/31权重表、JNI桥和资源出处均沿用D01–D07；未找到可验证独立官方发行包、许可证或商业所有权证据 |
| Meevii / UniKit / Learnings GRT | 【实际游戏代码证实】游戏内集成样本 | Meow DEX、BuildConfig、GDScript桥、GRT处理器已保存；未取得可信独立发行包，不能把游戏提取物命名成官方SDK |
| Metica | 官方Maven2.5.4取得 | 官方文档给坐标；Maven搜索索引零命中不代表不存在；Car桥另已提取，准确游戏内core版待确认 |
| AppDiscovery/Axon | MAX新事件分支+公开集成文档 | 没有找到可核验的独立“Axon模型SDK”发行包；服务端模型不在已取得材料中 |
| MobileAdsLite/Base25.1 | POM可取，AAR404 | 不将旧版组件拆分惯例套用到当前版本；已取得play-services-ads25.1/25.2主体 |
| FirebaseAnalytics | 22.1/22.4/23.2主体AAR只有约786B | 是依赖壳；已追加22.4 measurement-api/sdk/impl/base/sdk-api，避免把空壳当完整分析实现 |
| Firebase RemoteConfig | 取得24.0.1+官方GitHub公开实现参照 | 当前参照版，未证明与四款嵌入core准确一致；main源码非游戏版本锁定 |

原始嵌入证据不复制为假独立SDK；完整引用见[EMBEDDED_ONLY](ThirdPartySDKs/EMBEDDED_ONLY.json)。下载失败/路径发现过程见各 `*_MANIFEST.json`，TikTok最初错误Maven坐标已由官方GitHub标签→JitPack成功补齐，不将最初404当最终缺包。

## 验证结果与分析深度

[COLLECTION_VALIDATION](ThirdPartySDKs/COLLECTION_VALIDATION.json)核对已登记发行材料SHA256；[API_COMPARISON](ThirdPartySDKs/API_COMPARISON.json)核对183个选定声明，未证明整个库相同。

深入机制：MAX/Axon事件与收入、Adjust包构建/队列、AF收入编码/缓存、适配器信号、AppLovin用户匹配字段与InMobi条件式UnifiedID。其余SDK保留发行包及明确分析边界，不宣称已完成每家全部逆向。新原始证据索引：[TP01–TP09](EVIDENCE_INDEX.md#tp01)。
