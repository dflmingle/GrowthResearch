# 72号：第三方SDK身份关联能力矩阵

2026-11-20。归档实数103 AAR、67源码包已逐哈希记录；不以SDK数量作为新增成果。不重复下载已验证版本，只核验既有调用链及新增官方身份服务契约。

| SDK/服务 | 版本/材料 | 当前可证能力 | 等级 | 分析范围及未证 |
|---|---|---|---|---|
| MAX/Axon | MAX13.6.4;Axon1.3.4 | 设备ID/AppSet/CUID/user_data归一化和请求字段 | E1,E2；IG72C01,IG72C04,IG72C06,IG72C08,IG72C20 | 已核验所选完整调用链；没有完整生产图谱/匹配服务输出 |
| Unity Ads/Vector | 4.17.0/4.18.1 | 广告/分析标识和隐私构造、机会事件 | E1,E2；IG72C21,IG72C22,IG72C23,IG72C24,IG72C25,IG72C26,IG72C27 | 已核验所选调用链；Vector是服务端产品，不是独立客户端启用证据 |
| LevelPlay/ironSource | 9.3.0/9.4.0/9.5.0归档 | 用户/广告收入接口不自动成为跨设备join | UNKNOWN；L71D01 | 复用已有mediation分析；本轮未恢复新图谱；版本存在不是身份图谱证据；无新的逐字段合并契约 |
| AppsFlyer | 6.14.2/6.17.5 | 安装作用域ID、CUID/收入和伙伴转发 | E3；L72S08,L72S05,L72S06 | 复用官方字段/业务链；安装/归因和伙伴sharing不等于跨游戏个人图谱 |
| Adjust | 5.5.0/5.7.0/5.8.1 | 允许设备字段/partner参数/收入 | E1,E2,E3；L71D01,L71C09 | 复用所选源码和伙伴契约；SDK包构造不等于匹配/训练 |
| Singular | 12.17.0 | 开发者显式用户ID | E1；XS39 | 复用setter核验；未证目标业务调用或跨SDK共享 |
| Firebase Analytics/Installations | Analytics22.1.2;Installations19.0.0等归档 | 可选开发者稳定user_id支持BigQuery同人跨App/设备分析 | E3,E4；IG72S13,XS41 | FID/AII区别及官方跨App user ID契约；不自动回填历史/不许PII；不等于向Axon/Vector共享 |
| Unity Core/Auth/Analytics/IAP | Core1.19.0;Auth3.9.0;Analytics6.3.0;IAP5.5.1 | 项目玩家/组织外部账号；IAP身份共包 | E1,E2,E3,E4；C53S12,C53S16,XS11,IG72S02,IG72S03 | 提供者、消费者与账号链接已核验；E4是账号服务，不是广告图谱/训练列 |
| Meta Audience Network | 6.21.0/6.22.0;FacebookCore18.0.3 | Adjust官方签名校验的Facebook attribution provider | E1；XS34 | 已有归档/选定跨SDK提供者证据；非Facebook登录账号；FAN完整图谱未恢复 |
| Google Mobile Ads | 25.1.0/25.2.0/25.4.0等 | 竞价placement_req_id及广告上下文 | E1,E2；CGS26 | 已有归档/适配器链；广告请求关联非跨设备人图；不将所有Google数据视为共享 |
| Mintegral | 16.9.91 | UNKNOWN | UNKNOWN； | 归档核验；本轮未找到可补核心断点的身份合并链；不能从适配器/同名设备字段声称图谱；不宣称已逐类完成逆向 |
| Liftoff/Vungle | 7.6.3/7.7.1/7.7.6 | UNKNOWN | UNKNOWN； | 归档核验；本轮未找到可补核心断点的身份合并链；不能从适配器/同名设备字段声称图谱；不宣称已逐类完成逆向 |
| Pangle | 7.8.5.2/8.1.0.3/8.1.0.5 | UNKNOWN | UNKNOWN； | 归档核验；本轮未找到可补核心断点的身份合并链；不能从适配器/同名设备字段声称图谱；不宣称已逐类完成逆向 |
| Chartboost | 归档目录存在，但本轮未确认独立可用AAR/接口 | UNKNOWN | UNKNOWN； | 归档核验；本轮未找到可补核心断点的身份合并链；不能从适配器/同名设备字段声称图谱；不宣称已逐类完成逆向 |
| Branch | 公开Android API文档；本轮未下载二进制 | 开发者非PII别名可跨平台/重装持久归因 | E3,E4；IG72S12 | 官方setIdentity/logout契约；未证与两平台的图谱共享 |
| Amplitude | 公开文档；本轮未下载二进制 | 登录后的账号关联、同组织项目作用域 | E3,E4；IG72S11 | 官方device/user/Amplitude ID合并；稳定userID由客户指定；不是全球广告图谱 |
| Mixpanel | Simplified ID Merge API文档；未下载SDK | $device_id+$user_id同事件→identity cluster；logout reset | E3,E4；IG72S10 | 官方显式merge契约；共享设备未reset会误合并；两平台集成未知 |
| LiveRamp/RampID | 官方产品+Unity2026-04-02公告 | 跨渠道身份/受众激活 | E3,E4；IG72S04,IG72S05 | 第三方身份激活契约；Unity具体输入/返回映射和Vector消费未证 |
| UID2 | 公开namespace/确定性服务文档 | 广告身份framework | E3,E4；IG72S09 | 官方服务契约；未证两平台部署；不构造真实身份查询 |

新增E4以官方明确链接/合并/身份解析契约为准：Mixpanel、Amplitude、Branch、Firebase的开发者user-ID能力不能转移为Axon/Vector事实；LiveRamp/UID2也不能自动套用两家所有流量。

Mintegral/Vungle/Pangle/Chartboost虽有归档或目录，本轮没有足够证据给它们填完整生产图谱；这是明确分析缺口，不能把UNKNOWN改成没有能力。全部版本存在证据见[ARCHIVE_INVENTORY](identity72-experiments73/ARCHIVE_INVENTORY.json)，能力逐项见[机器矩阵](identity72-experiments73/SDK_CAPABILITY_MATRIX.json)。

每项调用链有源路径/哈希，文档有URL/摘录。所有实际生产匹配与Axon/Vector消费均未证。只要没有明确赋值、返回映射或服务契约，就不因字段同名建立跨SDKjoin。
