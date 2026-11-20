# Unity 账号身份、广告组件标识与 RampID

2026-11-19。**【官方公开证实】【SDK代码证实】Unity有可验证的跨设备/跨游戏账号体系，也正式支持借助LiveRamp身份能力在Exchange激活受众；尚不能证明两者已经合成供Vector使用的统一身份图谱。**

## 1. 三套身份体系分别有何证据

| 体系 | 直接证据 | 可确认范围 | 不可越级的边界 |
|---|---|---|---|
| Unity Player Accounts / Authentication | 官方Authentication3.9.0源包、OAuth调用、链接API及产品文档 | 用户登录后跨设备/平台；组织级玩家池及跨游戏标识；项目上下文内的玩家与外部身份映射 | 账号不等于设备；不能把所有项目的PlayerId设为同值；没有默认进入Ads/Vector的证明 |
| Unity Ads / LevelPlay组件标识 | Unity Ads4.17.0官方sources.jar与4.18.1发行包 | 安装ID、广告ID、App Set ID、可选LevelPlay AUID、Analytics ID与外部用户ID进入各自请求结构 | 其中AUID不是Player Accounts ID；analyticsUserId不是已证明的UGS PlayerId |
| LiveRamp RampID / Unity Exchange | Unity2026-04-02官方公告、LiveRamp产品说明 | 美加Exchange库存、接收伙伴支持下激活RampID受众，面向品牌/代理商 | 不是Unity自研LiveRamp图谱；未证某目标游戏/每个请求携带RampID，未证Vector消费RampID |

