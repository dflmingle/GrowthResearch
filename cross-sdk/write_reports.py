from pathlib import Path
import json,csv,hashlib
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cross-sdk'
ss=json.loads((R/'CODE_EVIDENCE.json').read_text(encoding='utf-8'));S={x['id']:x for x in ss}
matrix=json.loads((R/'SDK_MATRIX.json').read_text(encoding='utf-8'))
g=json.loads((ROOT/'prediction-system/EVIDENCE_GRAPH.json').read_text(encoding='utf-8'))
def ref(*ids):return '；'.join(f'[{i}]({S[i]["path"]}):L{S[i]["start_line"]}' for i in ids)
def write(name,t):(ROOT/name).write_text(t.strip()+'\n',encoding='utf-8')

catalog='# 静态代码证据目录\n\n所有SDK均未初始化；源码、反编译视图和目标游戏调用分别标记。包哈希与文件哈希分开保存。\n\n'
for s in ss:
 catalog+=f'## {s["id"]} · {s["sdk"]} {s["version"]}\n\n'
 catalog+=f'- 原文：[{s["path"]}](../{s["path"]}):L{s["start_line"]}—{s["end_line"]}；方法：`{s["class_or_method"]}`。\n'
 catalog+=f'- 文件SHA256：`{s["sha256"]}`。\n'
 a=s['official_package']
 catalog+=f'- 独立SDK包：[{a["path"]}](../{a["path"]})；SHA256：`{a["sha256"]}`；来源：{a.get("url")}。\n'
 catalog+=f'- 结论范围：{s["meaning"]}。目标游戏业务调用：{s["game_business_callsite"]}；生产发送/接收/训练：均未证实。\n\n'
(R/'CODE_CATALOG.md').write_text(catalog,encoding='utf-8')

t=f'''# SDK生态与版本矩阵

2026-11-19。本轮优先补齐客户端连接：新增官方Unity IAP 5.4.0/5.5.1、UGS Analytics 6.3.0、Singular 12.17.0；其余复用并验哈希。未重复下载已取得的相同SDK发行包。

完整[版本/原包SHA256/来源/时间/状态矩阵](cross-sdk/SDK_MATRIX.json)包含49项选定SDK版本记录；不是49项全部完成深度逆向。每条代码证据在[CODE_CATALOG](cross-sdk/CODE_CATALOG.md)关联准确原包及文件哈希。

## 分析投入与版本含义

| SDK | 本轮范围 | 结论上限 |
|---|---|---|
| MAX 13.2.0/13.6.2/13.6.3/13.6.4/13.7.0 | 复用旧版本证据；新反编译13.7 EventService/队列，javap公共API差分 | 四款游戏匹配前四版；13.7只是独立参照 |
| 独立Axon 1.3.4 | 复用已有AAR和身份/API分析 | 未证明四款游戏集成独立Axon SDK |
| Unity Ads 4.17.0/4.18.1及MAX Unity适配器 | 复用发行包；反编译两版adapter，核实token和同意转换 | 中介调用链，不是Vector获客已启用 |
| LevelPlay 9.3.0/9.4.0/9.5.0 | 复用既有请求/状态分析 | 未重新完整逆向；不把AUID当UPA PlayerId |
| Adjust 5.5.0/5.7.0/5.8.1 | 复用源码；新增远程触发/标识限制/API差分 | Car5.5/Jewel5.7匹配；5.8.1独立参照 |
| AppsFlyer 6.14.2/6.17.5 | 复用收入包/缓存证据；核对Rotate原版赋值 | 不证明MMP→网络后台postback启用 |
| Singular 12.17.0 | 官方vendor Maven AAR/POM；有限反编译事件/CUID入口 | 未取得sources JAR，未证明目标游戏使用，内部队列链未完全恢复 |
| Firebase Remote Config24.0.1/Analytics各已存版本 | 深读RC官方源码：FID、分析属性、personalization、ABT | 只是独立SDK实现，不冒充目标游戏确切RC版本 |
| Meta Core18.0.3/Audience Network、Google Mobile Ads | 复用已有包与分析；新增MAX Google25.4.0.0适配器请求ID映射 | 不把广告网络适配器认定为实际买量渠道 |
| Authentication3.9.0/Analytics6.3.0/IAP5.4.0及5.5.1 | 复用Auth原源码，新增后两者；追踪明确组件赋值与请求序列化 | Unity产品之间有客户端桥接；不证明Vector训练 |
| Pixel1.5.46/CAPI | 复用31号公开网页/官方接口证据 | cookie/点击/去重ID用途不同；本轮未运行网页或提交事件 |

## 新增包及时间

| 包 | 版本 | 发布日期证据 | 原包SHA256 |
|---|---|---|---|
'''
for sdk,v,date in [('com.unity.purchasing','5.4.0','CHANGELOG 2026-06-29'),('com.unity.purchasing','5.5.1','CHANGELOG 2026-11-13'),('com.unity.services.analytics','6.3.0','CHANGELOG 2026-03-05'),('Singular Android','12.17.0','未独立确认；保留HTTP Last-Modified')]:
 m=next(x for x in matrix if x['sdk']==sdk and x['version']==v);a=next(a for a in m['artifacts'] if a['path'].endswith(('.aar','.tgz')))
 t+=f'| {sdk} | {v} | {date} | `{a["sha256"]}` |\n'
