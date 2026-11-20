# Axon 身份与价值信号：能力、游戏调用、生产启用分层

2026-11-18。官方独立 SDK 新增证据详见[17](17_第三方身份图谱技术调查.md)。

## 哪些信息公开可证

**【AppLovin官方资料证实】**2026-08-06 隐私政策列设备/应用/网络环境、广告 ID、IDFV、App Set ID、安装/会话，以及发布者提供时的 Publisher User ID、邮箱、电话；披露从跨应用/设备及 MMP 获取数据，结合分析派生信息，用本应用或其他应用/网站行为进行个性化和 AI 广告改进。政策说明使用类别和目的，**不是五款游戏逐项实际上传记录，也不公开完整 Axon 特征表或身份匹配算法**。[AX03](EVIDENCE_INDEX.md#ax03)

**【官方 SDK 代码证实】**AppLovin 13.6.4 的 `EventServiceImpl` 已有结构化 Axon 事件分支；`r7.a(AppLovinUserData)` 可处理 user_id/email/phone，邮箱/电话有规范化及 SHA-256 路径；发送还受配置与非空数据条件限制。此 API 能力不能证明目标游戏传入联系方式。没有读取任何真实 ID。[TP03](EVIDENCE_INDEX.md#tp03) [TP07](EVIDENCE_INDEX.md#tp07)

## 不同意义的“身份关联”

| 层次 | 证据判断 |
|---|---|
| 展示机会级上下文预测 | 【AppLovin官方资料证实】自动选择机会、创意和竞价；具体预测函数未公开 |
| 设备广告标识 | 【官方 SDK 代码证实】广告 ID、限制标记、App Set ID 等条件化采集/序列化实现；并非账户身份 |
| 单应用多 SDK ID 联结 | 【游戏代码证实】Rotate ThinkingData ID→MAX；Meow AdUuid→MAX；AF CUID/分析 ID 链已有证据 |
| 跨应用行为使用 | 【AppLovin官方资料证实】政策披露该类别能力；具体五款流量/字段与使用状态未知 |
| 确定性身份匹配 | 【官方 SDK 代码证实】提供者输入的 user_data 规范化/哈希能力；【无法确认】五款启用、匹配率、跨应用合并 |
| 概率归因 | 【AppLovin官方资料证实】MMP 设置文档列 probabilistic modeling；不是跨设备身份图谱的证明 |
| 商业身份图谱/受众同步 | 【无法确认】未取得五款到某图谱供应商/受众后台的实际闭环 |

来源：[AX01](EVIDENCE_INDEX.md#ax01)、[AX03](EVIDENCE_INDEX.md#ax03)、[TP07](EVIDENCE_INDEX.md#tp07)、[TP08](EVIDENCE_INDEX.md#tp08)、[I01–I08](EVIDENCE_INDEX.md#i01)。

## 五款价值输入矩阵

以下“已发送”仅指**静态业务 API 调用证据**，不是网络送达或后台启用。

| 游戏信号 | 已证明接收端 | 价值语义 | 到 AppLovin 的证据 |
|---|---|---|---|
| Car 关卡里程碑、前5次激励等 | 【游戏代码证实】Adjust 等业务链 | 行为代理 | 【无法确认】需 partner 事件映射 |
| Car `taichi_us/t1/t2/t3` | 【游戏代码证实】Firebase | 实际展示收入缓存跨阈值，发送缓存金额；默认$0.50/.30/.20/.03 | 【无法确认】未证实 Adjust/AF 或 AppLovin 路由；不能假定 Firebase 自动转发 |
| Car 展示收入 | 【游戏代码证实】Adjust/Firebase/TikTok | 实际 provider 收入回调，精度取决上游 | 【无法确认】IAA 收入利用是产品能力，具体 app 开启未知 |
| Meow 时间窗×关卡/活跃分钟 | 【游戏代码证实】GRT 指定 AF/Meta/Learnings/Firebase | 早期参与代理 | 【无法确认】AF partner 开关/映射未知 |
| Meow GRT 收入处理器 | 【游戏代码证实】配置化接收端能力 | 累计或增量已实现收入；不证明未来 LTV | 【无法确认】生产 GRT 规则和 AppLovin 授权共享未知 |
| Rotate 标准 ILRD | 【游戏代码证实】AF `logAdRevenue` | 变现网络+MAX mediation+币种+广告收入 | 【无法确认】`APPLOVIN_MAX` 不表示回传给 AppLovin advertiser |
| Rotate 国家×day0–6、时长+收入 | 【游戏代码证实】AF/Firebase；另有 TikTok 收入 | 实际累计收入门槛/参与资格，部分代理金额 | 【无法确认】启用/映射/优化目标未知 |
| Jewel 90条默认 AdWorth | 【游戏代码证实】Firebase65、Meta custom43、Meta标准5、Adjust7，计数可重叠 | 价格/展示价值账本×行为规则，部分代理 purchase | 【无法确认】没有 AppLovin 输出标签；Adjust7可否转发需后台证据 |
| Amaze GO! | 【无法确认】无包 | 未知 | 未知 |

游戏证据：[C03–C06](EVIDENCE_INDEX.md#c03)、[M01–M05](EVIDENCE_INDEX.md#m01)、[R02–R06](EVIDENCE_INDEX.md#r02)、[D01–D07](EVIDENCE_INDEX.md#d01)。

## 两个不能混淆的收入路径

**【AppLovin官方资料证实】IAA/Blended 的 MAX 关联，不意味着可以把广告收入塞进 IAP checkout。**当前 Adjust/AF 集成指南明确：purchase/checkout 只传用户直接支付，禁止预测 LTV、广告展示收入等。AF 当前推荐其他事件→postinstall 且不带 values/revenue；不能把其 SDK `af_revenue` 字段存在等同 AppLovin 全额接收并用于 ROAS。[AX01](EVIDENCE_INDEX.md#ax01) [AX02](EVIDENCE_INDEX.md#ax02)

**【AppLovin官方资料证实】Ad Review 另有用途边界。**2026-09-16 官方声明：MAX 中 Ad Review 需发布者启用，数据用于质量治理，声称不建立用户/设备画像、不送 Axon；不能将 SafeDK 看见其他网络素材直接画成 Axon 训练输入。这是公司公开声明，未独立运行验证。[AX03](EVIDENCE_INDEX.md#ax03)
