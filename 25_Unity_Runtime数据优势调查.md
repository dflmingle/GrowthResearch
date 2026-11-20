# Unity Runtime 数据优势：可证实的接口、授权与尚缺的链路

2026-11-18。**已证明 Unity 有引擎层受控数据框架；没有证明所有 Unity 游戏的玩法自动进入 Vector，也没有证明 Runtime 是 2026 增长的主要原因。**官方产品表述、授权框架、客户端代码和四款实际使用分别核对。

## 1. 三种“数据优势”不能合并成一句话

| 层级 | 取得的证据 | 尚未取得 |
|---|---|---|
| 平台宣称 | 【官方公开证实】Vector 产品页称利用游戏 DNA、玩家行为、生态数据及新架构；2026 D7/D28 博客称 first-party gameplay data | 【无法确认】具体特征 schema、Runtime 来源占比、独立模型评估、与 Axon 的同基准实验 |
| 数据收集与使用框架 | 【官方公开证实】Developer Data Framework 分开控制 Collection、Usage、终端用户 consent；可由 Runtime、连接服务/外部分析等输入 | 【无法确认】某游戏组织的后台配置、每项字段实际上线情况 |
| 引擎接口 | 【SDK代码证实】Unity 6000.3 官方参考源码有 ConsentState、Get/SetConsentState 与变更回调 | 【无法确认】native collector 到 Vector 训练流水线实现、每场游戏的生产送达 |
| 研究游戏 | 【游戏代码证实】Car/Rotate 为 Unity 6.3；Meow 为 Godot、Jewel 为 Cocos | 【无法确认】Car/Rotate 对框架的具体授权；非 Unity 引擎游戏仍能接 Unity Ads/MMP，但不能认定具有 Unity 引擎 Runtime 数据 |