t+='''
UPM包同时核对registry SHA1与下载内容；SHA256用于本地追溯。HTTP Last-Modified、registry获取日期和正式发布日期分别保留，不能互换。源码可读不代表开源许可证：UPM条款见各包LICENSE/Third Party Notices，闭源AAR只称反编译视图。

## 获取限制与复用边界

Singular的Maven Central坐标404，改由官方`maven.singular.net`取得12.17.0 AAR；sources JAR404，未伪称开源。MAX/Unity Ads候选GitHub changelog404，保留失败；MAX插件更新说明不能代替Android核心更新说明。成功和失败记录见[ACQUISITION](cross-sdk/ACQUISITION.json)、[Singular](cross-sdk/packages/singular/12.17.0/provenance.json)。

公共API差分来自实际JAR的javap：[API_DELTAS](cross-sdk/API_DELTAS.json)。只比较选定类，不证明所有方法体相同。Amaze GO!仍无可验证游戏包；本轮新增SDK不改变此状态。
'''
write('47_SDK生态与版本矩阵.md',t)

mappings=[
 dict(id='ID01',source='Authentication IPlayerId.PlayerId',target='Analytics IdentityManager.PlayerId -> unityPlayerID',kind='明确组件读取与序列化',refs=['XS18','XS19','XS20'],scope='UGS项目玩家，不等于Analytics UserId'),
 dict(id='ID02',source='Core IExternalUserId.UserId',target='Analytics UserId; fallback InstallId',kind='明确赋值/优先级',refs=['XS18','XS19'],scope='开发者控制的命名空间；不是自动跨发行商ID'),
 dict(id='ID03',source='FirebaseAnalytics.getAppInstanceId()',target='IAP pps.UnityAppInstanceId -> Insights.PlayerIdentity.AppInstanceId',kind='JNI getter + 逐级赋值',refs=['XS01','XS02','XS03','XS11'],scope='5.5.1; ads consent +远程允许 +Firebase可用'),
 dict(id='ID04',source='FirebaseAnalytics.getSessionId()',target='IAP FirebaseSessionId -> protobuf tag4',kind='明确读取和序列化',refs=['XS03','XS10','XS13'],scope='会话标识；5.4.0不能据字段存在声称已发送'),
 dict(id='ID05',source='FirebaseApp.getOptions().getApplicationId()',target='IAP FirebaseAppId -> protobuf tag100',kind='明确应用上下文映射',refs=['XS41','XS13'],scope='项目/App标识，不是用户身份'),
 dict(id='ID06',source='IAP CoreRegistry IPlayerId / IExternalUserId / AnalyticsService.GetAnalyticsUserID',target='Insights PlayerId / UserId / AnalyticsId',kind='明确各自赋值，保持分字段',refs=['XS06','XS01','XS11'],scope='可同包出现，不代表这些字符串彼此相等'),
 dict(id='ID07',source='MAX adapter serverParameters.event_id',target='Google networkExtras.placement_req_id',kind='明确字段改名赋值',refs=['XS30'],scope='广告请求关联，不是人或跨App用户'),
 dict(id='ID08',source='MAX consent / doNotSell',target='Unity gdpr.consent / privacy.consent',kind='明确Boolean转换',refs=['XS28','XS29'],scope='配置缺失不自动当已同意；不证明实际初始化'),
 dict(id='ID09',source='official Facebook app signed AttributionIdProvider.aid',target='Adjust DeviceInfo.fbAttributionId -> PackageBuilder.fb_id',kind='签名检查、provider读取及包字段',refs=['XS34','XS44'],scope='不是Facebook账号ID，也不是Meta AppEvents匿名ID'),
 dict(id='ID10',source='Developer Singular customUserId',target='SingularInstance.saveCustomUserId',kind='显式setter',refs=['XS39'],scope='未证明任何目标游戏或其他MMP设置同值'),
]
(R/'IDENTITY_MAPPINGS.json').write_text(json.dumps(mappings,ensure_ascii=False,indent=2),encoding='utf-8')
t='''# 跨SDK身份关联与字段映射

2026-11-19。只将明确读取、赋值、转换或共享契约列为已证关联。**本轮最重要的新证据是Unity IAP→Firebase/UGS组件的实际读取及共封装，仍未证明统一跨应用身份图谱。**

| 输入→输出 | 证据 | 作用域与条件 |
|---|---|---|
'''
for x in mappings:t+=f'| {x["id"]} {x["source"]} → {x["target"]} | 【SDK代码证实】{ref(*x["refs"])} | {x["scope"]} |\n'
t+='''
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
'''
write('48_跨SDK身份关联与字段映射.md',t)

