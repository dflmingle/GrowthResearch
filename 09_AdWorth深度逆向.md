# Jewel Coloring：AdWorth 深度逆向

本轮增量审计：2026-11-18；原版 **1.24.1 / code 24 / ARM64**。原始XAPK、APK和so保持只读。以下“默认”均指该样本包内定义，**不是已观测的生产配置或事件上传**。

**核心答案：AdWorth 是嵌入 Bulldog 商业化框架的价值计量、条件筛选、加权和多平台事件分发模块。它确实能把行为与广告价值变成优化信号；但“正在按来源倍率、国家阈值给所有用户上报”的说法不成立：本轮恢复的90条默认事件没有引用来源权重表，也没有直接国家条件。**来源/国家能力、默认规则引用、线上实际启用必须分开。[D01–D05](EVIDENCE_INDEX.md#d01)

## 1. 本轮解决了此前缺失的配置

【代码证实】配置并非不存在，而是藏在 `assets/bin/Data/mainData` 的资源索引中。`BigFile::BigFile(bool)` RVA0x206ffa8 从包名初始化资源解码上下文；`setupConfFileRoot` RVA0x2070430 解析MainData；按原始变体RC4流程解析后得到protobuf映射，才能把逻辑文件名映射到无扩展名资源。**这是对本地原包资源的离线解析，未运行游戏、未访问配置后台。**[D01](EVIDENCE_INDEX.md#d01)

| 逻辑资源 | 原包内实际条目 | 恢复内容 |
|---|---|---|
| ad_worth_event.json | assets/bin/Data/76bfb5bbf13817586526c78ea06826ed | 44,580字节；90条事件、31张权重表；version=10.2.3、version_name=1.0.37、project_template_version=1.0 |
| dynamic_ad/ad_worth.json | assets/bin/Data/4cf2052c6808948ce8a5015b269070dc | 广告位价格表和国家×广告位bidder默认价格；package与本游戏一致 |
| adjust_name_token_map.json | assets/bin/Data/71cfaa19a8be85fbca1b50bf34b0c5f1 | 6个业务事件名称→Adjust token映射 |
| sdk_event.json | assets/bin/Data/be4221c008db51c5d15211bd6dfb7cf9 | ANA_kAdSourceGot、ANA_kGotUserIDFA、level/ad/app等原包事件配置 |
| ad_rule.json | 映射和哈希见provenance | 独立广告规则；包含play_time_sec<2400时的StopPreload规则定义，不是AdWorth价值计算公式 |

【代码证实】原始条目SHA256、解码结果SHA256、所在split和脚本见[decoded-config-provenance.json](jewel-coloring/deep/resources/decoded-config-provenance.json)。规则完整保存在[ad_worth_event.json](jewel-coloring/deep/resources/ad_worth_event.json.redacted.json)，90条可检索表见[rule-catalog.csv](jewel-coloring/deep/rule-catalog.csv)。配置版本字段不是“机制于该日期上线”的证明，亦不可直接当作游戏版本。[D01](EVIDENCE_INDEX.md#d01)

## 2. 它是谁的模块

| 判断 | 证据与结论 |
|---|---|
| 属于Adjust/AppsFlyer标准SDK吗 | **【代码证实】不是这些SDK的同名内置实现。**核心代码在libMyGame.so的`ad::event::* / ad::AdWorth*`；向Adjust是独立桥接调用。Jewel主DEX未发现标准AppsFlyer包和业务链。 |
| 是否只是某平台的薄封装 | **【代码证实】不只是。**它有本地累计账本、条件树、权重系数、时间点/频率、跨事件依赖、多平台输出与热更新。 |
| 可以确认的组件归属 | **【代码证实】嵌入Bulldog框架。**`BulldogSdk::_initBaseComponents`初始化；源码路径线索`g_sdk/BullDogClass/Classes_Ad/...`；Java桥引用`com.red.libbulldog.R$string`；和GTUser、BDHotUpdate、BulldogPlatform直接耦合。 |
| 是TaTa自研还是外购第三方SDK | **【无法确认】法律/商业所有者未证实。**Bulldog/Red命名说明技术组件关系，不证明谁开发、授权或维护；公开搜索仅取得空壳/重定向，没有可信供应商合同或官方产品说明。不得把它强行认作Metica、AppMetrica、Adjust或某个身份图谱商。 |

证据：[D02](EVIDENCE_INDEX.md#d02)。可接受的精确名称是“**随游戏静态链接的Bulldog商业化框架组件，封装多平台并提供自定义价值规则**”；“第三方/自研”的商业归属继续标未知。

## 3. 已追踪的类与调用链

【代码证实】本轮导出相关原生函数、原始RVA和直接调用，完整范围见[adworth-method-inventory.csv](jewel-coloring/deep/adworth-method-inventory.csv)、[method-index.json](jewel-coloring/deep/method-index.json)、[direct-callers.json](jewel-coloring/deep/direct-callers.json)。它覆盖可识别导出函数；接口/虚调用/匿名回调和隐藏符号不保证穷尽。[D02](EVIDENCE_INDEX.md#d02)

| 层 | 主要类/方法 | 数据责任 |
|---|---|---|
| 来源 | AdSourceUtils、AdSourceData、AdSource | 接收Adjust、Google referrer、Facebook来源等，按priority选当前来源，保存channel/subchannel/creative/country/price字段 |
| 广告价格 | AdWorthUtils、AdWorthRequestController | 广告位价格/国家默认值、服务端保存值、广告展示价格与统计；和底价/请求逻辑有关 |
| 事实统计 | AdWorthDataUtils、AdWorthStatistic、GameTimeDataMonitor、BulldogFile | 广告次数、价格累计、游戏时长、登录/安装年龄等 |
| 事件账本 | AdWorthEventDataUtils、worthWeightType | 多key累计、未发送value、每日value、权重表和状态 |
| 规则 | AdWorthEventUtils、AdWorthEvent、AWESingleCondition、AWECombinedCondition、各AWEC* | init资格、布尔树、关系运算、时机、事件是否已发、条件检查 |
| 发送 | AWESendPlatform、AWEWorthUpdate | 选择金额口径和接收平台，发送后减值/清零/时间更新，再更新事件状态 |

```text
广告展示/price回调
 → AdAdapterOnAdShowEvent::_recordTheAdShow
 → AdWorthUtils::hasDisplayPlacementWithPrice
 → AdWorthDataUtils::addUserTotalAdWorthForAdType
 → AdWorthEventDataUtils::addUserOldTotalAdWorthNum
 → 每个key：权重乘积 → 累计/未发送账本

BulldogSdk启动 / 3秒调度 / inter应展示或已展示的时机
 → AdWorthEventUtils → 时机与条件树
 → AWESendPlatform::_sendEvents
 → Adjust / Firebase / Meta包装器 / 条件化其他出口
 → 减interval或清零、时间戳、事件状态
```

【代码证实】`_scheduler` RVA0x1a18668 还检查首次版本门槛，满足后每3秒调度；不是所有事件每3秒发送。`checkEventSend` RVA0x1a2e680 先检查发送间隔，再虚调用条件树。发送状态在平台调用后本地更新，未见与服务端ACK组成事务。[D04](EVIDENCE_INDEX.md#d04) [D07](EVIDENCE_INDEX.md#d07)

## 4. 计算公式：价格、加权value和真实收入不能混为一谈

【代码证实】`_weightTheWorth` RVA0x1a22ae4 对适用该key的每个模型取系数，执行`fmul`累乘：

```text
weighted_increment(k,t) = input_worth(t) × ∏ coefficient(model,k,local_state(t))
total(k) += weighted_increment(k,t)
unsent(k) += range_filter(k, old_total, new_total, weighted_increment)
USD_view(k) = unsent(k) / 1000
```

`_addUserOldTotalWorth` RVA0x1a24b80更新累计；`_rangeByTotalSentWorth` RVA0x1a23330可按配置累计区间裁剪；`getUnsendWorthUSD` RVA0x1a21584实际除1000；不能把每个key都简化为无条件同一笔原始收入。[D03](EVIDENCE_INDEX.md#d03)

【代码证实】输入来自广告展示价格记录链；`dynamic_ad/ad_worth.json`包含198个广告位价格和国家bidder默认值，并有保存服务器数据/请求价格路径。**因此AdWorth的worth不是天然等于已结算、精确实收ILRD：在不同广告路径可能使用价格/估值。**尤其加权后的worth是开发者代理价值，不是广告网络额外支付的钱。当前未取得每条广告provider在生产中使用实值或回退值的完整运行trace。[D03](EVIDENCE_INDEX.md#d03)

### 来源权重：能算，但当前默认事件没用它

【代码证实】`_getCoefSubChannelWeight` RVA0x1a24498读取当前subchannel，按配置字符串做正则匹配；未匹配默认1，匹配后使用数值。恢复的表：

| 正则 | 系数 |
|---|---:|
| .*RIG.* | 1 |
| .*MIG.* | 5 |
| .*NMG.* | 10 |
| .*POG.* | 20 |

**【代码证实】表名`subChannelWeight1_fb_purchase`存在，但90条events的weightWorth.type中没有引用它。**同样不能把RIG/MIG/NMG/POG解释成已核实投放平台、国家或用户身份；没有命名约定证据。若未来热更新引用此表，才可能改变相应key的加权增量；本轮没有生产更新快照。[D01](EVIDENCE_INDEX.md#d01) [D03](EVIDENCE_INDEX.md#d03)

### 行为权重：默认确有引用

【代码证实】默认存在49处weightWorth条件，使用登录/安装年龄、今日或非首日时长、时长排名、登录日数、插屏展示率等模型。例：`loginDay2`为0→1、1→1.5、2→2、3→3、4→6、5→9、6→12；`dayTime`为0→1、30→1.5、40→2、50→2.5、60→3。`_getCoefLoginDay`与`loginDayMax`边界逻辑不同：前者超过最大表日数可回退1，后者保留末档，不应统称无限封顶放大。[D01](EVIDENCE_INDEX.md#d01) [D03](EVIDENCE_INDEX.md#d03)

【合理推断】这是手工配置的行为价值模型，而非已证明的机器学习LTV。它借助留存/参与去放大或筛选已产生广告价格价值；不需要跨应用行为作为必要输入。XGBoost模型另存在于dynamic_ad广告策略资源，未建立它预测AdWorth或用户长期收入的证据链。

### 国家与用户分层

- 【代码证实】AWECCountry按国家集合判断；AWECCostRecovery检查countryWorth>0，再比较`userTotalAdWorth/1000 >= countryWorth`；**当前90条默认事件没有country/costRecovery规则，也未恢复到countryWorth默认值表**。不能把该能力说成当前国家优化门槛。[D04](EVIDENCE_INDEX.md#d04)
- 【代码证实】国家×广告位`bidder_default`实际存在，例如US两项为7.95、16.48；这是广告价格相关默认值，**不是CPI、ROAS或用户价值转化阈值**。[D01](EVIDENCE_INDEX.md#d01)
- 【合理推断】即使默认事件没有直接国家条件，不同国家广告价格仍可能间接改变worth累计与达标速度；不能据默认价格表量化实际生产差异。
- 【代码证实】AWECUserGroup比较`BulldogSdk`的group字段；它不是个人身份图谱。默认events无userGroup条件。另有事件通过customInt输出本地/GTUser标签，这与广告框架的userGroup条件、游戏奖励分支不应混淆。[D04–D06](EVIDENCE_INDEX.md#d04)

## 5. 默认规则中最有意义的实际例子

| id | 包内触发条件 | 默认输出 / 金额口径 |
|---|---|---|
| 1 | init appType=iaa；尚未发；插屏展示≥5 | Firebase ANA_kRedGeneralEvent_LV、Meta idx1、Adjust RedGeneralEvent_LV；customInt[21]=1。注意eventName残留“Day020T150Inter20”不等于真实条件 |
| 18 | day0～6；event1已发；未发worth key5≥$0.10 | Firebase/Meta custom ANA_kRedGeneralEvent_AdWorth01、Adjust同名；发送normal value后清零 |
| 19 | key4未发worth≥$0.01 | Firebase ANA_kRedGeneralEvent_AdWorth001，normal后清零 |
| 23 | 安装/首开时间限制<24h；累计游戏时长间隔≥5分钟；key23≥0 | Meta idx10使用x100；Adjust adjust_D0；时间加间隔、worth清零 |
| 333 | init day0～13；游戏时长间隔≥10分钟；登录年龄最大档×非首日时长的加权worth>0 | Firebase ANA_AdWorth001_kLoginDays_Time_14D_E0，normal后清零 |
| 422 / 423 | day0～29；时长间隔≥10分钟；插屏展示率≥0.4/0.6、登录日率>0.4、平均插屏eCPM>1/>5及加权worth>0 | ANA_LoginEvent_TUser / ANA_LoginEvent_Rich_TUser；组合参与和价格筛选 |
| 504 / 505 | 插屏≥30且最高关≥50 / 插屏≥40且最高关≥60；尚未发 | MiddleLV / BigLV同时发Firebase、Meta custom、Adjust |
| 508 | day0～6；平均插屏eCPM>3、展示率>0.7、最高关≥30、时长间隔≥10分钟、加权worth>0 | Firebase D7T_S；customInt[20]=1；normal后清零 |
| 509 / 510 | worth≥$0.01且最高关≥50/30 | Firebase VO_S/VO_S2；customInt[20]=1；normal后清零 |
| 514 | init appType=iaa；key514未发送worth≥$0.10 | **Meta idx8→logPurchase(USD,value)**，随后清零。这是广告价值映射为purchase语义，不能当真实IAP订单 |

【代码证实】这些例子逐项来自原包JSON并对应原始条件/分发代码。49处weightWorth不是49个已观测活跃事件；init、当前appType、版本、时机、平台初始化/隐私和热更新都可能影响触发。[D01](EVIDENCE_INDEX.md#d01) [D04–D05](EVIDENCE_INDEX.md#d04)

Adjust映射已恢复：RedGeneralEvent_LV=`8pts6u`；ANA_kRedGeneralEvent_AdWorth01=`cdhgtw`；adjust_D0=`4soer9`；adjust_D7=`py56uo`；MiddleLV=`4mg2kf`；BigLV=`98xz5e`。这是事件标识，未使用或发送。**配置定义了多个不同语义出口，后台究竟注册什么名称/目标仍未知。**[D01](EVIDENCE_INDEX.md#d01)

## 6. 输出到底去哪里、是否改变游戏

【代码证实】默认sendPlatform定义覆盖Firebase 65条、facebookCustom 43条、facebook索引5条、adJust 7条；另外worthUpdate/timeUpdate/customInt是本地状态动作，不是广告平台。部分规则同时命中多个出口，计数不能相加当成不同事件数。TikTok/Google ARO在原生发送器中有能力，但这90条默认定义没有对应出口。[D01](EVIDENCE_INDEX.md#d01) [D05](EVIDENCE_INDEX.md#d05)

`AWEWorthUpdate::getBeSentWorth` RVA0x1a3dc50区分normal未发值、interval值、x100、每日分量和其他倍率；`AWESendPlatform::sendMsgToPlatform`先`_sendEvents`，再`_updateSendedValueAndData`；AdWorthEvent随后写本地已发/时间状态。**这是本地发送尝试，不是后端确认。**[D05](EVIDENCE_INDEX.md#d05)

【代码证实】customInt进入GTUser；来源priority也会进入GTUser。广告规则/预加载层另有读取GTUser group的路径。**【无法确认】本轮未建立“AdWorth某个输出标签→实际改变奖励数量/广告频率”的完整读写链。**原包`ad_rule.json`可以按单应用游玩时长控制StopPreload，这是独立广告策略，不等于AdWorth value本身决定奖励。没有证据证明源权重20导致给用户多播20倍广告。[D06](EVIDENCE_INDEX.md#d06)

## 7. 输入来源、默认/热更/生产的边界

| 输入 | 证据状态 |
|---|---|
| Adjust network/campaign/creative/costAmount | 【代码证实】Java listener→AdSource JNI；costAmount不是完整获客成本账本 |
| Google Install Referrer / broadcast | 【代码证实】AdSource桥接实现和native接收分支 |
| Facebook deferred link / referrer来源 | 【代码证实】客户端接口与native分支；本轮未访问content provider或解密真实归因结果 |
| AppsFlyer | 【无法确认】本样本未发现标准SDK或其输入业务链，不把Adjust字段改称AppsFlyer字段 |
| 国家 | 【代码证实】设备/IP/来源等代码路径；网络结果未采集，不证明具体用户所在地 |
| 广告价格/收入 | 【代码证实】展示→价格累计→事件账本；精确ILRD/回退估值逐provider生产占比未知 |
| 登录、时长、进度、广告次数/率 | 【代码证实】单应用本地统计与GTUser/BulldogFile/GameTimeDataMonitor |
| 配置 | 【代码证实】包内资源、保存服务器价格、热更新监听/重新初始化；各份在线实际内容未获取 |

【代码证实】`_addConfigUpdateListener/_reinitializeEvent`连接BDHotUpdate；price层`readEcpmFromServer`支持网络取得价格。**尚未证明Firebase Remote Config直接覆盖任意AdWorth事件JSON**；不能把同包存在RC API直接连到这份规则。[D07](EVIDENCE_INDEX.md#d07)

## 8. 历史演进与验证上限

【公开资料证实】本轮额外查询Aptoide：Jewel包名未找到、versions为空；尝试APKPure历史code23/22均403，记录于[history/attempts.json](jewel-coloring/deep/history/attempts.json)。未绕过限制。[D08](EVIDENCE_INDEX.md#d08)

【无法确认】没有取得可验证历史APK，因此机制首次出现时间、配置演进和上线日期无法确认。`230601/230706`等事件名、配置version_name=1.0.37只说明内部命名/版本线索，**不能当作历史上线记录**。

最终判定：**【代码证实】该机制已把单应用参与/留存与广告价格价值转换为多平台优化候选信号；【代码证实】架构支持来源和国家；【无法确认】默认未引用的来源权重、国家条件是否被生产热更启用、广告后台是否用于出价。**这比“AdWorth就是身份图谱”或“不同渠道一律乘20”更接近实际证据。
