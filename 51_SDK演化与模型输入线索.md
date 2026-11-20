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

IAP关键源码及官方发行内说明：[XS14](cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/PlayerData.cs):L88；[XS15](cross-sdk/packages/purchasing/5.4.0/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39；[XS01](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/PlayerData.cs):L97；[XS13](cross-sdk/packages/purchasing/5.5.1/extracted/package/Runtime/Stores/Data/Insights/PurchaseEventProtobufWriter.cs):L39；[XS16](cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L2；[XS17](cross-sdk/packages/purchasing/5.5.1/extracted/package/CHANGELOG.md):L88。
Analytics与Adjust：[XS23](cross-sdk/packages/services.analytics/6.3.0/extracted/package/CHANGELOG.md):L48；[XS37](cross-sdk/adjust-changelog.raw):L1；[公共API原始差分](cross-sdk/API_DELTAS.json)。

## 为什么这个版本差异比新增字段更重要

IAP5.5.1官方说明明确“此前Firebase Session ID虽被收集但遗漏发送，现在写入事件”。源码serializer与之对应。这是“已收集≠已构造请求”的直接实例，限制了此前凭字段或getter推断生产数据覆盖的结论。**只证明修复后的代码可达性，不证明特定游戏已经产生该字段。**

本轮未取得MAX Android核心13.7的有效对应官方changelog，候选地址404已留档；不拿Unity插件日志替代。最新是本次取得的registry/release口径，不声称全平台绝对最新。其他SDK未做全量历史差分，矩阵中保留分析状态。
