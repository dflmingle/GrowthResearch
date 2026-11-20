# 证据索引

审计日期：2026-11-18。研究根目录为 D:/GrowthResearch；工作区 GrowthResearch 是同一目录的junction。原包只读；没有运行生产广告/归因请求。

【代码证实】=原始DEX/ARM/原包配置支持；【公开资料证实】=可核验公开页面；【合理推断】=解释性判断；【无法确认】=证据未覆盖。静态调用≠服务器接收≠后台优化目标。

Java为JADX反编译视图，原始DEX和带指令偏移的节选在各static/dex-evidence或sdk-internals。GDScript由原.gdc反编译，不是手写复刻代码。ARM证据以RVA/so哈希为准；自动字面量注释仅作线索，调用/寄存器分支需结合原指令。

以下报告中的行号以本轮保存文件为准；类/方法及RVA是主要稳定定位。完整逐文件SHA256见 EVIDENCE_MANIFEST.json。

<a id="s01"></a>
## S01 · 样本身份、签名、原包完整性

原包哈希重新计算；完整SHA256/签名/ABI见JSON。sample identity中sdk_properties是原始属性，不表示实际启用。

- [SAMPLE_CATALOG.json](SAMPLE_CATALOG.json)
- [car-race/signature.txt](car-race/signature.txt)
- [car-race/reuse-manifest.json](car-race/reuse-manifest.json)
- [car-race/reused-evidence/AcquisitionMonetization-20261117/original-identity.json](car-race/reused-evidence/AcquisitionMonetization-20261117/original-identity.json)
- [meowdoku/static/sample-identity.json](meowdoku/static/sample-identity.json)
- [rotate-rings/static/sample-identity.json](rotate-rings/static/sample-identity.json)
- [jewel-coloring/static/sample-identity.json](jewel-coloring/static/sample-identity.json)
- [rotate-rings-1.2.2/static/sample-identity.json](rotate-rings-1.2.2/static/sample-identity.json)

<a id="v01"></a>
## V01 · SDK版本和主DEX分类

版本字段保留原DEX/class/field；AppsFlyer版本另查原始字符串证据：Meow classes.dex含!SDK-VERSION-STRING!:com.appsflyer:af-android-sdk:6.14.2；Rotate classes3.dex含AppsFlyer_6.17.5；adapter版本不是core版本。DEX候选business分类含依赖噪声，结论须另有调用链。

- [SDK_VERSION_EVIDENCE.json](SDK_VERSION_EVIDENCE.json)
- [meowdoku/static/dex-audit.json](meowdoku/static/dex-audit.json)
- [rotate-rings/static/dex-audit.json](rotate-rings/static/dex-audit.json)
- [jewel-coloring/static/dex-audit.json](jewel-coloring/static/dex-audit.json)
- [meowdoku/static/dex-interest-strings.json](meowdoku/static/dex-interest-strings.json)
- [rotate-rings/static/dex-interest-strings.json](rotate-rings/static/dex-interest-strings.json)
- [car-race/reused-evidence/monetization-20261117/dex-sdk-inventory.json](car-race/reused-evidence/monetization-20261117/dex-sdk-inventory.json)

<a id="c01"></a>
## C01 · Car Adjust初始化、归因与Referrer

ARMv7 RVA见asm文件首行；Campaign偏移0x14；GetCampaignType caller证据见callers.json。

- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.InitAdjust-32a2b98.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.InitAdjust-32a2b98.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.OnGetAttribution-32a33d4.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.OnGetAttribution-32a33d4.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.OnGetCampaign-32a32d0.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.OnGetCampaign-32a32d0.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.GetCampaignType-32a4978.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.GetCampaignType-32a4978.asm)
- [car-race/reused-evidence/monetization-20261117/adjust-install-referrer-dex.txt](car-race/reused-evidence/monetization-20261117/adjust-install-referrer-dex.txt)

<a id="c02"></a>
## C02 · Car场景挂载、provider及远程配置

序列化path ID和启用字段见JSON，区分当前Metica provider与备用MAX。

- [car-race/reused-evidence/monetization-20261117/serialized-evidence.json](car-race/reused-evidence/monetization-20261117/serialized-evidence.json)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Scripts.Data.FirebaseManager.InitializeAds-eb0004.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Scripts.Data.FirebaseManager.InitializeAds-eb0004.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.ZegoAd_Metica.Init-32e3ff0.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.ZegoAd_Metica.Init-32e3ff0.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.ZegoAd_Metica.Init-32e4004.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.ZegoAd_Metica.Init-32e4004.asm)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Scripts.Data.GameRemoteDataSO.OverriderData-eb600c.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Scripts.Data.GameRemoteDataSO.OverriderData-eb600c.asm)

<a id="c03"></a>
## C03 · Car进度/会话/玩法事件



- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.AdjustTracking.TrackingLevel-ee0058.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.AdjustTracking.TrackingLevel-ee0058.asm)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.AdjustTracking.TrackingSession-ee0380.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.AdjustTracking.TrackingSession-ee0380.asm)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__.SessionCounter.OnFirebaseReady-e06f24.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__.SessionCounter.OnFirebaseReady-e06f24.asm)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.GAME_PLAY._FINISH-ee0c4c.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.GAME_PLAY._FINISH-ee0c4c.asm)
- [car-race/reused-evidence/monetization-20261117/event-schema-catalog.json](car-race/reused-evidence/monetization-20261117/event-schema-catalog.json)

<a id="c04"></a>
## C04 · Car广告次数与国家收入阈值

OnAdRevenuePaidEvent RVA0x24401f8；原始ARM与Taichi路由/配置共同支持国家分桶、发送实值后清零。

- [car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.OnAdRevenuePaidEvent-24401f8.asm](car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.OnAdRevenuePaidEvent-24401f8.asm)
- [car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.TrackingForceAds-243ff18.asm](car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.TrackingForceAds-243ff18.asm)
- [car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.TrackingRewardAds-24400cc.asm](car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.TrackingRewardAds-24400cc.asm)
- [car-race/reused-evidence/monetization-20261117/report-methods.json](car-race/reused-evidence/monetization-20261117/report-methods.json)

<a id="c05"></a>
## C05 · Car展示级广告收入



- [car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.ImpressionSuccessEvent-32df658.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.ImpressionSuccessEvent-32df658.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.OnShowRevenuePaid-32deaf0.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.OnShowRevenuePaid-32deaf0.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Max__Zego.Advertisement.Max.AdRevenueTracking.ImpressionSuccessEvent-32c2988.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Max__Zego.Advertisement.Max.AdRevenueTracking.ImpressionSuccessEvent-32c2988.asm)

<a id="c06"></a>
## C06 · Car TikTok启动与ILRD



- [car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.ZegoTikTok.Bootstrap-32ed3e4.asm](car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.ZegoTikTok.Bootstrap-32ed3e4.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.ZegoTikTok.Report-32ed894.asm](car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.ZegoTikTok.Report-32ed894.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.TikTokAdRevenuePayload.Build-32ece30.asm](car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.TikTokAdRevenuePayload.Build-32ece30.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.ZegoTikTok.Send-32edab4.asm](car-race/reused-evidence/monetization-20261117/native/Zego.TikTok__Zego.TikTok.ZegoTikTok.Send-32edab4.asm)

<a id="c07"></a>
## C07 · Car频控与重生广告



- [car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.ShowInterstitialAds-243e748.asm](car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.ShowInterstitialAds-243e748.asm)
- [car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.SetAdsInterval-243e53c.asm](car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.SetAdsInterval-243e53c.asm)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Vehicle.GamePlay.PlayerCarController.OnRespawn-ed0468.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Vehicle.GamePlay.PlayerCarController.OnRespawn-ed0468.asm)
- [car-race/reused-evidence/monetization-20261117/serialized-evidence.json](car-race/reused-evidence/monetization-20261117/serialized-evidence.json)

<a id="c08"></a>
## C08 · Car首激励相关经济分层

enableUserSegmentation>=1且fire_firstRewardCPA才选分层；标记完整setter链未建立。

- [car-race/reused-evidence/monetization-20261117/economy-config-evidence.json](car-race/reused-evidence/monetization-20261117/economy-config-evidence.json)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Scripts.Data.GameInfoDataSO.UpdateUserSegmentData-eb2ee8.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__Scripts.Data.GameInfoDataSO.UpdateUserSegmentData-eb2ee8.asm)

<a id="c09"></a>
## C09 · Car购买/升级/经济schema

schema不等于已实际成交，原始原生函数由JSON定位。

- [car-race/reused-evidence/monetization-20261117/event-schema-catalog.json](car-race/reused-evidence/monetization-20261117/event-schema-catalog.json)
- [car-race/reused-evidence/monetization-20261117/extra-method-evidence.json](car-race/reused-evidence/monetization-20261117/extra-method-evidence.json)

<a id="m01"></a>
## M01 · Meow真实玩法到跨平台GRT行为事件

tracker: GRT_PLATFORMS约1446行、try_track_grt_*约1498/1518/1540行；game_state约6287/6290、session_manager约88；普通_send约1606；平台默认在unikit_analyze_module:15。

- [meowdoku/static/godot-source/tracker.gd](meowdoku/static/godot-source/tracker.gd)
- [meowdoku/static/godot-source/game_state.gd](meowdoku/static/godot-source/game_state.gd)
- [meowdoku/static/godot-source/session_manager.gd](meowdoku/static/godot-source/session_manager.gd)
- [meowdoku/static/godot-source/unikit_manager.gd](meowdoku/static/godot-source/unikit_manager.gd)
- [meowdoku/static/godot-source/unikit_analyze_module.gd](meowdoku/static/godot-source/unikit_analyze_module.gd)
- [meowdoku/static/business-configs-redacted.json](meowdoku/static/business-configs-redacted.json)

<a id="m02"></a>
## M02 · Meow AppsFlyer归因与字段

uploadUserProperties约91、init约136、sendEvent约149；6.14.2字面量见dex-interest-strings.json。

- [meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/AppsflyerAnalyze.java](meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/AppsflyerAnalyze.java)
- [meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/AppsflyerAnalyze$1.java](meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/AppsflyerAnalyze$1.java)

<a id="m03"></a>
## M03 · Meow TikTok和Firebase包装器

TikTok init约46、sendEvent约72；不是所有普通游戏事件都路由此处。

- [meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/TiktokAnalyze.java](meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/TiktokAnalyze.java)
- [meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/FirebaseAnalyze.java](meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/FirebaseAnalyze.java)

<a id="m04"></a>
## M04 · Meow初始化、隐私和缓存

launcher:1212；ModuleManager原DEX调用见sdk-internals；AnalyzeModule:105隐私门槛；BaseAnalyze:14/24顺序需谨慎。

- [meowdoku/static/godot-source/launcher.gd](meowdoku/static/godot-source/launcher.gd)
- [meowdoku/static/godot-source/unikit.gd](meowdoku/static/godot-source/unikit.gd)
- [meowdoku/static/java/classes4.dex/com/learnings/unikit/module/GrtModule.java](meowdoku/static/java/classes4.dex/com/learnings/unikit/module/GrtModule.java)
- [meowdoku/static/java/classes4.dex/com/learnings/unikit/module/AnalyzeModule.java](meowdoku/static/java/classes4.dex/com/learnings/unikit/module/AnalyzeModule.java)
- [meowdoku/static/java/classes4.dex/com/learnings/analyze/BaseAnalyze.java](meowdoku/static/java/classes4.dex/com/learnings/analyze/BaseAnalyze.java)
- [SDK_INTERNALS_INDEX.json](SDK_INTERNALS_INDEX.json)

<a id="m05"></a>
## M05 · Meow GRT配置、国家/渠道/年龄和收入公式

ConfigManager:约98请求/缓存、133工厂；IaaFbRoas:约69 onAdImpression；BaseGrtEvent:约70发送前过滤；LTVManager:约50/59已实现收入累计。

- [meowdoku/static/java/classes4.dex/com/learnings/grt/config/ConfigManager.java](meowdoku/static/java/classes4.dex/com/learnings/grt/config/ConfigManager.java)
- [meowdoku/static/java/classes4.dex/com/learnings/grt/event/LTVManager.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/LTVManager.java)
- [meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/BaseGrtEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/BaseGrtEvent.java)
- [meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/IaaFbRoasEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/IaaFbRoasEvent.java)
- [meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/LtvEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/LtvEvent.java)
- [meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/UacLtvRepeatEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/UacLtvRepeatEvent.java)
- [meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/TiktokVboEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/TiktokVboEvent.java)

<a id="m06"></a>
## M06 · Meow游戏插屏门槛、奖励回调

base_game_page:2713/2727开始插屏判断，VIP/概率/level/session/RAM/保护/CD/fill分支；不是固定间隔强播。

- [meowdoku/static/godot-source/base_game_page.gd](meowdoku/static/godot-source/base_game_page.gd)
- [meowdoku/static/godot-source/inter_unlock_level_config.gd](meowdoku/static/godot-source/inter_unlock_level_config.gd)
- [meowdoku/static/godot-source/inter_unlock_session_config.gd](meowdoku/static/godot-source/inter_unlock_session_config.gd)
- [meowdoku/static/godot-source/inter_unlock_memory_config.gd](meowdoku/static/godot-source/inter_unlock_memory_config.gd)
- [meowdoku/static/godot-source/inter_cd_lc_config.gd](meowdoku/static/godot-source/inter_cd_lc_config.gd)
- [meowdoku/static/godot-source/inter_extra_protect_lc_config.gd](meowdoku/static/godot-source/inter_extra_protect_lc_config.gd)
- [meowdoku/static/godot-source/unikit_manager.gd](meowdoku/static/godot-source/unikit_manager.gd)

<a id="m07"></a>
## M07 · Meow低活跃分层与实验

low active定义和分组只是客户端规则；线上实际分流未知。

- [meowdoku/static/godot-source/churn_user_tag.gd](meowdoku/static/godot-source/churn_user_tag.gd)
- [meowdoku/static/godot-source/inter_prob_config.gd](meowdoku/static/godot-source/inter_prob_config.gd)
- [meowdoku/static/godot-source/is_vip_config.gd](meowdoku/static/godot-source/is_vip_config.gd)

<a id="r01"></a>
## R01 · Rotate初始化/归因/分析ID

App.initDataSDK约177；g8.a实际AppsFlyer init，fallback6.2.3不是SDK版本。

- [rotate-rings/static/java/classes4.dex/com/unity3d/player/App.java](rotate-rings/static/java/classes4.dex/com/unity3d/player/App.java)
- [rotate-rings/static/java/classes2.dex/g8/a.java](rotate-rings/static/java/classes2.dex/g8/a.java)
- [rotate-rings/static/java/classes2.dex/g8/a$a.java](rotate-rings/static/java/classes2.dex/g8/a$a.java)
- [rotate-rings/static/java/classes9.dex/ta/b.java](rotate-rings/static/java/classes9.dex/ta/b.java)

<a id="r02"></a>
## R02 · Rotate广告收入真正业务分发

SDKManager:386 handleAdRevenue、802 lambda调用upload_revenue；evenue:1048总分发；SDKKeybehaviors:85 k返回真实游戏累计秒字段。

- [rotate-rings/static/java/classes6.dex/com/unity3d/player/SDKManager.java](rotate-rings/static/java/classes6.dex/com/unity3d/player/SDKManager.java)
- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java)
- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors.java)

<a id="r03"></a>
## R03 · Rotate AppsFlyer/Firebase/TikTok收入API

uploadPublic:457 uploadDataFB实际是GlDataManager$firebase；ta.e f发TTAdRevenueEvent，d初始化。

- [rotate-rings/static/java/classes2.dex/g8/a.java](rotate-rings/static/java/classes2.dex/g8/a.java)
- [rotate-rings/static/java/classes9.dex/ta/e.java](rotate-rings/static/java/classes9.dex/ta/e.java)
- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$uploadPublic.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$uploadPublic.java)

<a id="r04"></a>
## R04 · Rotate美国早期收入组合条件

约1625 upload_s_Online15_Revenue045_US，触发前后banner条件位置不同；pb.l.d安装小时计算；SDKKeybehaviors.k累计秒字段值的Unity端真实性未动态观测。

- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java)
- [rotate-rings/static/java/classes12.dex/pb/l.java](rotate-rings/static/java/classes12.dex/pb/l.java)

<a id="r05"></a>
## R05 · Rotate首插屏准入、远程配置和关闭名单

va.g a:首次准入+档位循环；va.f a: is_af_purchase/revenue_info；ta.c名单默认空。

- [rotate-rings/static/java/classes12.dex/va/g.java](rotate-rings/static/java/classes12.dex/va/g.java)
- [rotate-rings/static/java/classes12.dex/va/f.java](rotate-rings/static/java/classes12.dex/va/f.java)
- [rotate-rings/static/java/classes9.dex/ta/c.java](rotate-rings/static/java/classes9.dex/ta/c.java)
- [rotate-rings/static/java/classes9.dex/ta/b.java](rotate-rings/static/java/classes9.dex/ta/b.java)

<a id="r06"></a>
## R06 · Rotate国家×天数阈值

evenue:1013国家日事件；uploadPublic:76 cacheFirstCountryCode；ta.d:4405 j(String,int)国家数组。

- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java)
- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$uploadPublic.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$uploadPublic.java)
- [rotate-rings/static/java/classes9.dex/ta/d.java](rotate-rings/static/java/classes9.dex/ta/d.java)

<a id="r07"></a>
## R07 · Rotate拟S2S平台路由

uploadDataAllS2S/OnlyMeta写入ThinkingData o_def_key_event_start，不证明后端完成回传。

- [rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$uploadPublic.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$uploadPublic.java)

<a id="r08"></a>
## R08 · Rotate IL2CPP恢复限制

metadata magic非标准，Cpp2IL未恢复原生玩法；不把Java桥证据扩成完整玩法反编译。

- [rotate-rings/cpp2il.log](rotate-rings/cpp2il.log)

<a id="j01"></a>
## J01 · Jewel Adjust归因进入业务JNI

onAttributionChanged传network/campaign/creative/costAmount；com.facebook namespace内有自定义JNI，非全部官方Meta。

- [jewel-coloring/static/java/classes11.dex/n0/k.java](jewel-coloring/static/java/classes11.dex/n0/k.java)
- [jewel-coloring/static/native-evidence/adsource__AdSourceUtils__getCurrentSubChannelFrom__-1996088.asm](jewel-coloring/static/native-evidence/adsource__AdSourceUtils__getCurrentSubChannelFrom__-1996088.asm)

<a id="j02"></a>
## J02 · Jewel平台发送桥

platform约1271/1283/1328/1339发送；Test11111...55555不算生产事件；仅2个TikTok工具类不等于标准Business SDK。

- [jewel-coloring/static/java/classes6.dex/common/platform.java](jewel-coloring/static/java/classes6.dex/common/platform.java)
- [jewel-coloring/static/java/classes11.dex/com/red/google/RedFirebaseAnalytics.java](jewel-coloring/static/java/classes11.dex/com/red/google/RedFirebaseAnalytics.java)
- [jewel-coloring/static/java/classes10.dex/l9/a.java](jewel-coloring/static/java/classes10.dex/l9/a.java)

<a id="j03"></a>
## J03 · Jewel价值规则/分发/国家值条件

ARM64 RVA0x1a1810c、0x1a43d9c、0x1a32708；函数开头记录原so SHA256。CostRecovery比较total/1000与countryWorth，不等同获客成本。

- [jewel-coloring/static/native-method-evidence.json](jewel-coloring/static/native-method-evidence.json)
- [jewel-coloring/static/native-evidence/ad__event__AdWorthEventUtils___read__-1a1810c.asm](jewel-coloring/static/native-evidence/ad__event__AdWorthEventUtils___read__-1a1810c.asm)
- [jewel-coloring/static/native-evidence/ad__event__AWESendPlatform___sendThresholdToPlatform_std____ndk1__basic_string_char__std____ndk1__char_tr-1a43d9c.asm](jewel-coloring/static/native-evidence/ad__event__AWESendPlatform___sendThresholdToPlatform_std____ndk1__basic_string_char__std____ndk1__char_tr-1a43d9c.asm)
- [jewel-coloring/static/native-evidence/ad__event__AWECCostRecovery__getResult_ad__event__AdWorthEvent_const__-1a32708.asm](jewel-coloring/static/native-evidence/ad__event__AWECCostRecovery__getResult_ad__event__AdWorthEvent_const__-1a32708.asm)

<a id="j04"></a>
## J04 · Jewel来源权重和规则配置缺口

RVA0x1a24498调getCurrentSubChannelFrom；RVA0x1a188e8读adjust_name_token_map；明文两配置未取得，符号存在不证明线上启用。

- [jewel-coloring/static/native-evidence/ad__event__AdWorthEventDataUtils___getCoefSubChannelWeight_int__std____ndk1__map_std____ndk1__basic_strin-1a24498.asm](jewel-coloring/static/native-evidence/ad__event__AdWorthEventDataUtils___getCoefSubChannelWeight_int__std____ndk1__map_std____ndk1__basic_strin-1a24498.asm)
- [jewel-coloring/static/native-evidence/ad__event__AdWorthEventUtils___readAdJustConfigFromFile__-1a188e8.asm](jewel-coloring/static/native-evidence/ad__event__AdWorthEventUtils___readAdJustConfigFromFile__-1a188e8.asm)
- [jewel-coloring/static/native-symbol-candidates.json](jewel-coloring/static/native-symbol-candidates.json)

<a id="j05"></a>
## J05 · Jewel网络/时间点/发送后状态

RVA0x1a1c2bc网络/时间点/条件，0x1a41dc4减值/清零/时间戳；不是服务端ACK证据。

- [jewel-coloring/static/native-evidence/ad__event__AdWorthEventUtils__sendEventsInTimePoint_ad__event__AWESendingTime_-1a1c2bc.asm](jewel-coloring/static/native-evidence/ad__event__AdWorthEventUtils__sendEventsInTimePoint_ad__event__AWESendingTime_-1a1c2bc.asm)
- [jewel-coloring/static/native-evidence/ad__event__AWESendPlatform___updateSendedValueAndData__-1a41dc4.asm](jewel-coloring/static/native-evidence/ad__event__AWESendPlatform___updateSendedValueAndData__-1a41dc4.asm)

<a id="h01"></a>
## H01 · Rotate历史版本差分

同签名，旧版base-only；限定增长集合442同、132变、2移除、6新增；差异哈希不等同语义改变。

- [rotate-rings/history-comparison.json](rotate-rings/history-comparison.json)
- [rotate-rings/history-method-comparison.json](rotate-rings/history-method-comparison.json)
- [rotate-rings-1.2.2/samples/acquisition.json](rotate-rings-1.2.2/samples/acquisition.json)
- [rotate-rings-1.2.2/static/sample-identity.json](rotate-rings-1.2.2/static/sample-identity.json)
- [rotate-rings-1.2.2/static/growth-method-hashes.json](rotate-rings-1.2.2/static/growth-method-hashes.json)
- [rotate-rings/static/growth-method-hashes.json](rotate-rings/static/growth-method-hashes.json)
- [compare_growth.py](compare_growth.py)

<a id="q01"></a>
## Q01 · SDK内部持久队列及原DEX定位

Jewel Adjust PackageHandler的addI/read/write/sendFirst/sendNext；TikTok persist/readFromDisk/flush等；不把类内能力说成生产送达证明。

- [SDK_INTERNALS_INDEX.json](SDK_INTERNALS_INDEX.json)
- [jewel-coloring/static/sdk-internals](jewel-coloring/static/sdk-internals)
- [meowdoku/static/sdk-internals](meowdoku/static/sdk-internals)
- [rotate-rings/static/sdk-internals](rotate-rings/static/sdk-internals)
- [sdk_internals.py](sdk_internals.py)

<a id="p01"></a>
## P01 · 五款Google Play身份与页面快照

各JSON保留公开URL、访问UTC、JSON-LD产品名/发布者；google-play.html/txt同目录。

- [car-race/public/identity.json](car-race/public/identity.json)
- [meowdoku/public/identity.json](meowdoku/public/identity.json)
- [rotate-rings/public/identity.json](rotate-rings/public/identity.json)
- [amaze-go/public/identity.json](amaze-go/public/identity.json)
- [jewel-coloring/public/identity.json](jewel-coloring/public/identity.json)

<a id="p02"></a>
## P02 · 公开商店图与实际查看素材

20图已下载查看，只是商店素材，不能当成付费广告记录。

- [public-research/store-contact-sheet.jpg](public-research/store-contact-sheet.jpg)
- [car-race/public/store-image-sources.json](car-race/public/store-image-sources.json)
- [meowdoku/public/store-image-sources.json](meowdoku/public/store-image-sources.json)
- [rotate-rings/public/store-image-sources.json](rotate-rings/public/store-image-sources.json)
- [amaze-go/public/store-image-sources.json](amaze-go/public/store-image-sources.json)
- [jewel-coloring/public/store-image-sources.json](jewel-coloring/public/store-image-sources.json)

<a id="p03"></a>
## P03 · 广告库与官网请求记录

Meta403；Google/TikTok通用壳无可核验游戏广告；无记录不表示未投放。

- [public-research/sources.json](public-research/sources.json)
- [car-race/reused-evidence/AcquisitionMonetization-20261117/public-fetches.json](car-race/reused-evidence/AcquisitionMonetization-20261117/public-fetches.json)
- [meowdoku/public/market-fetches.json](meowdoku/public/market-fetches.json)
- [rotate-rings/public/market-fetches.json](rotate-rings/public/market-fetches.json)
- [amaze-go/public/market-fetches.json](amaze-go/public/market-fetches.json)
- [jewel-coloring/public/market-fetches.json](jewel-coloring/public/market-fetches.json)

<a id="p04"></a>
## P04 · 样本获取及失败记录

Amaze下载/索引失败明确保留；不同包名或停放域名不替代原包。

- [meowdoku/samples/acquisition.json](meowdoku/samples/acquisition.json)
- [rotate-rings/samples/acquisition.json](rotate-rings/samples/acquisition.json)
- [amaze-go/samples/acquisition.json](amaze-go/samples/acquisition.json)
- [jewel-coloring/samples/acquisition.json](jewel-coloring/samples/acquisition.json)
- [amaze-go/samples/alternate-attempts.json](amaze-go/samples/alternate-attempts.json)
- [amaze-go/public/sample-search.json](amaze-go/public/sample-search.json)

<a id="p05"></a>
## P05 · 官方SDK通用能力文档

仅用于解释API，不证明游戏广告后台启用。Adjust文档https://dev.adjust.com/en/sdk/android/features/ad-revenue/；AppsFlyer https://dev.appsflyer.com/hc/docs/ad-revenue-1；Firebase https://firebase.google.com/docs/analytics/measure-ad-revenue；InstallReferrer https://developer.android.com/google/play/installreferrer。

- [public-research/sources.json](public-research/sources.json)
- [public-research/official-doc-checks.json](public-research/official-doc-checks.json)
- [public-research/appsflyer-revenue-v2.txt](public-research/appsflyer-revenue-v2.txt)
- [public-research/appsflyer-sdk-reference.txt](public-research/appsflyer-sdk-reference.txt)
- [public-research/firebase-ad-revenue.txt](public-research/firebase-ad-revenue.txt)
- [public-research/install-referrer.txt](public-research/install-referrer.txt)

<!-- DEEP_AUDIT_20261118 -->

## 本轮增量证据说明

新增08/09/10。D01恢复了此前J03/J04缺失的包内配置；旧报告保持历史状态。本轮无设备操作，未取得生产热更、受众后台或Jewel历史APK。

<a id="d01"></a>
## D01 · Jewel原始资源索引解码与包内默认规则

替代上一轮J03/J04中“明文规则未取得”的研究限制：已解析原始mainData映射和目标资源；90事件/31权重表。原始条目及解码哈希见provenance。解析仅为本地资源，未使用生产凭证。

