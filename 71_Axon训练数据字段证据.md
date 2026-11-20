# 71号：Axon训练数据字段证据

2026-11-20。**找到的是公开接收/转发字段契约和模型输入类别，尚未取得Axon生产训练表、字段转换或标签生成规则。** 本轮不能把`revenue_usd`等伙伴字段直接标为已入模。

## 什么已经公开到字段级

| 数据层 | 可核验字段/类别 | 最强证据 | 能确认与不能确认 |
|---|---|---|---|
| MAX响应及本地收入通知 | 完整响应event_id→基础广播id；revenue_parameters和ad_values合并 | L71C01—04、CL70C18—24 | 明确客户端赋值；最终覆盖/订阅/网络去向未知 |
| Adjust→Axon伙伴postback | revenue_usd、is_organic、match_type、impression_based、app_name、partner_parameters | L71D01 L212—249 | 伙伴出站契约；不是训练列清单 |
| 身份/上下文伙伴字段 | idfa或gps_adid、idfv、android_id、ip_address、device_name、os_name及归因窗口 | L71D01 | 文档允许的字段契约；受平台/用户授权及可用性限制，不是每次都有值 |
| AF→AppLovin购买链 | checkout、Values & revenue、真实直接付款；landing/postinstall有其他口径 | CGS49/52 | IAP/付费收入共享规则；该checkout链明确排除IAA和预测LTV |
| 官方模型类别 | 自家广告互动；MAX给予参与竞价者的赢/输通知；广告主选择共享的数据 | CGS51 | 官方明确说models使用这些类别；无法逐字段绑定上述入口 |
| 广告主特定价值/未来多日预测 | 00—63号官方证据保留 | 60—63号及MA60矩阵 | 产品用途/架构轮廓；未公开实际分布目标、完整训练标签/版本 |

出处：[Adjust官方伙伴说明](https://help.adjust.com/en/partner-setup/applovin)的既有已核验原件，新增精确摘录L71D01；[Axon官方数据使用声明](https://legal.applovin.com/about-applovins-axon-ai/)为CGS51；全部哈希及片段见[证据目录](lineage71/SOURCE_CATALOG.md)。

## 已收集、已转发、已关联、已训练分别判断

1. SDK能构造相关字段：有代码证据。
2. Adjust可按配置将字段转给Axon：有官方伙伴契约。
3. 目标四游戏实际配置且平台收到：UNKNOWN。
4. 某经济展示、收入、归因安装成功join：UNKNOWN。
5. 该行进入具体训练表/特征列/成熟标签：UNKNOWN。
6. 某模型版本据此提高出价质量或利润：UNKNOWN。

产品级“models use advertisers' data”不能把第2层所有字段升级为第5层；也不能证明无授权跨业务混用。

## 本轮最有用的新连接和反证

MAX的`u().b(c3)`已定位到CommunicatorService收入广播。因此load后缀路径虽然没有公共`onAdRevenuePaid`，**可以条件发布本地收入topic**。这是新的MMP订阅入口线索；不是本次真实经济展示或训练数据已经产生。

广播基础ID来自完整响应，候选可共享，且合并可覆盖；官方serve唯一性文案不等于账本约束。账户S2S另有EVENT_ID/TS/PRECISION宏及无重试规则（L71S01/02）。两套接口不能因名字相近就拼成一个生产主键。

Adjust广告收入通路没有自动继承一般事件deduplicationId检查；官方MAX→Adjust例子未传ID/precision（L71C07—14、L71S03/05）。因此“某MMP支持收入”不足以证明完整、精确、不重复标签。AppsFlyer也公开提醒多收入路径重复风险（L71S07）。

## 官方排除项不能被竞争性推断推翻

CGS51明确排除敏感个人信息、受保护特征，以及**其他竞价者的出价和其他竞价者的用户数据**进入模型，并有儿童数据限制。因此不能从MAX看得到多个竞价结果，推出Axon拿竞争对手全部报价或用户行为训练。

赢/输通知的官方用途有支持，实际通知携带哪些字段、何时以何种粒度入模仍未知。安装后IAA/IAP是未来机会的历史候选，不能倒灌给获取该用户的原始广告机会。`is_organic`说明来源分类，不证明所有自然量都已进入该广告主模型。

## 当前训练字段结论

**没有任何新增证据达到“某个具体来源字段已进入Axon某训练列”的生产血缘等级。** 已比70号更具体地知道客户端通知入口、MMP出站字段和收入类型排除项。

最值得索取：平台授权的数据字典或无需真实值的血缘表，列`来源事件/ID→接收字段→去重键→标签定义/成熟窗口→适用广告主/模型版本`。若只能提供营销案例或泛化模型介绍，应停止这个断点的公开检索，保持UNKNOWN。