证据：[IG07](EVIDENCE_INDEX.md#ig07) [IG08](EVIDENCE_INDEX.md#ig08) [IG09](EVIDENCE_INDEX.md#ig09) [IG10](EVIDENCE_INDEX.md#ig10)。

## 2. 原始源码：从登录到项目玩家

官方UPM包：[provenance](identity-graph/sdk/authentication/3.9.0/provenance.json)，`com.unity.services.authentication-3.9.0.tgz` SHA256 `bf9efe33dc39a09756ee3defd0d621366a05a926793104a10c5d49c9582d4dde`；与registry SHA1匹配。包含Player Accounts源码；按包内Unity条款使用，不将可读源码误称开源许可证。**这是独立公开SDK，不是五款游戏已安装该版本的证明。**

以下位置相对 `identity-graph/sdk/authentication/3.9.0/extracted/package/`；原段和行号集中保存在 [IDENTITY_CODE_EXCERPTS](identity-graph/IDENTITY_CODE_EXCERPTS.json)。

| 技术链 | 原始类/方法/位置 | 字段、调用条件、接收方 | 等级 |
|---|---|---|---|
| 发起用户登录 | `Player Accounts/Runtime/PlayerAccountServiceInternal.cs:63`，`StartSignInAsync` | 必须配置ClientId，处于允许状态；调用系统浏览器。不是后台静默扫描设备账号 | 【SDK代码证实】 |
| OAuth授权请求 | 同文件`:154–185`，`BuildAuthorizationRequestUrl` | `https://player-login.unity.com/v1/oauth2/auth`；`client_id/redirect_uri/state/code_challenge`，S256 PKCE，可选scope | 【SDK代码证实】 |
| 回调与换token | 同文件`:229–273` | 校验state、code_verifier及状态；授权码只消费一次；`POST .../v1/oauth2/token`，`grant_type=authorization_code` | 【SDK代码证实】 |
| 账号声明 | `Player Accounts/Runtime/Models/IdToken.cs` | `sub/aud/iss/email/email_verified/is_private_email`等；本轮只读模型，没有解码任何真实token | 【SDK代码证实】 |
| 进入UGS项目 | `Runtime/AuthenticationServiceInternal.External.cs:334`附近，`SignInWithUnityAsync` | 将UPA access token作为`IdProvider=Unity`的外部凭据；发往Authentication服务；请求`ProjectId`头，见`AuthenticationNetworkClient.cs:123–127` | 【SDK代码证实】 |
| 项目玩家标识 | `Runtime/AuthenticationServiceInternal.cs:445–447`；`Runtime/Models/Security/AccessToken.cs` | UGS `PlayerIdComponent.PlayerId=accessTokenDecoded.Subject`；UGS token有`project_id/sub`。UPA token与UGS token不同，不可按同为`sub`断言值相同 | 【SDK代码证实】 |
| 外部账户绑定 | `AuthenticationServiceInternal.External.cs`的`LinkWithGoogleAsync/LinkWithUnityAsync/LinkWithExternalTokenAsync` | 玩家先授权登录UGS；传外部token；后者用`IsAuthorized`分支发链接请求，返回`ExternalIds`更新本地模型 | 【SDK代码证实】 |
| 取外部ID | `Runtime/Models/PlayerInfo.cs:206–234`的`GetUnityId/GetIdentityId`；`Identity.cs` | 按`ProviderId/ExternalId`读映射，**不是再读设备ID**；未链接则可为空 | 【SDK代码证实】 |
| 跨设备授权 | 官方Code Link及外部登录文档 | 用户以有效账户/授权码恢复同一玩家；第三方Google/Apple/自定义OIDC等提供受验证凭据 | 【官方公开证实】 |

【官方公开证实】[Unity Player Accounts](https://docs.unity.com/en-us/authentication/unity-player-accounts)明确写“organization-level player pool”“cross-game, cross-device”“organization-level player identifiers”。可以确认组织内账号互通产品能力；没有据此发明一个SDK字段叫`OrganizationPlayerId`，也没有宣称跨所有发行商项目共享同一个可见ID。[IG08](EVIDENCE_INDEX.md#ig08)

【官方公开证实】[身份管理](identity-graph/unity-identity-management.txt)说明一个玩家可链接多种外部身份，冲突需处理；强制链接可能使原账户不可恢复。匿名登录本身不提供可靠跨设备恢复，必须有外部身份、合法登录或其他恢复机制。**本研究没有实际登录、链接或强制迁移任何账号。**

## 3. 账号数据不能因同属Unity就直接送入广告模型

新增取得的产品专用隐私说明比总政策更具体：[Authentication隐私说明](identity-graph/unity-auth-privacy-overview.txt)与[Player Accounts隐私说明](identity-graph/unity-upa-privacy-overview.txt)。[IG08](EVIDENCE_INDEX.md#ig08)

- 【官方公开证实】Authentication默认生成UAS ID；外部身份/用户名等为可选；GDPR关系为开发者Controller、Unity Processor。
- 【官方公开证实】Player Accounts默认收集账号邮箱并生成UPA ID；Unity与开发者为独立Controller；用户选择创建/使用账号，不等于所有下游广告用途均获授权。文档明示跨多个应用，并分别处理账号删除与集成App数据删除。
- 【无法确认】没有找到UPA ID/邮箱→RampID或UPA→Vector的直接业务调用、服务端join文档、目标游戏启用记录。总隐私政策允许的广泛处理范围不能替代产品用途/授权证据，也不能反过来证明绝对隔离。

## 4. Unity Ads身份封装：比“只看GAID”更具体

【SDK代码证实】官方 [Unity Ads4.17.0 sources.jar来源](ThirdPartySDKs/Unity/Ads/4.17.0/provenance.json)中的以下代码提供了组件间的真实读取边界；源码相对 `ThirdPartySDKs/Unity/Ads/4.17.0/sources/com/unity3d/ads/core/`。[IG07](EVIDENCE_INDEX.md#ig07)

| 标识与逻辑字段 | 原始位置 | 条件与可确认结果 |
|---|---|---|
| `idfi` | `data/datasource/AndroidStaticDeviceInfoDataSource.kt:221–229` | Preferences缺失时生成安装UUID并保存；不是同一用户全部设备共用ID |
| `analyticsUserId` | `AndroidAnalyticsDataSource.kt:6–8`→`AndroidStaticDeviceInfoDataSource.kt:232–233` | 读取`<AppName>.v2.playerprefs`中的`unity.cloud_userid`，非空才进入初始化payload；本轮未证它等于Authentication PlayerId |
| `auid/auidString` | `AndroidStaticDeviceInfoDataSource.kt:239–245`→`AndroidDeviceInfoRepository.kt`→`domain/AndroidGetInitializationRequestPayload.kt:51`附近 | 源码注明AUID由LevelPlay提供；分别检查合法UUID转换和非空字符串，放入初始化请求；不是UPA/OIDC的subject |
| `externalUserIdentifier` | `AndroidGetInitializationRequestPayload.kt`末尾 | `UnityAds.userIdentifier`非空才写；SDK支持业务设置不等于目标App实际传账号 |
| 广告ID/App Set ID | `AndroidPrivacyDeviceInfoDataSource.kt:22–48` | `allowed.idfa`、`allowed.appsetId`分别控制PII字段；广告ID读取Google/Amazon，名称也不能解释为Android取得苹果IDFA |
| 会话/授权状态 | `domain/AndroidGetUniversalRequestSharedData.kt` | `sessionToken`或limited token、timestamps、developerConsent及`piiData`组成共享请求信息；不把会话token当自然人ID |

【SDK代码证实】4.18.1 `com.unity3d.services.core.device.reader.DeviceInfoReaderWithPrivacy.getDeviceInfoData`也有`allowedToSendPii()`及`shouldSendNonBehavioral()`条件；这证明SDK有隐私分支，**不是对所有调用路径/全部生产配置的合规认证**。

这些是SDK组件关联的正证据；既不能全部写成“完全没有身份关系”，也不能写成“已经证明Unity Ads把所有游戏账号送给Vector”。

## 5. RampID：正式受众激活能力，尚未恢复具体映射入口

**【官方公开证实】Unity2026-04-02公告** [RampID is Now Available Across Unity Exchange](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)，[本地原文](vector/exchange-rampid.txt)，明确：

1. RampID已在**美国及加拿大**Unity Exchange可用。
2. 品牌、代理商可以把已有身份受众策略延伸到Unity移动库存；接收伙伴与Unity双方都要支持。
3. 对外的256M美国月活设备是**可激活库存范围的官方口径**，不是每个设备均成功有RampID的统计，更不是匹配率或ROAS实验。

【官方公开证实】[LiveRamp RampID产品页](https://liveramp.com/our-platform/rampid)与[Identity Resolution](https://liveramp.com/our-platform/identity-resolution/)说明通过受许可的认证标识进行跨发布者/平台/浏览器/App/CTV连接、翻译和受众激活。这确认**第三方商业身份图谱产品能力**；不能把LiveRamp整体的匹配率宣传写成Unity数据的匹配率。[IG09](EVIDENCE_INDEX.md#ig09)

【无法确认】本轮没有取得Unity专用的“输入GAID/邮箱→LiveRamp映射→返回RampID”服务器接口、加密/伙伴命名空间、确定/推测身份节点类型或每个请求的映射成功记录。未证明Unity从玩家账号邮箱产生RampID，也未证明所有RampID都依赖邮箱。

## 6. 竞价身份字段：公开到哪一步

原始协议：[Unity Bid requests](identity-graph/unity-exchange-identity.txt)、[Data privacy](identity-graph/unity-exchange-privacy.txt)。[IG10](EVIDENCE_INDEX.md#ig10)

| 对象/字段 | 已知语义、调用条件与接收方 |
|---|---|
| `device.ifa` | 【官方公开证实】可用且隐私允许时的广告标识；不是PlayerId/RampID别名 |
| `device.ip/ua/geo`及设备属性 | 【官方公开证实】向参与竞价的接收伙伴传递相应环境字段；非所有字段在所有请求可用；不可由经纬度示例反推无条件采集精确定位 |
| `app.id/bundle/publisher.id` | 【官方公开证实】应用/发布者上下文；不能误当玩家账户 |
| `user.ext.consent` | 【官方公开证实】本页说明0时设备ID置零、IP遮罩，1表示同意；另有`regs.coppa/ext.gdpr/ext.us_privacy/ext.lgpd`等。lgpd opt-out分支说明去除IDFA/AAID/IP |
| RampID具体字段 | **【无法确认】上述取得版本没有`RampID/liveramp/eids`定义。不能声称已在`user.ext.eids[].uids[].id`发现Unity生产RampID。** |

【官方公开证实】IAB当前OpenRTB2.6标准提供`user.eids[]`和`source/uids[].id/atype`等扩展标识结构；历史扩展也常见`user.ext.eids`。本轮取得的[标准原文](identity-graph/iab-openrtb-26.raw)只能证明标准能力，**不能补成Unity具体partner wire format或给出虚构payload**。

接收方边界同样重要：Exchange→支持RampID的DSP受众激活，不等于Unity Ads自营获客模型或Vector必然接收/训练相同ID。伙伴名单没有单笔交易、匹配或跨业务训练的证明力。

## 7. 对目标游戏与买量优化的最终判断

**【无法确认】Car Race、Meowdoku、Rotate Rings、Jewel Coloring没有本轮可证的UPA→广告图谱、RampID启用或Vector实际获客记录；Amaze GO!无包体。** 游戏已证的行为/广告收入回传可支持各平台优化，前提是对应MMP授权及后台启用，详见既有16/19/24号报告；不要由Unity引擎、Ads适配器或Exchange产品能力倒推具体游戏已投放。

Unity的**账号关联能力**、**广告SDK标识桥接能力**与**基于LiveRamp的跨渠道受众买量能力**均有正证据；它们之间的服务端图谱合并及Vector训练连接仍未证实。