- [jewel_resources.py](jewel_resources.py)
- [DEEP_SAMPLE_INTEGRITY.json](DEEP_SAMPLE_INTEGRITY.json)
- [jewel-coloring/deep/resources/decoded-config-provenance.json](jewel-coloring/deep/resources/decoded-config-provenance.json)
- [jewel-coloring/deep/resources/target-resource-map.json](jewel-coloring/deep/resources/target-resource-map.json)
- [jewel-coloring/deep/resources/ad_worth_event.json.redacted.json](jewel-coloring/deep/resources/ad_worth_event.json.redacted.json)
- [jewel-coloring/deep/resources/ad_worth.json.redacted.json](jewel-coloring/deep/resources/ad_worth.json.redacted.json)
- [jewel-coloring/deep/resources/adjust_name_token_map.json.redacted.json](jewel-coloring/deep/resources/adjust_name_token_map.json.redacted.json)
- [jewel-coloring/deep/resources/sdk_event.json.redacted.json](jewel-coloring/deep/resources/sdk_event.json.redacted.json)
- [jewel-coloring/deep/rule-analysis.json](jewel-coloring/deep/rule-analysis.json)
- [jewel-coloring/deep/rule-catalog.json](jewel-coloring/deep/rule-catalog.json)
- [jewel-coloring/deep/rule-catalog.csv](jewel-coloring/deep/rule-catalog.csv)
- [jewel-coloring/deep/asm/BigFile__BigFile_bool_-206ffa8.asm](jewel-coloring/deep/asm/BigFile__BigFile_bool_-206ffa8.asm)
- [jewel-coloring/deep/asm/BigFile__setupConfFileRoot__-2070430.asm](jewel-coloring/deep/asm/BigFile__setupConfFileRoot__-2070430.asm)
- [jewel-coloring/deep/asm/BigFile__rc4_crypt_unsigned_char___long_-20709d4.asm](jewel-coloring/deep/asm/BigFile__rc4_crypt_unsigned_char___long_-20709d4.asm)
- [jewel-coloring/deep/asm/BigFile__decryptAndDecompress_cocos2d__ResizableBuffer___long_-2072000.asm](jewel-coloring/deep/asm/BigFile__decryptAndDecompress_cocos2d__ResizableBuffer___long_-2072000.asm)

<a id="d02"></a>
## D02 · AdWorth组件归属和全量可识别函数/调用清单

524个唯一RVA的AdWorth/事件相关函数；范围是导出可识别函数，非证明没有隐藏实现。g_sdk/BullDogClass与com.red.libbulldog支持技术组件归属，不证明商业权属。

- [jewel-coloring/deep/symbol-index.json](jewel-coloring/deep/symbol-index.json)
- [jewel-coloring/deep/adworth-method-inventory.csv](jewel-coloring/deep/adworth-method-inventory.csv)
- [jewel-coloring/deep/method-index.json](jewel-coloring/deep/method-index.json)
- [jewel-coloring/deep/direct-callers.json](jewel-coloring/deep/direct-callers.json)
- [deep_native.py](deep_native.py)
- [jewel-coloring/deep/java/classes12.dex/com/facebook/appevents/b/AdSourceUtils.java](jewel-coloring/deep/java/classes12.dex/com/facebook/appevents/b/AdSourceUtils.java)
- [jewel-coloring/deep/asm/BulldogSdk___initBaseComponents_BulldogDelegate___int__int__int_-1937ee0.asm](jewel-coloring/deep/asm/BulldogSdk___initBaseComponents_BulldogDelegate___int__int__int_-1937ee0.asm)
- [jewel-coloring/deep/asm/BulldogSdk___initGDPRAndRemaining__-1938174.asm](jewel-coloring/deep/asm/BulldogSdk___initGDPRAndRemaining__-1938174.asm)

<a id="d03"></a>
## D03 · AdWorth输入账本与乘法系数计算

原始ARM fmul形成系数乘积；USD getter除1000。来源正则表未被90个默认事件引用；广告价格/估值与实收ILRD须区分。

- [jewel-coloring/deep/asm/ad__AdWorthUtils__hasDisplayPlacementWithPrice_std____ndk1__basic_string_char__std____ndk1__char_traits_char__-1a05f4c.asm](jewel-coloring/deep/asm/ad__AdWorthUtils__hasDisplayPlacementWithPrice_std____ndk1__basic_string_char__std____ndk1__char_traits_char__-1a05f4c.asm)
- [jewel-coloring/deep/asm/ad__AdWorthDataUtils__addUserTotalAdWorthForAdType_std____ndk1__basic_string_char__std____ndk1__char_traits_ch-1a0a160.asm](jewel-coloring/deep/asm/ad__AdWorthDataUtils__addUserTotalAdWorthForAdType_std____ndk1__basic_string_char__std____ndk1__char_traits_ch-1a0a160.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__addUserOldTotalAdWorthNum_float_-1a24f7c.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__addUserOldTotalAdWorthNum_float_-1a24f7c.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___addUserOldTotalWorth_float_-1a24b80.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___addUserOldTotalWorth_float_-1a24b80.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___weightTheWorth_int__float_-1a22ae4.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___weightTheWorth_int__float_-1a22ae4.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getWeightCoefWithMode_int__ad__event__WorthWeightMode__std____ndk1__map_std-1a22c1c.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getWeightCoefWithMode_int__ad__event__WorthWeightMode__std____ndk1__map_std-1a22c1c.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefSubChannelWeight_int__std____ndk1__map_std____ndk1__basic_string_cha-1a24498.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefSubChannelWeight_int__std____ndk1__map_std____ndk1__basic_string_cha-1a24498.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefLoginDay_int__std____ndk1__map_int__float__std____ndk1__less_int___s-1a23444.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefLoginDay_int__std____ndk1__map_int__float__std____ndk1__less_int___s-1a23444.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefLoginDayMax_int__std____ndk1__map_int__float__std____ndk1__less_int_-1a235ec.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefLoginDayMax_int__std____ndk1__map_int__float__std____ndk1__less_int_-1a235ec.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefDayTime_int__std____ndk1__map_int__float__std____ndk1__less_int___st-1a2374c.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___getCoefDayTime_int__std____ndk1__map_int__float__std____ndk1__less_int___st-1a2374c.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___rangeByTotalSentWorth_int__float__float__float_-1a23330.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___rangeByTotalSentWorth_int__float__float__float_-1a23330.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__getUnsendWorthUSD_int__const-1a21584.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__getUnsendWorthUSD_int__const-1a21584.asm)

<a id="d04"></a>
## D04 · 条件树、国家、用户组和游戏时长

AND/OR、关系运算、时间单位value*60、国家集合、total/1000比较、BulldogSdk group比较；条件类存在不等于默认事件引用。

- [jewel-coloring/deep/asm/ad__event__AdWorthEvent__checkEventSend_bool__const-1a2e680.asm](jewel-coloring/deep/asm/ad__event__AdWorthEvent__checkEventSend_bool__const-1a2e680.asm)
- [jewel-coloring/deep/asm/ad__event__AWECombinedCondition__getResult_ad__event__AdWorthEvent_const__-1a2fc58.asm](jewel-coloring/deep/asm/ad__event__AWECombinedCondition__getResult_ad__event__AdWorthEvent_const__-1a2fc58.asm)
- [jewel-coloring/deep/asm/ad__event__AWECWorthInterval__getResult_ad__event__AdWorthEvent_const__-1a32018.asm](jewel-coloring/deep/asm/ad__event__AWECWorthInterval__getResult_ad__event__AdWorthEvent_const__-1a32018.asm)
- [jewel-coloring/deep/asm/ad__event__AWECWeightWorth__getResult_ad__event__AdWorthEvent_const__-1a34830.asm](jewel-coloring/deep/asm/ad__event__AWECWeightWorth__getResult_ad__event__AdWorthEvent_const__-1a34830.asm)
- [jewel-coloring/deep/asm/ad__event__AWECTimeInterval__getResult_ad__event__AdWorthEvent_const__-1a31ddc.asm](jewel-coloring/deep/asm/ad__event__AWECTimeInterval__getResult_ad__event__AdWorthEvent_const__-1a31ddc.asm)
- [jewel-coloring/deep/asm/ad__event__AWECCountry__getResult_ad__event__AdWorthEvent_const__-1a36654.asm](jewel-coloring/deep/asm/ad__event__AWECCountry__getResult_ad__event__AdWorthEvent_const__-1a36654.asm)
- [jewel-coloring/deep/asm/ad__event__AWECCostRecovery__getResult_ad__event__AdWorthEvent_const__-1a32708.asm](jewel-coloring/deep/asm/ad__event__AWECCostRecovery__getResult_ad__event__AdWorthEvent_const__-1a32708.asm)
- [jewel-coloring/deep/asm/ad__event__AWECUserGroup__getResult_ad__event__AdWorthEvent_const__-1a33c00.asm](jewel-coloring/deep/asm/ad__event__AWECUserGroup__getResult_ad__event__AdWorthEvent_const__-1a33c00.asm)
- [jewel-coloring/deep/asm/ad__event__AWECSubChannelName__getResult_ad__event__AdWorthEvent_const__-1a37aac.asm](jewel-coloring/deep/asm/ad__event__AWECSubChannelName__getResult_ad__event__AdWorthEvent_const__-1a37aac.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__updateCommonValue__-1a1fc20.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__updateCommonValue__-1a1fc20.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__getCountryWorth_std____ndk1__basic_string_char__std____ndk1__char_traits_cha-1a1fd54.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils__getCountryWorth_std____ndk1__basic_string_char__std____ndk1__char_traits_cha-1a1fd54.asm)

<a id="d05"></a>
## D05 · 平台金额语义、Meta purchase映射和发送状态

event514 facebook idx8→logPurchase USD；这是价值代理映射，不是证明真实IAP。normal/interval/x100等金额口径不同；发送尝试后更新本地状态≠ACK。

- [jewel-coloring/deep/asm/ad__event__AWESendPlatform___sendEvents__-1a42190.asm](jewel-coloring/deep/asm/ad__event__AWESendPlatform___sendEvents__-1a42190.asm)
- [jewel-coloring/deep/asm/ad__event__AWESendPlatform__sendMsgToPlatform__-1a44350.asm](jewel-coloring/deep/asm/ad__event__AWESendPlatform__sendMsgToPlatform__-1a44350.asm)
- [jewel-coloring/deep/asm/ad__event__AWESendPlatform___updateSendedValueAndData__-1a41dc4.asm](jewel-coloring/deep/asm/ad__event__AWESendPlatform___updateSendedValueAndData__-1a41dc4.asm)
- [jewel-coloring/deep/asm/ad__event__AWEWorthUpdate__getBeSentWorth_ad__event__AWEWorthSendType__float_-1a3dc50.asm](jewel-coloring/deep/asm/ad__event__AWEWorthUpdate__getBeSentWorth_ad__event__AWEWorthSendType__float_-1a3dc50.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___sendFackBookEvent__-1a1a210.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___sendFackBookEvent__-1a1a210.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEvent__sendMsgToPlatform__-1a2e648.asm](jewel-coloring/deep/asm/ad__event__AdWorthEvent__sendMsgToPlatform__-1a2e648.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEvent___updateEvent__-1a2e270.asm](jewel-coloring/deep/asm/ad__event__AdWorthEvent___updateEvent__-1a2e270.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEvent___updateEventStatus__-1a2e594.asm](jewel-coloring/deep/asm/ad__event__AdWorthEvent___updateEventStatus__-1a2e594.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils__sendAdJustEvent_std____ndk1__basic_string_char__std____ndk1__char_traits_char___-1a1c6e0.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils__sendAdJustEvent_std____ndk1__basic_string_char__std____ndk1__char_traits_char___-1a1c6e0.asm)
- [jewel-coloring/deep/asm/ad__event__AWESendPlatform___sendThresholdToPlatform_std____ndk1__basic_string_char__std____ndk1__char_traits_-1a43d9c.asm](jewel-coloring/deep/asm/ad__event__AWESendPlatform___sendThresholdToPlatform_std____ndk1__basic_string_char__std____ndk1__char_traits_-1a43d9c.asm)
- [jewel-coloring/deep/java/classes6.dex/common/platform.java](jewel-coloring/deep/java/classes6.dex/common/platform.java)
- [identity-deep/raw-methods/jewel-coloring/Lcommon_platform___EventUserAdWorthEventAllIn1.txt](identity-deep/raw-methods/jewel-coloring/Lcommon_platform___EventUserAdWorthEventAllIn1.txt)

<a id="d06"></a>
## D06 · AdWorth输出标签与独立广告策略边界

customInt与来源平台值进入GTUser；直接caller记录有预加载/规则group消费者，但未建立某AdWorth标签改变奖励/广告频率闭环。ad_rule按本应用play_time控制StopPreload，不直接是AdWorth公式。

- [jewel-coloring/deep/resources/ad_rule.json.redacted.json](jewel-coloring/deep/resources/ad_rule.json.redacted.json)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___addUserOldTotalWorth_float_-1a24b80.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventDataUtils___addUserOldTotalWorth_float_-1a24b80.asm)
- [jewel-coloring/deep/asm/ad__event__AWESendPlatform___sendEvents__-1a42190.asm](jewel-coloring/deep/asm/ad__event__AWESendPlatform___sendEvents__-1a42190.asm)
- [jewel-coloring/deep/asm/gtuser2__GTUser__BDInternalsetCustomInt_int__int_-1ae5c98.asm](jewel-coloring/deep/asm/gtuser2__GTUser__BDInternalsetCustomInt_int__int_-1ae5c98.asm)
- [jewel-coloring/deep/asm/gtuser2__GTUser__getUserGroup__-1adb7cc.asm](jewel-coloring/deep/asm/gtuser2__GTUser__getUserGroup__-1adb7cc.asm)
- [jewel-coloring/deep/asm/adsource__AdSourceUtils___updateMaxPrioritySource_adsource__AdSource__-19946ac.asm](jewel-coloring/deep/asm/adsource__AdSourceUtils___updateMaxPrioritySource_adsource__AdSource__-19946ac.asm)

<a id="d07"></a>
## D07 · 配置/版本/热更新和调度

默认资源读取、init资格、首次版本门槛、3秒调度和BDHotUpdate监听；未取生产热更文件，未证明Firebase RC直接覆盖所有事件。

- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___init__-1a17f98.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___init__-1a17f98.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___read__-1a1810c.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___read__-1a1810c.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___initEvents_std____ndk1__map_std____ndk1__basic_string_char__std____ndk1__char_t-1a18f2c.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___initEvents_std____ndk1__map_std____ndk1__basic_string_char__std____ndk1__char_t-1a18f2c.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___checkVersion_std____ndk1__map_std____ndk1__basic_string_char__std____ndk1__char-1a18c28.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___checkVersion_std____ndk1__map_std____ndk1__basic_string_char__std____ndk1__char-1a18c28.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___addConfigUpdateListener__-1a187f4.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___addConfigUpdateListener__-1a187f4.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___reinitializeEvent__-1a1ba7c.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___reinitializeEvent__-1a1ba7c.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___scheduler__-1a18668.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils___scheduler__-1a18668.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils__sendWithInterAdShouldShow__-1a1c254.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils__sendWithInterAdShouldShow__-1a1c254.asm)
- [jewel-coloring/deep/asm/ad__event__AdWorthEventUtils__sendWithInterAdShow__-1a1c1ec.asm](jewel-coloring/deep/asm/ad__event__AdWorthEventUtils__sendWithInterAdShow__-1a1c1ec.asm)
- [jewel-coloring/deep/asm/ad__AdWorthUtils___readFromServerSaved__-1a043c0.asm](jewel-coloring/deep/asm/ad__AdWorthUtils___readFromServerSaved__-1a043c0.asm)
- [jewel-coloring/deep/asm/ad__AdWorthUtils__readEcpmFromServer__-1a05130.asm](jewel-coloring/deep/asm/ad__AdWorthUtils__readEcpmFromServer__-1a05130.asm)

<a id="d08"></a>
## D08 · Jewel历史版本获取尝试与供应商公开证据缺口

历史code23/22返回403，Aptoide无包/无versions；搜索页面无可验证供应商内容。不可据配置内部版本/日期式事件名推上线时间。

- [jewel-coloring/deep/history/attempts.json](jewel-coloring/deep/history/attempts.json)
- [jewel_history_probe.py](jewel_history_probe.py)
- [public-research/deep/jewel-history.json](public-research/deep/jewel-history.json)
- [public-research/deep/jewel-versions.json](public-research/deep/jewel-versions.json)
- [public-research/deep/fetches.json](public-research/deep/fetches.json)
- [public-research/deep/adworth-search.txt](public-research/deep/adworth-search.txt)
- [public-research/deep/bulldog-search.txt](public-research/deep/bulldog-search.txt)
- [public-research/deep/tatagame-search.txt](public-research/deep/tatagame-search.txt)

<a id="i01"></a>
## I01 · 四包身份/受众API逐DEX候选与否定证据范围

主DEX逐方法扫描，1325个候选方法包含依赖噪声。业务链另外核验；SDK helper自调用、枚举和字符串不能当生产图谱证据。未读取真实用户ID。

- [deep_identity.py](deep_identity.py)
- [identity-deep/api-callers.json](identity-deep/api-callers.json)
- [identity-deep/class-origins.json](identity-deep/class-origins.json)
- [identity-deep/vendor-literal-candidates.json](identity-deep/vendor-literal-candidates.json)
- [identity-deep.log](identity-deep.log)

<a id="i02"></a>
## I02 · Car Adjust Adid业务缓存及原生调用边界

Adid业务字段+0x50；未建立cross-app或External Device ID设置业务链。SDK/原生未覆盖的服务端能力不作不存在结论。

- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.TryGetAdId-32a3088.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.TryGetAdId-32a3088.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.OnGetAdId-32a38e8.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.OnGetAdId-32a38e8.asm)
- [car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.GetAdid-32a48e4.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Adjust__Zego.Adjust.ZegoAdjust.GetAdid-32a48e4.asm)
- [car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.USER.GenerateTrackingUser-ee4bbc.asm](car-race/reused-evidence/monetization-20261117/native/Assembly-CSharp__CarRace.Tracking.USER.GenerateTrackingUser-ee4bbc.asm)
- [identity-deep/api-callers.json](identity-deep/api-callers.json)

<a id="i03"></a>
## I03 · Meow本地UUID、Learnings ID和UserTag联结

UUID包私有持久化；Learnings ID=MD5(androidId+本应用firstInstallTime)或UUID回退；UserTag/LUID同应用联结。不会计算任何真实设备的ID。

- [meowdoku/deep/java/classes4.dex/com/learnings/analyze/UUIDManager.java](meowdoku/deep/java/classes4.dex/com/learnings/analyze/UUIDManager.java)
- [meowdoku/deep/java/classes4.dex/com/learnings/analyze/LearningsIdManager.java](meowdoku/deep/java/classes4.dex/com/learnings/analyze/LearningsIdManager.java)
- [meowdoku/deep/java/classes4.dex/com/learnings/analyze/AnalyzeManager.java](meowdoku/deep/java/classes4.dex/com/learnings/analyze/AnalyzeManager.java)
- [meowdoku/deep/java/classes4.dex/com/learnings/unikit/module/UserTagModule.java](meowdoku/deep/java/classes4.dex/com/learnings/unikit/module/UserTagModule.java)
- [meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/AppsflyerAnalyze.java](meowdoku/static/java/classes4.dex/com/learnings/analyze/platform/AppsflyerAnalyze.java)
- [identity-deep/raw-methods/meowdoku/Lcom_learnings_analyze_UUIDManager___getUUID.txt](identity-deep/raw-methods/meowdoku/Lcom_learnings_analyze_UUIDManager___getUUID.txt)
- [identity-deep/raw-methods/meowdoku/Lcom_learnings_analyze_LearningsIdManager___getLearningsIdInfo.txt](identity-deep/raw-methods/meowdoku/Lcom_learnings_analyze_LearningsIdManager___getLearningsIdInfo.txt)

<a id="i04"></a>
## I04 · Meow账户认证和分析属性链

AuthManager启动guest/恢复会话；ServerLogin→syncAccountId写learnings_account_id属性；不是替换AF CUID。请求headers包名/版本/learnings-id/luid/device-id；未访问服务或token。

- [meowdoku/static/godot-source/auth_manager.gd](meowdoku/static/godot-source/auth_manager.gd)
- [meowdoku/static/godot-source/unikit.gd](meowdoku/static/godot-source/unikit.gd)
- [meowdoku/static/godot-source/unikit_manager.gd](meowdoku/static/godot-source/unikit_manager.gd)
- [meowdoku/deep/java/classes4.dex/com/learnings/auth/LxAuth.java](meowdoku/deep/java/classes4.dex/com/learnings/auth/LxAuth.java)
- [meowdoku/deep/java/classes4.dex/com/learnings/auth/ServerLoginExecutor.java](meowdoku/deep/java/classes4.dex/com/learnings/auth/ServerLoginExecutor.java)
- [meowdoku/deep/java/classes4.dex/com/learnings/auth/network/AuthApiClient.java](meowdoku/deep/java/classes4.dex/com/learnings/auth/network/AuthApiClient.java)
- [meowdoku/deep/java/classes4.dex/com/learnings/unikit/LearningsKit.java](meowdoku/deep/java/classes4.dex/com/learnings/unikit/LearningsKit.java)
- [meowdoku/deep/java/classes5.dex/com/meevii/abtest/business/AbAccountIdManager.java](meowdoku/deep/java/classes5.dex/com/meevii/abtest/business/AbAccountIdManager.java)
- [identity-deep/raw-methods/meowdoku/Lcom_learnings_auth_LxAuth___syncAccountId.txt](identity-deep/raw-methods/meowdoku/Lcom_learnings_auth_LxAuth___syncAccountId.txt)

<a id="i05"></a>
## I05 · Meow UID2桥与缺失实现

UID2 init成功配置回调可达；MeeviiAdPlugin类未在主DEX定义；wrapper捕获Throwable；游戏GDScript只有register_uid2定义。不是已启用邮箱映射证明。

- [meowdoku/static/godot-source/unikit_ad_module.gd](meowdoku/static/godot-source/unikit_ad_module.gd)
- [meowdoku/deep/java/classes4.dex/com/learnings/unikit/module/AdModule.java](meowdoku/deep/java/classes4.dex/com/learnings/unikit/module/AdModule.java)
- [meowdoku/deep/java/classes5.dex/com/meevii/adsdk/MeeviiAd.java](meowdoku/deep/java/classes5.dex/com/meevii/adsdk/MeeviiAd.java)
- [meowdoku/deep/java/classes5.dex/com/meevii/adsdk/MeeviiAd$1.java](meowdoku/deep/java/classes5.dex/com/meevii/adsdk/MeeviiAd$1.java)
- [meowdoku/deep/java/classes5.dex/com/meevii/adsdk/bridge/Uid2PluginManager.java](meowdoku/deep/java/classes5.dex/com/meevii/adsdk/bridge/Uid2PluginManager.java)
- [meowdoku/static/dex-class-index.txt](meowdoku/static/dex-class-index.txt)
- [identity-deep/api-callers.json](identity-deep/api-callers.json)

<a id="i06"></a>
## I06 · Rotate同应用SDK ID与Meta Protected Audience

AppsFlyer CUID=传入的统一分析ID，ta_distinct_id追加；conversion AF UID映射；PA是SDK内事件路径/系统条件能力，生产开关未观测。

- [rotate-rings/static/java/classes2.dex/g8/a.java](rotate-rings/static/java/classes2.dex/g8/a.java)
- [rotate-rings/static/java/classes2.dex/g8/a$a.java](rotate-rings/static/java/classes2.dex/g8/a$a.java)
- [rotate-rings/deep/java/classes9.dex/com/facebook/appevents/gps/pa/PACustomAudienceClient.java](rotate-rings/deep/java/classes9.dex/com/facebook/appevents/gps/pa/PACustomAudienceClient.java)
- [identity-deep/api-callers.json](identity-deep/api-callers.json)

<a id="i07"></a>
## I07 · Jewel公共共享设备ID真实读写及native业务消费者

native先缓存/BulldogFile，长度50才共享分支；Java外存game_share_info_id.txt，私有diu_did_21038。原DEX确认permission!=0进入尝试；不修改/绕过。没有读取实际设备文件。

- [jewel-coloring/deep/java/classes6.dex/common/platform.java](jewel-coloring/deep/java/classes6.dex/common/platform.java)
- [jewel-coloring/deep/java/classes5.dex/n9/a.java](jewel-coloring/deep/java/classes5.dex/n9/a.java)
- [jewel-coloring/deep/java/classes6.dex/r9/h.java](jewel-coloring/deep/java/classes6.dex/r9/h.java)
- [jewel-coloring/deep/java/classes12.dex/com/facebook/appevents/b/AdSourceUtils.java](jewel-coloring/deep/java/classes12.dex/com/facebook/appevents/b/AdSourceUtils.java)
- [identity-deep/raw-methods/jewel-coloring/Lcommon_platform___getLocalSharedDeviceId.txt](identity-deep/raw-methods/jewel-coloring/Lcommon_platform___getLocalSharedDeviceId.txt)
- [identity-deep/raw-methods/jewel-coloring/Lcommon_platform____getLocalSharedDeviceIdSaveID.txt](identity-deep/raw-methods/jewel-coloring/Lcommon_platform____getLocalSharedDeviceIdSaveID.txt)
- [jewel-coloring/deep/asm/DeviceIdUtils__getDeviceId__-1aed42c.asm](jewel-coloring/deep/asm/DeviceIdUtils__getDeviceId__-1aed42c.asm)
- [jewel-coloring/deep/asm/BulldogPlatform__getLocalSharedDeviceId__-1b1cd28.asm](jewel-coloring/deep/asm/BulldogPlatform__getLocalSharedDeviceId__-1b1cd28.asm)
- [jewel-coloring/deep/asm/gtuser2__GTUser__setup_int_-1adaedc.asm](jewel-coloring/deep/asm/gtuser2__GTUser__setup_int_-1adaedc.asm)
- [jewel-coloring/deep/asm/gtuser2__GTUser___sendDataToServer__-1adbb98.asm](jewel-coloring/deep/asm/gtuser2__GTUser___sendDataToServer__-1adbb98.asm)
- [jewel-coloring/deep/asm/gtuser2__GTDataProp__toJson__-1ae9b9c.asm](jewel-coloring/deep/asm/gtuser2__GTDataProp__toJson__-1ae9b9c.asm)
- [jewel-coloring/deep/asm/gtuser2__GTDataPurchase__toJson__-1aebdcc.asm](jewel-coloring/deep/asm/gtuser2__GTDataPurchase__toJson__-1aebdcc.asm)

<a id="i08"></a>
## I08 · 广告SDK网络侧身份能力及误报核查

InMobi能力受remote enabled/opt-out控制；Liveramp CMP是CMP名称，NEUSTAR是IP位置枚举，tapad_单字符串不足，CrossPromotion无SDK外业务caller。均不得直接推生产图谱启用。

- [rotate-rings/deep/java/classes11.dex/com/inmobi/unifiedId/InMobiUnifiedIdService.java](rotate-rings/deep/java/classes11.dex/com/inmobi/unifiedId/InMobiUnifiedIdService.java)
- [identity-deep/api-callers.json](identity-deep/api-callers.json)
- [identity-deep/vendor-literal-candidates.json](identity-deep/vendor-literal-candidates.json)

<a id="p06"></a>
## P06 · 公开隐私政策、集团共享与受众声明

Oakever政策2026-08-05含custom/lookalike/集团共享条款，仅公司级披露；Jewel商店所链BrilliantSort政策2026-01-20；Hurelax仅壳。具体URL/访问UTC见fetches，不证明特定游戏生产受众。

- [public-research/deep/fetches.json](public-research/deep/fetches.json)
- [public-research/deep/oakever-policy.txt](public-research/deep/oakever-policy.txt)
- [public-research/deep/oakever-policy-links.json](public-research/deep/oakever-policy-links.json)
- [public-research/deep/oakever-partners-correct.json](public-research/deep/oakever-partners-correct.json)
- [public-research/deep/oakever-partners-correct.txt](public-research/deep/oakever-partners-correct.txt)
- [public-research/deep/oakever-vendors.txt](public-research/deep/oakever-vendors.txt)
- [public-research/deep/jewel-policy.txt](public-research/deep/jewel-policy.txt)
- [public-research/deep/zego-policy.txt](public-research/deep/zego-policy.txt)
- [public-research/deep/hurelax-policy.txt](public-research/deep/hurelax-policy.txt)

<a id="p07"></a>
## P07 · 官方身份能力和Android存储边界

只引用取得有效内容的官方UID2/Appsflyer/Firebase/Android文档解释通用能力。Adjust/Meta尝试404以及InMobi通用页不充当游戏启用证据。

- [public-research/deep/additional-fetches.json](public-research/deep/additional-fetches.json)
- [public-research/deep/uid2-overview.txt](public-research/deep/uid2-overview.txt)
- [public-research/deep/appsflyer-cuid.txt](public-research/deep/appsflyer-cuid.txt)
- [public-research/deep/firebase-userid.txt](public-research/deep/firebase-userid.txt)
- [public-research/deep/android-storage.txt](public-research/deep/android-storage.txt)

<!-- SDK_AXON_AUDIT_20261118 -->

## AppLovin与独立SDK增量证据

