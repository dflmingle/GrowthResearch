# 72号：Unity身份图谱逆向

2026-11-20。**Unity账号服务有明确跨游戏/设备身份契约，Unity Exchange有RampID受众激活契约；两者都不能直接等同Vector的个人跨游戏价值图谱。** Ads客户端另有设备和广告实例标识；它们不是账号ID的别名。

## 三个系统分别核验

| 系统 | 已证链路 | 等级 | 不能升级为 |
|---|---|---|---|
| Player Accounts/Authentication | OAuth流程/claims→外部身份login/link→项目PlayerId；组织级跨游戏账号 | IG72C10—19/28、IG72S02/03；E1—E4 | 所有Unity引擎App自动登录、账号数据自动进广告模型 |
| Unity Ads | SDK安装/分析来源、广告ID/AppSet隐私字段→初始化/通用请求；机会ID→事件快照 | IG72C21—27、L71C15/16/18/19；E1/E2 | 跨设备个人匹配、永久广告身份 |
| Exchange/LiveRamp | 美加RampID启用库存与接收伙伴支持条件 | IG72S04/05；E3/E4服务契约 | Unity自研LiveRamp图谱、每个请求已匹配、Vector已消费 |

## 账号提供者和显式身份映射

Authentication3.9.0 `AuthenticationServiceInternal`从解码token的Subject设置PlayerId；外部Identity模型明确`TypeId=ProviderId`、`UserId=ExternalId`（IG72C18/28）。这是明确赋值，不是字段名联想。

Player Accounts的OAuth请求/返回、组织级账号和项目认证上下文分别保留（IG72C10—17）；官方支持跨games/devices/platforms和组织级player pool（IG72S02）。前提是用户登录、项目/组织正确配置及授权；同人跨设备需要同一个合法外部账户，不是从IP反推。

link/unlink有授权状态与身份冲突检查；官方说明已链接其他玩家时会报错，不是任意无声合并（IG72C14、IG72S03）。退出、clearCredentials、profile切换影响缓存与PlayerId；安装ID/Engine ID和玩家ID不能跨级等同，53—55号提供者结论保留。

## Ads身份的生命周期

设备ID和隐私字段按SDK配置/PII允许条件构造，当前是否有有效广告ID不能从SDK安装推定。安装/analytics ID来源可桥接，但Unity Analytics、Firebase FID、App Instance ID、项目ID不是同一个身份。

`impressionOpportunityId`是广告加载生命周期的键；`trackingToken`可变，operative eventId每次新建；旧事件构造值持久化后不被所查重试路径重新读取。它们能关联广告对象与反馈，不证明跨设备用户图谱，也不是经济收入账本主键。

没有公开链证明UPA组织ID→Ads gamer ID→RampID→Vector训练列；同包共存/同公司服务不构成join。

## RampID的真实契约边界

Unity2026-04-02公告原件明确美国、加拿大Exchange及支持RampID的接收伙伴共同支持，品牌/代理商可激活受众。LiveRamp整体服务有跨渠道解析/翻译能力；**256M美国月活设备是库存口径，非已成功匹配人数或匹配率**。

已核验Unity OpenRTB版本没有恢复具体RampID字段映射、输入ID→返回RampID的Unity专属契约；不能因标准支持eids就写成Unity每次请求已传该字段。不同伙伴命名空间/密钥和同意条件仍需材料。Exchange需求方受众激活不等于Vector自营模型收到相同输入。

## 价值预测用途

Vector有跨游戏行为模式、aggregate cohort insights及D7/D28产品用途公开说明（MA60S17、CGS42）；这些与聚合统计、共享模型参数、合法个人历史都可能兼容，不能唯一选择个人级架构。

所以可确认的是**账户图谱和第三方广告身份激活能力**；Vector实际个人级身份图谱、训练输入和四游戏启用仍UNKNOWN。必须保留“有契约”与“有生产成功”之间的差距。

来源、原包及源码SHA256、类/方法和行号见[目录](identity72-experiments73/SOURCE_CATALOG.md)；六级证据独立记录，没有E5/E6。
