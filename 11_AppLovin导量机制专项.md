# AppLovin / Axon 实际导量机制专项

2026-11-18。与本轮[19](19_AppLovin导量证据与技术闭环.md)合读；本报告保留产品和公开证据边界，独立 SDK 的新发现见[15](15_AppLovin_MAX与Axon技术分析.md)。

## 结论

**【无法确认】尚未取得五款目标游戏通过 AppLovin 实际获客的可靠记录。**没有可核验的目标包名×AppLovin 媒体×广告主×展示日期/地区记录，也没有授权的 MMP partner 配置、归因导出或 postback 送达日志。这不等于它们没有投放。[AX04](EVIDENCE_INDEX.md#ax04)

| 游戏 | 已取得的近端证据 | 仍未跨过的证据边界 |
|---|---|---|
| Car Race | 【游戏代码证实】Adjust campaign 回调、事件和广告收入；Metica 管理 MAX；有通用 AppLovin trackEvent 桥 | campaign 分类的 `mx` 不是已证实的 AppLovin 来源；通用桥未证明关卡/国家阈值进入 AppLovin |
| Meowdoku | 【游戏代码证实】AppsFlyer conversion data；UserTag 枚举明确含 `applovin_int`；GRT 可发 AF | 枚举是来源识别能力，没有真实归因实例或 campaign 记录 |
| Rotate Rings | 【游戏代码证实】AF conversion listener、标准广告收入、时长/国家/安装年龄事件 | `APPLOVIN_MAX` 是变现 mediation 枚举，不是 acquisition media_source |
| Jewel Coloring | 【游戏代码证实】Adjust attribution→AdSourceUtils；AdWorth 的 Adjust 输出 | Adjust→AppLovin partner 映射、生产规则和投放状态未知 |
| Amaze GO! | 【无法确认】无可验证包体 | 不从同发行商另一产品推定集成、投放或事件 |

证据：[C01–C06](EVIDENCE_INDEX.md#c01)、[M01–M05](EVIDENCE_INDEX.md#m01)、[R01–R06](EVIDENCE_INDEX.md#r01)、[D01–D07](EVIDENCE_INDEX.md#d01)、[TP02](EVIDENCE_INDEX.md#tp02)、[TP08](EVIDENCE_INDEX.md#tp08)。静态调用不是生产送达记录。

## 三件必须分开的事

1. **【官方 SDK 代码证实】MAX 变现接入**：本游戏请求和展示其他广告主广告，得到收入回调。适配器接收 network bid token / bid response，不证明本游戏购买该网络流量。[TP03](EVIDENCE_INDEX.md#tp03) [TP06](EVIDENCE_INDEX.md#tp06)
2. **【AppLovin官方资料证实】AppLovin 广告需求/库存**：AppLovin 在合作应用的广告位展示广告；公开库存跨 puzzle、match/sort、casual/action、words/cards，常见关间插屏和奖励视频。[AX02](EVIDENCE_INDEX.md#ax02)
3. **【AppLovin官方资料证实】AppDiscovery / AppLovin Ads 获客**：广告主选择目标、上传素材、配置 MMP、启动付费活动；Axon 自动优化竞价、定向及创意选择。MAX 使用者不自动成为付费获客广告主。[AX01](EVIDENCE_INDEX.md#ax01) [AX02](EVIDENCE_INDEX.md#ax02)

## 官方可以还原的闭环

**【AppLovin官方资料证实】**当前公开目标包括 Ad/IAA ROAS、IAP ROAS、Blended ROAS、CPP、CPE；IAA/Blended 要求应用使用 MAX。官网也明确以教程、成就、首会话长度等 milestone 说明 CPE。当前已保存资料没有足够依据进一步列出具体 CPI 出价产品的现行配置，因此不把“记录安装”直接写成“五款正在跑 CPI”。[AX02](EVIDENCE_INDEX.md#ax02)

| 步骤 | 可以证明的内容 | 不可推定的内容 |
|---|---|---|
| 机会评估→竞价→创意 | 【AppLovin官方资料证实】自动 bidding、targeting、creative selection；视频为主要库存 | 模型特征权重、实时 bid 公式、目标游戏受众 |
| 展示/点击→安装 | 【AppLovin官方资料证实】tracking macros 含 campaign、创意集、展示应用、国家、event ID、placement | 游戏包内 MAX key 不等于其获客 campaign |
| 首启→MMP | 【游戏代码证实】四个有包游戏具备 Adjust/AF 入口 | 任意一次安装实际归给 AppLovin |
| MMP→AppLovin | 【AppLovin官方资料证实】必须启用 partner、选择 sharing 范围、映射事件 | 客户端调用 logEvent 即表示 partner 已收到 |
| 真实收入→优化 | 【AppLovin官方资料证实】MAX 是 IAA/Blended 前提，MMP purchase 有明确金额定义 | 自定义代理价值可以充作真实 IAP revenue |
| 优化→下一轮展示 | 【合理推断】转化/收入反馈帮助选择更有价值的机会 | 任一目标游戏已用指定事件训练、实际 ROAS、预算与地域 |

依据：[AX01](EVIDENCE_INDEX.md#ax01)、[AX02](EVIDENCE_INDEX.md#ax02)、[AX05](EVIDENCE_INDEX.md#ax05)。MMP 服务端回传可包含其他渠道及自然用户：因此**即便取得“AppLovin 收到安装”的记录，也还需看归因来源，才能证明由它导量**。

## 最小补证

【无法确认】要把某款从“具备链路”提升为“实际投放”，至少需要授权导出的 AppLovin campaign/素材记录或 MMP 的明确 AppLovin attribution；要证明闭环，还需要 partner 启用、事件映射、sharing 范围与送达日志。无需交付 API 密钥。没有这些资料，不报告预算、CPI、ROAS 或国家投放结论。