本轮新增11–19，不改写00–10历史结论；SDK内部能力、游戏业务调用、后台启用、实际投放分别证明。新标签：实际游戏代码/官方SDK代码/官方文档/公开投放证据/合理推断/无法确认；11–13沿用AppLovin专项标签。没有目标产品的已证实AppLovin投放记录。

<a id="ax01"></a>
## AX01 · AppLovin与MMP官方partner配置、事件映射与checkout语义

通用集成文档，不是目标游戏投放记录。AppLovin自身文档明确checkout排除广告收入/预测LTV；Adjust/AF后台需partner启用、来源范围及映射。

- [axon/VERIFIED_SOURCES.json](axon/VERIFIED_SOURCES.json)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 AX01（13份材料）。

<a id="ax02"></a>
## AX02 · 当前AppLovin获客目标、MAX前提与流量类型

IAA/IAP/Blended/CPP/CPE及MMP流程、视频/关间/奖励库存；官网营销数字不是目标游戏投放量。

- [axon/gaming-apps.html](axon/gaming-apps.html)
- [axon/gaming-apps.txt](axon/gaming-apps.txt)
- [axon/game-inventory.html](axon/game-inventory.html)
- [axon/game-inventory.txt](axon/game-inventory.txt)
- [axon/doc-scale-your-campaign.html](axon/doc-scale-your-campaign.html)
- [axon/doc-scale-your-campaign.txt](axon/doc-scale-your-campaign.txt)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 AX02（6份材料）。

<a id="ax03"></a>
## AX03 · AppLovin隐私披露与Ad Review用途边界

政策披露跨应用/设备及MMP数据类别；2026-09-16公司明确声明Ad Review不进入Axon。公开声明非独立生产审计。

- [axon/applovin-privacy.html](axon/applovin-privacy.html)
- [axon/applovin-privacy.txt](axon/applovin-privacy.txt)
- [axon/blog-data-boundary.html](axon/blog-data-boundary.html)
- [axon/blog-data-boundary.txt](axon/blog-data-boundary.txt)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 AX03（4份材料）。

<a id="ax04"></a>
## AX04 · 真实投放证据搜索范围、失败与不可移植的其他产品记录

未取得五款目标游戏×AppLovin的可靠付费投放记录；搜索挑战/429/错配/前端壳不能作正面证据。inventory的Oakever/iKame资源是其他产品和供给页线索。

- [axon/fetches-initial.json](axon/fetches-initial.json)
- [axon/fetches-discovery.json](axon/fetches-discovery.json)
- [axon/fetches-focused.json](axon/fetches-focused.json)
- [axon/fetches-final.json](axon/fetches-final.json)
- [axon/inventory-asset-observations.json](axon/inventory-asset-observations.json)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 AX04（42份材料）。

<a id="ax05"></a>
## AX05 · AppLovin追踪宏字段

campaign/创意/国家/展示应用/placement/eventID为公开支持宏，不证明目标活动使用。

- [axon/doc-tracking-url-macros.html](axon/doc-tracking-url-macros.html)
- [axon/doc-tracking-url-macros.txt](axon/doc-tracking-url-macros.txt)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 AX05（2份材料）。

<a id="tp01"></a>
## TP01 · 独立官方SDK原始材料、来源、许可与SHA256

公开Maven/厂商仓库/JitPack及官方GitHub来源；POM许可证≠任意再分发授权。Last-Modified与仓库lastUpdated非首次发布日期。Bulldog/Meevii为嵌入样本，Amaze无包。

- [ThirdPartySDKs/CATALOG.json](ThirdPartySDKs/CATALOG.json)
- [ThirdPartySDKs/COLLECTION_VALIDATION.json](ThirdPartySDKs/COLLECTION_VALIDATION.json)
- [ThirdPartySDKs/ARTIFACT_VALIDATION.json](ThirdPartySDKs/ARTIFACT_VALIDATION.json)
- [ThirdPartySDKs/ORIGINAL_SAMPLE_INTEGRITY.json](ThirdPartySDKs/ORIGINAL_SAMPLE_INTEGRITY.json)
- [ThirdPartySDKs/EMBEDDED_ONLY.json](ThirdPartySDKs/EMBEDDED_ONLY.json)
- [ThirdPartySDKs/ADAPTER_COVERAGE.json](ThirdPartySDKs/ADAPTER_COVERAGE.json)
- [ThirdPartySDKs/DETECTED_ADAPTER_MANIFEST.json](ThirdPartySDKs/DETECTED_ADAPTER_MANIFEST.json)
- [ThirdPartySDKs/DETECTED_DEPENDENCY_MANIFEST.json](ThirdPartySDKs/DETECTED_DEPENDENCY_MANIFEST.json)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP01（310份材料）。

<a id="tp02"></a>
## TP02 · 四款内置SDK版本、原始DEX方法与官方API声明差分

MAX分别13.6.4/13.2.0/13.6.2/13.6.3；Adjust5.5/5.7；AF6.14.2/6.17.5。183个选定声明匹配，不宣称方法体或整个SDK相同；方法文件包含descriptor哈希防重载覆盖。

- [ThirdPartySDKs/Embedded/car-race/audit.json](ThirdPartySDKs/Embedded/car-race/audit.json)
- [ThirdPartySDKs/Embedded/jewel-coloring/audit.json](ThirdPartySDKs/Embedded/jewel-coloring/audit.json)
- [ThirdPartySDKs/Embedded/meowdoku/audit.json](ThirdPartySDKs/Embedded/meowdoku/audit.json)
- [ThirdPartySDKs/Embedded/rotate-rings/audit.json](ThirdPartySDKs/Embedded/rotate-rings/audit.json)
- [ThirdPartySDKs/VERSION_MATCHES.json](ThirdPartySDKs/VERSION_MATCHES.json)
- [ThirdPartySDKs/API_COMPARISON.json](ThirdPartySDKs/API_COMPARISON.json)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP02（130份材料）。

<a id="tp03"></a>
## TP03 · MAX收入/公开API与13.2/13.6.4 Axon事件协议差分

13.6.4 EventServiceImpl条件化v1/app Axon载荷、axon_events默认表、dedupe/user_data/visitInfo；旧4.0/pix分支仍保留。13.2同类无新分支。MAX收入需保留precision；库能力不等于业务启用或Axon模型。

