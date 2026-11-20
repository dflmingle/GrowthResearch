# 72号：Axon / Vector训练血缘补证与未解断点

2026-11-20。**取得新的可公开引用的一手契约，实质补齐收入导入→版本修正→归因cohort→伙伴共享的若干规则；没有取得运营方授权的实收日志、后台导出或平台训练表。** 如果将本轮完成标准限定为上述授权生产材料，该标准尚未达成。公开契约推进与生产证实分开记账。

## 本轮真正新增的连接

### 1. SDK收入不一定是最终标签版本

AppsFlyer官方ROI360文档（更新2026-11-19；L72S01）说明：

- SDK展示级接收不保证最终仍以展示级报告；可按设备聚合。
- 混合模式先用SDK数据满足Day X时效，随后用API设备级收入替换；Android无可用设备标识的SDK数据不会被该API数据替换。
- Aggregate API按国家/日收入除触发次数生成eRPA；这是分摊估计，**不是观察到某玩家或某次展示真实赚了该金额**。

因此不能把早期SDK回调、后到API、MMP报表各当独立收入直接相加；也不能拿某次导出的最终值冒充当时就可用的特征。L72S04进一步说明不同报表更新节奏不一致，S2S修订可发生在D1/2/3/7/14，部分raw export/Pull工具不会像可修订报表一样回填。

这补齐了**标签版本/迟到修正契约**，不是证明Axon/Vector实际使用哪个版本。

### 2. “开启去重”有严格适用范围

L72S02：跨两个mediation互相引用的去重选项适用于指定API场景，不能当作所有收入的全局恰好一次开关。该设置忽略SDK展示级集成，也忽略MAX/LevelPlay的设备级API集成；官方称这些路径在该类交叉重复问题上无需去重。

这段说明不保证开发者重复调用、手动`af_revenue`、多connector、不同账本镜像都被去重。71号Adjust一般事件dedup与专用AdRevenue的区别仍有效。

Adjust新增官方说明（L72S11）：API按账户拉取，可能在Android API与iOS SDK分别配置时仍取得iOS API数据；**Ad Revenue Sources filter**可以分别用于报表、partner sharing、conversion mapping。它是来源筛选契约，不能升级为已按经济展示主键消除重复。

### 3. MMP→广告网络有两个不同出口

AppsFlyer《Share ad revenue data with partners》（2026-09-15；L72S05/06/07）明确：

| 出口 | 官方时效/常见用途 | 条件与边界 |
|---|---|---|
| UA signals | 日级；常见D3/D7优化 | ROI360 Advanced；partner激活、权限；混合配置时发送设备级数据 |
| ad revenue postback | 实时；常见D0/D1优化 | SDK展示级或混合模式；显式选af_ad_revenue并映射；“Select all events”会排除它 |

“常见D0/D1或D3/D7”是文档用例，不能当厂商训练窗口的完整定义；也不能宣称D28不能用其他数据。

**all-source不等于所有竞争渠道归因详情共享。** 官方明确：其他渠道的事件在选择all-source后不带其归因数据。能共享部分收入/样本，不等于收到对手campaign、竞价或完整用户画像。

### 4. MAX作收入来源，不等于Axon作接收方

该官方页面把MAX、Unity及LevelPlay列为mediation数据来源；接收网络是另一张表。新原件明确列Unity Ads可接收UA signals与postbacks，并规定`af_ad_revenue→ad_revenue`。

**此快照接收表未列AppLovin/Axon。** 不能用MAX位于来源列表证明Axon也支持这两条同样出口；同样不能凭一张表的缺席断言Axon普遍不支持IAA优化。Axon另有71号Adjust伙伴字段和官方自愿共享类别，但专用IAA出站/入模链仍需独立契约。[结构化表提取](access72/PARTNER_TABLE_EXTRACT.json)保留来源表/映射表/接收表的区别。

### 5. 从活动报表到安装cohort需要重建

L72S03/08/10：收入归因报表可以复制原conversion的media source/campaign上下文；AppsFlyer ID作用于安装实例，卸载重装可能换ID；LTV按安装日期分组，raw activity按事件日期分组。故不能把某个月活动收入直接当该月安装者的成熟D28 LTV。

文档中的network/ad unit/placement组合用于描述聚合上下文，不能直接解释成全球唯一经济展示主键。相同广告位可连续展示多次。

L72S09：device_event_time是设备时钟，original_event_time涉及截断/迟到处理，某些报告的event_time还可能按小时取整；这些都不能自动替代**模型当时可用时间available_at**。现有数据没有接收/特征版本水位，仍无法做生产bid-time效果验证。

## 对两家的最终证据状态

| 层级 | Axon | Vector/Unity |
|---|---|---|
| 客户端构造 | 71号MAX广播、MMP金额路径已证 | 71号机会、事件快照、持久化路径已证 |
| 官方转发契约 | Adjust→Axon字段及来源范围；IAA专用出口仍缺 | 本轮独立MMP文档确认Unity接收双出口及事件映射 |
| 目标游戏配置/实收 | UNKNOWN | UNKNOWN |
| 归因安装与经济收入去重 | 仍缺真实schema和对账材料 | 仍缺真实schema和对账材料 |
| 模型用途 | 官方广告互动、赢输通知、自愿共享数据类别 | 官方事件类别、预启动学习、D7/D28产品用途 |
| 物理训练列、标签版本、模型版本→出价 | UNKNOWN | UNKNOWN |

不存在新增证据允许声称四游戏已在某平台入模、某类别改进了预测精度或买量利润。

## 仍需哪份授权材料

最小交付可以不含个人值：伙伴配置导出/审阅说明；原始经济键→MMP事件键→安装实例键的基数；数据源/precision/修订与去重规则；接收ACK及可用水位；训练目标列/窗口与模型版本→决策版本。现有公开文档只能补接口语义，不能代替这些实际记录。

来源及原件哈希：[证据目录](access72/SOURCE_CATALOG.md)。没有重复SDK分析，没有生产请求，没有新收集用户标识。