write('49_行为价值事件端到端调用链.md',f'''
# 行为与价值事件：到哪一层已经有证据

2026-11-19。六层分别为：SDK能力、原版业务调用、请求构造代码、生产成功发送、服务器接收、模型训练使用。**静态的SendWebRequest调用只能证明构造/派发实现，不能证明本研究观察到发送成功。**

## 1. 新增完整客户端链：Unity IAP 5.5.1

SDK购买生命周期→`GooglePlayStoreExtendedPurchaseService.SendPurchasePaidEvent/SendPurchaseFulfilledEvent`→`PurchaseEventEmitter`→`PlayerData.CreatePlayerIdentityAsync`→`BuildEnvelope`→`PurchaseEventProtobufWriter`→`Forward`→条件Runtime Insights模块或HTTP gateway。这是SDK内明确调用，**不是目标游戏已安装5.5.1的证明**。{ref('XS42','XS07','XS08','XS01','XS10','XS13','XS09')}

| 数据 | 赋值及语义 | 不能扩大成什么 |
|---|---|---|
| paid/fulfilled/failed/intent | 不同购买阶段的事件variant；paid从PendingOrder，fulfilled从ConfirmedOrder | 不能把intent当支付，或将paid+fulfilled计两笔收入 |
| Transaction ID | `order.Info.TransactionID`→StoreTransactionId；Google receipt读取原始JSON/signature | 不能由客户端字段证明已验单、最终到账或退款已处理 |
| PriceMicro | 产品catalog metadata `localizedPrice × 1,000,000`，币种取metadata，quantity独立 | 不是必然实际成交金额，更不是预测LTV；折扣/税费/退款需另核对 |
| 时间 | UTC事件时间、安装时间、会话及应用版本分别赋值 | 到达时间不等于事件时间；没有恢复成熟cohort构造 |
| 身份 | UGS PlayerId/ExternalId/AnalyticsId、允许的平台ID、Firebase ID分字段 | 同包不是统一自然人身份或成功server join |
| 传输 | protobuf，`X-Schema-Name=insights.producers.iapsdk.v1alpha1.IAPSDKEvent`，schema/proto版本头 | Schema v1不是Vector模型版本 |

原始价格及identity：{ref('XS11','XS12')}。网关常量`https://prd.insights.analytics.unity3d.com/v1/ingest/producer`，只读未调用。Runtime分支依赖具体编译符号/平台，不能把所有Unity版本都写成经引擎模块。{ref('XS40')}

**队列/ACK边界：**所查IAP ForwardGateway构造请求后回调dispose；未找到该方法内持久队列、业务重试或成功ACK后的账本状态。UUID的注释要求重试保持稳定，并不等于已经实现重试或服务端去重。与UGS Analytics的buffer/dispatcher是不同路径。

## 2. UGS Analytics6.3.0：身份到事件缓冲再到HTTP

`AnalyticsService.Initialize`→Authentication/Core组件→IdentityManager→`RecordEvent`/标准事件→BufferX→Dispatcher→项目/环境scoped collect endpoint。事件头包含userID、unityPlayerID、安装/会话和eventUUID；同意状态可阻止收集。2xx成功与4xx坏请求都会清缓冲，网络/5xx保留并写磁盘。**“清了缓存”不是一律成功。**{ref('XS18','XS19','XS20','XS21','XS22')}

## 3. 原版游戏链复用及本轮关键复核

| 游戏 | 已证业务→规则→SDK | 请求/传输证据及剩余断点 |
|---|---|---|
| Car Race | 正展示收入→累计与国家阈值→Firebase；另一路ILRD→Adjust/Firebase/TikTok | Adjust构包/持久队列已证；Firebase-only阈值到Axon未证；同收入阈值事件不可再加成第二份收入 |
| Meowdoku | 安装时间窗/关卡/活跃及实际收入→GRT过滤/once/累计或增量→配置选中的AF/Meta等 | 实际线上GRT配置、各接收端开启、SDK成功发送及MMP partner映射未知 |
| Rotate Rings | 实际ad revenue double→AFAdRevenueData(network,APPLOVIN_MAX,USD,d)；另有规则值 | 本轮原Java明确还发ad_revenue2与ad_revenue4；三路的后台消费/去重未知，不能自行将其营收相加 |
| Jewel Coloring | 已恢复AdWorth默认规则/账本/系数→Firebase/Meta/Adjust | 优化代理value和标准purchase语义不等于真实IAP；AdWorth→MAX EventService未证 |

Rotate原始赋值：{ref('XS43')}；官方AF6.17.5 `AFf1tSDK`载荷与队列复用[16号](16_Adjust_AppsFlyer归因与Postback.md)/[REVENUE_PAYLOAD_ANALYSIS](ThirdPartySDKs/REVENUE_PAYLOAD_ANALYSIS.json)。Car/Meow/Jewel原函数、规则及路由依据复用[03号](03_广告收入与价值优化.md)、[09号](09_AdWorth深度逆向.md)、[10号](10_买量优化机制最终对比.md)。**03号Jewel早期“配置未找到”已由09号补齐，以09/10为准。**

## 4. MAX及Singular的范围

MAX13.7的trackEvent→生效axon_events过滤→结构化/legacy构造→调度器→persistent postback实现，与既有13.6.4结构相近。`user_data`需独立对象/开关，`dedupe_id`由调用options提供。公共API存在不表示游戏调用了42项默认名称。{ref('XS31','XS32','XS33')}；持久队列复用[22号](22_AppLovin事件协议版本差分.md)。

Singular12.17.0只追到`eventJSON→SingularInstance.logEvent`、CUID setter及自定义revenue flag。**未恢复完整队列/端点/ACK，不伪装为端到端链，也未证目标游戏接入。**{ref('XS38','XS39')}

所有“真实IAA”保留原始precision/估算来源；所有“真实IAP”保留生命周期及metadata/成交口径；代理value、预测LTV、达标、广告完成、发奖与收入回调分别记录。本轮无平台训练标签生产证据。
''')