证据：[VG03](EVIDENCE_INDEX.md#vg03)、[VG06](EVIDENCE_INDEX.md#vg06)、既有 [样本目录](SAMPLE_CATALOG.json)。Amaze 无包体，不推定引擎或共享状态。

## 2. 官方默认值与控制

【官方公开证实】[Collection Settings 原文](vector/ddf-data-collection-settings.html)，最后更新 2026-08-20：

- 新 Unity 6.2+ 项目，云连接且 Diagnostics 默认启用时，Essential Data 可开始收集；包括 crash、telemetry、configuration metadata 等服务所需数据。
- 从旧项目升级，或曾关闭 Diagnostics，并不等于自动启用；需要显式配置。
- **Additional Recommended Data 未显式设置则视为关闭**，例子包括会话元数据、实验配置状态、引擎运行模式。例子不是每款游戏实际采集清单。

【官方公开证实】[Usage Settings](vector/ddf-data-usage-settings.html)：未配置时仅按所用产品/服务为本客户使用的默认理解，其余使用选项不自动启用。与其他已选择参与的开发者合并、建模贡献/聚合洞察等分别受设置约束；不能原样分享其他开发者的细粒度数据。

【官方公开证实】[End-user consent](vector/ddf-end-user-consent.html)：`analytics_intent` 控制带用户标识的分析用途；`ads_intent` 控制个性化广告用途及广告专用标识。deny 会抑制相应用途标识/特定事件。在没有其他可知 consent 机制时，文档解释的缺省为 analytics granted、ads denied。**不是将“未填写”解释成“允许广告用途”。**

【官方公开证实】[Editor 配置文档](vector/doc-configure-diagnostics-editor.html)明确：关闭 Diagnostics 停止相应 diagnostic 收集，**不影响通过其他 Unity 产品或 Dashboard 链接独立收集的 Developer Data**。因此不能说一个开关关闭了所有 Ads、Analytics、MMP 数据。新文档对 diagnostic 的精确范围优先于笼统理解。

【官方公开证实】[框架用途清单](vector/ddf-your-data-in-action.html)强调逐步迁移、既有服务须明确授权，列出 6.2 的性能稳定性、项目 Diagnostics、Unity AI、Unity Analytics；**没有给出一条可核验的“特定 Runtime 事件→Vector 训练标签”完整链**。页面没有列出 Vector 也不能证明 Vector 绝不使用 Runtime；它只说明不能从框架存在跳到全量广告训练。

## 3. 公开代码核对

【SDK代码证实】取得 Unity 官方 **6000.3 分支**，没有只拿 master 当游戏版本证据：

| 原始文件 / 方法 | 实际实现边界 |
|---|---|
| [EndUserConsent.bindings.cs 快照](vector/unity-runtime-cs-release.html)：`UnityEngine.UnityConsent.EndUserConsent.GetConsentState/SetConsentState` | `NativeMethod` 的 extern 绑定，证明原生接口存在；不是 native 数据采集实现源码 |
| 同文件 `consentStateChanged` / `OnConsentStateChanged` | 原生通知后读取状态并调用 C# 订阅者 |
| [ConsentState.bindings.cs 快照](vector/unity-runtime-cs-release-state.html) | `AdsIntent`、`AnalyticsIntent`，构造默认 `Unspecified`；不等于广告同意 Granted |

精确行号与 SHA256 见 [CODE_EVIDENCE.json](vector/CODE_EVIDENCE.json) 的 `runtime_consent/runtime_state`；官方来源 [UnityCsReference 6000.3](https://github.com/Unity-Technologies/UnityCsReference/tree/6000.3/Modules/UnityConsent)、[API](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/UnityConsent.EndUserConsent.SetConsentState.html)。参考源码按 Unity Reference Only License，不称已获得完整闭源引擎源码。

【SDK代码证实】Unity Ads 4.17/4.18.1 本身有设备、会话、TCF/developerConsent、广告机会 token；这些可跨引擎集成，**和 Unity 引擎运行时行为采集不是同一套证据**。详见 [24](24_Unity与AppLovin技术对比.md)。没有因广告 SDK 初始化而替开发者改变任何数据权限。

## 4. Unity Exchange 与身份：新增的明确公开证据

【官方公开证实】[2026-04-02 公告](https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming)称 Unity Exchange 在**美国、加拿大**支持 LiveRamp RampID，用于品牌广告主/代理商的身份受众激活，要求 Unity 和接收合作方双方支持。[本地快照](vector/exchange-rampid.txt)。这比单纯 SDK 广告 ID 字符串更强，属于**公开证实的商业身份互通能力**。

但【无法确认】四款游戏使用 RampID、Vector 必须依靠 RampID、每次广告请求都带有它、或它带来了财报中的哪部分增长。不能把品牌程序化库存能力挪成手游 UA 已启用事实。

【官方公开证实】[Exchange get-started](vector/doc-get-started.html)：发布方请求→DSP HTTP OpenRTB 2.5→第一价格拍卖→客户端预缓存→展示后的通知/跟踪。它证明供给和竞价集成能力；**不能证明 Vector 作为买方必然使用 Exchange 全部供给，也不能把该协议当 Axon/Vector 服务端算法的复原**。[VG07](EVIDENCE_INDEX.md#vg07)

## 5. 是否增加了 Axon 没有的能力

【合理推断】Unity 作为引擎提供方，有机会在同意和授权下获得游戏运行/会话上下文、连接游戏特征与玩家偏好。这可能比只观察广告互动更早解释长期留存和变现潜力，也可能降低冷启动稀疏性。

【无法确认】这项机会是否已充分实现、覆盖多少游戏、如何与 MMP/广告标识关联、是否优于 Axon 现有的跨应用广告互动/收入数据。缺少消融实验，不能证明“加 Runtime 就能降低 CPI 或提高 ROAS”。同样不能说 Axon 只会看广告点击：既有官方政策和 MMP 文档明确支持更多数据类别。

【官方公开证实】另有一条更具体、但不同于通用 Runtime 的公开表述：[2026-07-21 Unite Seoul 回顾](vector/unity-2026-keynote.txt)称 IAP SDK 5.4 / D2C 购买数据可以丰富 Vector 模型。它说明 Unity 正在连接引擎服务与增长产品；**购买服务数据、Developer Data 的广泛类别、某款游戏的授权采集不是同一事实**。不能用这段声明证明四款游戏已上传 IAP/D2C，或证明纯 IAA 的 Runtime 特征已有收益消融结果。

下一层需要的证据是：经授权的特征/数据字典、用途开关及接收日志、可复核的按游戏/国家覆盖率、在相同样本上 Runtime 特征开关的脱敏聚合消融结果。当前不具备，故停在明确边界，不通过探测未授权服务端补齐。