- [ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxAd.java](ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxAd.java)
- [ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxAdRevenueListener.java](ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxAdRevenueListener.java)
- [ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxAdWaterfallInfo.java](ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxAdWaterfallInfo.java)
- [ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxNetworkResponseInfo.java](ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/mediation/MaxNetworkResponseInfo.java)
- [ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/sdk/AppLovinEventParameters.java](ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/sdk/AppLovinEventParameters.java)
- [ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/sdk/AppLovinEventService.java](ThirdPartySDKs/AppLovin/MAX/13.2.0/decompiled/com/applovin/sdk/AppLovinEventService.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP03（57份材料）。

<a id="tp04"></a>
## TP04 · Adjust匹配发行版源码的收入/事件/归因包与持久队列

独立原始sources；/ad_revenue、partner_params、标识条件、队列落盘/backoff；不等于目标游戏partner送达。

- [ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/PackageBuilder.java](ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/PackageBuilder.java)
- [ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/PackageHandler.java](ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/PackageHandler.java)
- [ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/ActivityHandler.java](ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/ActivityHandler.java)
- [ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/AdjustConfig.java](ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/AdjustConfig.java)
- [ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/Adjust.java](ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/Adjust.java)
- [ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/AdjustAttribution.java](ThirdPartySDKs/Adjust/Android/5.5.0/sources/com/adjust/sdk/AdjustAttribution.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP04（16份材料）。

<a id="tp05"></a>
## TP05 · AppsFlyer匹配发行版API、广告收入载荷和磁盘缓存

官方AAR反编译，不称官方开源。AF6.17.5 logAdRevenue数据校验/状态检查，AFf1tSDK adrevenue_sdk编码，APPLOVIN_MAX仅mediation；AFRequestCache分类/限额/淘汰，不宣称恰好一次。

- [ThirdPartySDKs/AppsFlyer/Android/6.14.2/cache-candidates.json](ThirdPartySDKs/AppsFlyer/Android/6.14.2/cache-candidates.json)
- [ThirdPartySDKs/AppsFlyer/Android/6.17.5/cache-candidates.json](ThirdPartySDKs/AppsFlyer/Android/6.17.5/cache-candidates.json)
- [ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/AppsFlyerConversionListener.java](ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/AppsFlyerConversionListener.java)
- [ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/AppsFlyerLib.java](ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/AppsFlyerLib.java)
- [ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/AppsFlyerProperties.java](ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/AppsFlyerProperties.java)
- [ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/internal/AFg1rSDK.java](ThirdPartySDKs/AppsFlyer/Android/6.14.2/decompiled/com/appsflyer/internal/AFg1rSDK.java)
- [ThirdPartySDKs/AppsFlyer/Android/6.17.5/decompiled/com/appsflyer/AFAdRevenueData.java](ThirdPartySDKs/AppsFlyer/Android/6.17.5/decompiled/com/appsflyer/AFAdRevenueData.java)
- [ThirdPartySDKs/AppsFlyer/Android/6.17.5/decompiled/com/appsflyer/AppsFlyerConversionListener.java](ThirdPartySDKs/AppsFlyer/Android/6.17.5/decompiled/com/appsflyer/AppsFlyerConversionListener.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP05（29份材料）。

<a id="tp06"></a>
## TP06 · 官方MAX适配器源码与网络依赖POM

collectSignal、Google QueryInfo与各网络token、bid response载入能证中介协作；不能证明开发商通过适配网络买量。

- [ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.0.0.0/sources/com/applovin/mediation/adapters/AmazonAdMarketplaceMediationAdapter.java](ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.0.0.0/sources/com/applovin/mediation/adapters/AmazonAdMarketplaceMediationAdapter.java)
- [ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.1.1.0/sources/com/applovin/mediation/adapters/AmazonAdMarketplaceMediationAdapter.java](ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.1.1.0/sources/com/applovin/mediation/adapters/AmazonAdMarketplaceMediationAdapter.java)
- [ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.3.0.0/sources/com/applovin/mediation/adapters/AmazonAdMarketplaceMediationAdapter.java](ThirdPartySDKs/AppLovin/Adapter-amazon-tam-adapter/11.3.0.0/sources/com/applovin/mediation/adapters/AmazonAdMarketplaceMediationAdapter.java)
- [ThirdPartySDKs/AppLovin/Adapter-bidmachine-adapter/3.5.1.0/sources/com/applovin/mediation/adapters/BidMachineMediationAdapter.java](ThirdPartySDKs/AppLovin/Adapter-bidmachine-adapter/3.5.1.0/sources/com/applovin/mediation/adapters/BidMachineMediationAdapter.java)
- [ThirdPartySDKs/AppLovin/Adapter-bidmachine-adapter/3.7.1.0/sources/com/applovin/mediation/adapters/BidMachineMediationAdapter.java](ThirdPartySDKs/AppLovin/Adapter-bidmachine-adapter/3.7.1.0/sources/com/applovin/mediation/adapters/BidMachineMediationAdapter.java)
- [ThirdPartySDKs/AppLovin/Adapter-bigoads-adapter/5.9.0.0/sources/com/applovin/mediation/adapters/BigoAdsMediationAdapter.java](ThirdPartySDKs/AppLovin/Adapter-bigoads-adapter/5.9.0.0/sources/com/applovin/mediation/adapters/BigoAdsMediationAdapter.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP06（91份材料）。

<a id="tp07"></a>
## TP07 · 官方SDK用户匹配/标识与隐私条件能力

AppLovin user_data规范化/哈希是条件化能力；InMobi UnifiedID与TikTok标识/队列/受众能力不等于游戏启用；无实际身份数据采集。

- [ThirdPartySDKs/InMobi/Android/11.1.1/decompiled/com/inmobi/sdk/InMobiSdk.java](ThirdPartySDKs/InMobi/Android/11.1.1/decompiled/com/inmobi/sdk/InMobiSdk.java)
- [ThirdPartySDKs/InMobi/Android/11.1.1/decompiled/com/inmobi/unifiedId/InMobiUnifiedIdInterface.java](ThirdPartySDKs/InMobi/Android/11.1.1/decompiled/com/inmobi/unifiedId/InMobiUnifiedIdInterface.java)
- [ThirdPartySDKs/InMobi/Android/11.1.1/decompiled/com/inmobi/unifiedId/InMobiUnifiedIdService.java](ThirdPartySDKs/InMobi/Android/11.1.1/decompiled/com/inmobi/unifiedId/InMobiUnifiedIdService.java)
- [ThirdPartySDKs/Meta/FacebookCore/18.0.3/decompiled/com/facebook/appevents/AppEventQueue.java](ThirdPartySDKs/Meta/FacebookCore/18.0.3/decompiled/com/facebook/appevents/AppEventQueue.java)
- [ThirdPartySDKs/Meta/FacebookCore/18.0.3/decompiled/com/facebook/appevents/AppEventsLogger.java](ThirdPartySDKs/Meta/FacebookCore/18.0.3/decompiled/com/facebook/appevents/AppEventsLogger.java)
- [ThirdPartySDKs/Meta/FacebookCore/18.0.3/decompiled/com/facebook/appevents/AppEventStore.java](ThirdPartySDKs/Meta/FacebookCore/18.0.3/decompiled/com/facebook/appevents/AppEventStore.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP07（20份材料）。

<a id="tp08"></a>
## TP08 · 实际游戏到MAX的事件桥/用户ID、来源枚举追踪

Car UnityBridge→MeticaApplovinFunctions.trackEvent但具体游戏价值事件未知；Meow AdUuid→MAX、MediaSourceTag applovin_int枚举；Rotate ThinkingData distinctId→MAX。主DEX未建立AppLovinUserData业务链，负面范围不覆盖native/服务器。

- [ThirdPartySDKs/BUSINESS_TRACES.json](ThirdPartySDKs/BUSINESS_TRACES.json)
- [ThirdPartySDKs/BRIDGE_ANALYSIS.json](ThirdPartySDKs/BRIDGE_ANALYSIS.json)
- [ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinFunctions$1.java](ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinFunctions$1.java)
- [ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinFunctions$Companion.java](ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinFunctions$Companion.java)
- [ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinFunctions.java](ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinFunctions.java)
- [ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinInitializer$Companion.java](ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinInitializer$Companion.java)
- [ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinInitializer$initializeSdk$1.java](ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinInitializer$initializeSdk$1.java)
- [ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinInitializer$initializeSdkInternal$2$2.java](ThirdPartySDKs/Embedded/car-race/bridge-java/classes8.dex/com/metica/ads/internal/adapter/applovin/ApplovinInitializer$initializeSdkInternal$2$2.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP08（54份材料）。

<a id="tp09"></a>
## TP09 · Metica公开发行渠道、SDK与缺包/来源发现记录

Metica文档给Maven Central com.metica:metica-sdk；取到2.5.4，未证明Car内准确同版；Learnings/Bulldog独立官方发行包未取得。TikTok官方标签与JitPack匹配。

- [ThirdPartySDKs/DISCOVERY_MANIFEST.json](ThirdPartySDKs/DISCOVERY_MANIFEST.json)
- [ThirdPartySDKs/DISCOVERY_ADDITIONAL.json](ThirdPartySDKs/DISCOVERY_ADDITIONAL.json)
- [ThirdPartySDKs/DISCOVERED_MANIFEST.json](ThirdPartySDKs/DISCOVERED_MANIFEST.json)
- [ThirdPartySDKs/METICA_MANIFEST.json](ThirdPartySDKs/METICA_MANIFEST.json)
- [ThirdPartySDKs/Discovery/adjust-release-550.json](ThirdPartySDKs/Discovery/adjust-release-550.json)
- [ThirdPartySDKs/Discovery/adjust-release-570.json](ThirdPartySDKs/Discovery/adjust-release-570.json)
- [ThirdPartySDKs/Discovery/adjust-release.json](ThirdPartySDKs/Discovery/adjust-release.json)
- [ThirdPartySDKs/Discovery/learnings-github.json](ThirdPartySDKs/Discovery/learnings-github.json)
- [ThirdPartySDKs/Discovery/metica-github-org.json](ThirdPartySDKs/Discovery/metica-github-org.json)
- [ThirdPartySDKs/Discovery/metica-maven-search.json](ThirdPartySDKs/Discovery/metica-maven-search.json)
- [ThirdPartySDKs/Discovery/tiktok-contents.json](ThirdPartySDKs/Discovery/tiktok-contents.json)
- [ThirdPartySDKs/Discovery/tiktok-release-161.json](ThirdPartySDKs/Discovery/tiktok-release-161.json)
- [ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/BuildConfig.java](ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/BuildConfig.java)
- [ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/MeticaInitConfig.java](ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/MeticaInitConfig.java)
- [ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/MeticaSdk.java](ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/MeticaSdk.java)
- [ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/ads/mediation/MeticaApplovinFunctions.java](ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/ads/mediation/MeticaApplovinFunctions.java)
- [ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/ads/internal/adapter/applovin/ApplovinFunctions.java](ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/ads/internal/adapter/applovin/ApplovinFunctions.java)
- [ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/ads/internal/adapter/applovin/ApplovinInitializer.java](ThirdPartySDKs/Metica/Android/2.5.4/final-java/com/metica/ads/internal/adapter/applovin/ApplovinInitializer.java)

完整逐文件来源及SHA256：EVIDENCE_MANIFEST.json 的 TP09（33份材料）。

<!-- AXON_DEEP_20261118 -->

## Axon事件与用户ID深度专项

新增20/21/22；SDK自动直发、游戏显式业务、默认事件表和网络成功分别判断。MMP partner回传独立。本轮新证据补齐Meow AdUuid来源、Car本地GUID链及13.6.2/13.6.3协议，未取得生产事件接收或实际投放记录。

<a id="xd01"></a>
## XD01 · 四包全DEX AppLovin事件/身份调用交叉引用

15/8/14/12个DEX，所有命名空间；62条候选事件invoke含重载与SDK自动路径，不是62个业务事件。Car generic桥可见，其他三款未建立SDK外显式事件调用；native/反射/服务端另论。

- [axon/deep/games/car-race/calls.json](axon/deep/games/car-race/calls.json)
- [axon/deep/games/jewel-coloring/calls.json](axon/deep/games/jewel-coloring/calls.json)
- [axon/deep/games/meowdoku/calls.json](axon/deep/games/meowdoku/calls.json)
- [axon/deep/games/rotate-rings/calls.json](axon/deep/games/rotate-rings/calls.json)
- [axon/deep/game-scan-summary.json](axon/deep/game-scan-summary.json)
- [axon/deep/event-callsite-catalog.json](axon/deep/event-callsite-catalog.json)
- [axon/deep/identity-callsite-catalog.json](axon/deep/identity-callsite-catalog.json)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD01（455份材料）。

<a id="xd02"></a>
## XD02 · Car原生/Unity桥入口与trackEvent字面量归属

Car两个generic bridge存在但具体游戏触发未证；原生metadata trackEvent字面量可在AdjustAndroid.TrackEvent RVA0xDE7BF0定位，不作为MAX直发证据。ARM来自原包同哈希SO/metadata；未使用托管stub证明实现。

- [axon/deep/native-car/callers.json](axon/deep/native-car/callers.json)
- [axon/deep/native-car/metadata-target-literals.json](axon/deep/native-car/metadata-target-literals.json)
- [axon/deep/native-car/method-evidence.json](axon/deep/native-car/method-evidence.json)
- [axon/deep/native-car/user-id-intermediate-check.json](axon/deep/native-car/user-id-intermediate-check.json)
- [car-race/reused-evidence/monetization-20261117/method-index.json](car-race/reused-evidence/monetization-20261117/method-index.json)
- [axon/deep/bridges/car-race/classes10.dex/java/com/metica/unity_bridge/UnityBridge.java](axon/deep/bridges/car-race/classes10.dex/java/com/metica/unity_bridge/UnityBridge.java)
- [axon/deep/bridges/car-race/classes10.dex/java/com/metica/internal/repository/ConfigCache$CachedData$$serializer.java](axon/deep/bridges/car-race/classes10.dex/java/com/metica/internal/repository/ConfigCache$CachedData$$serializer.java)
- [axon/deep/bridges/car-race/classes10.dex/java/com/metica/internal/repository/ConfigCache$CachedData$Companion.java](axon/deep/bridges/car-race/classes10.dex/java/com/metica/internal/repository/ConfigCache$CachedData$Companion.java)
- [axon/deep/bridges/car-race/classes10.dex/java/com/metica/internal/repository/ConfigCache$CachedData.java](axon/deep/bridges/car-race/classes10.dex/java/com/metica/internal/repository/ConfigCache$CachedData.java)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD02（153份材料）。

<a id="xd03"></a>
## XD03 · 四个匹配MAX版本事件协议与SDK自动调用方

13.6.2/13.6.3/13.6.4有v1/app与相同默认42名表；13.2同类无。SDK自动landing默认旧路由。callsite与反编译受原始JVM/DEX佐证，不推断生产生效配置和初次发布日期。

- [axon/deep/versions/13.2.0/constant-pool-refs.json](axon/deep/versions/13.2.0/constant-pool-refs.json)
- [axon/deep/versions/13.6.2/constant-pool-refs.json](axon/deep/versions/13.6.2/constant-pool-refs.json)
- [axon/deep/versions/13.6.3/constant-pool-refs.json](axon/deep/versions/13.6.3/constant-pool-refs.json)
- [axon/deep/versions/13.6.4/constant-pool-refs.json](axon/deep/versions/13.6.4/constant-pool-refs.json)
- [axon/deep/protocol-matrix.json](axon/deep/protocol-matrix.json)
- [axon/deep/numbered-excerpts.json](axon/deep/numbered-excerpts.json)
- [axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/EventServiceImpl.java](axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/EventServiceImpl.java)
- [axon/deep/versions/13.6.2/java/com/applovin/impl/sdk/EventServiceImpl.java](axon/deep/versions/13.6.2/java/com/applovin/impl/sdk/EventServiceImpl.java)
- [axon/deep/versions/13.6.3/java/com/applovin/impl/sdk/EventServiceImpl.java](axon/deep/versions/13.6.3/java/com/applovin/impl/sdk/EventServiceImpl.java)
- [axon/deep/versions/13.6.4/java/com/applovin/impl/sdk/EventServiceImpl.java](axon/deep/versions/13.6.4/java/com/applovin/impl/sdk/EventServiceImpl.java)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD03（152份材料）。

<a id="xd04"></a>
## XD04 · MAX持久postback队列到网络任务与回调

PersistentPostbackManager network.b、network.c磁盘pb队列、PostbackServiceImpl、TaskDispatchPostback/网络类及成功失败回调均保留；客户端postback不是MMP partner postback。没有成功发送运行观测。

- [axon/deep/games/car-race/sinks.json](axon/deep/games/car-race/sinks.json)
- [axon/deep/games/jewel-coloring/sinks.json](axon/deep/games/jewel-coloring/sinks.json)
- [axon/deep/games/meowdoku/sinks.json](axon/deep/games/meowdoku/sinks.json)
- [axon/deep/games/rotate-rings/sinks.json](axon/deep/games/rotate-rings/sinks.json)
- [axon/deep/network-candidates.json](axon/deep/network-candidates.json)
- [axon/deep/network-decompilation.json](axon/deep/network-decompilation.json)
- [axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/b.java](axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/b.java)
- [axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/c.java](axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/c.java)
- [axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/d.java](axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/d.java)
- [axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/e.java](axon/deep/versions/13.2.0/java/com/applovin/impl/sdk/network/e.java)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD04（863份材料）。

<a id="xd05"></a>
## XD05 · MAX用户ID管理器到cuid与请求/事件逻辑字段

setUserIdentifier预attach缓存/attach转交；pui默认持久化com.applovin.sdk.user_id，qq3默认传cuid；旧事件扁平map、新事件/广告请求app_info。逻辑字段不等于已观察线上字节。

- [axon/deep/type-resolution.json](axon/deep/type-resolution.json)
- [axon/deep/versions/13.2.0/java/com/applovin/sdk/AppLovinSdkSettings.java](axon/deep/versions/13.2.0/java/com/applovin/sdk/AppLovinSdkSettings.java)
- [axon/deep/versions/13.6.2/java/com/applovin/sdk/AppLovinSdkSettings.java](axon/deep/versions/13.6.2/java/com/applovin/sdk/AppLovinSdkSettings.java)
- [axon/deep/versions/13.6.3/java/com/applovin/sdk/AppLovinSdkSettings.java](axon/deep/versions/13.6.3/java/com/applovin/sdk/AppLovinSdkSettings.java)
- [axon/deep/versions/13.6.4/java/com/applovin/sdk/AppLovinSdkSettings.java](axon/deep/versions/13.6.4/java/com/applovin/sdk/AppLovinSdkSettings.java)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD05（22份材料）。

<a id="xd06"></a>
## XD06 · 三款实际用户ID上游与Meow AF/MAX同源补证

Meow builder从AnalyzeManager UUID设AdUuid，与既有AF CUID同源；Rotate distinctId→MAX；Car本地GUID/测试覆盖→initConfig→Metica preservedID→MAX。静态条件链，不读取实际ID，不推跨应用。

- [axon/deep/metica-car-index.json](axon/deep/metica-car-index.json)
- [axon/deep/bridge-decompilation.json](axon/deep/bridge-decompilation.json)
- [ThirdPartySDKs/BUSINESS_TRACES.json](ThirdPartySDKs/BUSINESS_TRACES.json)
- [axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/AdInitParameter$Builder.java](axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/AdInitParameter$Builder.java)
- [axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/AdInitParameter.java](axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/AdInitParameter.java)
- [axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/common/AdUuid.java](axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/common/AdUuid.java)
- [axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/common/SharedProxy.java](axon/deep/bridges/meowdoku/classes5.dex/java/com/meevii/adsdk/common/SharedProxy.java)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD06（27份材料）。

<a id="xd07"></a>
## XD07 · 配置更新、13.6.4独立user_data与字段条件

SettingsManager按注册key读取JSON/缓存生效值；默认不等于生产。user_data独立对象，send_user_data默认true但需非空有效输入；setUserIdentifier不创建该对象；13.6.4广告请求也可消费。

- [axon/deep/versions/13.2.0/final/com/applovin/impl/e5$b.java](axon/deep/versions/13.2.0/final/com/applovin/impl/e5$b.java)
- [axon/deep/versions/13.2.0/final/com/applovin/impl/m4.java](axon/deep/versions/13.2.0/final/com/applovin/impl/m4.java)
- [axon/deep/versions/13.2.0/final/com/applovin/impl/n4.java](axon/deep/versions/13.2.0/final/com/applovin/impl/n4.java)
- [axon/deep/versions/13.6.2/final/com/applovin/impl/a5.java](axon/deep/versions/13.6.2/final/com/applovin/impl/a5.java)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD07（17份材料）。

<a id="xd08"></a>
## XD08 · 新增公开投放记录调查与静态证据校验

官方博客搜索仅壳；Yahoo准确目标查询500；仍未取得产品×AppLovin付费投放记录。VALIDATION核对原始DEX协议字段、原始SO/metadata与archive一致，不证明生产送达。

- [axon/deep/public-probe.json](axon/deep/public-probe.json)
- [axon/deep-official-blog-search-links.json](axon/deep-official-blog-search-links.json)
- [axon/deep-yahoo-meow-links.json](axon/deep-yahoo-meow-links.json)
- [axon/deep-yahoo-rotate-links.json](axon/deep-yahoo-rotate-links.json)
- [axon/deep-yahoo-car-links.json](axon/deep-yahoo-car-links.json)
- [axon/deep-yahoo-jewel-links.json](axon/deep-yahoo-jewel-links.json)
- [axon/deep/VALIDATION.json](axon/deep/VALIDATION.json)

完整原始位置与SHA256见EVIDENCE_MANIFEST.json的XD08（19份材料）。


<!-- VECTOR_AXON_STUDY_2026_11_18 -->

<a id="vg01"></a>

## VG01 · Unity 2025—2026 已实现季度财报与分类口径

官方公开证实；不把 Strategic Grow 或公司收入当 Vector/广告主 ROAS。

- [unity-ir-2025-q1 公开原文](https://investors.unity.com/news/news-details/2025/Unity-Reports-First-Quarter-2025-Financial-Results/default.aspx)；[本地原始响应](vector/unity-ir-2025-q1.html)
- [unity-ir-2025-q2 公开原文](https://investors.unity.com/news/news-details/2025/Unity-Reports-Second-Quarter-2025-Financial-Results/default.aspx)；[本地原始响应](vector/unity-ir-2025-q2.html)
- [unity-ir-2025-q3 公开原文](https://investors.unity.com/news/news-details/2025/Unity-Reports-Third-Quarter-2025-Financial-Results/default.aspx)；[本地原始响应](vector/unity-ir-2025-q3.html)
- [unity-q4-2025-final 公开原文](https://investors.unity.com/news/news-details/2026/Unity-Reports-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx)；[本地原始响应](vector/unity-q4-2025-final.html)
- [unity-ir-2026-q1 公开原文](https://investors.unity.com/news/news-details/2026/Unity-Reports-First-Quarter-2026-Financial-Results/default.aspx)；[本地原始响应](vector/unity-ir-2026-q1.html)
- [unity-ir-2026-q2 公开原文](https://investors.unity.com/news/news-details/2026/Unity-Reports-Second-Quarter-2026-Financial-Results/default.aspx)；[本地原始响应](vector/unity-ir-2026-q2.html)
- [unity-ir-2026-q3 公开原文](https://investors.unity.com/news/news-details/2026/Unity-Reports-Third-Quarter-2026-Financial-Results/default.aspx)；[本地原始响应](vector/unity-ir-2026-q3.html)
- [vector/FINANCIAL_COMPARISON.csv](vector/FINANCIAL_COMPARISON.csv)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG01。

<a id="vg02"></a>

## VG02 · AppLovin 同期广告/持续经营收入

官方公开证实；排除 2025Q1 Apps 收入，保留后续终止经营重列背景。

- [app-ir-2025-q1 公开原文](https://investors.applovin.com/news/news-details/2025/AppLovin-Announces-First-Quarter-2025-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2025-q1.html)
- [app-ir-2025-q2 公开原文](https://investors.applovin.com/news/news-details/2025/AppLovin-Announces-Second-Quarter-2025-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2025-q2.html)
- [app-ir-2025-q3 公开原文](https://investors.applovin.com/news/news-details/2025/AppLovin-Announces-Third-Quarter-2025-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2025-q3.html)
- [app-ir-2025-q4 公开原文](https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2025-q4.html)
- [app-ir-2026-q1 公开原文](https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-First-Quarter-2026-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2026-q1.html)
- [app-ir-2026-q2 公开原文](https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Second-Quarter-2026-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2026-q2.html)
- [app-ir-2026-q3 公开原文](https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Third-Quarter-2026-Financial-Results/default.aspx)；[本地原始响应](vector/app-ir-2026-q3.html)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG02。

<a id="vg03"></a>

## VG03 · Vector 产品、D28 发布和学习门槛

官方公开证实；beta、内部测试与厂商案例有限定，未证明战胜 Axon。

- [unity-vector-correct 公开原文](https://unity.com/products/unity-ads/vector)；[本地原始响应](vector/unity-vector-correct.html)
- [d28-blog 公开原文](https://unity.com/blog/d28-roas)；[本地原始响应](vector/d28-blog.html)
- [d7-d28-iap 公开原文](https://unity.com/blog/d7-vs-d28-iap-roas-campaigns)；[本地原始响应](vector/d7-d28-iap.html)
- [doc-intro-to-roas-campaigns 公开原文](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md)；[本地原始响应](vector/doc-intro-to-roas-campaigns.html)
- [doc-roas-campaign-best-practices 公开原文](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/roas-campaign-best-practices.md)；[本地原始响应](vector/doc-roas-campaign-best-practices.html)
- [vector-link-unico-studio 公开原文](https://unity.com/resources/unico-studio)；[本地原始响应](vector/vector-link-unico-studio.html)
- [vector-link-zephyrmobile 公开原文](https://unity.com/resources/zephyrmobile)；[本地原始响应](vector/vector-link-zephyrmobile.html)
- [vector-link-voodoo 公开原文](https://unity.com/resources/voodoo)；[本地原始响应](vector/vector-link-voodoo.html)
- [unity-2026-keynote 公开原文](https://unity.com/blog/unite-seoul-keynote-2026-recap)；[本地原始响应](vector/unity-2026-keynote.html)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG03。

<a id="vg04"></a>

## VG04 · Unity 与 MMP 事件/广告收入共享及独立 S2S 协议

官方公开证实；partner/Game ID/授权和映射不等于目标游戏启用；没有访问事件端点。

- [doc-integrate-adjust-with-unity 公开原文](https://docs.unity.com/en-us/grow/acquire/partner-integration/adjust/integrate-adjust-with-unity.md)；[本地原始响应](vector/doc-integrate-adjust-with-unity.html)
- [doc-integrate-appsflyer-with-unity 公开原文](https://docs.unity.com/en-us/grow/acquire/partner-integration/appsflyer/integrate-appsflyer-with-unity.md)；[本地原始响应](vector/doc-integrate-appsflyer-with-unity.html)
- [unity-ads-partner 公开原文](https://help.adjust.com/en/partner-setup/unity-ads)；[本地原始响应](vector/unity-ads-partner.html)
- [af-unity-partner 公开原文](https://support.appsflyer.com/hc/en-us/articles/208005086-Unity-Ads-campaign-configuration)；[本地原始响应](vector/af-unity-partner.html)
- [doc-send-postbacks 公开原文](https://docs.unity.com/en-us/grow/acquire/partner-integration/custom/send-postbacks.md)；[本地原始响应](vector/doc-send-postbacks.html)
- [doc-postback-request 公开原文](https://docs.unity.com/en-us/grow/acquire/partner-integration/custom/postback-request.md)；[本地原始响应](vector/doc-postback-request.html)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG04。

<a id="vg05"></a>

## VG05 · Unity Ads 4.17/4.18.1 与 LevelPlay 9.3/9.4/9.5 选定代码

SDK代码证实；请求/竞价/广告事件/队列/隐私与ILRD，不声称恢复 Vector 服务端。

- [vector/SDK_AUDIT.json](vector/SDK_AUDIT.json)
- [vector/CODE_EVIDENCE.json](vector/CODE_EVIDENCE.json)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdRequest.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdRequest.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/OperativeEventObserver.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/OperativeEventObserver.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/UniversalRequestEventSender.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/events/UniversalRequestEventSender.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/work/OperativeEventJob.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/work/OperativeEventJob.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonGetHeaderBiddingToken.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonGetHeaderBiddingToken.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/LegacyShowUseCase.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/LegacyShowUseCase.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java)
- [vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/ads/core/domain/AndroidGetAdRequest.java](vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/ads/core/domain/AndroidGetAdRequest.java)
- [vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.java](vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/ads/core/domain/events/GetOperativeEventRequest.java)
- [vector/sdk/Unity/LevelPlay/9.3.0/java/com/unity3d/mediation/LevelPlayAdInfo.java](vector/sdk/Unity/LevelPlay/9.3.0/java/com/unity3d/mediation/LevelPlayAdInfo.java)
- [vector/sdk/Unity/Dependency-mediation-sdk/9.4.0/java/com/unity3d/mediation/LevelPlayAdInfo.java](vector/sdk/Unity/Dependency-mediation-sdk/9.4.0/java/com/unity3d/mediation/LevelPlayAdInfo.java)
- [vector/sdk/Unity/LevelPlay/9.5.0/java/com/unity3d/mediation/LevelPlayAdInfo.java](vector/sdk/Unity/LevelPlay/9.5.0/java/com/unity3d/mediation/LevelPlayAdInfo.java)
- [vector/sdk/Unity/LevelPlay/9.5.0/java/com/unity3d/mediation/LevelPlay.java](vector/sdk/Unity/LevelPlay/9.5.0/java/com/unity3d/mediation/LevelPlay.java)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG05。

<a id="vg06"></a>

## VG06 · Developer Data Runtime 框架、官方 6000.3 Consent 参考绑定

官方公开证实、SDK代码证实；收集/用途/consent 分离；不能证明四款 Runtime 到 Vector 生产链。

- [ddf-doc-md 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework.md)；[本地原始响应](vector/ddf-doc-md.html)
- [ddf-data-collection-settings 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/data-collection-settings.md)；[本地原始响应](vector/ddf-data-collection-settings.html)
- [ddf-data-usage-settings 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/data-usage-settings.md)；[本地原始响应](vector/ddf-data-usage-settings.html)
- [ddf-end-user-consent 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/end-user-consent.md)；[本地原始响应](vector/ddf-end-user-consent.html)
- [ddf-your-data-in-action 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/your-data-in-action.md)；[本地原始响应](vector/ddf-your-data-in-action.html)
- [ddf-what-is-developer-data 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/what-is-developer-data.md)；[本地原始响应](vector/ddf-what-is-developer-data.html)
- [ddf-how-the-framework-works 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/how-the-framework-works.md)；[本地原始响应](vector/ddf-how-the-framework-works.html)
- [ddf-getting-started 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/getting-started.md)；[本地原始响应](vector/ddf-getting-started.html)
- [ddf-external-data-integration 公开原文](https://docs.unity.com/en-us/cloud/developer-data-framework/external-data-integration.md)；[本地原始响应](vector/ddf-external-data-integration.html)
- [developer-data-terms 公开原文](https://unity.com/legal/developer-data-framework-additional-terms)；[本地原始响应](vector/developer-data-terms.html)
- [developer-data-legacy 公开原文](https://unity.com/legal/developer-data-framework-additional-terms-legacy)；[本地原始响应](vector/developer-data-legacy.html)
- [doc-configure-diagnostics-editor 公开原文](https://docs.unity.com/en-us/cloud/developer-data/configure-diagnostics-editor.md)；[本地原始响应](vector/doc-configure-diagnostics-editor.html)
- [unity-runtime-cs-release 公开原文](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/6000.3/Modules/UnityConsent/EndUserConsent.bindings.cs)；[本地原始响应](vector/unity-runtime-cs-release.html)
- [unity-runtime-cs-release-state 公开原文](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/6000.3/Modules/UnityConsent/ConsentState.bindings.cs)；[本地原始响应](vector/unity-runtime-cs-release-state.html)
- [unity-ddf-consent-api 公开原文](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/UnityConsent.EndUserConsent.SetConsentState.html)；[本地原始响应](vector/unity-ddf-consent-api.html)
- [unity-runtime-blog-keynote 公开原文](https://unity.com/blog/highlights-from-unite-2025-keynote)；[本地原始响应](vector/unity-runtime-blog-keynote.html)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG06。

<a id="vg07"></a>

## VG07 · Unity Exchange 公开竞价与美加 RampID 接入

官方公开证实；商业身份互通能力，不证明四款或 Vector 使用，更不证明全部库存被 Vector 购买。

- [doc-get-started 公开原文](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/get-started.md)；[本地原始响应](vector/doc-get-started.html)
- [exchange-rampid 公开原文](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)；[本地原始响应](vector/exchange-rampid.html)
- [exchange-tools 公开原文](https://unity.com/blog/ironsource-expands-its-ad-exchange-with-powerful-new-tools)；[本地原始响应](vector/exchange-tools.html)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG07。

<a id="vg08"></a>

## VG08 · 可复算的 IAA ROAS 离线模型与校验

合成经济场景及计算校验；不是实测投放或任一平台精度。

- [vector/model/inputs.json](vector/model/inputs.json)
- [vector/model/roas_model.py](vector/model/roas_model.py)
- [vector/model/verify_model.py](vector/model/verify_model.py)
- [vector/model/plot_model.py](vector/model/plot_model.py)
- [vector/model/MODEL_VALIDATION.json](vector/model/MODEL_VALIDATION.json)
- [vector/model/output/arms.csv](vector/model/output/arms.csv)
- [vector/model/output/daily_actual_template.csv](vector/model/output/daily_actual_template.csv)
- [vector/model/output/economics.png](vector/model/output/economics.png)
- [vector/model/output/learning.csv](vector/model/output/learning.csv)
- [vector/model/output/prediction_bias.csv](vector/model/output/prediction_bias.csv)
- [vector/model/output/results.json](vector/model/output/results.json)
- [vector/model/output/scaling.csv](vector/model/output/scaling.csv)

完整来源、抓取时间和 SHA256 见 EVIDENCE_MANIFEST.json 的 VG08。


<!-- NON_GAME_ECOSYSTEM_2026_11_19 -->

<a id="ng01"></a>

## NG01 · AppLovin 网站事件、GTM/Shopify 接入和隐私要求

官方公开证实；接口要求不是所有商家已启用，隐私约束与事件语义单列。

- [doc-events 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/events-and-objects)；[本地快照](nongame/doc-events.raw)；HTTP 200
- [doc-gtm 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/google-tag-manager)；[本地快照](nongame/doc-gtm.raw)；HTTP 200
- [doc-shopify 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/shopify-integration)；[本地快照](nongame/doc-shopify.raw)；HTTP 200
- [app-shopify 原始来源](https://apps.shopify.com/axon)；[本地快照](nongame/app-shopify.raw)；HTTP 200
- [doc-privacy 原始来源](https://support.applovin.com/en/growth/introduction/privacy-guidelines)；[本地快照](nongame/doc-privacy.raw)；HTTP 200
- [doc-data-sharing 原始来源](https://legal.applovin.com/data-sharing-requirements/)；[本地快照](nongame/doc-data-sharing.raw)；HTTP 200

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG01。

<a id="ng02"></a>

## NG02 · CAPI、去重、历史客户订单和转化衡量

官方公开证实；没有向生产端点发请求，未读取或使用商家凭证。

- [doc-capi 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api)；[本地快照](nongame/doc-capi.raw)；HTTP 200
- [doc-dedupe 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/deduplicating-events)；[本地快照](nongame/doc-dedupe.raw)；HTTP 200
- [doc-order-history 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/order-history-data)；[本地快照](nongame/doc-order-history.raw)；HTTP 200
- [doc-attribution 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/measurement-and-attribution)；[本地快照](nongame/doc-attribution.raw)；HTTP 200

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG02。

<a id="ng03"></a>

## NG03 · 独立 Axon Android 1.3.4 发行包与非游戏App接口

SDK代码证实为公开API/发行物；文档哈希及匹配语义另列。不是目标App实装版本，也未完整恢复该SDK私有队列/网络。

- [doc-android-axon 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/mobile-app-integration/android/integration)；[本地快照](nongame/doc-android-axon.raw)；HTTP 200
- [doc-ios-axon 原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/mobile-app-integration/ios/integration)；[本地快照](nongame/doc-ios-axon.raw)；HTTP 200
- [axon-sdk-metadata 原始来源](https://repo.maven.apache.org/maven2/com/applovin/axon-sdk/maven-metadata.xml)；[本地快照](nongame/axon-sdk-metadata.raw)；HTTP 200
- [axon-sdk-pom 原始来源](https://repo.maven.apache.org/maven2/com/applovin/axon-sdk/1.3.4/axon-sdk-1.3.4.pom)；[本地快照](nongame/axon-sdk-pom.raw)；HTTP 200
- [nongame/sdk/axon/1.3.4/AppLovinInitProvider.javap.txt](nongame/sdk/axon/1.3.4/AppLovinInitProvider.javap.txt)
- [nongame/sdk/axon/1.3.4/archive-index.json](nongame/sdk/axon/1.3.4/archive-index.json)
- [nongame/sdk/axon/1.3.4/axon-sdk-1.3.4.aar](nongame/sdk/axon/1.3.4/axon-sdk-1.3.4.aar)
- [nongame/sdk/axon/1.3.4/Axon.javap.txt](nongame/sdk/axon/1.3.4/Axon.javap.txt)
- [nongame/sdk/axon/1.3.4/AxonEventService.javap.txt](nongame/sdk/axon/1.3.4/AxonEventService.javap.txt)
- [nongame/sdk/axon/1.3.4/AxonInitializationConfiguration.javap.txt](nongame/sdk/axon/1.3.4/AxonInitializationConfiguration.javap.txt)
- [nongame/sdk/axon/1.3.4/AxonPrivacySettings.javap.txt](nongame/sdk/axon/1.3.4/AxonPrivacySettings.javap.txt)
- [nongame/sdk/axon/1.3.4/AxonUserData.javap.txt](nongame/sdk/axon/1.3.4/AxonUserData.javap.txt)
- [nongame/sdk/axon/1.3.4/classes.jar](nongame/sdk/axon/1.3.4/classes.jar)
- [nongame/sdk/axon/1.3.4/classes.json](nongame/sdk/axon/1.3.4/classes.json)
- [nongame/sdk/axon/1.3.4/provenance.json](nongame/sdk/axon/1.3.4/provenance.json)

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG03。

<a id="ng04"></a>

## NG04 · 9款非游戏 App 的官方政策与商店身份

公开资料证实6款具名、1款发行商级范围、2款未证目标接入；没有APK版本/初始化/生产流量证明。

- [utility-zedge 原始来源](https://www.zedge.net/privacy)；[本地快照](nongame/utility-zedge.raw)；HTTP 200
- [utility-zedge-play 原始来源](https://play.google.com/store/apps/details?id=net.zedge.android)；[本地快照](nongame/utility-zedge-play.raw)；HTTP 200
- [utility-inshot 原始来源](https://inshot.com/privacy.html)；[本地快照](nongame/utility-inshot.raw)；HTTP 200
- [utility-inshot-play 原始来源](https://play.google.com/store/apps/details?id=com.camerasideas.instashot)；[本地快照](nongame/utility-inshot-play.raw)；HTTP 200
- [utility-flashlight-correct 原始来源](https://www.rvappstudios.com/privacypolicy.html)；[本地快照](nongame/utility-flashlight-correct.raw)；HTTP 200
- [utility-flashlight-play 原始来源](https://play.google.com/store/apps/details?id=com.rvappstudios.flashlight)；[本地快照](nongame/utility-flashlight-play.raw)；HTTP 200
- [content-dramabox 原始来源](https://www.dramabox.com/privacy)；[本地快照](nongame/content-dramabox.raw)；HTTP 200
- [content-dramabox-play 原始来源](https://play.google.com/store/apps/details?id=com.storymatrix.drama)；[本地快照](nongame/content-dramabox-play.raw)；HTTP 200
- [content-reelshort-official-policy 原始来源](https://crazymaplestudios.com/v/privacy-agreement.html)；[本地快照](nongame/content-reelshort-official-policy.raw)；HTTP 200
- [content-reelshort-play 原始来源](https://play.google.com/store/apps/details?id=com.newleaf.app.android.victor)；[本地快照](nongame/content-reelshort-play.raw)；HTTP 200
- [content-audiomack-official-policy 原始来源](https://audiomack.com/about/privacy-policy)；[本地快照](nongame/content-audiomack-official-policy.raw)；HTTP 200
- [content-audiomack-play 原始来源](https://play.google.com/store/apps/details?id=com.audiomack)；[本地快照](nongame/content-audiomack-play.raw)；HTTP 200
- [life-winwalk 原始来源](https://www.winwalk.app/privacy-policy)；[本地快照](nongame/life-winwalk.raw)；HTTP 200
- [life-winwalk-play 原始来源](https://play.google.com/store/apps/details?id=com.winwalk.android)；[本地快照](nongame/life-winwalk-play.raw)；HTTP 200
- [life-weward-correct 原始来源](https://www.wewardapp.com/legal/privacy-policy)；[本地快照](nongame/life-weward-correct.raw)；HTTP 200
- [life-cashwalk 原始来源](https://cashwalklabs.io/privacy-policy)；[本地快照](nongame/life-cashwalk.raw)；HTTP 200
- [life-cashwalk-play 原始来源](https://play.google.com/store/apps/details?id=com.cashwalklabs.cashwalk)；[本地快照](nongame/life-cashwalk-play.raw)；HTTP 200
- [nongame/SAMPLE_CATALOG.json](nongame/SAMPLE_CATALOG.json)

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG04。

<a id="ng05"></a>

## NG05 · 3个商家真实网页嵌入与Gruns/Blissy反例边界

公开网页代码证实主题嵌入/配置；未执行脚本或读取购物车。CMP text/plain 和通用来源表不能冒充事件发送。

- [site-hexclad 原始来源](https://hexclad.com/pages/privacy-policy)；[本地快照](nongame/site-hexclad.raw)；HTTP 200
- [site-hexclad-home 原始来源](https://hexclad.com/)；[本地快照](nongame/site-hexclad-home.raw)；HTTP 200
- [site-resparked 原始来源](https://resparked.com/policies/privacy-policy)；[本地快照](nongame/site-resparked.raw)；HTTP 200
- [site-resparked-home 原始来源](https://resparked.com/)；[本地快照](nongame/site-resparked-home.raw)；HTTP 200
- [site-trueclassic 原始来源](https://www.trueclassictees.com/policies/privacy-policy)；[本地快照](nongame/site-trueclassic.raw)；HTTP 200
- [site-gruns 原始来源](https://gruns.co/policies/privacy-policy)；[本地快照](nongame/site-gruns.raw)；HTTP 200
- [site-gruns-home 原始来源](https://gruns.co/)；[本地快照](nongame/site-gruns-home.raw)；HTTP 200
- [site-blissy 原始来源](https://blissy.com/pages/privacy-policy)；[本地快照](nongame/site-blissy.raw)；HTTP 200
- [site-ridge 原始来源](https://ridge.com/pages/privacy-policy)；[本地快照](nongame/site-ridge.raw)；HTTP 200
- [site-obvi 原始来源](https://myobvi.com/policies/privacy-policy)；[本地快照](nongame/site-obvi.raw)；HTTP 200
- [nongame/SOURCE_EXCERPTS.json](nongame/SOURCE_EXCERPTS.json)

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG05。

<a id="ng06"></a>

## NG06 · 公开Pixel字符串表、条件采集、匹配分支及Shopify归因资产

公开网页代码证实静态实现；a/1.5.46、496项字符串唯一轮转161；没有执行JS、查询带商家key配置或收集真实邮箱/cookie。

- [pixel-source 原始来源](https://s.axon.ai/pixel.js)；[本地快照](nongame/pixel-source.raw)；HTTP 200
- [site-hexclad-embed 原始来源](https://cdn.shopify.com/extensions/01a1d715-90ff-762d-a244-f5fd2461e624/applovin-shop-integration-103/assets/app-embed.js)；[本地快照](nongame/site-hexclad-embed.raw)；HTTP 200
- [site-gruns-loader 原始来源](https://c.albss.com/p/l/loader.iife.js)；[本地快照](nongame/site-gruns-loader.raw)；HTTP 200
- [nongame/analyze_pixel.py](nongame/analyze_pixel.py)
- [nongame/pixel-string-table.json](nongame/pixel-string-table.json)
- [nongame/pixel-partial-static.js](nongame/pixel-partial-static.js)
- [nongame/PIXEL_STATIC_EVIDENCE.json](nongame/PIXEL_STATIC_EVIDENCE.json)

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG06。

<a id="ng07"></a>

## NG07 · Wurl CTV内容情境与隐私范围

官方公开证实场景标签、观看行为受众和DSP产品能力；媒体观众政策403，企业网站政策明确不适用，不推定Wurl到Axon字段流。

- [wurl-home 原始来源](https://www.wurl.com/)；[本地快照](nongame/wurl-home.raw)；HTTP 200
- [wurl-advertising 原始来源](https://www.wurl.com/solutions/wurl-advertising/)；[本地快照](nongame/wurl-advertising.raw)；HTTP 200
- [wurl-policy-correct 原始来源](https://www.wurl.com/privacy-notice/)；[本地快照](nongame/wurl-policy-correct.raw)；HTTP 200
- [wurl-media-policy 原始来源](https://www.wurl.com/wurl-advertising-and-media-services-privacy-notice/)；[本地快照](nongame/wurl-media-policy.raw)；HTTP 403

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG07。

<a id="ng08"></a>

## NG08 · Unity非游戏/Exchange/外部数据与具名AppLovin竞价伙伴

官方公开证实协议和共享用途声明，未取得逐笔交易；含Player Sign In跨项目能力，不证明广告训练关联。

- [unity-policy 原始来源](https://unity.com/legal/game-player-and-app-user-privacy-policy)；[本地快照](nongame/unity-policy.raw)；HTTP 200
- [unity-exchange-bid-fields 原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-requests.md)；[本地快照](nongame/unity-exchange-bid-fields.raw)；HTTP 200
- [unity-ads-android-native 原始来源](https://docs.unity.com/en-us/grow/ads/android-sdk/initialize-sdk.md)；[本地快照](nongame/unity-ads-android-native.raw)；HTTP 200
- [unity-ddf-external 原始来源](https://docs.unity.com/en-us/cloud/developer-data-framework/external-data-integration.md)；[本地快照](nongame/unity-ddf-external.raw)；HTTP 200
- [unity-analytics-correct 原始来源](https://docs.unity.com/ugs/en-us/manual/analytics/manual/record-custom-events)；[本地快照](nongame/unity-analytics-correct.raw)；HTTP 200
- [unity-analytics-revenue 原始来源](https://docs.unity.com/ugs/en-us/manual/analytics/manual/record-transaction-events)；[本地快照](nongame/unity-analytics-revenue.raw)；HTTP 200

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG08。

<a id="ng09"></a>

## NG09 · AppLovin跨数字属性数据与Axon公开模型说明

官方公开证实跨app/网站个性化能力、广告主自愿数据及自身MAX win/loss；明示排除其他竞价者用户/出价和敏感/特定受保护类别。不是商家到游戏IAA的逐字段训练证明。

- [applovin-policy-direct 原始来源](https://legal.applovin.com/privacy/)；[本地快照](nongame/applovin-policy-direct.raw)；HTTP 200
- [applovin-axon-about 原始来源](https://legal.applovin.com/about-applovins-axon-ai/)；[本地快照](nongame/applovin-axon-about.raw)；HTTP 200
- [consumer-brands 原始来源](https://www.applovin.com/en/consumer-brands)；[本地快照](nongame/consumer-brands.raw)；HTTP 200

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG09。

<a id="ng10"></a>

## NG10 · 本轮采集方法、候选失败与静态证据目录

包含403/429/404/搜索壳及错误重定向；抓取数量不是有效证据数量。无生产事件或设备访问。

- [nongame/PUBLIC_SOURCE_INDEX.json](nongame/PUBLIC_SOURCE_INDEX.json)
- [nongame/build_evidence.py](nongame/build_evidence.py)
- [nongame/collect.py](nongame/collect.py)
- [nongame/download_axon.py](nongame/download_axon.py)
- [nongame/fetches-deep.json](nongame/fetches-deep.json)
- [nongame/fetches-final-sources.json](nongame/fetches-final-sources.json)
- [nongame/fetches-focus.json](nongame/fetches-focus.json)
- [nongame/fetches-initial.json](nongame/fetches-initial.json)
- [nongame/fetches-last-batch.json](nongame/fetches-last-batch.json)
- [nongame/fetches-precise-policies.json](nongame/fetches-precise-policies.json)
- [nongame/fetches-resolve-last.json](nongame/fetches-resolve-last.json)
- [nongame/fetches-resolved.json](nongame/fetches-resolved.json)
- [nongame/fetches-samples-next.json](nongame/fetches-samples-next.json)

完整SHA256及抓取时间见 EVIDENCE_MANIFEST.json 的 NG10。

<!-- IDENTITY_GRAPH_2026_11_19 -->

<a id="ig01"></a>

## IG01 · MAX Android设备ID、App Set与发布者/客户资料

官方SDK静态代码；字段封装不是服务端图谱或目标游戏发送成功。

- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/a6.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/a6.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/c5.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/c5.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/i1$a.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/i1$a.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/i1.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/i1.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/r7.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/r7.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/t7.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/t7.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/v.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/v.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/y5.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/y5.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/y6.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/y6.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/sdk/AppLovinSdk.java](identity-graph/sdk/max-13.6.4/java/com/applovin/sdk/AppLovinSdk.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/sdk/AppLovinUserData.java](identity-graph/sdk/max-13.6.4/java/com/applovin/sdk/AppLovinUserData.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/EventServiceImpl.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/EventServiceImpl.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/k.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/k.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/l.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/l.java)
- [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java)
- [ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar](ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar)
- [identity-graph/SDK_IDENTITY_AUDIT.json](identity-graph/SDK_IDENTITY_AUDIT.json)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig02"></a>

## IG02 · 独立Axon1.3.4身份能力

官方独立发行物，非目标游戏实装证明；静态分析不含网络执行。

- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/g.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/g.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/g0.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/g0.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/h0.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/h0.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/k0.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/k0.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/l3.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/l3.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/m2.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/m2.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/p.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/p.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/w0.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/w0.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/y2.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/impl/y2.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/sdk/Axon.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/sdk/Axon.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/sdk/AxonPrivacySettings.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/sdk/AxonPrivacySettings.java)
- [identity-graph/sdk/axon-1.3.4/java/com/applovin/sdk/AxonUserData.java](identity-graph/sdk/axon-1.3.4/java/com/applovin/sdk/AxonUserData.java)
- [nongame/sdk/axon/1.3.4/provenance.json](nongame/sdk/axon/1.3.4/provenance.json)
- [nongame/sdk/axon/1.3.4/classes.jar](nongame/sdk/axon/1.3.4/classes.jar)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig03"></a>

## IG03 · Pixel访客/点击/客户键与条件采集

公开网页代码证实；原始偏移和SHA保留；未执行JS或查询商家配置。

- [nongame/pixel-source.raw](nongame/pixel-source.raw)；[原始来源](https://s.axon.ai/pixel.js)
- [nongame/pixel-string-table.json](nongame/pixel-string-table.json)
- [identity-graph/PIXEL_IDENTITY_EXCERPTS.json](identity-graph/PIXEL_IDENTITY_EXCERPTS.json)
- [identity-graph/analyze_identity.py](identity-graph/analyze_identity.py)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig04"></a>

## IG04 · CAPI及订单历史的身份与价值建模用途

官方接口要求及建模目的，不是某用户的实际匹配或训练记录。

- [nongame/doc-capi.raw](nongame/doc-capi.raw)；[原始来源](https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api)
- [nongame/doc-order-history.raw](nongame/doc-order-history.raw)；[原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/order-history-data)
- [nongame/doc-attribution.raw](nongame/doc-attribution.raw)；[原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/measurement-and-attribution)
- [nongame/doc-data-sharing.raw](nongame/doc-data-sharing.raw)；[原始来源](https://legal.applovin.com/data-sharing-requirements/)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig05"></a>

## IG05 · AppLovin跨属性结合及Axon数据使用范围

官方政策/产品说明正证据；不证明目标游戏投放或电商到游戏的逐字段训练。

- [nongame/applovin-policy-direct.raw](nongame/applovin-policy-direct.raw)；[原始来源](https://legal.applovin.com/privacy/)
- [nongame/applovin-axon-about.raw](nongame/applovin-axon-about.raw)；[原始来源](https://legal.applovin.com/about-applovins-axon-ai/)
- [identity-graph/applovin-how-ads.raw](identity-graph/applovin-how-ads.raw)；[原始来源](https://legal.applovin.com/how-applovin-shows-you-ads/)；HTTP 403

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig06"></a>

## IG06 · 平台ID作用域、ATT及cookie matching边界

Google/Apple官方资料；同设备scope与跨设备账户严格区分。

- [identity-graph/google-appset-guide.raw](identity-graph/google-appset-guide.raw)；[原始来源](https://developer.android.com/identity/app-set-id)；HTTP 200
- [identity-graph/google-appset-correct.raw](identity-graph/google-appset-correct.raw)；[原始来源](https://developers.google.com/android/reference/com/google/android/gms/appset/AppSetIdInfo)；HTTP 200
- [identity-graph/google-ads-id.raw](identity-graph/google-ads-id.raw)；[原始来源](https://support.google.com/googleplay/android-developer/answer/6048248?hl=en)；HTTP 200
- [identity-graph/apple-idfv-data.raw](identity-graph/apple-idfv-data.raw)；[原始来源](https://developer.apple.com/tutorials/data/documentation/uikit/uidevice/identifierforvendor.json)；HTTP 200
- [identity-graph/apple-idfa-data.raw](identity-graph/apple-idfa-data.raw)；[原始来源](https://developer.apple.com/tutorials/data/documentation/adsupport/asidentifiermanager/advertisingidentifier.json)；HTTP 200
- [identity-graph/apple-att.raw](identity-graph/apple-att.raw)；[原始来源](https://developer.apple.com/app-store/user-privacy-and-data-use/)；HTTP 200
- [identity-graph/google-cookie-match.raw](identity-graph/google-cookie-match.raw)；[原始来源](https://developers.google.com/authorized-buyers/rtb/cookie-guide)；HTTP 200

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig07"></a>

## IG07 · Unity Authentication3.9.0官方源包与Unity Ads身份桥接

官方代码；UPA/UGS/LevelPlay AUID/Analytics ID不混同；不是目标游戏启用。

- [identity-graph/sdk/authentication/3.9.0/archive-index.json](identity-graph/sdk/authentication/3.9.0/archive-index.json)
- [identity-graph/sdk/authentication/3.9.0/authentication-3.9.0.tgz](identity-graph/sdk/authentication/3.9.0/authentication-3.9.0.tgz)
- [identity-graph/sdk/authentication/3.9.0/provenance.json](identity-graph/sdk/authentication/3.9.0/provenance.json)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/LICENSE.md](identity-graph/sdk/authentication/3.9.0/extracted/package/LICENSE.md)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/package.json](identity-graph/sdk/authentication/3.9.0/extracted/package/package.json)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/PlayerAccountServiceInternal.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/PlayerAccountServiceInternal.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/Models/IdToken.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Player Accounts/Runtime/Models/IdToken.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.External.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.External.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Network/AuthenticationNetworkClient.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Network/AuthenticationNetworkClient.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Identity.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Identity.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/PlayerInfo.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/PlayerInfo.cs)
- [identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Security/AccessToken.cs](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Security/AccessToken.cs)
- [ThirdPartySDKs/Unity/Ads/4.17.0/provenance.json](ThirdPartySDKs/Unity/Ads/4.17.0/provenance.json)
- [ThirdPartySDKs/Unity/Ads/4.17.0/unity-ads-4.17.0-sources.jar](ThirdPartySDKs/Unity/Ads/4.17.0/unity-ads-4.17.0-sources.jar)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidAnalyticsDataSource.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidAnalyticsDataSource.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidAppSetIdDataSource.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidAppSetIdDataSource.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidDeviceInfoRepository.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidDeviceInfoRepository.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetInitializationRequestPayload.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetInitializationRequestPayload.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt)
- [vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java](vector/sdk/Unity/Ads/4.18.1/java/com/unity3d/services/core/device/reader/DeviceInfoReaderWithPrivacy.java)
- [identity-graph/IDENTITY_CODE_EXCERPTS.json](identity-graph/IDENTITY_CODE_EXCERPTS.json)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig08"></a>

## IG08 · Unity账号互通、身份管理及产品专用隐私角色

官方组织级/跨设备能力；无账号到广告图谱或Vector的直接连接证明。

- [identity-graph/unity-player-accounts.raw](identity-graph/unity-player-accounts.raw)；[原始来源](https://docs.unity.com/ugs/en-us/manual/authentication/manual/unity-player-accounts)；HTTP 200
- [identity-graph/unity-upa-doc-md.raw](identity-graph/unity-upa-doc-md.raw)；[原始来源](https://docs.unity.com/en-us/authentication/unity-player-accounts.md)；HTTP 200
- [identity-graph/unity-anonymous.raw](identity-graph/unity-anonymous.raw)；[原始来源](https://docs.unity.com/ugs/en-us/manual/authentication/manual/use-anon-sign-in)；HTTP 200
- [identity-graph/unity-code-link.raw](identity-graph/unity-code-link.raw)；[原始来源](https://docs.unity.com/en-us/authentication/platform-signin/code-link)；HTTP 200
- [identity-graph/unity-openid.raw](identity-graph/unity-openid.raw)；[原始来源](https://docs.unity.com/en-us/authentication/openid-connect)；HTTP 200
- [identity-graph/unity-identity-management.raw](identity-graph/unity-identity-management.raw)；[原始来源](https://docs.unity.com/en-us/authentication/identity-management.md)；HTTP 200
- [identity-graph/unity-auth-privacy-overview.raw](identity-graph/unity-auth-privacy-overview.raw)；[原始来源](https://docs.unity.com/en-us/authentication/privacy-and-consent/overview.md)；HTTP 200
- [identity-graph/unity-upa-privacy-overview.raw](identity-graph/unity-upa-privacy-overview.raw)；[原始来源](https://docs.unity.com/en-us/authentication/privacy-and-consent/data-privacy-unity-player-accounts.md)；HTTP 200
- [identity-graph/unity-upa-data-safety.raw](identity-graph/unity-upa-data-safety.raw)；[原始来源](https://docs.unity.com/en-us/authentication/privacy-and-consent/google-data-unity-player-accounts.md)；HTTP 200

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig09"></a>

## IG09 · Unity Exchange RampID及LiveRamp身份能力

官方美加受众激活，需要双方支持；不证明UPA映射、每个请求或Vector训练。

- [vector/exchange-rampid.html](vector/exchange-rampid.html)；[原始来源](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)
- [vector/exchange-rampid.txt](vector/exchange-rampid.txt)；[原始来源](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)
- [identity-graph/liveramp-rampid-product.raw](identity-graph/liveramp-rampid-product.raw)；[原始来源](https://liveramp.com/our-platform/rampid)；HTTP 200
- [identity-graph/liveramp-identity.raw](identity-graph/liveramp-identity.raw)；[原始来源](https://liveramp.com/our-platform/identity-resolution/)；HTTP 200
- [identity-graph/liveramp-identity-graph.raw](identity-graph/liveramp-identity-graph.raw)；[原始来源](https://liveramp.com/our-platform/identity-graph/)；HTTP 200

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig10"></a>

## IG10 · Unity竞价身份字段、同意信号与IAB标准

Unity取得文档没有RampID wire字段；IAB标准不能充当Unity已用eids证明。

- [identity-graph/unity-exchange-identity.raw](identity-graph/unity-exchange-identity.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-requests.md)；HTTP 200
- [identity-graph/unity-exchange-privacy.raw](identity-graph/unity-exchange-privacy.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/data-privacy.md)；HTTP 200
- [identity-graph/iab-openrtb-26.raw](identity-graph/iab-openrtb-26.raw)；[原始来源](https://raw.githubusercontent.com/InteractiveAdvertisingBureau/openrtb2.x/main/2.6.md)；HTTP 200

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig11"></a>

## IG11 · 既有游戏业务ID及事件路径复用

实际游戏静态调用与MMP/MAX不同路径；不把单应用关联升级成跨应用账号图谱。

- [20_Axon实际事件调用链.md](20_Axon实际事件调用链.md)
- [21_MAX用户ID与身份数据流.md](21_MAX用户ID与身份数据流.md)
- [22_AppLovin事件协议版本差分.md](22_AppLovin事件协议版本差分.md)
- [axon/deep/native-car/method-evidence.json](axon/deep/native-car/method-evidence.json)
- [axon/deep/native-car/user-id-intermediate-check.json](axon/deep/native-car/user-id-intermediate-check.json)
- [axon/deep/metica-car-index.json](axon/deep/metica-car-index.json)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<a id="ig12"></a>

## IG12 · 身份专项采集记录与失败边界

包含404/403/错误候选；仅合法公开GET和静态分析，无设备/生产事件/真实ID。

- [identity-graph/fetches-auth-privacy.json](identity-graph/fetches-auth-privacy.json)
- [identity-graph/fetches-follow.json](identity-graph/fetches-follow.json)
- [identity-graph/fetches-identity-final.json](identity-graph/fetches-identity-final.json)
- [identity-graph/fetches-initial.json](identity-graph/fetches-initial.json)
- [identity-graph/fetches-precise.json](identity-graph/fetches-precise.json)
- [identity-graph/fetches-standards.json](identity-graph/fetches-standards.json)
- [identity-graph/collect.py](identity-graph/collect.py)
- [identity-graph/decompile_ids.py](identity-graph/decompile_ids.py)
- [identity-graph/download_auth.py](identity-graph/download_auth.py)
- [identity-graph/build_evidence.py](identity-graph/build_evidence.py)
- [identity-graph/validate.py](identity-graph/validate.py)

完整SHA256、来源和抓取时间见EVIDENCE_MANIFEST.json本组；SDK版本边界及未知服务器连接见31–34号报告。

<!-- AUCTION_PROTOCOL_2026_11_19 -->

<a id="bp01"></a>

## BP01 · AppLovin官方oRTB请求、响应、创意和版本记录

官方协议证实；只针对取得文档，不是Axon服务器实现。

- [auction/al-introduction.raw](auction/al-introduction.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/introduction)；HTTP 200
- [auction/al-request.raw](auction/al-request.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/bid-requests)；HTTP 200
- [auction/al-response.raw](auction/al-response.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/bid-responses)；HTTP 200
- [auction/al-creatives.raw](auction/al-creatives.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/creative-types)；HTTP 200
- [auction/al-changelog.raw](auction/al-changelog.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/demand-side-platforms/applovin-ortb-specification/changelog)；HTTP 200

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp02"></a>

## BP02 · Unity Exchange请求/响应/超时/loss/隐私与SKAN

官方协议证实；记录版本/tmax/multi-seat歧义，非抓包。

- [identity-graph/unity-exchange-identity.raw](identity-graph/unity-exchange-identity.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-requests.md)；HTTP 200
- [identity-graph/unity-exchange-privacy.raw](identity-graph/unity-exchange-privacy.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/data-privacy.md)；HTTP 200
- [auction/unity-overview.raw](auction/unity-overview.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange.md)；HTTP 200
- [auction/unity-response.raw](auction/unity-response.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-responses.md)；HTTP 200
- [auction/unity-get-started.raw](auction/unity-get-started.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/get-started.md)；HTTP 200
- [auction/unity-ios.raw](auction/unity-ios.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/ios14-support.md)；HTTP 200
- [auction/unity-loss.raw](auction/unity-loss.raw)；[原始来源](https://docs.unity.com/en-us/grow/programmatic/unity-exchange/loss-notifications.md)；HTTP 200

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp03"></a>

## BP03 · MAX统一竞价、waterfall合并和SDK bidder入驻

官方公开规则；并非所有中介服务器调度或throttling算法。

- [auction/al-dynamics.raw](auction/al-dynamics.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/auction-dynamics)；HTTP 200
- [auction/al-sdk-bidder.raw](auction/al-sdk-bidder.raw)；[原始来源](https://support.applovin.com/en/max/demand-partners/sdk-bidder-testing-and-integration-process)；HTTP 200

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp04"></a>

## BP04 · MAX13.6.4私有请求、signal、waterfall、expiration与反馈

官方SDK静态代码；不是OpenRTB原样透传，没有生产执行。

- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/a6$a.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/a6$a.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/a6.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/a6.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/c3.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/c3.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/g3.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/g3.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/h2.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/h2.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/l6.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/l6.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/u5.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/u5.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/v3.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/v3.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MaxAdapterParametersImpl.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MaxAdapterParametersImpl.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MaxAdWaterfallInfoImpl.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MaxAdWaterfallInfoImpl.java)
- [auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java](auction/sdk/MAX-13.6.4/java/com/applovin/impl/mediation/MediationServiceImpl.java)
- [ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar](ThirdPartySDKs/AppLovin/MAX/13.6.4/classes.jar)
- [auction/MAX_LITERAL_HITS.json](auction/MAX_LITERAL_HITS.json)
- [auction/SDK_AUDIT.json](auction/SDK_AUDIT.json)
- [auction/CODE_EVIDENCE.json](auction/CODE_EVIDENCE.json)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp05"></a>

## BP05 · Unity Ads protobuf请求、竞价token与隐私共享层

官方SDK源码；token为序列化输入，不是模型权重；逐字段服务器转码未知。

- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdRequest.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdRequest.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonGetHeaderBiddingToken.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonGetHeaderBiddingToken.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt)
- [ThirdPartySDKs/Unity/Ads/4.17.0/provenance.json](ThirdPartySDKs/Unity/Ads/4.17.0/provenance.json)
- [ThirdPartySDKs/Unity/Ads/4.17.0/unity-ads-4.17.0-sources.jar](ThirdPartySDKs/Unity/Ads/4.17.0/unity-ads-4.17.0-sources.jar)
- [vector/SDK_AUDIT.json](vector/SDK_AUDIT.json)
- [vector/CODE_EVIDENCE.json](vector/CODE_EVIDENCE.json)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp06"></a>

## BP06 · LevelPlay9.4.0候选、auction结果、状态和fallback

官方发行包静态代码；JADX大小写重命名保留；未恢复服务器定价。

- [auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/AbstractC0163i3.java](auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/AbstractC0163i3.java)
- [auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/AbstractC0181j3.java](auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/AbstractC0181j3.java)
- [auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/C0241m2.java](auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/C0241m2.java)
- [auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/C0262n2.java](auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/C0262n2.java)
- [auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/C0325q2.java](auction/sdk/LevelPlay-9.4.0/follow/com/ironsource/C0325q2.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/A1.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/A1.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/C.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/C.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/Dc.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/Dc.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/P3$c$a.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/P3$c$a.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/Ve.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/Ve.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/W1.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/W1.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/mediationsdk/demandOnly/d.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/mediationsdk/demandOnly/d.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/mediationsdk/demandOnly/l.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/mediationsdk/demandOnly/l.java)
- [auction/sdk/LevelPlay-9.4.0/java/com/ironsource/mediationsdk/utils/IronSourceConstants.java](auction/sdk/LevelPlay-9.4.0/java/com/ironsource/mediationsdk/utils/IronSourceConstants.java)
- [ThirdPartySDKs/Unity/Dependency-mediation-sdk/9.4.0/classes.jar](ThirdPartySDKs/Unity/Dependency-mediation-sdk/9.4.0/classes.jar)
- [auction/sdk/LevelPlay-9.4.0/FOLLOWUP.json](auction/sdk/LevelPlay-9.4.0/FOLLOWUP.json)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp07"></a>

## BP07 · 身份与隐私字段证据复用

设备广告ID、AppSet、CUID、UPA/RampID分开；未证任意ID自动映射到DSP。

- [identity-graph/IDENTITY_CODE_EXCERPTS.json](identity-graph/IDENTITY_CODE_EXCERPTS.json)
- [identity-graph/SDK_IDENTITY_AUDIT.json](identity-graph/SDK_IDENTITY_AUDIT.json)
- [vector/exchange-rampid.html](vector/exchange-rampid.html)；[原始来源](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)
- [31_AppLovin设备身份图谱.md](31_AppLovin设备身份图谱.md)
- [32_Unity身份互通与RampID.md](32_Unity身份互通与RampID.md)
- [34_跨设备身份关联证据链.md](34_跨设备身份关联证据链.md)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp08"></a>

## BP08 · Axon/Vector价值竞价与反馈公开说明

官方定性用途与产品条件；无闭源模型/权重/真实效果排名。

- [nongame/applovin-axon-about.raw](nongame/applovin-axon-about.raw)；[原始来源](https://legal.applovin.com/about-applovins-axon-ai/)
- [nongame/applovin-policy-direct.raw](nongame/applovin-policy-direct.raw)；[原始来源](https://legal.applovin.com/privacy/)
- [nongame/doc-order-history.raw](nongame/doc-order-history.raw)；[原始来源](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/order-history-data)
- [axon/gaming-product.html](axon/gaming-product.html)
- [axon/gaming-apps.html](axon/gaming-apps.html)
- [axon/doc-set-up-mmp-tracking.html](axon/doc-set-up-mmp-tracking.html)
- [vector/doc-revenue-bids.html](vector/doc-revenue-bids.html)
- [vector/doc-intro-to-roas-campaigns.html](vector/doc-intro-to-roas-campaigns.html)；[原始来源](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md)
- [24_Unity与AppLovin技术对比.md](24_Unity与AppLovin技术对比.md)
- [25_Unity_Runtime数据优势调查.md](25_Unity_Runtime数据优势调查.md)
- [20_Axon实际事件调用链.md](20_Axon实际事件调用链.md)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp09"></a>

## BP09 · 全部原表字段、规范化差分及文档示例解析

444原表行含辅助表；234核心路径/91双方列出；不是生产字段量或优势排名。

- [auction/extract_protocol.py](auction/extract_protocol.py)
- [auction/PROTOCOL_FIELDS.json](auction/PROTOCOL_FIELDS.json)
- [auction/PROTOCOL_FIELDS.md](auction/PROTOCOL_FIELDS.md)
- [auction/build_diff.py](auction/build_diff.py)
- [auction/FIELD_DIFF.json](auction/FIELD_DIFF.json)
- [auction/FIELD_DIFF.md](auction/FIELD_DIFF.md)
- [auction/DOCUMENT_EXAMPLES.json](auction/DOCUMENT_EXAMPLES.json)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp10"></a>

## BP10 · 本地合成竞价模拟器及实际实验产物

人为模型与协议规则分开；不连接广告网络，结果不代表供应商表现。

- [auction/model/auction_model.py](auction/model/auction_model.py)
- [auction/model/plot_results.py](auction/model/plot_results.py)
- [auction/model/run_experiments.py](auction/model/run_experiments.py)
- [auction/model/test_auction_model.py](auction/model/test_auction_model.py)
- [auction/model/output/arms.csv](auction/model/output/arms.csv)
- [auction/model/output/feedback.json](auction/model/output/feedback.json)
- [auction/model/output/matched_tmax_control.json](auction/model/output/matched_tmax_control.json)
- [auction/model/output/request-applovin.json](auction/model/output/request-applovin.json)
- [auction/model/output/request-unity.json](auction/model/output/request-unity.json)
- [auction/model/output/response-applovin.json](auction/model/output/response-applovin.json)
- [auction/model/output/response-unity.json](auction/model/output/response-unity.json)
- [auction/model/output/results.json](auction/model/output/results.json)
- [auction/model/output/sample_traces.json](auction/model/output/sample_traces.json)
- [auction/model/output/synthetic_economics.png](auction/model/output/synthetic_economics.png)
- [auction/model/output/waterfall_example.json](auction/model/output/waterfall_example.json)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<a id="bp11"></a>

## BP11 · 采集与逆向范围、失败候选、可重跑验证

合法公开GET/既有SDK静态分析；soft404/跳首页不算协议证据；无生产事件。

- [auction/PUBLIC_SOURCE_INDEX.json](auction/PUBLIC_SOURCE_INDEX.json)
- [auction/collect.py](auction/collect.py)
- [auction/follow_sources.py](auction/follow_sources.py)
- [auction/fetch_additional.py](auction/fetch_additional.py)
- [auction/sdk_audit.py](auction/sdk_audit.py)
- [auction/code_evidence.py](auction/code_evidence.py)
- [auction/build_evidence.py](auction/build_evidence.py)
- [auction/validate.py](auction/validate.py)
- [auction/fetches-additional.json](auction/fetches-additional.json)
- [auction/fetches-mediation.json](auction/fetches-mediation.json)
- [auction/fetches-protocol-initial.json](auction/fetches-protocol-initial.json)
- [auction/fetches-resolved.json](auction/fetches-resolved.json)

完整SHA256/获取时间/版本与范围见EVIDENCE_MANIFEST.json本组；原代码行号见auction/CODE_EVIDENCE.json。

<!-- PREDICTION_SYSTEM_2026_11_19 -->

<a id="ps01"></a>

## PS01 · 模型来源逐条摘录与公开技术线索

A官方用途 B接口 D招聘/专利；不混为生产证明。

完整来源、产品、日期、URL、行号及SHA256见[SOURCE_CATALOG](prediction-system/SOURCE_CATALOG.md)和[SOURCE_EXCERPTS](prediction-system/SOURCE_EXCERPTS.json)。

- S01 [nongame/applovin-axon-about.txt](nongame/applovin-axon-about.txt):L58；级别A；[原始URL](https://legal.applovin.com/about-applovins-axon-ai/)
- S02 [nongame/applovin-axon-about.txt](nongame/applovin-axon-about.txt):L54；级别A；[原始URL](https://legal.applovin.com/about-applovins-axon-ai/)
- S03 [nongame/applovin-axon-about.txt](nongame/applovin-axon-about.txt):L72；级别A；[原始URL](https://legal.applovin.com/about-applovins-axon-ai/)
- S04 [nongame/applovin-policy-direct.txt](nongame/applovin-policy-direct.txt):L124；级别A；[原始URL](https://legal.applovin.com/privacy/)
- S05 [axon/gaming-apps.txt](axon/gaming-apps.txt):L71；级别A；[原始URL](https://www.applovin.com/en/gaming-apps)
- S06 [axon/max-ilrd.txt](axon/max-ilrd.txt):L124；级别B；[原始URL](https://support.applovin.com/en/max/android/overview/advanced-settings#impression-level-user-revenue-api)
- S07 [axon/max-ilrd.txt](axon/max-ilrd.txt):L188；级别B；[原始URL](https://support.applovin.com/en/max/android/overview/advanced-settings#impression-level-user-revenue-api)
- S08 [axon/doc-in-app-purchase-revenue-sharing.txt](axon/doc-in-app-purchase-revenue-sharing.txt):L14；级别A；[原始URL](https://support.applovin.com/en/growth/promoting-your-apps/troubleshooting/in-app-purchase-revenue-sharing)
- S09 [axon/doc-adjust.txt](axon/doc-adjust.txt):L39；级别A；[原始URL](https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/adjust)
- S10 [axon/doc-appsflyer.txt](axon/doc-appsflyer.txt):L177；级别A；[原始URL](https://support.applovin.com/en/growth/promoting-your-apps/track-and-optimize/appsflyer)
- S11 [nongame/doc-order-history.txt](nongame/doc-order-history.txt):L13；级别A；[原始URL](https://support.applovin.com/en/growth/promoting-your-websites/track-and-optimize/order-history-data)
- S12 [vector/unity-vector-correct.txt](vector/unity-vector-correct.txt):L10；级别A；[原始URL](https://unity.com/products/unity-ads/vector)
- S13 [vector/unity-vector-correct.txt](vector/unity-vector-correct.txt):L34；级别A；[原始URL](https://unity.com/products/unity-ads/vector)
- S14 [vector/doc-intro-to-roas-campaigns.txt](vector/doc-intro-to-roas-campaigns.txt):L22；级别A；[原始URL](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md)
- S15 [vector/doc-intro-to-roas-campaigns.txt](vector/doc-intro-to-roas-campaigns.txt):L42；级别A；[原始URL](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md)
- S16 [vector/doc-intro-to-roas-campaigns.txt](vector/doc-intro-to-roas-campaigns.txt):L79；级别A；[原始URL](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md)
- S17 [vector/doc-intro-to-roas-campaigns.txt](vector/doc-intro-to-roas-campaigns.txt):L97；级别A；[原始URL](https://docs.unity.com/en-us/grow/acquire/campaigns/roas/intro-to-roas-campaigns.md)
- S18 [vector/doc-send-postbacks.txt](vector/doc-send-postbacks.txt):L28；级别B；[原始URL](https://docs.unity.com/en-us/grow/acquire/partner-integration/custom/send-postbacks.md)
- S19 [vector/doc-send-postbacks.txt](vector/doc-send-postbacks.txt):L91；级别B；[原始URL](https://docs.unity.com/en-us/grow/acquire/partner-integration/custom/send-postbacks.md)
- S20 [vector/ddf-end-user-consent.txt](vector/ddf-end-user-consent.txt):L23；级别A；[原始URL](https://docs.unity.com/en-us/cloud/developer-data-framework/end-user-consent.md)
- S21 [vector/unity-2026-keynote.txt](vector/unity-2026-keynote.txt):L120；级别A；[原始URL](https://unity.com/blog/unite-seoul-keynote-2026-recap)
- S22 [vector/d28-blog.txt](vector/d28-blog.txt):L21；级别A；[原始URL](https://unity.com/blog/d28-roas)
- S23 [vector/d28-blog.txt](vector/d28-blog.txt):L43；级别A；[原始URL](https://unity.com/blog/d28-roas)
- S24 [prediction-system/applovin-excluded-rival-data.txt](prediction-system/applovin-excluded-rival-data.txt):L14；级别A；[原始URL](https://www.applovin.com/en/blog/catch-bad-ads-not-data)
- S25 [prediction-system/applovin-job-4712559006-clean.txt](prediction-system/applovin-job-4712559006-clean.txt):L6；级别D；[原始URL](https://boards.greenhouse.io/applovin/jobs/4712559006?gh_jid=4712559006)
- S26 [prediction-system/applovin-job-4716524006-clean.txt](prediction-system/applovin-job-4716524006-clean.txt):L8；级别D；[原始URL](https://boards.greenhouse.io/applovin/jobs/4716524006?gh_jid=4716524006)
- S27 [prediction-system/applovin-job-4705264006-clean.txt](prediction-system/applovin-job-4705264006-clean.txt):L8；级别D；[原始URL](https://boards.greenhouse.io/applovin/jobs/4705264006?gh_jid=4705264006)
- S28 [prediction-system/unity-job-JOBREQ-2616286-clean.txt](prediction-system/unity-job-JOBREQ-2616286-clean.txt):L1；级别D；[原始URL](https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity/job/Mountain-View-CA-USA/Senior-Machine-Learning-Engineer--Vector-Bidding-Science_JOBREQ-2616286)
- S29 [prediction-system/unity-job-JOBREQ-2615964-clean.txt](prediction-system/unity-job-JOBREQ-2615964-clean.txt):L1；级别D；[原始URL](https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity/job/Mountain-View-CA-USA/Staff-Backend-Engineer--ML-Inference-Systems_JOBREQ-2615964)
- S30 [prediction-system/unity-job-JOBREQ-2616596-clean.txt](prediction-system/unity-job-JOBREQ-2616596-clean.txt):L1；级别D；[原始URL](https://unitytech.wd1.myworkdayjobs.com/wday/cxs/unitytech/Unity/job/Mountain-View-CA-USA/Principal-Machine-Learning-Engineer--Ads-Modeling_JOBREQ-2616596)
- S31 [prediction-system/applovin-historical-patent.txt](prediction-system/applovin-historical-patent.txt):L387；级别D；[原始URL](https://patents.google.com/patent/US20130159103A1/en)
- S32 [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/sdk/m.java):L1328；级别B
- S33 [identity-graph/sdk/max-13.6.4/java/com/applovin/impl/t7.java](identity-graph/sdk/max-13.6.4/java/com/applovin/impl/t7.java):L1；级别B
- S34 [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt):L213；级别B
- S35 [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt):L20；级别B
- S36 [ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt](ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetUniversalRequestSharedData.kt):L19；级别B
- S37 [vector/exchange-rampid.txt](vector/exchange-rampid.txt):L13；级别A；[原始URL](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)
- S38 [identity-graph/unity-player-accounts.txt](identity-graph/unity-player-accounts.txt):L18；级别A
- S39 [20_Axon实际事件调用链.md](20_Axon实际事件调用链.md):L8；级别B
- S40 [10_买量优化机制最终对比.md](10_买量优化机制最终对比.md):L9；级别B

原文件哈希及获取时间见EVIDENCE_MANIFEST.json；实际生产运行、服务器训练与目标游戏启用没有独立日志证明。

<a id="ps02"></a>

## PS02 · 证据关系图及新一轮公开获取原始材料

31节点38边；未知连接保持虚线；搜索失败保留。

- [prediction-system/build_system.py](prediction-system/build_system.py)
- [00—46阶段证据图快照](cross-sdk/EVIDENCE_GRAPH.before47.json)
- [prediction-system/finalize.py](prediction-system/finalize.py)
- [prediction-system/REPORT_REUSE_INDEX.json](prediction-system/REPORT_REUSE_INDEX.json)
- [prediction-system/SEARCH_LEDGER.json](prediction-system/SEARCH_LEDGER.json)
- [prediction-system/SOURCE_CATALOG.md](prediction-system/SOURCE_CATALOG.md)

原文件哈希及获取时间见EVIDENCE_MANIFEST.json；实际生产运行、服务器训练与目标游戏启用没有独立日志证明。

<a id="ps03"></a>

## PS03 · 41—46核心系统研究报告

官方数据用途和接口证据拼图，不宣称恢复闭源模型。

- [41_核心模型证据拼图总览.md](41_核心模型证据拼图总览.md)
- [42_Axon跨来源数据与价值预测证据.md](42_Axon跨来源数据与价值预测证据.md)
- [43_Vector跨来源数据与价值预测证据.md](43_Vector跨来源数据与价值预测证据.md)
- [44_身份行为价值关联图谱.md](44_身份行为价值关联图谱.md)
- [45_关键断点与反证清单.md](45_关键断点与反证清单.md)
- [46_双方预测系统重建与可信度.md](46_双方预测系统重建与可信度.md)

原文件哈希及获取时间见EVIDENCE_MANIFEST.json；实际生产运行、服务器训练与目标游戏启用没有独立日志证明。

<a id="ps04"></a>

## PS04 · 辅助合成特征消融实验

81组人为数据；不构成Axon/Vector效果或身份图谱证明。

- [ltv/model/experiment.py](ltv/model/experiment.py)
- [ltv/model/output/recall_ablation.png](ltv/model/output/recall_ablation.png)
- [ltv/model/output/results.json](ltv/model/output/results.json)
- [ltv/model/output/roas_ablation.png](ltv/model/output/roas_ablation.png)
- [ltv/model/output/summary.json](ltv/model/output/summary.json)
- [ltv/model/output/SUMMARY.md](ltv/model/output/SUMMARY.md)

原文件哈希及获取时间见EVIDENCE_MANIFEST.json；实际生产运行、服务器训练与目标游戏启用没有独立日志证明。

<!-- CROSS_SDK_47_52 -->

<a id="cs01"></a>

## CS01 · 跨SDK源码、原包与调用链

本轮44段代码定位；49项选定版本矩阵。所有新SDK仅静态分析，未初始化，未发送生产事件。

- [cross-sdk/SDK_MATRIX.json](cross-sdk/SDK_MATRIX.json)
- [cross-sdk/CODE_CATALOG.md](cross-sdk/CODE_CATALOG.md)
- [cross-sdk/CODE_EVIDENCE.json](cross-sdk/CODE_EVIDENCE.json)
- [cross-sdk/IDENTITY_MAPPINGS.json](cross-sdk/IDENTITY_MAPPINGS.json)
- [cross-sdk/API_DELTAS.json](cross-sdk/API_DELTAS.json)
- [cross-sdk/ACQUISITION.json](cross-sdk/ACQUISITION.json)
- [cross-sdk/DECOMPILE.json](cross-sdk/DECOMPILE.json)
- [cross-sdk/packages/singular/12.17.0/provenance.json](cross-sdk/packages/singular/12.17.0/provenance.json)
- XS01 [PlayerData.CreatePlayerIdentityAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L97；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS02 [PlayerData.FetchEnabledFirebaseIdsAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L176；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS03 [FirebaseAnalyticsClient.FetchAppInstanceIdAsync/FetchSessionIdValueAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L60；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS04 [ConnectionsSettingsClient.CachedEnabledAttributes/FetchAndCacheAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs):L44；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS05 [ConnectionsSettingsClient.FetchEnabledAttributesAsync/ParseEnabledAttributes/PostAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs):L104；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS06 [CoreRegistryHelper properties](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs):L38；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS07 [GooglePlayStoreExtendedPurchaseService.SendPurchasePaidEvent/SendPurchaseFulfilledEvent](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs):L58；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS08 [PurchaseEventEmitter.SendPurchasePaidEvent/SendPurchaseFulfilledEvent](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L92；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS09 [PurchaseEventEmitter.Forward/ForwardGateway/ForwardModule](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L190；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS10 [PurchaseEventEmitter.BuildEnvelope](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L243；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS11 [PurchaseEventEmitter.MapIdentity](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L363；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS12 [PurchaseEventEmitter.BuildSku](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L404；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS13 [PurchaseEventProtobufWriter.SerializeIaps](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS14 [PlayerData.CreatePlayerIdentityAsync (older)](cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/PlayerData.cs):L88；com.unity.purchasing 5.4.0，原包/文件SHA256见代码目录。
- XS15 [SerializeIaps (older)](cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39；com.unity.purchasing 5.4.0，原包/文件SHA256见代码目录。
- XS16 [Official package CHANGELOG 5.5.1](cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L2；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS17 [Official package CHANGELOG 5.4.3](cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L88；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS18 [AnalyticsService.Initialize](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs):L49；com.unity.services.analytics 6.3.0，原包/文件SHA256见代码目录。
- XS19 [IdentityManager constructor/Initialize](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs):L42；com.unity.services.analytics 6.3.0，原包/文件SHA256见代码目录。
- XS20 [BufferX event header writing](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs):L373；com.unity.services.analytics 6.3.0，原包/文件SHA256见代码目录。
- XS21 [Dispatcher.UploadCompleted](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/Dispatcher.cs):L93；com.unity.services.analytics 6.3.0，原包/文件SHA256见代码目录。
- XS22 [ConsentManager.DataFrameworkConsentChanged](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/ConsentManager.cs):L51；com.unity.services.analytics 6.3.0，原包/文件SHA256见代码目录。
- XS23 [Official Analytics changelog6.1.0](cross-sdk/packages/services.analytics/6.3.0/extracted/package/CHANGELOG.md):L48；com.unity.services.analytics 6.3.0，原包/文件SHA256见代码目录。
- XS24 [ConfigFetchHttpClient.createFetchRequestBody](ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/ConfigFetchHttpClient.java):L321；Google/FirebaseRemoteConfig 24.0.1，原包/文件SHA256见代码目录。
- XS25 [RemoteConfigComponent.get](ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/RemoteConfigComponent.java):L172；Google/FirebaseRemoteConfig 24.0.1，原包/文件SHA256见代码目录。
- XS26 [Personalization.logArmActive](ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/internal/Personalization.java):L63；Google/FirebaseRemoteConfig 24.0.1，原包/文件SHA256见代码目录。
- XS27 [FirebaseRemoteConfig.updateAbtWithActivatedExperiments](ThirdPartySDKs/Google/FirebaseRemoteConfig/24.0.1/sources/com/google/firebase/remoteconfig/FirebaseRemoteConfig.java):L688；Google/FirebaseRemoteConfig 24.0.1，原包/文件SHA256见代码目录。
- XS28 [UnityAdsMediationAdapter.collectSignal](cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java):L101；AppLovin/Adapter-unityads-adapter 4.18.1.0，原包/文件SHA256见代码目录。
- XS29 [UnityAdsMediationAdapter.updatePrivacyConsent](cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java):L268；AppLovin/Adapter-unityads-adapter 4.18.1.0，原包/文件SHA256见代码目录。
- XS30 [GoogleMediationAdapter ad request builder](cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java):L494；AppLovin/Adapter-google-adapter 25.4.0.0，原包/文件SHA256见代码目录。
- XS31 [EventServiceImpl.trackEvent](cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java):L181；AppLovin/MAX 13.7.0，原包/文件SHA256见代码目录。
- XS32 [EventServiceImpl structured payload](cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java):L245；AppLovin/MAX 13.7.0，原包/文件SHA256见代码目录。
- XS33 [EventServiceImpl scheduler/postback builder](cross-sdk/java/max-137/com/applovin/impl/sdk/EventServiceImpl.java):L46；AppLovin/MAX 13.7.0，原包/文件SHA256见代码目录。
- XS34 [DeviceInfo.getFacebookAttributionId](ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/DeviceInfo.java):L440；Adjust/Android 5.8.1，原包/文件SHA256见代码目录。
- XS35 [ActivityHandler.processRemoteTriggersI](ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/ActivityHandler.java):L2352；Adjust/Android 5.8.1，原包/文件SHA256见代码目录。
- XS36 [ActivityHandler.shouldProcessEventI](ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/ActivityHandler.java):L3503；Adjust/Android 5.8.1，原包/文件SHA256见代码目录。
- XS37 [Adjust official CHANGELOG](cross-sdk/adjust-changelog.raw):L1；Adjust/Android 5.8.1，原包/文件SHA256见代码目录。
- XS38 [Singular.eventJSON/customRevenue](cross-sdk/java/singular-1217/com/singular/sdk/Singular.java):L261；Singular Android 12.17.0，原包/文件SHA256见代码目录。
- XS39 [Singular.setCustomUserId/unsetCustomUserId](cross-sdk/java/singular-1217/com/singular/sdk/Singular.java):L382；Singular Android 12.17.0，原包/文件SHA256见代码目录。
- XS40 [PurchaseEventEmitter gateway endpoint and branch](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L188；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS41 [FirebaseAnalyticsClient.FetchAppIdAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L127；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS42 [PurchaseService purchase lifecycle callsite](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/PurchaseService.cs):L314；com.unity.purchasing 5.5.1，原包/文件SHA256见代码目录。
- XS43 [Rotate original g8.a revenue wrapper](rotate-rings/static/java/classes2.dex/g8/a.java):L100；AppsFlyer/Android 6.17.5，原包/文件SHA256见代码目录。
- XS44 [PackageBuilder session parameters](ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/PackageBuilder.java):L276；Adjust/Android 5.8.1，原包/文件SHA256见代码目录。

<a id="cs02"></a>

## CS02 · 47—52报告与关系图更新

- [47_SDK生态与版本矩阵.md](47_SDK生态与版本矩阵.md)
- [48_跨SDK身份关联与字段映射.md](48_跨SDK身份关联与字段映射.md)
- [49_行为价值事件端到端调用链.md](49_行为价值事件端到端调用链.md)
- [50_远程配置与实验控制机制.md](50_远程配置与实验控制机制.md)
- [51_SDK演化与模型输入线索.md](51_SDK演化与模型输入线索.md)
- [52_Axon_Vector客户端系统重建.md](52_Axon_Vector客户端系统重建.md)
- [prediction-system/EVIDENCE_GRAPH.json](prediction-system/EVIDENCE_GRAPH.json)
- [cross-sdk/EVIDENCE_GRAPH.before47.json](cross-sdk/EVIDENCE_GRAPH.before47.json)
- [cross-sdk/EVIDENCE_GRAPH.after52.json](cross-sdk/EVIDENCE_GRAPH.after52.json)
- [cross-sdk/VALIDATION.json](cross-sdk/VALIDATION.json)

原图31节点/38边/40来源保存在before47；当前48节点/53边/84来源。旧未知训练边保留，客户端关联不升级为实际训练。完整文件哈希在EVIDENCE_MANIFEST.json的CS01/CS02。


<a id="ci53"></a>

## CI53 · Unity Core身份提供者与Insights数据血缘（53—55）

独立官方SDK静态证据；不代表目标游戏启用、生产送达或Vector逐字段训练。

- [53_Unity_Core身份提供者与生命周期.md](53_Unity_Core身份提供者与生命周期.md)
- [54_Unity_Insights事件协议与接收边界.md](54_Unity_Insights事件协议与接收边界.md)
- [55_跨SDK身份价值血缘最终核验.md](55_跨SDK身份价值血缘最终核验.md)
- [原包版本/哈希/依赖](core-insights/PACKAGE_PROVENANCE.json)
- [代码目录](core-insights/CODE_CATALOG.md) / [带原始片段的JSON](core-insights/CODE_EVIDENCE.json)
- [逐字段血缘](core-insights/FIELD_LINEAGE.json) / [发送侧协议重建](core-insights/PROTOCOL_SCHEMA.json)
- [官方公开获取记录](core-insights/ACQUISITION.json) / [固定提交绑定](core-insights/BOUNDARY_ACQUISITION.json)
- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [旧图快照](core-insights/EVIDENCE_GRAPH.before53.json) / [本轮快照](core-insights/EVIDENCE_GRAPH.after55.json)
- [验证结果](core-insights/VALIDATION.json)

- **C53S01** [CorePackageInitializer.InitializeComponents/InitializeInstallationId](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Registration/CorePackageInitializer.cs):L111；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S02** [InstallationId.CreateIdentifier/GetOrCreateIdentifier](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/InstallationId.cs):L7；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S03** [EngineInstallationId.GetOrCreateIdentifier/CreateIdentifier](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/EngineInstallationId.cs):L7；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S04** [UnityEngineIdentifier.UserId](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityEngineIdentifier.cs):L5；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S05** [ExternalUserIdProperty.UserId/Dispose](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Core/ExternalUserIdProperty.cs):L8；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S06** [ExternalUserId.UserId/UserIdChanged](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Configuration/ExternalUserId.cs):L6；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S07** [versionDefines](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Core/Unity.Services.Core.asmdef):L1；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S08** [UnityServices.ExternalUserId/ResetStaticsOnLoad](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Core/UnityServices.cs):L79；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S09** [UnityAdsIdentifier.UserId](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityAdsIdentifier.cs):L3；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S10** [UnityAnalyticsIdentifier.UserId](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/UnityAnalyticsIdentifier.cs):L6；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S11** [AndroidUtils.GetSharedPreferences/SharedPreferencesPutString](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Device/UserIdProviders/AndroidUtils.cs):L7；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S12** [AuthenticationPackageInitializer.InitializeService](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Core/AuthenticationPackageInitializer.cs):L77；Authentication 3.9.0；原包/文件SHA256见代码目录。
- **C53S13** [PlayerIdComponent](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Models/Components/PlayerIdComponent.cs):L6；Authentication 3.9.0；原包/文件SHA256见代码目录。
- **C53S14** [AuthenticationCache.Prefix/GetKey](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/Utilities/Cache/AuthenticationCache.cs):L7；Authentication 3.9.0；原包/文件SHA256见代码目录。
- **C53S15** [AuthenticationServiceInternal.SignOut/SwitchProfile](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs):L224；Authentication 3.9.0；原包/文件SHA256见代码目录。
- **C53S16** [AuthenticationServiceInternal sign-in completion](identity-graph/sdk/authentication/3.9.0/extracted/package/Runtime/AuthenticationServiceInternal.cs):L425；Authentication 3.9.0；原包/文件SHA256见代码目录。
- **C53S17** [AnalyticsService.Initialize](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/AnalyticsService.cs):L49；Analytics 6.3.0；原包/文件SHA256见代码目录。
- **C53S18** [IdentityManager constructor/Initialize/ExternalUserIdChanged](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/IdentityManager.cs):L22；Analytics 6.3.0；原包/文件SHA256见代码目录。
- **C53S19** [BufferX.PushStandardEventStart/PushCommonEventStart](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/Runtime/BufferX.cs):L366；Analytics 6.3.0；原包/文件SHA256见代码目录。
- **C53S20** [CoreRegistryHelper.InstallationId/Resolve](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/CoreRegistryHelper.cs):L27；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S21** [PlayerData.CreatePlayerIdentityAsync/FetchEnabledFirebaseIdsAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L90；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S22** [PurchaseEventEmitter.Send*Event](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L44；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S23** [PurchaseEventEmitter.Forward/ForwardModule/ForwardGateway](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L188；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S24** [PurchaseEventEmitter.BuildEnvelope/MapIdentity/BuildSku](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs):L243；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S25** [PurchaseEventProtobufWriter complete serializer](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L14；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S26** [IAPSDKEvent and lifecycle variants](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/IAPSDKEvent.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S27** [PlayerIdentity](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/PlayerIdentity.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S28** [ConnectionsSettingsClient.CachedEnabledAttributes/ParseEnabledAttributes/PostAsync](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/ConnectionsSettingsClient.cs):L15；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S29** [FirebaseAnalyticsClient getters](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Stores/Android/AAR/FirebaseAnalyticsClient.cs):L60；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S30** [SessionEventEmitter.SendAuthenticationCompleteEvent/BuildEnvelope](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/SessionEventEmitter.cs):L18；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S31** [IapCoreInitializeCallback.InitializeSessionEvents/PrefetchConnectionsSettings](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/ServicesCore/IapCoreInitializeCallback.cs):L24；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S32** [ImpressionScope](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Insights/ImpressionScope.cs):L8；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S33** [RequiresInsights assembly declaration](cross-sdk/packages/purchasing/5.5.1/extracted/package/Editor/AssemblyInfo.cs):L9；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S34** [versionDefines](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Unity.Purchasing.Stores.asmdef):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S35** [EngineDiagnostics.LogEvent/IsEventAllowed/SetBlockedEventTypes](core-insights/EngineDiagnostics-6000-7.raw):L14；Runtime pinned public branch or dated document；原包/文件SHA256见代码目录。
- **C53S36** [Identifiers.installationId/userId](core-insights/Identifiers-6000-7.raw):L13；Runtime pinned public branch or dated document；原包/文件SHA256见代码目录。
- **C53S37** [RequiresInsightsAttribute/CollectionRequirement](core-insights/RequiresInsights-6000-7.raw):L11；Runtime pinned public branch or dated document；原包/文件SHA256见代码目录。
- **C53S38** [Identifiers 6000.6 binding](core-insights/Identifiers-6000-6.raw):L10；Runtime pinned public branch or dated document；原包/文件SHA256见代码目录。
- **C53S39** [EngineDiagnostics 6000.6 binding](core-insights/EngineDiagnostics-6000-6.raw):L11；Runtime pinned public branch or dated document；原包/文件SHA256见代码目录。
- **C53S40** [Unity IAP privacy overview](core-insights/iap-privacy-overview.txt):L24；Document pinned public branch or dated document；原包/文件SHA256见代码目录。
- **C53S41** [Core 1.19.0 official changelog](core-insights/sdk/core/1.19.0/extracted/package/CHANGELOG.md):L1；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S42** [IAP 5.5.1/5.4.x official changelog](cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S43** [SessionManager.StartNewSession](cross-sdk/packages/services.analytics/6.3.0/extracted/package/Runtime/SessionManager.cs):L12；Analytics 6.3.0；原包/文件SHA256见代码目录。
- **C53S44** [GooglePlayStoreExtendedPurchaseService.Send*Event](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/Android/GooglePlay/Extensions/GooglePlayStoreExtendedPurchaseService.cs):L45；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S45** [AppInstallInfo.GetInstallTimestamp/FetchInstallTimestamp](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/AppInstallInfo.cs):L24；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S46** [PaymentOption enum](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Insights/PaymentOption.cs):L5；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S47** [ConsentState/DataCollectionMode](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/Consent.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S48** [DeviceInfo](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/DeviceInfo.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S49** [OrderData/Sku/Store/ProductType](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/OrderData.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S50** [StorePayload/OwnershipType](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/StorePayload.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S51** [EventType.IapSdk](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/EventType.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S52** [Reporting](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/Models/Reporting.cs):L1；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S53** [PlayerData session preference and optional Analytics getter](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L23；IAP 5.5.1；原包/文件SHA256见代码目录。
- **C53S54** [CorePackageInitializer.InitializeExternalUserId](core-insights/sdk/core/1.19.0/extracted/package/Runtime/Registration/CorePackageInitializer.cs):L255；Core 1.19.0；原包/文件SHA256见代码目录。
- **C53S55** [PurchaseService.Purchase/InvokePurchasePendingEvent](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Purchasing/Core/Purchasing/PurchaseService.cs):L250；IAP 5.5.1；原包/文件SHA256见代码目录。


<a id="pv56"></a>

## PV56 · 价值预测独立验证第一轮：资产审计与数据契约

- [56号报告](56_数据资产与授权可得性审计.md)：无已核验授权真实cohort，停止真实训练；不新增57—60真实结论。
- [资产快照/路径哈希/CSV质量](prediction-validation/results/asset_audit.json)、[JSON结构范围](prediction-validation/results/json_structure_inventory.json)。
- [接入规范](prediction-validation/data_contracts/README.md)、[JSON Schema](prediction-validation/data_contracts/bundle.schema.json)、[字段字典](prediction-validation/data_contracts/DATA_DICTIONARY.md)。
- [时间/会计/隐私门控实现](prediction-validation/src/validation.py)、[测试](prediction-validation/tests/test_contract.py)、[合成试跑](prediction-validation/results/round56_smoke_v1/smoke_result.json)。
- [M0—M5设计（未训练）](prediction-validation/experiments/protocol.json)、[运行说明](prediction-validation/README.md)。
- [检查结果](prediction-validation/results/DELIVERABLE_VALIDATION.json)、[原产物保留快照](prediction-validation/results/prior_artifacts.before56.json)。

【真实数据验证】没有真实玩家/LTV预测结论。【合成实验支持】仅会计/门控与既有条件机制；不用于证明平台精度或身份增益。【仍无证据】授权真实收入、bid-time历史、跨App增量及真实ROAS。详情以56号停止条件为准。


<a id="cg56"></a>

## CG56 · 56—59客户端买量机制痕迹专项

- [56_安装前竞价信号与Token血缘.md](56_安装前竞价信号与Token血缘.md)
- [57_自然量与跨渠道价值学习信号.md](57_自然量与跨渠道价值学习信号.md)
- [58_Axon_Vector完整买量反馈闭环.md](58_Axon_Vector完整买量反馈闭环.md)
- [59_普通游戏盈利跃迁机制与反证.md](59_普通游戏盈利跃迁机制与反证.md)

旧56号数据资产审计与prediction-validation保持原样，本轮不是其真实模型实验。

- [逐字段安装前血缘](client-growth/PREBID_FIELD_LINEAGE.json) / [原包来源及哈希](client-growth/PACKAGE_PROVENANCE.json)
- [原始片段及行号](client-growth/SOURCE_EVIDENCE.complete.json) / [来源目录](client-growth/SOURCE_CATALOG.md)
- [本轮24条边及条件](client-growth/EDGE_CATALOG.md) / [完整关系图](prediction-system/EVIDENCE_GRAPH.json) / [旧图快照](client-growth/EVIDENCE_GRAPH.before_client56.json)
- [完整性及证据引用核验](client-growth/VALIDATION.json)

<a id="cgs01"></a>

- **CGS01** [AndroidBuildHeaderBiddingToken.invoke](client-growth/SOURCE_CATALOG.md#cgs01)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt:L33；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs02"></a>

- **CGS02** [CommonGetHeaderBiddingToken.invoke](client-growth/SOURCE_CATALOG.md#cgs02)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonGetHeaderBiddingToken.kt:L13；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs03"></a>

- **CGS03** [AndroidSessionRepository session/counters](client-growth/SOURCE_CATALOG.md#cgs03)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidSessionRepository.kt:L77；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs04"></a>

- **CGS04** [AndroidCampaignRepository](client-growth/SOURCE_CATALOG.md#cgs04)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidCampaignRepository.kt:L11；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs05"></a>

- **CGS05** [HB WebView counter hooks](client-growth/SOURCE_CATALOG.md#cgs05)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt:L405；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs06"></a>

- **CGS06** [updateCampaignState](client-growth/SOURCE_CATALOG.md#cgs06)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt:L467；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs07"></a>

- **CGS07** [markCampaignStateShown](client-growth/SOURCE_CATALOG.md#cgs07)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctions.kt:L274；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs08"></a>

- **CGS08** [AndroidHandleGatewayAdResponse.invoke](client-growth/SOURCE_CATALOG.md#cgs08)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse.kt:L204；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs09"></a>

- **CGS09** [AndroidDeviceInfoRepository](client-growth/SOURCE_CATALOG.md#cgs09)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/repository/AndroidDeviceInfoRepository.kt:L21；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs10"></a>

- **CGS10** [AndroidPrivacyDeviceInfoDataSource.fetch](client-growth/SOURCE_CATALOG.md#cgs10)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidPrivacyDeviceInfoDataSource.kt:L20；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs11"></a>

- **CGS11** [AndroidFIdDataSource.invoke](client-growth/SOURCE_CATALOG.md#cgs11)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidFIdDataSource.kt:L10；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs12"></a>

- **CGS12** [FId Constants](client-growth/SOURCE_CATALOG.md#cgs12)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/services/core/fid/Constants.kt:L1；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs13"></a>

- **CGS13** [FIdBridge.getAppInstanceId](client-growth/SOURCE_CATALOG.md#cgs13)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/services/core/fid/FIdBridge.kt:L7；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs14"></a>

- **CGS14** [CachedFIdDataSource](client-growth/SOURCE_CATALOG.md#cgs14)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/CachedFIdDataSource.kt:L11；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs15"></a>

- **CGS15** [ServiceProvider FIdDataSource binding](client-growth/SOURCE_CATALOG.md#cgs15)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/services/core/di/ServiceProvider.kt:L1188；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs16"></a>

- **CGS16** [HandleGatewayUniversalResponse](client-growth/SOURCE_CATALOG.md#cgs16)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidHandleGatewayUniversalResponse.kt:L28；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs17"></a>

- **CGS17** [CommonInitAwaitingGetHeaderBiddingToken](client-growth/SOURCE_CATALOG.md#cgs17)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/CommonInitAwaitingGetHeaderBiddingToken.kt:L40；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs18"></a>

- **CGS18** [AndroidGetLimitedSessionToken.invoke](client-growth/SOURCE_CATALOG.md#cgs18)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetLimitedSessionToken.kt:L16；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs19"></a>

- **CGS19** [AndroidStaticDeviceInfoDataSource static fields](client-growth/SOURCE_CATALOG.md#cgs19)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidStaticDeviceInfoDataSource.kt:L73；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs20"></a>

- **CGS20** [AndroidDynamicDeviceInfoDataSource.fetch](client-growth/SOURCE_CATALOG.md#cgs20)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/data/datasource/AndroidDynamicDeviceInfoDataSource.kt:L57；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs21"></a>

- **CGS21** [AndroidGetAdRequest.invoke](client-growth/SOURCE_CATALOG.md#cgs21)：ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidGetAdRequest.kt:L31；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs22"></a>

- **CGS22** [4.18.1 AndroidBuildHeaderBiddingToken.invoke](client-growth/SOURCE_CATALOG.md#cgs22)：client-growth/java/unity-4181/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.java:L178；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs23"></a>

- **CGS23** [UnityAdsMediationAdapter.collectSignal](client-growth/SOURCE_CATALOG.md#cgs23)：cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java:L101；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs24"></a>

- **CGS24** [UnityAdsMediationAdapter.updatePrivacyConsent](client-growth/SOURCE_CATALOG.md#cgs24)：cross-sdk/java/max-unity-418/com/applovin/mediation/adapters/UnityAdsMediationAdapter.java:L268；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs25"></a>

- **CGS25** [GoogleMediationAdapter.collectSignal](client-growth/SOURCE_CATALOG.md#cgs25)：cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java:L224；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs26"></a>

- **CGS26** [GoogleMediationAdapter.createAdRequestWithParameters](client-growth/SOURCE_CATALOG.md#cgs26)：cross-sdk/java/max-google-254/com/applovin/mediation/adapters/GoogleMediationAdapter.java:L458；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs27"></a>

- **CGS27** [MediationServiceImpl.collectSignal](client-growth/SOURCE_CATALOG.md#cgs27)：client-growth/java/max-dispatch/com/applovin/impl/mediation/MediationServiceImpl.java:L221；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs28"></a>

- **CGS28** [g5 SignalCacheManager](client-growth/SOURCE_CATALOG.md#cgs28)：client-growth/java/max-history-cache/com/applovin/impl/g5.java:L18；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs29"></a>

- **CGS29** [i5 signal provider spec](client-growth/SOURCE_CATALOG.md#cgs29)：client-growth/java/max-1364/com/applovin/impl/i5.java:L14；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs30"></a>

- **CGS30** [MAX configuration defaults](client-growth/SOURCE_CATALOG.md#cgs30)：client-growth/java/max-1364/com/applovin/impl/v3.java:L85；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs31"></a>

- **CGS31** [g5$c bytecode cache age check](client-growth/SOURCE_CATALOG.md#cgs31)：client-growth/g5$c.javap.txt:L9；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs32"></a>

- **CGS32** [a6 mediated ad request body](client-growth/SOURCE_CATALOG.md#cgs32)：client-growth/java/max-1364/com/applovin/impl/a6.java:L103；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs33"></a>

- **CGS33** [a6.run](client-growth/SOURCE_CATALOG.md#cgs33)：client-growth/java/max-1364/com/applovin/impl/a6.java:L164；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs34"></a>

- **CGS34** [a6.ad_info/user_data](client-growth/SOURCE_CATALOG.md#cgs34)：client-growth/java/max-1364/com/applovin/impl/a6.java:L221；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs35"></a>

- **CGS35** [w3 metric names and scopes](client-growth/SOURCE_CATALOG.md#cgs35)：client-growth/java/max-history-cache/com/applovin/impl/w3.java:L24；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs36"></a>

- **CGS36** [y3 metric update/read](client-growth/SOURCE_CATALOG.md#cgs36)：client-growth/java/max-history-cache/com/applovin/impl/y3.java:L103；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs37"></a>

- **CGS37** [c5 umsm flag](client-growth/SOURCE_CATALOG.md#cgs37)：client-growth/java/max-history-cache/com/applovin/impl/c5.java:L788；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs38"></a>

- **CGS38** [MediationServiceImpl timestamp stats write](client-growth/SOURCE_CATALOG.md#cgs38)：client-growth/java/max-dispatch/com/applovin/impl/mediation/MediationServiceImpl.java:L408；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs39"></a>

- **CGS39** [LevelPlay9.5 q3 collector](client-growth/SOURCE_CATALOG.md#cgs39)：client-growth/java/lp-follow/com/ironsource/C0318q3.java:L14；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs40"></a>

- **CGS40** [LevelPlay9.5 g2 bidding data](client-growth/SOURCE_CATALOG.md#cgs40)：client-growth/java/lp-follow/com/ironsource/C0118g2.java:L70；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs41"></a>

- **CGS41** [LevelPlay9.5 Q1 collection completion](client-growth/SOURCE_CATALOG.md#cgs41)：client-growth/java/levelplay-950/com/ironsource/Q1.java:L161；【SDK代码证实】，版本/原包哈希与限定见原始目录。

<a id="cgs42"></a>

- **CGS42** [ROAS prelaunch data and all-source sharing](client-growth/SOURCE_CATALOG.md#cgs42)：vector/doc-roas-campaign-best-practices.txt:L36；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs43"></a>

- **CGS43** [Attributed/unattributed/organic definitions](client-growth/SOURCE_CATALOG.md#cgs43)：client-growth/unity-attribution-types.md:L28；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs44"></a>

- **CGS44** [Unity AppsFlyer install/event sharing scopes and maps](client-growth/SOURCE_CATALOG.md#cgs44)：vector/doc-integrate-appsflyer-with-unity.txt:L113；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs45"></a>

- **CGS45** [Unity AppsFlyer revenue connection/permissions](client-growth/SOURCE_CATALOG.md#cgs45)：vector/doc-integrate-appsflyer-with-unity.txt:L185；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs46"></a>

- **CGS46** [Unity Adjust all-sources and dedicated revenue mapping](client-growth/SOURCE_CATALOG.md#cgs46)：vector/doc-integrate-adjust-with-unity.txt:L43；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs47"></a>

- **CGS47** [Learning maturity/thresholds](client-growth/SOURCE_CATALOG.md#cgs47)：vector/doc-intro-to-roas-campaigns.txt:L79；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs48"></a>

- **CGS48** [Unity S2S IDs/time/attribution/revenue contract](client-growth/SOURCE_CATALOG.md#cgs48)：vector/doc-send-postbacks.txt:L28；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs49"></a>

- **CGS49** [AppLovin AppsFlyer all-sources mapping and excluded purchase revenue](client-growth/SOURCE_CATALOG.md#cgs49)：axon/doc-appsflyer.txt:L183；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs50"></a>

- **CGS50** [Adjust Axon partner/source choices and unmapped events](client-growth/SOURCE_CATALOG.md#cgs50)：axon/adjust-applovin.txt:L89；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs51"></a>

- **CGS51** [Axon model inputs/advertiser-shared data and explicit exclusions](client-growth/SOURCE_CATALOG.md#cgs51)：nongame/applovin-axon-about.txt:L54；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs52"></a>

- **CGS52** [AppLovin checkout revenue semantic restrictions](client-growth/SOURCE_CATALOG.md#cgs52)：axon/doc-in-app-purchase-revenue-sharing.txt:L13；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs53"></a>

- **CGS53** [Vector product correlations and postback sources](client-growth/SOURCE_CATALOG.md#cgs53)：vector/unity-vector-correct.txt:L10；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs54"></a>

- **CGS54** [AppLovin gaming ROAS and MAX prerequisites](client-growth/SOURCE_CATALOG.md#cgs54)：axon/gaming-apps.txt:L18；【官方公开证实】，版本/原包哈希与限定见原始目录。

<a id="cgs55"></a>

- **CGS55** [AppLovin click/impression device and request tracking macros](client-growth/SOURCE_CATALOG.md#cgs55)：axon/doc-tracking-url-macros.txt:L14；【官方公开证实】，版本/原包哈希与限定见原始目录。

新证据补齐广告历史→Token外层、允许条件下Firebase Analytics App Instance ID→Unity Pii、SDK signal→MAX构包，以及全来源/自然量postback的官方学习契约。未补齐目标游戏生产回传、身份join成功、逐字段训练与因果ROAS。


<a id="ma60"></a>

## MA60 · 模型架构公开证据第一轮（60）

- [60号主报告](60_Axon_Vector模型架构公开证据.md)：两家各五组证据、生产架构边界及61—64调查优先级。
- [SOURCE_CATALOG.md](model-architecture/SOURCE_CATALOG.md)
- [CLAIM_MATRIX.csv](model-architecture/CLAIM_MATRIX.csv)
- [ARCHITECTURE_HYPOTHESES.md](model-architecture/ARCHITECTURE_HYPOTHESES.md)
- [CONTRADICTIONS.md](model-architecture/CONTRADICTIONS.md)
- [EVIDENCE_GAPS.md](model-architecture/EVIDENCE_GAPS.md)
- [SOURCE_EVIDENCE.json](model-architecture/SOURCE_EVIDENCE.json)
- [PATENT_RECORDS.json](model-architecture/PATENT_RECORDS.json)
- [ACQUISITION_LEDGER.json](model-architecture/ACQUISITION_LEDGER.json)
- [VALIDATION.json](model-architecture/VALIDATION.json)
- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [旧图快照](model-architecture/EVIDENCE_GRAPH.before60.json) / [新增边](model-architecture/NEW_EDGES.json)

新增重点：Axon2未来多日价值分布与实时资本配置的官方陈述；Vector跨游戏行为模式/聚合cohort用于bid decision的官方陈述。两者均非生产网络/损失函数恢复；跨业务受益的前瞻声明不升级为部署。61—64本轮未制作。

<a id="ma60s01"></a>

- **MA60S01** [AppLovin / Axon 2](model-architecture/SOURCE_CATALOG.md#ma60s01)；【官方公开证实】；model-architecture/public/al-business.txt:L31；日期/原文/哈希/部署措辞见目录。

<a id="ma60s02"></a>

- **MA60S02** [AppLovin / Axon](model-architecture/SOURCE_CATALOG.md#ma60s02)；【官方公开证实】；nongame/applovin-axon-about.txt:L54；日期/原文/哈希/部署措辞见目录。

<a id="ma60s03"></a>

- **MA60S03** [AppLovin / AppLovin AppsFlyer partner](model-architecture/SOURCE_CATALOG.md#ma60s03)；【官方公开证实】；axon/doc-appsflyer.txt:L183；日期/原文/哈希/部署措辞见目录。

<a id="ma60s04"></a>

- **MA60S04** [AppLovin / AppLovin Ads / Axon](model-architecture/SOURCE_CATALOG.md#ma60s04)；【官方公开证实】；model-architecture/public/al-introducing.txt:L27；日期/原文/哈希/部署措辞见目录。

<a id="ma60s05"></a>

- **MA60S05** [AppLovin / Discovery / Prospecting](model-architecture/SOURCE_CATALOG.md#ma60s05)；【官方公开证实】；model-architecture/public/al-discovery.txt:L21；日期/原文/哈希/部署措辞见目录。

<a id="ma60s06"></a>

- **MA60S06** [AppLovin / Advertising platform research](model-architecture/SOURCE_CATALOG.md#ma60s06)；【间接技术线索】；prediction-system/applovin-job-4712559006-clean.txt:L8；日期/原文/哈希/部署措辞见目录。

<a id="ma60s07"></a>

- **MA60S07** [AppLovin / ML data infrastructure](model-architecture/SOURCE_CATALOG.md#ma60s07)；【间接技术线索】；prediction-system/applovin-job-4716524006-clean.txt:L8；日期/原文/哈希/部署措辞见目录。

<a id="ma60s08"></a>

- **MA60S08** [AppLovin / Ad Review vs Axon](model-architecture/SOURCE_CATALOG.md#ma60s08)；【官方公开证实】；prediction-system/applovin-excluded-rival-data.txt:L14；日期/原文/哈希/部署措辞见目录。

<a id="ma60s09"></a>

- **MA60S09** [AppLovin / Ad ROAS / Blended ROAS](model-architecture/SOURCE_CATALOG.md#ma60s09)；【官方公开证实】；axon/gaming-apps.txt:L20；日期/原文/哈希/部署措辞见目录。

<a id="ma60s10"></a>

- **MA60S10** [AppLovin / IAP revenue sharing](model-architecture/SOURCE_CATALOG.md#ma60s10)；【官方公开证实】；axon/doc-in-app-purchase-revenue-sharing.txt:L13；日期/原文/哈希/部署措辞见目录。

<a id="ma60s11"></a>

- **MA60S11** [AppLovin / Historical patent metadata](model-architecture/SOURCE_CATALOG.md#ma60s11)；【间接技术线索】；prediction-system/applovin-historical-patent.txt:L28；日期/原文/哈希/部署措辞见目录。

<a id="ma60s12"></a>

- **MA60S12** [AppLovin / Historical patent claims](model-architecture/SOURCE_CATALOG.md#ma60s12)；【间接技术线索】；prediction-system/applovin-historical-patent.txt:L1595；日期/原文/哈希/部署措辞见目录。

<a id="ma60s13"></a>

- **MA60S13** [Unity / Vector D28 IAA / Hybrid](model-architecture/SOURCE_CATALOG.md#ma60s13)；【官方公开证实】；vector/d28-blog.txt:L15；日期/原文/哈希/部署措辞见目录。

<a id="ma60s14"></a>

- **MA60S14** [Unity / Unity Ads ROAS learning](model-architecture/SOURCE_CATALOG.md#ma60s14)；【官方公开证实】；vector/doc-roas-campaign-best-practices.txt:L36；日期/原文/哈希/部署措辞见目录。

<a id="ma60s15"></a>

- **MA60S15** [Unity / Unity Ads ROAS cohorts](model-architecture/SOURCE_CATALOG.md#ma60s15)；【官方公开证实】；vector/doc-intro-to-roas-campaigns.txt:L79；日期/原文/哈希/部署措辞见目录。

<a id="ma60s16"></a>

- **MA60S16** [Unity / Vector IAP D7 / D28](model-architecture/SOURCE_CATALOG.md#ma60s16)；【官方公开证实】；model-architecture/public/unity-d7-d28.txt:L145；日期/原文/哈希/部署措辞见目录。

<a id="ma60s17"></a>

- **MA60S17** [Unity / Vector bid-time player/game intelligence](model-architecture/SOURCE_CATALOG.md#ma60s17)；【官方公开证实】；model-architecture/public/unity-d7-d28.txt:L208；日期/原文/哈希/部署措辞见目录。

<a id="ma60s18"></a>

- **MA60S18** [Unity / Vector Gamer AI inference](model-architecture/SOURCE_CATALOG.md#ma60s18)；【间接技术线索】；prediction-system/unity-job-JOBREQ-2615964-clean.txt:L1；日期/原文/哈希/部署措辞见目录。

<a id="ma60s19"></a>

- **MA60S19** [Unity / Vector Ads Modeling](model-architecture/SOURCE_CATALOG.md#ma60s19)；【间接技术线索】；prediction-system/unity-job-JOBREQ-2616596-clean.txt:L1；日期/原文/哈希/部署措辞见目录。

<a id="ma60s20"></a>

- **MA60S20** [Unity / Vector Bidding Science](model-architecture/SOURCE_CATALOG.md#ma60s20)；【间接技术线索】；prediction-system/unity-job-JOBREQ-2616286-clean.txt:L1；日期/原文/哈希/部署措辞见目录。

<a id="ma60s21"></a>

- **MA60S21** [Unity / Vector correlations and ecosystem](model-architecture/SOURCE_CATALOG.md#ma60s21)；【官方公开证实】；vector/unity-vector-correct.txt:L10；日期/原文/哈希/部署措辞见目录。

<a id="ma60s22"></a>

- **MA60S22** [Unity / IAP / D2C to Vector](model-architecture/SOURCE_CATALOG.md#ma60s22)；【官方公开证实】；vector/unity-2026-keynote.txt:L120；日期/原文/哈希/部署措辞见目录。

<a id="ma60s23"></a>

- **MA60S23** [Unity / Developer Data consent](model-architecture/SOURCE_CATALOG.md#ma60s23)；【官方公开证实】；vector/ddf-end-user-consent.txt:L14；日期/原文/哈希/部署措辞见目录。

<a id="ma60s24"></a>

- **MA60S24** [Unity / IAP5.5.1 Insights forwarding](model-architecture/SOURCE_CATALOG.md#ma60s24)；【SDK代码证实】；cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventEmitter.cs:L188；日期/原文/哈希/部署措辞见目录。

<a id="ma60s25"></a>

- **MA60S25** [Unity / Unity Ads4.17 prebid history](model-architecture/SOURCE_CATALOG.md#ma60s25)；【SDK代码证实】；ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/domain/AndroidBuildHeaderBiddingToken.kt:L33；日期/原文/哈希/部署措辞见目录。

<a id="ma60s26"></a>

- **MA60S26** [Unity / MMP S2S revenue association](model-architecture/SOURCE_CATALOG.md#ma60s26)；【官方公开证实】；vector/doc-send-postbacks.txt:L28；日期/原文/哈希/部署措辞见目录。

<a id="ma60s27"></a>

- **MA60S27** [AppLovin / Incrementality and measurement](model-architecture/SOURCE_CATALOG.md#ma60s27)；【官方公开证实】；model-architecture/public/al-measurement.txt:L20；日期/原文/哈希/部署措辞见目录。

<a id="ma60s28"></a>

- **MA60S28** [AppLovin / Creative and targeting](model-architecture/SOURCE_CATALOG.md#ma60s28)；【官方公开证实】；model-architecture/public/al-silos.txt:L40；日期/原文/哈希/部署措辞见目录。



<a id="rv61"></a>

## RV61 · 61＋63收入分布与价值出价专项

- [61号收入标签与价值分布预测](61_收入标签与价值分布预测.md)
- [63号预测价值到实时竞价与预算约束](63_预测价值到实时竞价与预算约束.md)
- [SOURCE_CATALOG.md](model-architecture/round61-63/SOURCE_CATALOG.md)
- [SOURCE_EVIDENCE.json](model-architecture/round61-63/SOURCE_EVIDENCE.json)
- [COMPETING_HYPOTHESES.md](model-architecture/round61-63/COMPETING_HYPOTHESES.md)
- [ACQUISITION_LEDGER.json](model-architecture/round61-63/ACQUISITION_LEDGER.json)
- [NEW_EDGES.json](model-architecture/round61-63/NEW_EDGES.json)
- [MATH_EXAMPLES.json](model-architecture/round61-63/MATH_EXAMPLES.json)
- [VALIDATION.json](model-architecture/round61-63/VALIDATION.json)
- [更新后CLAIM_MATRIX](model-architecture/CLAIM_MATRIX.csv) / [原28行快照](model-architecture/round61-63/CLAIM_MATRIX.before.csv)
- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [更新前快照](model-architecture/round61-63/EVIDENCE_GRAPH.before.json)

新增正式数据/预算约束，不是新增生产网络结构：Unity CPI计费ROAS自动竞价、7日滚动预算/国家组分配和探索；Unity丢失事件不追溯补发警告；AppLovin网站去重时段与手游MMP边界。Axon条件分布/风险出价、Vector标签与共享表示仍未知。

<a id="rv61s01"></a>

- **RV61S01** [Unity/Post-install event data](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s01)；【官方公开证实】；model-architecture/round61-63/public/u-appdata-direct.txt:L10。

<a id="rv61s02"></a>

- **RV61S02** [Unity/Post-install data loss](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s02)；【官方公开证实】；model-architecture/round61-63/public/u-appdata-direct.txt:L38。

<a id="rv61s03"></a>

- **RV61S03** [Unity/Revenue event mapping](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s03)；【官方公开证实】；model-architecture/round61-63/public/u-integration-best.txt:L60。

<a id="rv61s04"></a>

- **RV61S04** [Unity/Singular mapping exception](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s04)；【官方公开证实】；model-architecture/round61-63/public/u-integration-best.txt:L107。

<a id="rv61s05"></a>

- **RV61S05** [Unity/Budget hierarchy/throttling](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s05)；【官方公开证实】；model-architecture/round61-63/public/u-budget-intro.txt:L20。

<a id="rv61s06"></a>

- **RV61S06** [Unity/Multi-country allocation](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s06)；【官方公开证实】；model-architecture/round61-63/public/u-budget-intro.txt:L63。

<a id="rv61s07"></a>

- **RV61S07** [Unity/ROAS automated bidding](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s07)；【官方公开证实】；model-architecture/round61-63/public/u-budget-best.txt:L14。

<a id="rv61s08"></a>

- **RV61S08** [Unity/Exploration budget](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s08)；【官方公开证实】；model-architecture/round61-63/public/u-budget-best.txt:L34。

<a id="rv61s09"></a>

- **RV61S09** [Unity/Seven-day pacing](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s09)；【官方公开证实】；model-architecture/round61-63/public/u-budget-best.txt:L73。

<a id="rv61s10"></a>

- **RV61S10** [Unity/Country ROAS and budget setup](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s10)；【官方公开证实】；model-architecture/round61-63/public/u-create-roas.txt:L16。

<a id="rv61s11"></a>

- **RV61S11** [Unity/CVR/CPI/eCPM exposure](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s11)；【官方公开证实】；model-architecture/round61-63/public/u-bid-intro.txt:L20。

<a id="rv61s12"></a>

- **RV61S12** [AppLovin/Scale and budget recommendations](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s12)；【官方公开证实】；model-architecture/round61-63/public/al-scale-right.txt:L47。

<a id="rv61s13"></a>

- **RV61S13** [AppLovin/Pixel/SDK/S2S deduplication](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s13)；【官方公开证实】；model-architecture/round61-63/public/al-website-dedup.txt:L13。

<a id="rv61s14"></a>

- **RV61S14** [Adjust/Android5.8.1 revenue validation](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s14)；【SDK代码证实】；ThirdPartySDKs/Adjust/Android/5.8.1/sources/com/adjust/sdk/AdjustEvent.java:L142。

<a id="rv61s15"></a>

- **RV61S15** [AppLovin/MAX unified first-price auction](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s15)；【官方公开证实】；auction/al-dynamics.txt:L13。

<a id="rv61s16"></a>

- **RV61S16** [Unity/Exchange deadline/first-price](model-architecture/round61-63/SOURCE_CATALOG.md#rv61s16)；【官方公开证实】；auction/unity-get-started.txt:L20。



<a id="ct62"></a>

## CT62 · 跨游戏知识迁移与冷启动（62号）

- [62号报告与四机制矩阵/训练竞价分离图](62_跨游戏知识迁移与冷启动机制.md)
- [SOURCE_CATALOG.md](model-architecture/round62/SOURCE_CATALOG.md)
- [SOURCE_EVIDENCE.json](model-architecture/round62/SOURCE_EVIDENCE.json)
- [AUTHOR_TRACE.json](model-architecture/round62/AUTHOR_TRACE.json)
- [TRACE_LEDGER.json](model-architecture/round62/TRACE_LEDGER.json)
- [FOUR_MECHANISMS.csv](model-architecture/round62/FOUR_MECHANISMS.csv)
- [FOUR_MECHANISMS.json](model-architecture/round62/FOUR_MECHANISMS.json)
- [NEW_EDGES.json](model-architecture/round62/NEW_EDGES.json)
- [VALIDATION.json](model-architecture/round62/VALIDATION.json)
- [CLAIM_MATRIX](model-architecture/CLAIM_MATRIX.csv) / [原44行快照](model-architecture/round62/CLAIM_MATRIX.before.csv)
- [关系图](prediction-system/EVIDENCE_GRAPH.json) / [更新前快照](model-architecture/round62/EVIDENCE_GRAPH.before.json)

最强路径：两家A（同目标App全来源样本），Vector另有B聚合cohort的bid-time用途披露。C共享参数与D个人历史未唯一识别；A/B/C理论上不必D，但训练用途/隐私条件仍需满足。沿原文作者和相关链接未得新生产模型材料，建议停止重复广搜。

<a id="ct62s01"></a>

- **CT62S01** [Unity/Vector cross-game article authorship](model-architecture/round62/SOURCE_CATALOG.md#ct62s01)；【官方公开证实】；model-architecture/public/unity-d7-d28.txt:L123；范围及反证见目录。

<a id="ct62s02"></a>

- **CT62S02** [Unity/Cross-game use at bid decision](model-architecture/round62/SOURCE_CATALOG.md#ct62s02)；【官方公开证实】；model-architecture/public/unity-d7-d28.txt:L208；范围及反证见目录。

<a id="ct62s03"></a>

- **CT62S03** [Unity/Linked ROAS onboarding announcement](model-architecture/round62/SOURCE_CATALOG.md#ct62s03)；【官方公开证实】；model-architecture/round62/public/unity-march-linked.txt:L123；范围及反证见目录。

<a id="ct62s04"></a>

- **CT62S04** [Unity/Same-app cross-source prelaunch learning](model-architecture/round62/SOURCE_CATALOG.md#ct62s04)；【官方公开证实】；vector/doc-roas-campaign-best-practices.txt:L36；范围及反证见目录。

<a id="ct62s05"></a>

- **CT62S05** [Unity/No prerequisite install campaign](model-architecture/round62/SOURCE_CATALOG.md#ct62s05)；【官方公开证实】；vector/doc-intro-to-roas-campaigns.txt:L91；范围及反证见目录。

<a id="ct62s06"></a>

- **CT62S06** [Unity/Unattributed source scope](model-architecture/round62/SOURCE_CATALOG.md#ct62s06)；【官方公开证实】；model-architecture/round62/public/unity-acquire-attribution.txt:L26；范围及反证见目录。

<a id="ct62s07"></a>

- **CT62S07** [AppLovin/Axon public training categories](model-architecture/round62/SOURCE_CATALOG.md#ct62s07)；【官方公开证实】；nongame/applovin-axon-about.txt:L60；范围及反证见目录。

<a id="ct62s08"></a>

- **CT62S08** [AppLovin/Advertiser-owned all-source sharing](model-architecture/round62/SOURCE_CATALOG.md#ct62s08)；【官方公开证实】；axon/adjust-applovin.txt:L113；范围及反证见目录。

<a id="ct62s09"></a>

- **CT62S09** [AppLovin/Cross-category prospective gaming benefit](model-architecture/round62/SOURCE_CATALOG.md#ct62s09)；【官方公开证实】；model-architecture/public/al-introducing.txt:L47；范围及反证见目录。

<a id="ct62s10"></a>

- **CT62S10** [Unity/Developer Data privacy gating](model-architecture/round62/SOURCE_CATALOG.md#ct62s10)；【官方公开证实】；vector/ddf-end-user-consent.txt:L20；范围及反证见目录。

<a id="ct62s11"></a>

- **CT62S11** [AppLovin/Ad Review data exclusion](model-architecture/round62/SOURCE_CATALOG.md#ct62s11)；【官方公开证实】；prediction-system/applovin-excluded-rival-data.txt:L14；范围及反证见目录。



<a id="final64"></a>

## FINAL64 · 普通游戏盈利跃迁最终综合（无新增生产证据）

- [64号独立最终报告](64_普通游戏盈利跃迁最终机制判断.md)
- [25行因果矩阵：总框架＋四款×五机制](model-architecture/FINAL_CAUSAL_MATRIX.csv)
- [四款逐案审计及技术链图](model-architecture/FOUR_GAME_VERDICTS.md)
- [停止与授权恢复条件](model-architecture/STOP_AND_RESUME_CRITERIA.md)
- [复用原始URL/方法/RVA/SHA256目录](model-architecture/final64/SOURCE_CATALOG.md)
- [机器可读来源账本](model-architecture/final64/SOURCE_LEDGER.json)
- [新增关系边](model-architecture/final64/NEW_EDGES.json)
- [更新前图快照](model-architecture/final64/EVIDENCE_GRAPH.before.json) / [历史文件哈希](model-architecture/final64/HISTORY.before.json)
- [交付校验](model-architecture/final64/VALIDATION.json)

结论：价值排序、同App全来源历史、跨游戏聚合或参数迁移、变现改善、素材/国家/预算/归因均为竞争性解释；没有四款目标游戏指定模型消费、实际导量盈利或因果增量的新证据。新增图边实线只表静态业务入口；送达/训练/盈利边保留未知。官方原编号MA60/RV61/CT62复用，未改变旧对象；F64C01—F64C19仅为既有静态原件的新索引。

<a id="f64c01"></a>

- **F64C01** 【游戏代码证实】Car Race / IAAController.OnAdRevenuePaidEvent; RVA 0x24401f8；[car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.OnAdRevenuePaidEvent-24401f8.asm](car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.OnAdRevenuePaidEvent-24401f8.asm)；SHA256 `bf266496658413d368f2a46bab606c166793b015a5490327857b326dddfc468f`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c02"></a>

- **F64C02** 【游戏代码证实】Car Race / AdMeticaDefault.OnShowRevenuePaid; RVA 0x32deaf0；[car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.OnShowRevenuePaid-32deaf0.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.OnShowRevenuePaid-32deaf0.asm)；SHA256 `22b2d95afc3f5ddf000049f104eaf282a2a6f695e420fd552c86bf23e19ee51b`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c03"></a>

- **F64C03** 【游戏代码证实】Car Race / AdRevenueTracking.ImpressionSuccessEvent; RVA 0x32c2988；[car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Max__Zego.Advertisement.Max.AdRevenueTracking.ImpressionSuccessEvent-32c2988.asm](car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Max__Zego.Advertisement.Max.AdRevenueTracking.ImpressionSuccessEvent-32c2988.asm)；SHA256 `78a6f8f5b4611db9378bd500e2aa46eb96996a85acf7dda0542f6d611ca5718e`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c04"></a>

- **F64C04** 【游戏代码证实】Meowdoku / LTVManager.getLTV/increaseLTV/mergeData; L50-L81；[meowdoku/static/java/classes4.dex/com/learnings/grt/event/LTVManager.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/LTVManager.java)；SHA256 `161bbd9f22f5b521ea2769ae1c32add65cdcd7f7065c122bd41fe10f1c3193a8`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c05"></a>

- **F64C05** 【游戏代码证实】Meowdoku / BaseGrtEvent.sendEvent; L66-L94；[meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/BaseGrtEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/BaseGrtEvent.java)；SHA256 `3c177cf9efb516a75634d0c929a224cbfff6638a6a221ab8afb5469497d77818`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c06"></a>

- **F64C06** 【游戏代码证实】Meowdoku / IaaFbRoasEvent.onAdImpression；[meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/IaaFbRoasEvent.java](meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/IaaFbRoasEvent.java)；SHA256 `7d5bfced2a0ea0d8b04ee084a852a9873fbebb37383d09acfc5d00f32684eb0b`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c07"></a>

- **F64C07** 【游戏代码证实】Meowdoku / ConfigManager; configuration load/version/update；[meowdoku/static/java/classes4.dex/com/learnings/grt/config/ConfigManager.java](meowdoku/static/java/classes4.dex/com/learnings/grt/config/ConfigManager.java)；SHA256 `d76a4ba8453ab7690bb2d2e47ad9d3e7eabd5fcde649d7d0b645588283531e98`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c08"></a>

- **F64C08** 【游戏代码证实】Meowdoku / Tracker; game_start/game_end/ad/guide/subscription events；[meowdoku/static/godot-source/tracker.gd](meowdoku/static/godot-source/tracker.gd)；SHA256 `db9296a002f8abe109ddf5a97901a8a2c0434458439a0cd6ce543beed09a48ca`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c09"></a>

- **F64C09** 【游戏代码证实】Rotate Rings / g8.a.adRevenue; L100-L123；[rotate-rings/static/java/classes2.dex/g8/a.java](rotate-rings/static/java/classes2.dex/g8/a.java)；SHA256 `7c2c6b011ec46caed6c287ad292aa85aa51c16ed81fd81dcabc29ecc355c6c5a`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c10"></a>

- **F64C10** 【游戏代码证实】Rotate Rings / SDKManager.handleAdRevenue; L386; async upload L802；[rotate-rings/static/java/classes6.dex/com/unity3d/player/SDKManager.java](rotate-rings/static/java/classes6.dex/com/unity3d/player/SDKManager.java)；SHA256 `25e108286d650247410744d20698e56f3a74606b5275beb287efbb3943cf9098`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c11"></a>

- **F64C11** 【游戏代码证实】Rotate Rings / upload_revenue / upload_pltv7_byday_bycountry; L1013/L1048；[rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java](rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java)；SHA256 `7b1c69c3a3135bd393e9037b29c816aaa415dddcd505017051d53061e4e30ab2`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c12"></a>

- **F64C12** 【游戏代码证实】Rotate Rings / ta.d.j(String,int); L4405；[rotate-rings/static/java/classes9.dex/ta/d.java](rotate-rings/static/java/classes9.dex/ta/d.java)；SHA256 `7f6d569462e26a7ca5726d3655c7494fdd281dd4bf3e67858a029fe421cad6aa`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c13"></a>

- **F64C13** 【游戏代码证实】Jewel Coloring / ad_worth_event.json; extras/events; 90 rules / 31 tables；[jewel-coloring/deep/resources/ad_worth_event.json.redacted.json](jewel-coloring/deep/resources/ad_worth_event.json.redacted.json)；SHA256 `990577a343081611b3b46d460964ce3963404045281fd03c1ae402b3b4665c01`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c14"></a>

- **F64C14** 【游戏代码证实】Jewel Coloring / AWESendPlatform::sendMsgToPlatform; RVA 0x1a44350；[jewel-coloring/deep/asm/ad__event__AWESendPlatform__sendMsgToPlatform__-1a44350.asm](jewel-coloring/deep/asm/ad__event__AWESendPlatform__sendMsgToPlatform__-1a44350.asm)；SHA256 `f8bb8a56bb671d691b7ac32a64881366fb15085448efc9de4a207db31ca2e839`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c15"></a>

- **F64C15** 【游戏代码证实】Jewel Coloring / AWEWorthUpdate::getBeSentWorth; RVA 0x1a3dc50；[jewel-coloring/deep/asm/ad__event__AWEWorthUpdate__getBeSentWorth_ad__event__AWEWorthSendType__float_-1a3dc50.asm](jewel-coloring/deep/asm/ad__event__AWEWorthUpdate__getBeSentWorth_ad__event__AWEWorthSendType__float_-1a3dc50.asm)；SHA256 `5769f3bca001626d1a67ff6dabd789ccb941d1ba784dcd06d48cc2214271a219`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c16"></a>

- **F64C16** 【游戏代码证实】Jewel Coloring / raw entry / decoded SHA256 / split / logical resource mapping；[jewel-coloring/deep/resources/decoded-config-provenance.json](jewel-coloring/deep/resources/decoded-config-provenance.json)；SHA256 `4a1a1814bfb9a4be85f0345b3366d435fa15f3acc681781a9d33a4d1d988f65d`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c17"></a>

- **F64C17** 【游戏代码证实】four games / DEX class/method/descriptor/invoke offsets；[axon/deep/event-callsite-catalog.json](axon/deep/event-callsite-catalog.json)；SHA256 `1e439919ec9986495cb0e4a137ed5e6af4a00fb8ed69b09d6f9e4004ff023b92`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c18"></a>

- **F64C18** 【游戏代码证实】four games / scan summary; 15/8/14/12 DEX；[axon/deep/game-scan-summary.json](axon/deep/game-scan-summary.json)；SHA256 `448779ff5ca26eda591008bf8f9ed4bd413d9fbceab70d28160ab9e15f71f7fc`；仅静态范围，生产送达/训练/效果未证。

<a id="f64c19"></a>

- **F64C19** 【游戏代码证实】Jewel Coloring / BulldogSdk::_initBaseComponents; RVA 0x1937ee0；[jewel-coloring/deep/asm/BulldogSdk___initBaseComponents_BulldogDelegate___int__int__int_-1937ee0.asm](jewel-coloring/deep/asm/BulldogSdk___initBaseComponents_BulldogDelegate___int__int__int_-1937ee0.asm)；SHA256 `d1cdfbd765e6b33e4a94917692cb565d3ecefad1bdfadd2be2fd99034cb16a90`；仅静态范围，生产送达/训练/效果未证。


<a id="pe65"></a>

## PE65 · 公开扩量与数据准入（不做SDK逆向/模型训练）

- [65号审计报告](65_公开扩量证据与模型实验可行性审计.md)
- [四款精确身份表](public-evidence/GAME_IDENTITY_REGISTRY.csv) / [事件时间线](public-evidence/EXTERNAL_UA_TIMELINES.csv)
- [外部原始来源与访问限制](public-evidence/EXTERNAL_SOURCE_CATALOG.md) / [四类竞争解释](public-evidence/COMPETING_EXPLANATIONS.md)
- [9候选数据目录](public-experiments/DATASET_CATALOG.csv) / [数据许可与真实文件审计](public-experiments/DATASET_LICENSE_AUDIT.md)
- [E0—E4准入](public-experiments/EXPERIMENT_ADMISSION_MATRIX.csv) / [受限实验协议](public-experiments/EXPERIMENT_PROTOCOL.md)
- [停止条件](public-evidence/STOP_CONDITIONS.md) / [校验](public-evidence/VALIDATION65.json)

新增观察：四款当前身份与快照可核；AppBrain估算近30天Car360万、Meow930万、Rotate850万、Jewel80万，非归因安装/广告花费/利润。0个可确定突然扩量起点。3个公开发行物许可支持受限通用研究，0个满足完整手游价值/迁移/安装前LTV要求；E0/E1/E4 LIMITED替代，E2/E3 STOP，原目标均无GO，未训练模型。关系图保留旧对象，仅追加观察、准入与未知因果边。


<a id="round66"></a>

## ROUND66 · 两款公开轨迹与真实零售预测（不外推游戏）

- [66号外部轨迹报告](66_Rotate与Meow历史买量轨迹调查.md) / [外部时间线](66_外部推广证据时间线.csv)
- [66号UCI预测实验报告](66_UCI用户未来消费金额预测实验.md) / [全部模型/基线结果及CI](66_模型实验结果.csv)
- [新外部来源URL/日期/哈希](public-evidence/round66/SOURCE_CATALOG.md) / [版本目录原位置](public-evidence/round66/VERSION_DIRECTORY_ROWS.csv)
- [预固定协议](public-experiments/round66/PREREGISTERED_PROTOCOL.md) / [真实运行源码](public-experiments/round66/run_experiment66.py) / [运行清单](public-experiments/round66/RUN_MANIFEST.json)
- [评价修正与初始结果保留](public-experiments/round66/EVALUATION_CORRECTION.md) / [泄漏边界fixture](public-experiments/round66/BOUNDARY_TESTS.json)
- [最终校验](public-evidence/round66/VALIDATION66.json)

A线新事实：Meow精确包名10月3日归档近30天估570万，当前930万；两个时点的估算差异约63.2%，不是付费安装、突然变点、真实预算或利润。两款版本目录可读，但无连续前后各4周量、paid creative或AppLovin/Unity渠道证据；停止重复搜索。B线实际UCI发票实验：客户与时间完全隔离，28天M1/M2相对历史日均MAE有家族校正支持；7天主要检验不足、RMSE未改善、零基线MAE更低。修复Top10零值/平分假象，保留初始结果；未改模型或金额口径。零售预测不证明任何目标游戏/平台生产消费或盈利。


<a id="iv67"></a>

## IV67 · UCI独立时间验证（非手游/平台生产证据）

- [67号独立时间报告](67_用户价值预测独立时间验证.md) / [拟合前协议](67_独立实验协议.md)
- [模型结果与CI](67_模型对照结果.csv) / [金额概率分箱](67_预测校准分析.csv) / [分层周别与新客户](67_分层预测误差.csv)
- [运行代码](public-experiments/round67/run67.py) / [原66冻结重建](public-experiments/round67/FROZEN66_RECONSTRUCTION.json)
- [主要及探索性配对比较](public-experiments/round67/PAIRED_COMPARISONS.csv) / [运行哈希](public-experiments/round67/RUN_MANIFEST.json)
- [边界与历史保留验证](public-experiments/round67/BOUNDARY_AND_PROVENANCE_TESTS.json) / [最终交付校验](public-experiments/round67/VALIDATION67.json)

新事实：10-10—11-07共839客户/4037时点行，原66冻结M2的MAE相对历史日均改善36.58%，重训M2改善37.81%，8项家族比较支持；两阶段/校准相对直接M2的MAE与RMSE优势未确认。零基线MAE仍很强，M3仅略优且CI跨0；高消费排序有信号但尾部低估、总额漂移及校准代价仍在。概率不从直接金额模型伪造。保留旧00—66与原数据，未恢复游戏搜索，未证明Axon/Vector或游戏盈利。


IV67补充核验：预定周×消费层描述诊断已补齐，9个固定预测器全部重建一致；[225行交叉诊断](public-experiments/round67/WEEK_BY_TIER_DIAGNOSTIC.csv)、[重建边界](public-experiments/round67/WEEK_TIER_DIAGNOSTIC_MANIFEST.json)。每周尾层仅2—3客户、总体仅3不同客户，未获得稳定长尾改善或新增确认性结论。


<a id="pd68"></a>

## PD68 · 全新公开数据源与跨产品迁移准入

- [68号报告](68_全新公开数据源调查.md)、[17候选目录](68_DATASET_CATALOG.csv)、[许可审计](68_DATASET_LICENSE_AUDIT.md)
- [跨产品准入与69建议](68_CROSS_PRODUCT_TRANSFER_READINESS.md)、[6项实验矩阵](68_EXPERIMENT_ADMISSION_MATRIX.csv)
- [原始来源/摘录/哈希](public-experiments/round68/SOURCE_CATALOG.md)、[完整数据下载记录](public-experiments/round68/ASSET_ACQUISITION.json)、[电子交易原包](public-experiments/round68/ASSET_ELECTRONICS.json)
- [Complete Journey](public-experiments/round68/AUDIT_JOURNEY.json)、[珠宝](public-experiments/round68/AUDIT_JEWELRY.json)、[电子](public-experiments/round68/AUDIT_ELECTRONICS.json)、[租赁](public-experiments/round68/AUDIT_VIBRENT.json)
- [最终保留与结构校验](public-experiments/round68/VALIDATION68.json)

新证据：取得独立Complete Journey全量1469307行及两个商店完整交易发行物；电子缺键78.58%、金额缺16.40%及1970异常，珠宝无表头，Vibrent套餐标价非扣款。A级真实游戏/B级媒体IAA准入均0，当前跨产品训练组合0；不关联个人ID的参数/聚合迁移可设计但未执行。严格零值/观测缺失门槛未满足，69号先补证不训练；无UCI原始使用、无新增模型结果、无Axon/Vector效果主张。旧对象与历史报告原样保留。


<a id="os69"></a>

## OS69 · 原始发布者、字段契约与观察覆盖

- [Complete Journey](69_CompleteJourney原始数据与观察覆盖审计.md)、[Jewelry](69_REES46Jewelry字段语义审计.md)、[Electronics](69_REES46Electronics缺失与异常审计.md)
- [原始来源及作者证据索引](69_原始数据来源及作者证据索引.csv)、[八门槛最终判断](69_实验准入最终判断.md)
- [CJ作者处理原代码](public-experiments/round69/sources/journey-prep.txt)、[全量原件秒数/时区/删日核验](public-experiments/round69/JOURNEY_PREPROCESSING_VERIFICATION.json)
- [Jewelry官方v1原包/header](public-experiments/round69/VERSION_PROBES.json)、[两版对照](public-experiments/round69/JEWELRY_VERSION_COMPARISON.json)、[13列契约](public-experiments/round69/JEWELRY_FIELD_CONTRACT.csv)
- [电子旧版完整下载](public-experiments/round69/VERSION_ELECTRONICS_FULL.json)、[事件/日期版本差分](public-experiments/round69/ELECTRONICS_VERSION_COMPARISON.json)
- [Jewelry短行](public-experiments/round69/JEWELRY_RAW_STRUCTURE.json)、[电子短行与日期](public-experiments/round69/ELECTRONICS_RAW_STRUCTURE.json)、[电子逐日缺失](public-experiments/round69/ELECTRONICS_DAILY_COVERAGE.csv)
- [未发送作者问题](public-experiments/round69/AUTHOR_QUESTIONS_UNSENT.md)、[最终保留校验](public-experiments/round69/VALIDATION69.json)

对68号补充：CJ2017为作者人工映射，秒数按basket后缀构造，12-25被假定闭店删除；sales_value不是顾客实付。Jewelry官方旧版13列表头已恢复；5352个共同解析空值均对应11字段短行。电子431954个price解析空值均为6字段短行，正常行另有1637398空用户，1970原字面在旧版已存在。字段/源证据GO，三数据完整真实未来价值和跨产品训练仍STOP；旧对象不改写，无模型/UCI/个人匹配/作者联系。


## GI69：真实游戏数据、广告请求与价值反馈专项（2026-11-20）

与原零售69号并行保留。没有新增可直接训练的真实游戏玩家文件；没有发送申请、签约、训练或生产测试。

- [69总览](69_真实游戏数据来源与获取可行性.md)：6候选准入卡，真实训练均STOP或排除。
- [Uken](69_Uken数据获取与准入审计.md)：SFU2015参与者30万行/44字段说明，明确无上传数据权限；缩放、观察窗口和完整NDA未知。
- [Unity交易研究](69_Unity交易数据来源审计.md)：真实IAP论文、OSF两份补充文件已下载验哈希；原数据内部受控、作者不能共享、仅付费者、跨游戏ID不关联；R样本为合成。
- [MAG](69_MAG游戏经营数据审计.md)：五游戏原论文/数据包身份尚未匹配，UNKNOWN/STOP，不以无检索结果否定其存在。
- [字段时间线](69_广告请求与收入反馈字段时间线.md)：24条广告前/响应/展示/收入/MMP/Apple归因字段链；复用220条哈希核验材料。
- [Axon/Vector连接](69_Axon_Vector训练与竞价数据连接证据.md)：官方产品用途与客户端字段级消费保持分开，没有新增生产训练血缘。
- [70号建议](69_NEXT_RESEARCH_PRIORITY.md)：优先数据授权、成熟cohort与接收→训练列契约；没有合格数据不训练。

原始URL、位置、日期、SHA256：[SOURCE_CATALOG](game-industry69/SOURCE_CATALOG.md)、[来源对象](game-industry69/SOURCE_EVIDENCE.json)、[代码片段](game-industry69/CODE_EVIDENCE.json)、[获取记录](game-industry69/FETCH_MANIFEST.json)。[字段CSV](game-industry69/SDK_FIELD_TIMELINE.csv)、[准入CSV](game-industry69/DATASET_ADMISSION.csv)。

图追加GI69节点/边/来源，保留全部历史对象；六层不跳级，所有本轮生产送达/接收/训练状态未证。[核验结果](game-industry69/VALIDATION.json)。


## CL70：真实游戏授权准备与竞价/事件关联补证（2026-11-20）

本轮有新的客户端赋值链，未取得新原始玩家数据/许可、未训练、未发送申请或生产测试。

- [Uken授权与申请准备](70_Uken数据授权与申请准备.md)：由SFU官方目录找到现行统计系管理/咨询转介及Uken公开入口；不是已证实数据许可渠道。[四份未发送草稿](closure70/application/RESEARCH_BRIEF_AND_DATA_REQUEST.md)。
- [真实游戏新增来源审计](70_真实游戏数据新增来源审计.md)：Unity补充材料复用验哈希；Age原作者记录核验；MAG仍无法准确匹配原研究；数据训练STOP。
- [Axon/MAX闭环](70_Axon竞价数据闭环.md)：完整响应event_id→赢家map→下一请求previous_loaded_request_id；同广告对象收入回调；click/load与impression分支边界补齐。
- [Vector/Unity Ads闭环](70_Vector竞价数据闭环.md)：适配器新load UUID→load/show objectId→Unity机会→广告对象→operative关联；Token ID不可自动等同，trackingToken可刷新。
- [22项预测输入/反馈时间线](70_预测输入与收入反馈时间线.csv)：逐项共同ID/显式赋值、时间、触发、接收方与生产/训练未知。
- [下一阶段建议](70_下一阶段突破建议.md)：优先授权成熟游戏cohort与经济事件/MMP/训练列关联契约，不再重复SDK清单。

新增38段静态代码证据+6份官方联系/元数据，复用27条既核验材料；片段数量不等于独立发现数量。[SOURCE_CATALOG](closure70/SOURCE_CATALOG.md)、[原包/源码哈希及片段](closure70/CODE_EVIDENCE.json)、[关联机器表](closure70/EVENT_ASSOCIATIONS.json)、[字节码核验记录](closure70/BYTECODE_CHECK.json)。

关系图追加CL70节点/边/来源，所有00—69报告及旧图对象保留。真实生产发送、接收和字段级模型训练均未新增证明。[完整性核验](closure70/VALIDATION.json)。


## L71：训练血缘、经济展示与真实游戏数据准入（2026-11-20）

本轮新增条件关联，不新增生产接收/训练或盈利证据。MAX响应T()→收入广播基础id，后续两层putAll可覆盖；load内部调用现定位到本地收入topic，仍无所查公共收入回调。Unity事件快照→持久化重试已核对。MMP伙伴字段≠训练列，Uken权利方及许可仍未知，申请未发送、训练STOP。

- [71_MAX经济展示与收入关联.md](71_MAX经济展示与收入关联.md)
- [71_Unity机会ID与事件关联.md](71_Unity机会ID与事件关联.md)
- [71_MMP到广告平台数据血缘.md](71_MMP到广告平台数据血缘.md)
- [71_Axon训练数据字段证据.md](71_Axon训练数据字段证据.md)
- [71_Vector训练数据字段证据.md](71_Vector训练数据字段证据.md)
- [71_Uken数据授权最终申请包.md](71_Uken数据授权最终申请包.md)
- [71_端到端训练反馈关系图.json](71_端到端训练反馈关系图.json)
- [71_下一阶段突破建议.md](71_下一阶段突破建议.md)

[原始URL/哈希/源码位置](lineage71/SOURCE_CATALOG.md)；[22行字段血缘](lineage71/FIELD_LINEAGE.csv)；[代码原包哈希及六层状态](lineage71/CODE_EVIDENCE.json)；[申请人待补信息](lineage71/application/APPLICANT_INFORMATION.md)；[完整性核验](lineage71/VALIDATION.json)。公开SDK/文档止于伙伴配置、opaque token及服务端接口；实收、训练列和ROAS不升级。保留00—70历史文件及原图对象。


## L72：真实游戏数据访问与预测验证准入（2026-11-20）

停止旧SDK扫描。新增公开MMP契约：SDK/API混合替换与报表修订、去重选项适用范围、日级UA signals/实时postbacks、all-source省略其他来源归因、Unity明确接收映射；不是实际配置/接收或训练列。Age新增机构公开业务路由，非数据许可。Uken主体/保管人未明，申请未发送。严格目标“新获准数据或授权生产血缘”未达成；A/B/C实验STOP，无训练/效果数字。

- [72_真实游戏数据获取进展.md](72_真实游戏数据获取进展.md)
- [72_Axon_Vector训练血缘突破.md](72_Axon_Vector训练血缘突破.md)
- [72_跨游戏迁移实验设计.md](72_跨游戏迁移实验设计.md)
- [72_普通游戏盈利改善因果矩阵.csv](72_普通游戏盈利改善因果矩阵.csv)
- [72_公开逆向停止清单.md](72_公开逆向停止清单.md)
- [72_下一阶段行动计划.md](72_下一阶段行动计划.md)

[原件URL/日期/哈希/摘录](access72/SOURCE_CATALOG.md)；[准入矩阵](access72/EXPERIMENT_ADMISSION.json)；[本轮关系图](access72/RELATION_GRAPH.json)；[访问路由](access72/ACCESS_ROUTES.json)；[搜索与操作边界](access72/SEARCH_BOUNDARY.json)；[完整性核验](access72/VALIDATION.json)。历史00—71文件与原图对象保留。


## 72身份专题与73独立实验（2026-11-20）

本节为新增专题，保留此前access72及00—71历史文件。E1读取、E2构造、E3官方接收/用途、E4服务关联契约；E5生产匹配/E6匹配结果入预测均未取得。

TalkingData/Criteo STOP；BPID和独立价值实验均为合成。42行B＋360行D＋2行STOP，共404行；不证明真实LTV、ROAS、个人跨App图谱或两家相对优势。

| 交付 | 内容 |
|---|---|
| [72_AppLovin身份图谱逆向.md](72_AppLovin身份图谱逆向.md) | 边界、方法和最终判断 |
| [72_Unity身份图谱逆向.md](72_Unity身份图谱逆向.md) | 边界、方法和最终判断 |
| [72_下一阶段突破建议.md](72_下一阶段突破建议.md) | 边界、方法和最终判断 |
| [72_第三方SDK身份关联能力矩阵.md](72_第三方SDK身份关联能力矩阵.md) | 边界、方法和最终判断 |
| [72_设备标识与身份标识完整清单.md](72_设备标识与身份标识完整清单.md) | 边界、方法和最终判断 |
| [72_证据等级与反证清单.md](72_证据等级与反证清单.md) | 边界、方法和最终判断 |
| [72_跨应用身份关联证据图.json](72_跨应用身份关联证据图.json) | 机器可读证据/结果 |
| [72_身份图谱到价值预测的数据血缘.md](72_身份图谱到价值预测的数据血缘.md) | 边界、方法和最终判断 |
| [72_非游戏身份数据入口分析.md](72_非游戏身份数据入口分析.md) | 边界、方法和最终判断 |
| [73_BPID身份匹配算法实验.md](73_BPID身份匹配算法实验.md) | 边界、方法和最终判断 |
| [73_Criteo广告价值预测实验.md](73_Criteo广告价值预测实验.md) | 边界、方法和最终判断 |
| [73_下一阶段研究建议.md](73_下一阶段研究建议.md) | 边界、方法和最终判断 |
| [73_实验结果汇总.csv](73_实验结果汇总.csv) | 机器可读证据/结果 |
| [73_数据许可及质量审计.md](73_数据许可及质量审计.md) | 边界、方法和最终判断 |
| [73_设备应用关系图实验.md](73_设备应用关系图实验.md) | 边界、方法和最终判断 |
| [73_身份关联增益与错误率实验.md](73_身份关联增益与错误率实验.md) | 边界、方法和最终判断 |

来源：[SOURCE_CATALOG](identity72-experiments73/SOURCE_CATALOG.md)；复现：[README](identity72-experiments73/README.md)；完整性：[VALIDATION](identity72-experiments73/VALIDATION.json)。

主图仅追加32节点、43边、65来源；原211节点/250边/525来源和所有旧元数据保留。72自包含图标明未知边，合成实验不使用E5/E6。

下一步优先授权真实游戏cohort和匿名化身份/标签/模型血缘；停止同版本重复扫描和受限来源镜像。未经指示未发送申请、签约或发布。


## 74号：身份图谱是否驱动买量优势（2026-11-20）

结论：第三方解析/命名空间/失败契约有新增补证；Unity账号/Exchange合作与AppLovin跨App用途和C_id类别披露有证。特定解析结果入Axon/Vector的C_graph和独立增益D仍UNKNOWN。没有新训练或真实收益。

| 交付 | 内容 |
|---|---|
| [74_图谱与群体学习对照实验设计.md](74_图谱与群体学习对照实验设计.md) | 本轮结论、方法或停止条件 |
| [74_研究边界与停止条件.md](74_研究边界与停止条件.md) | 本轮结论、方法或停止条件 |
| [74_身份关联商业价值证据矩阵.csv](74_身份关联商业价值证据矩阵.csv) | 18项A/B/C_id/C_graph/D证据矩阵 |
| [74_身份图谱生产证据.md](74_身份图谱生产证据.md) | 本轮结论、方法或停止条件 |
| [74_身份特征进入价值模型的证据.md](74_身份特征进入价值模型的证据.md) | 本轮结论、方法或停止条件 |

[一手来源及SHA256](identity-value74/SOURCE_CATALOG.md)；[覆盖与失败](identity-value74/SEARCH_COVERAGE.json)；[补充勘误](identity-value74/CORRECTIONS.md)；[准入STOP](identity-value74/EXPERIMENT_READINESS.json)；[验证](identity-value74/VALIDATION.json)。

仅追加16节点/19边/17来源，原243/293/590对象及旧元数据保留。00—73共129份编号文件保持原字节。未重扫SDK、重试数据下载、采集身份或调用生产匹配/广告服务。


## 75号：身份图谱黑盒验证与可识别性（2026-11-20）

先完成设计与可行性审计，无真实投放、身份查询、外部请求、旧SDK扫描或真人数据。H0/H3按训练来源与在线依赖两轴定义；广告响应不能直接恢复个人图谱或价值优势。

| 交付 | 范围 |
|---|---|
| [75_下一步最小可执行方案.md](75_下一步最小可执行方案.md) | 研究设计、边界或本地合成结果 |
| [75_合成实验设计验证.md](75_合成实验设计验证.md) | 研究设计、边界或本地合成结果 |
| [75_同设备跨App关联实验.md](75_同设备跨App关联实验.md) | 研究设计、边界或本地合成结果 |
| [75_实验授权与数据边界.md](75_实验授权与数据边界.md) | 研究设计、边界或本地合成结果 |
| [75_混杂因素与反证实验.md](75_混杂因素与反证实验.md) | 研究设计、边界或本地合成结果 |
| [75_跨设备同人关联实验.md](75_跨设备同人关联实验.md) | 研究设计、边界或本地合成结果 |
| [75_身份图谱黑盒实验总设计.md](75_身份图谱黑盒实验总设计.md) | 研究设计、边界或本地合成结果 |
| [75_黑盒可识别性矩阵.csv](75_黑盒可识别性矩阵.csv) | 56行条件可识别性 |

[本地来源/复现](blackbox75/README.md)；[冻结协议](blackbox75/PREREGISTRATION.md)；[5700重复结果](blackbox75/results/REPLICATE_RESULTS.csv)；[19场景摘要](blackbox75/results/DESIGN_SUMMARY.csv)；[当前准入](blackbox75/EXPERIMENT_READINESS.json)；[VALIDATION](blackbox75/VALIDATION.json)。

合成给出三组不同内部机制、逐行相同外部输出的反例；统计响应显著也可能来自库存/频控/目标上下文。未新增Axon/Vector实际入模或独立收益证据。下一步先做自有本地mock可观测性先导，平台固定回放需L2明确授权。

主图仅追加18节点/21边/16来源；旧259/312/607对象和元数据保留，00—74共134份编号文件保持原字节。