write('50_远程配置与实验控制机制.md',f'''
# 远程配置、采集门控与反馈控制

2026-11-19。**本轮已定位服务端响应可控制哪些客户端采集；没有把远程配置能力当成在线推断。**

## 1. IAP5.5.1：真正控制标识读取的允许列表

`ConnectionsSettingsClient`构造项目/安装/平台/版本上下文，目标`/v1/get-connections-settings`；仅解析`attributeOverride`中Boolean true键。缓存未就绪/失败时返回空集合，不读取相应标识；下次缓存miss可重试，非无限阻塞。共享缓存以session为范围，重置generation防止旧请求写回新session。`PlayerData`在AdsIntent granted之后还检查此allowlist，再调用GAID/IDFA/Firebase getter。**这是配置→读取分支的代码正证据。**{ref('XS04','XS05','XS01','XS02')}

后台“Google Analytics已链接或Recommended”等产品条件在IAP changelog中出现；客户端不能据此推导服务器计算allowlist的全部逻辑。未访问配置端点，也不知道任何目标游戏的实际返回值。{ref('XS17')}

## 2. Firebase RC24.0.1：条件输入与分组回传

配置fetch body包含Firebase Installation ID/token、Analytics user properties、custom signals等；`INSTANCE_ID`变量来源是FID，不是靠名字推成Analytics App Instance ID。fetch/activate/default分开，fetched不等于已生效。激活的ABT元数据可调用`replaceAllExperiments`；personalization参数被读且元数据有效时，listener调用Analytics `personalization_assignment`及内部choice事件。相同参数choiceId在内存中抑制重复，不是跨进程服务器exact-once。{ref('XS24','XS25','XS26','XS27')}

这证明Firebase配置与分析之间的明确桥接；**不证明这些分组进入Axon/Vector，也未证明目标游戏用此版本或开启Personalization**。一般RC重试、ETag和throttle存在于原源码，不能拿fetch成功当实验已分组、用户已曝光或训练已完成。

## 3. MAX13.7及跨网络隐私

trackEvent按生效`axon_events`选协议；此前SettingsManager已证可更新注册配置。事件schema、可选user_data、客户端dedupe字段和日志队列分别处理，默认表不是生产表。13.7所选API与13.6.4没有新增声明，不据此宣称所有内部行为一致。{ref('XS31','XS32')}；远程设置实现复用[22号](22_AppLovin事件协议版本差分.md)。

MAX→Unity适配器在collectSignal和load前设置已知同意/出售限制，再读取Unity token。MAX→Google适配器可写npa/rdp。**隐私参数桥接已证；不能证明全部生产路径或所有网络均正确执行隐私策略。**{ref('XS28','XS29','XS30')}

## 4. Adjust5.8.1：远程触发、共享设置与客户端去重

`ActivityHandler.processRemoteTriggersI`解析`remote_triggers`，非空label/payload且listener存在时向主线程回调；没有业务listener就不能说改变游戏。5.6官方增加此API、5.7增加第三方共享设置读取/变化监听、5.8增加设备ID读取总开关。`shouldProcessEventI`只有调用方提供deduplicationId才查询有限本地记录；不保证跨设备/跨通道去重。{ref('XS35','XS36','XS37')}

## 5. ACK、重试、采样：不能混同

| 模块 | 本轮可证 | 不可证明 |
|---|---|---|
| IAP gateway | 构造HTTP、发起任务、completed dispose | 持久重试、成功业务ACK、服务端去重、训练ACK |
| UGS Analytics Dispatcher | 2xx与4xx分别处理但都清缓冲；网络/5xx保留写盘 | 4xx是成功、清盘即接收成功、训练完成 |
| MAX persistent postback | 复用已证磁盘/重试机制，有限次数 | 所有业务已触发、永不丢失、服务器exact-once |
| 游戏once/AdWorth/GRT状态 | 复用本地规则与发送后更新 | 状态写入意味着SDK入队/服务器ACK |
| Sampling/实验分配 | 已证可选门控、分组元数据和事件过滤 | 本轮没有恢复Axon/Vector生产采样率、分桶算法或模型实验配置 |

{ref('XS09','XS21')}。所有服务URL只作代码定位，未提交测试事件或读取真实配置。
''')

