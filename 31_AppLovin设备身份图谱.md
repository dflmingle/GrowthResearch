# AppLovin 设备标识、网站身份与 Axon 关联链

2026-11-19。范围：公开发行 SDK、既有游戏静态证据、公开 Pixel 与官方文档；未运行 SDK、访问设备、提交事件或读取真实标识。

## 结论与证明边界

**【SDK代码证实】【官方公开证实】AppLovin 已有跨属性广告识别与转化匹配体系，不能再表述为“只有一个广告 ID、完全没有跨场景证据”。** Android SDK 可以把广告 ID、App Set ID、发布者 ID 和上下文放入同一逻辑请求；网站 Pixel/CAPI 可以把访客标识、广告点击标记、商家客户 ID、规范化联系方式及订单价值放进转化链。隐私政策明确披露跨应用、设备、网站信息的收集与结合，Axon 官方说明这些类别中的授权数据用于广告预测。[IG01](EVIDENCE_INDEX.md#ig01) [IG03](EVIDENCE_INDEX.md#ig03) [IG04](EVIDENCE_INDEX.md#ig04) [IG05](EVIDENCE_INDEX.md#ig05)

**【无法确认】没有恢复一张把全部 GAID、IDFA、IDFV、浏览器和账户统一到自然人的服务端图；也没有目标游戏的跨设备匹配结果或由该匹配产生的投放日志。** “客户端能共封装”“官方披露会结合”“某用户已被匹配”“匹配用于某游戏获客”“电商数据训练游戏模型”是五种不同结论。

## 1. Android：字段名不等于平台标识类型

主要原始实现为官方 MAX **13.6.4**，不是全部目标游戏实装版本。反编译定位与原文件哈希见 [IDENTITY_CODE_EXCERPTS.json](identity-graph/IDENTITY_CODE_EXCERPTS.json)；与游戏内版本、实际调用的连接复用 [21号报告](21_MAX用户ID与身份数据流.md)及其 XD05–XD07 证据。

| 标识/上下文 | 原始代码及接口 | 条件、去向与可证明的关联范围 |
|---|---|---|
| GAID / Amazon广告ID | `com.applovin.impl.v.collectGoogleAdvertisingInfo`，`v.java:98–120` 调 `AdvertisingIdClient.getAdvertisingIdInfo`；FireOS分支`:125–143` | 【SDK代码证实】读取ID及限制跟踪状态；异常走空/回退。`sdk.m.a(Map,boolean)`，`m.java:1343–1349`写 **`idfa`**、`dnt/dnt_code`。Android这里的`idfa`不是苹果IDFA |
| App Set ID | `i1.a(Context)`→`AppSet.getClient().getAppSetIdInfo()`→`i1$a.a`→`m.a(new m$b(id,scope))` | 【SDK代码证实】类存在、调用成功才有结果；`m.java:1350–1353`在配置`c5.J3`允许且结果非空时写 **`idfv/idfv_scope`**。Android这里不是苹果IDFV |
| 发布者用户ID | `AppLovinSdkSettings.setUserIdentifier`→core→`t7.a(String)`；`t7.java:78–83` | 【SDK代码证实】`pui`控制持久化，`qq3`控制`m.H()`中的`cuid`；不是自动哈希邮箱或全球账户命名空间 |
| SDK随机token | `t7.a(e5)`，`:58–65`及`m.H()` | 【SDK代码证实】独立随机生成/持久化；`applovin_random_token/compass_random_token/art`等受各自配置控制。不能据变量名认定跨App稳定 |
| 可选客户资料 | `AppLovinSdk.setUserData`、`AppLovinUserData`→`r7.a` | 【SDK代码证实】与`setUserIdentifier/cuid`独立；非空对象、`send_user_data`等条件满足才可进入广告请求/事件`user_data`。目标游戏的业务设置未证实 |
| IP、设备/网络环境 | 官方政策列IP、设备、操作系统、网络及广告交互；SDK collector有对应环境信息 | 【官方公开证实】接收端能观测连接IP并按产品规则处理；本轮不把某个IP JSON字段、IP→GAID的join或设备指纹评分算法写成已逆向完成 |

`idfa`、`idfv`的跨平台命名是本轮直接沿返回值确认的结果，不能依据名称推断“Android拿到iOS ID”或“一个App Set ID跨所有开发商”。[IG01](EVIDENCE_INDEX.md#ig01)

【官方公开证实】Google App Set ID 在同设备、同Play开发者范围可相同；非Play等条件可退为App范围；最后一个同集合App卸载、长时间不访问、恢复出厂等可重置。苹果IDFV是同设备同vendor范围，换设备/不同vendor不相同。IDFA/GAID受平台授权、删除/重置及政策限制。苹果明确：IDFV不能与其他信息结合去跟踪其他公司的App/网站；不能把这些标识当作绕过ATT的替代品。[IG06](EVIDENCE_INDEX.md#ig06)

## 2. 哪些是确定性，哪些只是可能的概率匹配

| 链接 | 判断 | 仍缺什么 |
|---|---|---|
| 同一有效GAID在授权的不同App请求中出现 | 【合理推断】可按相同设备级标识做确定性相等关联 | 服务端实际join、保存周期、重置处理、同意过滤；不证明同一自然人或跨设备 |
| App Set ID / 苹果IDFV在其合法scope内相同 | 【官方公开证实】具有限定范围关联能力 | 不证明被用于跨发行商广告图谱；SDK封装不决定允许用途 |
| 同一商家的稳定`user_id`跨浏览器/设备回传 | 【官方公开证实】CAPI有客户ID输入；【合理推断】统一命名空间下可作确定性账户连接 | 该商家实际使用、命名空间及服务器匹配结果 |
| 规范化邮箱/电话的无盐SHA-256 | 【SDK代码证实】可形成可比对的键；【合理推断】相同规范化输入可做确定性键相等匹配 | 哈希相等不等于已验证本人；共享联系方式、格式差异、账号转让均会影响身份语义 |
| IP+UA+机型+时间/广告互动 | 【合理推断】可作上下文/概率估计输入 | 没有恢复概率公式、置信阈值、household规则或特定跨设备边；**IP相同不是确定性同人** |
| MMP的probabilistic attribution | 【官方公开证实】相关Adjust/AppLovin文档支持归因窗口；见既有AX证据 | 概率归因一次安装不等于持久跨设备身份图谱 |

这里的“确定性”指键或已验证登录凭据的连接方式，不保证标识对应一个唯一人；本轮没有对真实用户进行匹配测试。

## 3. Pixel 身份链：逐个标识与调用条件

原文 [pixel-source.raw](nongame/pixel-source.raw)，快照内版本`a/1.5.46`，SHA256 `3ffaa7d19ed8af5dde44adc80a89e362348662453f50880c50688d021dcb49ce`。以下位置为原文**0起始字符偏移**，不是反混淆稿偏移；[PIXEL_IDENTITY_EXCERPTS.json](identity-graph/PIXEL_IDENTITY_EXCERPTS.json)保留原文与有界注释。[IG03](EVIDENCE_INDEX.md#ig03)

| 环节 | 原始位置/方法/字段 | 条件与接收方 | 证据等级 |
|---|---|---|---|
| 访客标识 | 常量区`11660`；`Ae`在`17350`校验UUID；初始化区约`28300` | 从`axwrt`/`_axwrt` cookie、有效本地备份取值，缺失才生成；cookie域探测与有效期检查。不是跨域cookie自动共享 | 【公开网页代码证实】 |
| 持久化 | `Ie`在`14753`写`document.cookie`，`E/Ee/Pe`跟踪来源；`_axwrt_backup/_axwrt_ts` | 域scope及cookie可用时写入；存在localStorage/恢复路径；一年参数不保证浏览器实际保留一年 | 【公开网页代码证实】 |
| 点击/归因标记 | 初始化约`29500`；`g.eventId=Ee("event_id", URL.aleid或axeid, "_axeid")`；`g.art=Ee("art",alart或axart,"_axart")` | URL优先，随后cookie/存储；标记进入后续事件；`aleid`是广告归因标记，不是自然人ID，也不是`dedupe_id` | 【公开网页代码证实】【官方公开证实】 |
| 会话 | `let Qe=_e(K)`在`29847`，`K="_axsid"`；`g.sid` | sessionStorage缺失时生成并触发该分支；会话ID不等于跨设备ID | 【公开网页代码证实】 |
| Cookie matching | 同`29847`；`Image.src=https://cm.g.doubleclick.net/pixel?google_nid=aplv&google_cm&cek=...` | 初建上述会话标记时执行/等待load；接收方Google cookie matching接口；不是邮箱或Google账号的读取接口 | 【公开网页代码证实】 |
| 手动客户资料 | `Oe`在`18091`；`user_data.email/phone/user_id` | 业务传入后规范化；SHA-256处理邮箱/电话、保留可接受的预哈希值；`user_id`作为提供的客户键 | 【公开网页代码证实】 |
| 自动邮箱采集 | `Me`在`20870`；配置处理`32677`；`autoEmailCapture`、`_emailCaptureSetup`、`submitEmail`等 | **远程配置精确为true**才启用相关监听；监听候选表单/dataLayer，hash后可并入事件。没有商家线上配置/同意状态证据 | 【公开网页代码证实】 |
| 事件合包 | `We`在`23625`；`axon.wrt/sid/eventId/art/visitInfo`，`userData` | 收入等业务数据可和标识共封装；`visitInfo`含首次/最近访问、次数/当前访问起点；是网站访问记录而非跨站图谱查询结果 | 【公开网页代码证实】 |
| 发送能力 | 原文约`11200`的发送闭包；`sendBeacon`、条件`fetch`回退 | 目标`https://b.applovin.com/v1/pixel`；未执行，**没有生产请求送达/匹配成功证明** | 【公开网页代码证实】 |

【官方公开证实】Google Cookie Matching文档描述广告买方标识与Google cookie的映射机制。与Pixel该分支结合，能证明**浏览器广告标识互操作的客户端入口**；不能证明Google账户、跨设备邮箱、广告主完整客户档案已共享。[IG06](EVIDENCE_INDEX.md#ig06)

## 4. CAPI、哈希及价值数据如何连接

【官方公开证实】[CAPI](https://support.applovin.com/en/growth/promoting-your-websites/api/conversion-api)的`POST https://b.applovin.com/v1/event`由商家授权API key调用，包含`pixel_id/events[]`。事件级有`event_time/event_source_url/data/user_data`，可含`dedupe_id`。身份输入有`client_id/axwrt/alart/user_id/email/phone`等至少一个及存在时要求传的点击参数；可选`ifa/idfv`，不是要求网站强行获得移动广告ID。用户IP/UA必须为真实事件环境，不能填服务器IP或测试身份。[IG04](EVIDENCE_INDEX.md#ig04)

【SDK代码证实】MAX13.6.4 `r7`与独立Axon1.3.4 `l3.a(AxonUserData)`均具备邮箱小写/trim、Gmail类本地部分规范化、`email/email_v2/email_domain`及电话处理；独立Axon还可输出`drop_phone_hashed`。不同组件不能假设完全同版：MAX13.6.4的本轮`r7`实现没有同样的last10字段。哈希是可匹配的伪名化键，不是匿名化。[IG01](EVIDENCE_INDEX.md#ig01) [IG02](EVIDENCE_INDEX.md#ig02)

【官方公开证实】订单历史指南明确要求规范化无盐SHA-256，盐化/重复哈希不能匹配；明确用途是建模已有客户并寻找新的高价值用户。`purchase.value/currency/transaction_id`提供业务价值标签，`dedupe_id`去重同一动作，`transaction_id`去重订单；都不承担通用用户身份。**这是“身份/客户数据+价值→获客建模”最直接的产品用途证据，仍不是某笔订单实际匹配结果。**[IG04](EVIDENCE_INDEX.md#ig04)

## 5. 目标游戏实际到了哪一层

| 游戏 | 已证业务连接 | 不能升级成的结论 |
|---|---|---|
| Car Race | 【实际游戏代码证实】Zego本地GUID→Metica初始化ID及其fallback→MAX`setUserIdentifier`；ARM `ZegoUserUID.get_Value` RVA`0x32F5EC4`，`AdMeticaDefault.get_NextUserId` `0x32D967C`，Java`ApplovinInitializer.initializeSdkInternal` | 本地GUID不是跨设备账户；未证邮箱`user_data`或Axon账户匹配 |
| Meowdoku | 【实际游戏代码证实】`AdInitParameter$Builder.build`取`AnalyzeManager.getUUID`→`AdUuid.setUuid`→`MaxInitHelper$MaxInit.userJourney`→MAX；AF CUID同源UUID | 证明单应用框架联结，不证明同发行商所有App统一账号 |
| Rotate Rings | 【实际游戏代码证实】`w6.e.i`取`GlDataManager$thinking.distinctId`→MAX用户ID | ThinkingData/MAX串联不是跨App图谱 |
| Jewel Coloring | 已证AdWorth/GTUser等其他路径；【无法确认】本轮沿用全DEX审计结果，未建立业务调用MAX用户ID/客户资料的证据 | 不代表MAX没有设备标识，也不代表服务器没有其他匹配 |
| Amaze GO! | 【无法确认】无可验证包体 | 不补造链路 |

原始调用方及实装SDK版本见 [XD06](EVIDENCE_INDEX.md#xd06)、[I03](EVIDENCE_INDEX.md#i03)、[I06](EVIDENCE_INDEX.md#i06)及[21号报告](21_MAX用户ID与身份数据流.md)。这些是业务调用静态证据，不是发送成功或生产归因记录。

## 6. 是否有证据用于 Axon

**【官方公开证实】有产品层用途证据。** AppLovin隐私政策`127/135`附近披露跨App/设备数据结合、App/网站行为结合用于相关广告；[Axon AI说明](https://legal.applovin.com/about-applovins-axon-ai/)写明用设备/网络、应用/广告/其他数字属性互动和广告主自愿共享数据训练及优化，预测展示对特定广告主的价值；订单历史页面直接说明寻找高价值新客户。[IG05](EVIDENCE_INDEX.md#ig05)

**【无法确认】没有逐字段证明`_axwrt→GAID→email`的生产连接、连接置信度、Axon具体训练特征，也没有这些游戏的投放及匹配日志。** 不能断言所有电商客户数据默认训练所有游戏IAA模型。官方还排除敏感/受保护类别、儿童数据及其他竞价者的用户/出价信息，不能以MAX掌握竞价为由扩大数据范围。

本轮因`How AppLovin Shows You Ads`公开GET返回403而未取得该页；已记录失败，不绕过。结论仅依据可取得的隐私政策、Axon说明、接口及源码。