write('51_SDK演化与模型输入线索.md',f'''
# 跨版本演化：哪些改变确实影响数据可达性

2026-11-19。二进制/源码差分、官方changelog和生产生效三层分开。独立SDK新版本不代表目标游戏升级。

| 版本/变化 | 代码与更新说明 | 可能影响 | 不能推断 |
|---|---|---|---|
| IAP5.4.0→5.5.1 Firebase桥接 | 5.4.0 Android读取注释；5.5.1有JNI getter及远程allowlist；官方5.4.3说明增加条件采集 | 允许时购买上下文可关联Firebase分析 | 未对5.4.3二进制逐条验证；不把5.4.0字段存在当启用 |
| IAP5.5.1 Session ID修复 | 5.4.0 serializer无tag4，5.5.1明确写FirebaseSessionId；官方5.5.1说明遗漏已修复 | 从“内存/模型字段”推进为“可序列化进入请求” | 并非所有设备字段非空，也不保证收取或训练 |
| IAP5.4.0→5.5.1 Runtime路由 | 旧临时`UNITY_6000_5_OR_NEWER && IAP_INSIGHTS_MODULE_ENABLED`；新`UNITY_INSIGHTS_REQUIREMENTS_API && ENABLE_CLOUD_SERVICES_ENGINE_DIAGNOSTICS`，更新说明谈6000.7.0a7+ | 特定Editor/平台可经Insights模块，否则gateway | 不把旧注释或未来TODO当实际分支；native消费者仍不可见 |
| Analytics6.1→6.3 | changelog6.1接入DDF；6.3源码有AnalyticsIntent监听和legacy互斥 | 同意变化可控制事件采集/删除流程 | 不是所有Unity用户默认授权广告；没有把AnalyticsIntent改写成AdsIntent |
| MAX13.6.4→13.7 | 所选Sdk/Settings/EventService公共声明无变化；新反编译仍有axon_events/visitInfo/user_data/dedupe路径 | 结构化通路延续 | 不把既有art/visitInfo误报为13.7新增；不证明私有方法全等 |
| Adjust5.5→5.8.1 | javap新增remote trigger listener、sharing settings API、读取限制；官方5.6/5.7/5.8分段说明 | 可限制输入或接收后端触发 | 5.8.1只是HTTP处理修复，不因版本新就推测新LTV模型 |
| MAX Unity adapter4.17→4.18 | 所查两版都TokenConfiguration(format)→getToken，且隐私转换存在 | 条件化竞价signal桥接 | 不把4.18路径当首次新增，也不证明Unity/Axon共享用户价值 |

IAP关键源码及官方发行内说明：{ref('XS14','XS15','XS01','XS13','XS16','XS17')}。
Analytics与Adjust：{ref('XS23','XS37')}；[公共API原始差分](cross-sdk/API_DELTAS.json)。

## 为什么这个版本差异比新增字段更重要

IAP5.5.1官方说明明确“此前Firebase Session ID虽被收集但遗漏发送，现在写入事件”。源码serializer与之对应。这是“已收集≠已构造请求”的直接实例，限制了此前凭字段或getter推断生产数据覆盖的结论。**只证明修复后的代码可达性，不证明特定游戏已经产生该字段。**

本轮未取得MAX Android核心13.7的有效对应官方changelog，候选地址404已留档；不拿Unity插件日志替代。最新是本次取得的registry/release口径，不声称全平台绝对最新。其他SDK未做全量历史差分，矩阵中保留分析状态。
''')

write('52_Axon_Vector客户端系统重建.md',f'''
# Axon / Vector客户端系统重建与断点评估

2026-11-19。本轮新增44段可追溯代码证据、15条关系边；证据图现有**{len(g['nodes'])}节点、{len(g['edges'])}边、{len(g['sources'])}来源**。[当前JSON](prediction-system/EVIDENCE_GRAPH.json)、[00—46阶段原图快照](cross-sdk/EVIDENCE_GRAPH.before47.json)、[本轮固定快照](cross-sdk/EVIDENCE_GRAPH.after52.json)。旧节点、边和来源保持原对象，未将原unknown边改成已证训练。

## 新增连接与六层证据

| 客户端连接 | SDK能力 | 原版业务 | 请求构造代码 | 成功发送 | 服务器接收 | 用于模型训练 |
|---|---|---|---|---|---|---|
| UGS Authentication/Core→Analytics identity/buffer | 已证 | 目标游戏未证 | 已证 | 未证 | 未证 | 未证 |
| Firebase getters→IAP5.5.1→Insights | 已证且有条件 | 目标游戏该版本未证 | 已证 | 未证 | 未证 | 未证 |
| IAP UGS/分析/交易/价格共封装 | 已证 | SDK内purchase回调已证，非目标游戏实跑 | 已证 | 未证 | 未证 | 未证 |
| Firebase RC→Analytics/ABT assignment | 已证 | 目标游戏该功能未证 | 调Analytics API已证；未重新恢复Google全部传输层 | 未证 | 未证 | 未证 |
| MAX→Unity token/同意、MAX event_id→Google request ID | 已证 | 所选适配器生产调用未证 | 适配器参数/请求代码已证 | 未证 | 未证 | 未证 |
| Facebook Attribution provider→Adjust fb_id | 已证且受开关/签名/可访问性限制 | 目标游戏运行结果未证 | 已证 | 未证 | 未证 | 未证 |
| Rotate原版→AF标准ILRD及额外事件 | 已证 | 原DEX调用已证 | API参数已证，SDK包链复用16号 | 未证 | 未证 | 未证 |

每条新边带SDK版本、原包与文件SHA256、方法/行号、触发条件、六层标记及补充的A/U边；见[代码目录](cross-sdk/CODE_CATALOG.md)及图的`cross_sdk_extension`。

```mermaid
flowchart LR
 AUTH[Authentication IPlayerId] -->|XU01 SDK赋值| AN[Analytics身份]
 EXT[Core ExternalUserId] -->|XU01 SDK赋值| AN
 AN -->|XU02 同意与缓冲代码| COL[Analytics collect]
 FB[Firebase Instance与Session ID] -->|XU03 AdsIntent和远程允许| IAP[IAP PlayerIdentity]
 AUTH -->|XU05 独立PlayerId字段| IAP
 REM[远程attributeOverride] -->|XU04 读取门控| IAP
 IAP -->|XU06 protobuf及购买生命周期| INS[Insights gateway或Runtime]
 INS -.->|XU07 未证内部数据血缘| V[Vector训练]
 RC[Firebase配置metadata] -->|XG02 条件赋值曝光| FA[Firebase Analytics]
 MAX[MAX适配器] -->|XA01 隐私与token请求| UA[Unity Ads]
 UA -->|XA01 token回调| MAX
 MAX -->|XA02 请求event_id| G[Google placement_req_id]
 ROT[Rotate原收入wrapper] -->|XM01 原版静态调用| AF[AppsFlyer收入]
 AF -.->|原A08 伙伴授权与生产送达未知| AX[Axon优化]
```

## 哪些输入线索变得更强

**Vector侧：**官方IAP/D2C→Vector总体用途已有S21；本轮补了IAP如何实际读身份、交易阶段、产品价格、安装时间、允许的Firebase/广告标识并构造Insights请求。二者形成更强的拼图，**仍不能跳过Insights→训练集的服务端断点**。尤其PriceMicro为metadata价格，不能未经核对当最终收入标签。

**Axon侧：**确认MAX13.7协议路径延续、适配器请求上下文与隐私转换；MMP业务事件和收入API链继续成立。没有新增四款游戏显式价值规则→MAX EventService的证据，也没有生产MMP partner ACK。MAX→Unity token是媒体竞价信号通路，不是双方互传全部玩家价值/模型训练数据。

## 最关键的反面发现

1. IAP5.4.0存在Firebase字段不代表真正调用getter；Session ID进入内存也不代表被序列化。5.5.1修复有官方说明与源码双证。
2. UUID、交易ID、client cache和HTTP completed都不代表服务器exact-once。UGS Analytics4xx也会清缓存；IAP gateway没有所查方法内持久重试保证。
3. Firebase FID≠Analytics Instance ID，IAP IEngineInstallationId≠已证与Analytics IInstallationId相同；新UGS ID也不能直接等于Unity Ads读的旧PlayerPrefs键。
4. AdWorth/GRT代理值、阈值、paid/fulfilled阶段和原始收入需要分账；不能把其总和当标签。

## 仍须服务端证据解决

【无法确认】生产启用的SDK/编译分支和远程allowlist、事件成功接收、跨通道去重、退款及迟到处理、ID命名空间与join、Insights/MMP数据进入哪些训练任务、实际安装前特征快照、模型标签及出价效果。客户端更多字段不能独自完成这些证明。

## 下一步具体模块

优先 **Unity Services Core1.19.0的`IInstallationId/IEngineInstallationId/IExternalUserId`提供者及新Engine Identifiers桥**，与本轮IAP5.5.1、Analytics6.3.0对照。原因是本轮已发现两个消费者，但尚未证明其安装ID接口是否同源、何时重置、如何受用途设置控制；这是仍可能由公开客户端源码补齐的具体断点。

其后优先Runtime Insights原生接收层的公开绑定/官方schema及正式数据用途文档；若只剩闭源消费者、训练与生产ACK，应停止靠SDK命名拼接，保留未知并寻求授权匿名化血缘/消融案例。
''')
print('wrote 47—52 reports, catalogue and identity mapping')
