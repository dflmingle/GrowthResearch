from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'prediction-system'
g=json.loads((R/'EVIDENCE_GRAPH.json').read_text(encoding='utf-8'))
S={x['id']:x for x in g['sources']}

def refs(*ids):
 return ' '.join(f'[{i}]({S[i]["path"]})（原文L{S[i]["start_line"]}—{S[i]["end_line"]}）' for i in ids)
def write(name,text):
 (ROOT/name).write_text(text.strip()+'\n',encoding='utf-8')

write('41_核心模型证据拼图总览.md',f'''
# Axon / Vector核心预测系统：证据拼图总览

2026-11-19。基于00—40号原研究，新增公开招聘、专利及反面材料调查。**能够证明双方用价值预测指导出价；不能证明已恢复完整跨来源用户表示、训练标签表或服务端模型，更不能据此评出哪家预测更准。**

## 本轮得到的实质连接

| 连接 | Axon | Vector |
|---|---|---|
| 多来源数据→模型用途 | 【官方公开证实】设备/网络、应用/广告/数字属性互动、伙伴及自愿广告主数据；自身MAX赢输标通知 | 【官方公开证实】游戏DNA、玩家行为及生态数据；MMP安装/会话/购买/广告收入；IAP/D2C购买数据可丰富模型 |
| 身份→具体安装前特征 | 【SDK代码证实】有标识共封装；【无法确认】具体join及快照 | 【SDK代码证实】有ID、token及隐私分支；【无法确认】UPA/RampID到Vector的连接 |
| 真实价值→学习 | 【官方公开证实】IAA/IAP/Blended ROAS及MAX/MMP产品链；【无法确认】内部标签表 | 【官方公开证实】收入潜力预测、成熟cohort和D0/D7/D28窗口；【无法确认】内部loss和逐条标签血缘 |
| 预测→出价 | 【官方公开证实】按该展示对特定广告主的价值出价 | 【官方公开证实】按预测收入潜力与tROAS动态出价 |
| 用户表示与特征平台 | 【间接技术线索】招聘明确representation、embeddings、multi-task、feature serving | 【间接技术线索】Vector建模、在线推断、bidding/pacing及市场价格预测团队 |

主要原始依据：{refs('S01','S02','S12','S13','S14','S21','S25','S26','S28','S29')}。

## H1—H5判定

| 假设 | 判定 | 最关键的限制 |
|---|---|---|
| H1 跨应用行为和身份关联提供有效特征 | **部分支持，增益未证实** | 官方允许/披露跨属性行为用途不等于具体历史已join，更不证明身份特征产生增量ROAS；无统一真实消融 |
| H2 真实IAA/IAP构成LTV标签 | **产品学习路径有直接支持，内部实现未恢复** | Unity成熟窗口尤其明确；Axon收入链不可把IAA塞入purchase；两家标签去重、缺失和归因冲突处理仍未知 |
| H3 用户/应用/广告/历史价值关联预测新用户价值 | **总体用途已证，具体表示仅间接支持** | 不能把招聘里的Embedding、多任务学习或旧专利升级为已部署架构 |
| H4 预测价值→报价→反馈 | **产品层闭环已证，数值与在线更新未知** | 实时CPM函数、预算pacing、探索率、反馈训练延迟无可核验生产trace |
| H5 存在可验证差异 | **产品/接口/证据范围有差异，效果优劣无法确认** | 不知道双方覆盖率、匹配准确率、标签噪声和同条件边际ROAS，不能把披露多少当成实力排名 |

## 阅读与复核

- [42 Axon](42_Axon跨来源数据与价值预测证据.md)：包含本轮新增Ad Review训练排除声明、用户表示招聘及旧专利边界。
- [43 Vector](43_Vector跨来源数据与价值预测证据.md)：包含Vector专属招聘中的在线推断和竞价/pacing线索。
- [44 关系图](44_身份行为价值关联图谱.md)：每条连接的提供方、接收方、原文定位、条件和断点。
- [45 反证与断点](45_关键断点与反证清单.md)、[46 重建与可信度](46_双方预测系统重建与可信度.md)。
- [机器可读图](prediction-system/EVIDENCE_GRAPH.json)：31节点、38条边、40条原始/追溯证据；[精确摘录](prediction-system/SOURCE_EXCERPTS.json)。

图中实线只表示**在所述范围内有证据**，例如SDK具备能力或官方声明用途；不等于观察到生产传输。所有`production_actual_proven=false`，另以`production_evidence`保存官方生产用途陈述，避免混为独立审计结果。未连接任何生产广告服务，未读取个人标识。
''')

write('42_Axon跨来源数据与价值预测证据.md',f'''
# Axon：跨来源数据、用户表示与价值预测

2026-11-19。**已证“允许的数据类别→预测用途→价值出价”；仍缺“哪条历史→哪一用户表示→哪个训练样本”的内部血缘。**证据关系图A01—A20。

## 1. 官方直接确认的训练输入及边界

Axon官方说明明确使用设备/网络信息、App/广告/其他数字属性互动、伙伴共享数据、广告主自愿共享用户数据，以及自身收到的MAX赢/输标通知；持续训练优化并按特定广告主价值决定出价。隐私政策还披露跨App/设备信息收集与结合、过去App或网站行为用于广告相关性。**【官方公开证实】**这是模型用途层证据，超过“仅收集SDK字段”，但没有列出每个具体feature及join键。{refs('S01','S02','S03','S04')}

**反面边界有明确新证据。**2026-09-16 Adam Foroughi的官方文章直接写：Ad Review不据此建立用户/设备档案，不把该数据输入Axon或其他AppLovin模型；其他网络的广告输出不用于其训练，并移除用户级journey展示。Axon说明另排除其他bidder的出价/用户数据、敏感信息、受保护类别和儿童数据。**【官方明确排除】**不能因MAX能看到候选/广告审查信息，便认定Axon学习了全行业用户级广告输出。该排除针对来源和用途；不否定广告主合法授权的实际广告收入反馈。{refs('S24','S01')}

## 2. 身份与历史关联：可证到哪一层

| 层 | 原始依据 | 判定 |
|---|---|---|
| 获取标识 | MAX13.6.4 `sdk.m.a(Map,boolean)`、`t7` | 【SDK代码证实】GAID、AppSet、CUID分别受可用性/配置约束；Android字段名idfa/idfv不能当苹果标识 |
| 同一请求共封装 | collector与CUID manager | 【SDK代码证实】可构成关联输入，不证明后台已join；AppSet和发行商ID受作用域限制 |
| 过去跨属性行为→模型总体用途 | Axon说明、隐私政策 | 【官方公开证实】类别用途；具体来源集合、历史长度、跨设备置信度未披露 |
| 用户表示→Axon特征表 | ML招聘 | 【间接技术线索】有工程方向，缺实际部署/数据血缘 |
| 电商身份+订单→高价值新客 | 订单历史官方指南 | 【官方公开证实】电商客户建模；不能跨成手游IAA模型默认训练 |

{refs('S32','S33','S04','S11')}。详细Pixel/CAPI静态路径复用[31号](31_AppLovin设备身份图谱.md)，本轮不重跑身份采集。

## 3. 本轮新增：用户表示和特征基础设施招聘

公开Greenhouse API取得45条职位，官方原始JSON保存在[prediction-system/applovin-public-jobs.raw](prediction-system/applovin-public-jobs.raw)，职位更新时间均按API字段记录，不能当初次发布日期。

| 职位/原始定位 | 实际文字 | 可得结论与禁止推断 |
|---|---|---|
| Software Engineer, Machine Learning；`jobs[id=4712559006].content` | user signals、representation learning、ranking/retrieval、embeddings、feature interaction、multi-task learning、离线/在线增量实验 | 【间接技术线索】广告平台研究方向；没有明确Axon模型名称/版本，不证明某种Embedding生产部署 |
| ML Data Infrastructure Engineer；`4716524006` | model training and feature serving、从raw ingestion到feature delivery、reproducibility/traceability；Spark/Flink及feature store为技能项 | 【间接技术线索】团队职责包含训练/服务数据链；不能据此写已采用某厂牌feature store或训练频率 |
| Measurement Data Scientist；`4705264006` | platform/3rd-party/internal attribution、MMM/MTA/incrementality/RCT/GeoLift | 【间接技术线索】存在测量需求；不证明当前投放报告都经过增量校正 |

{refs('S25','S26','S27')}。更新时间2026-11-05；本次公开获取2026-11-19。

## 4. 真实收入与代理价值不能混用

MAX `onAdRevenuePaid()`提供金额与precision：`exact`来自实时拍卖，`estimated`、`publisher_defined`质量不同，不能统称最终财务结算收入。官方支持ILRD共享给MMP，Ad ROAS产品要求live app、MAX、MMP、素材和目标。**【SDK/API证实】【官方公开证实】**由此能支持IAA价值优化产品链；**【无法确认】**具体ILRD行进入何训练表、窗口、loss、退款/无效流量回溯及数据缺失处理。{refs('S05','S06','S07')}

IAP指南只接受用户真实支付；明确排除广告收入、预测收入和预测LTV。Adjust/AF需要伙伴共享、来源范围、事件映射，AF指南中的checkout不能拿来装IAA或GRT/AdWorth代理金额。**MMP接收某事件≠AppLovin收到≠已用于训练。**{refs('S08','S09','S10')}

## 5. 专利、论文与工程文章的证据上限

取得US20130159103A1 *Advertisement Selection Based on Mobile Applications*：优先权2011-12-16、公开2013-06-20，发明人Adam Foroughi、John Krystynak、Andrew Karam、Furqan Rydhan、Matthew Bornski。文中描述已安装App列表、特征及使用级别辅助广告选择。**【专利间接线索】**只是早期构想，不证明现代Axon调用安装列表，也不能覆盖现代权限限制。Google Patents页面标注Abandoned并声明法律状态非法律结论；本报告不作法律有效性判断。{refs('S31')}

没有取得可明确归属现代Axon的生产模型论文/技术会议完整实现。已有ESMM/MMoE等[公开论文](ltv/fetches-model-literature.json)只能提供行业路线，不可归属Axon。公开招聘把表示学习作为方向，也不能补成论文中的MMoE具体架构。

## 6. 目标游戏与下一条关键证据

四款游戏的MAX变现、MMP收入链及本地价值规则已有静态证据；仍未建立“具体游戏价值规则→MAX EventService→结构化Axon”的显式业务链，也未取得伙伴postback送达/训练用途日志。**【无法确认】**这不否定服务器集成，却禁止把游戏规则图直接连到Axon训练。{refs('S39','S40')}

最值得获取：**经授权、脱敏且带字段血缘的MMP/MAX收入→Axon训练用途说明或技术案例**，同时给出安装前特征时间、水位及幂等规则。仅增加SDK字段无法补这个断点。
''')

write('43_Vector跨来源数据与价值预测证据.md',f'''
# Vector：跨来源行为、收入学习与实时出价证据

2026-11-19。**相比“Unity有引擎所以掌握所有玩法”的推断，可靠证据是：玩家/游戏信息的产品用途、明确收入窗口与成熟cohort、MMP接口，以及Vector专属的建模和竞价团队说明。**

## 1. 已直接披露的数据与标签链

Vector页面写game DNA、real player behavior、ecosystem data，并推荐MMP发送attributed/unattributed installs、sessions、purchases、ad revenue及lifetime postback window。**【官方公开证实】**这是明确的数据供给建议与模型用途描述；不表示任意游戏默认开放全部数据。{refs('S12','S13')}

ROAS文档明确用机器学习预测每位用户收入潜力并动态出价，支持Ad Revenue D0/D7/D28、IAP D7/D28、Hybrid D7/D28。D28当前文档仍有beta标记。D28公告明确预测28天广告收入并按国家tROAS调整报价。**【官方公开证实】**预测目标和反馈窗口，不是无限生命周期LTV，也没有公开逐样本loss。{refs('S14','S15','S22')}

| 学习环节 | 直接证据与限制 |
|---|---|
| 事件关联 | S2S `gamer_id/aid/ifa`、`campaign_id`、广告主`game_id`、`install_ts`、归因标记；可追踪输入接口，不证明实际join成功 |
| 收入语义 | `event=ad_revenue`或`purchase`及amount/currency；session不是收入；对增量或累计需MMP契约明确 |
| 成熟度 | 文档例子D0 1月1日→1月3日成熟，D7→1月10日，D28→1月31日；不能把窗口结束直接视为当时全部数据已到齐 |
| 学习门槛 | IAA 1000归因安装且成熟广告收入>0；D28 IAA当前表使用D7成熟收入；IAP 75位D7成熟付费者；Hybrid 1000安装+正D7广告收入+35位D7付费者 |
| 仍未知 | 内部去重键、退款回滚、事件迟到窗口、归因冲突、截尾/缺失建模及每标签权重 |

{refs('S18','S19','S16','S17')}。custom S2S文档关于IDFA等存在历史/接口特定表述，不能据此推翻ATT或认定所有受限iOS请求都有IDFA。

## 2. Runtime与购买服务：两条不同证据

- **【官方公开证实】**Developer Data的collection、usage和end-user intent分别约束使用；`ads_intent=denied`限制广告专用标识及个性化用途，不能把未设置解读为全部广告授权。**【无法确认】**某Runtime事件的native采集→Vector特征/标签完整血缘。{refs('S20')}
- **【官方公开证实】**2026-07-21 Unite Seoul回顾明确IAP SDK/D2C购买数据可丰富Vector寻找未来玩家。它比笼统“引擎数据”更具体，但仍是“can help enrich”，不能升级为四款目标游戏已启用。{refs('S21')}

Ads SDK4.17.0的`AndroidStaticDeviceInfoDataSource`、`AndroidPrivacyDeviceInfoDataSource`和shared request可追踪安装ID、LevelPlay AUID、同意与允许的PII。**【SDK代码证实】**请求构造；**【无法确认】**它们如何被转换为Vector安装前表示。{refs('S34','S35','S36')}

## 3. 本轮新增：明确归属Vector的公开招聘

由Unity官方careers页面SSR发现Workday职位，再读取公开职位详情，未登录或绕过访问限制。原文JSON和`jobPostingInfo.jobDescription`定位随证据图保存；`startDate/postedOn`按原字段保留，不猜首次发布日期。

| 团队/职位 | 原文技术线索 | 可信边界 |
|---|---|---|
| Vector Bidding Science，JOBREQ-2616286 | real-time bidding、bidding/pacing algorithms、bid landscape forecasting、离线/在线A/B；RL/control theory、survival analysis为技能要求 | 【间接技术线索】业务分工和研发范围明确；不能证明已部署强化学习或某种市场价格算法 |
| Vector Gamer AI推断基础设施，JOBREQ-2615964 | 广告排序及bidding决策、低延迟高吞吐online inference；GCP/Kubernetes/Golang/监控，Triton为加分项 | 【间接技术线索】文中陈述生产职责，强于行业猜测；仍未独立验证部署，不能把Triton加分项写成已使用 |
| Vector Ads Modeling，JOBREQ-2616596 | user behavior modeling、rich user data、large-scale compute、research→production | 【间接技术线索】建模方向，未公开Embedding结构或具体跨App表示 |

{refs('S28','S29','S30')}。本轮将其统一放D级，不因官方发布就升级为生产架构证明。

## 4. 反证与身份隔离边界

UPA明确组织内跨游戏/设备账号；RampID明确美加Unity Exchange受众激活且双方支持。**【官方公开证实】**两项能力；**【无法确认】**UPA→RampID、UPA→Vector、RampID→Vector的训练连接。Exchange的品牌受众激活不等于Vector手游获客模型。{refs('S37','S38')}

## 5. 效果证据不能替代因果拆分

D28公告给出2026-03-08—04-08内部closed-beta的配对D7对照，属于官方匿名化案例方法线索，非本研究独立授权实验：按游戏统计留存和ARPU改善比例；未给完整成本、样本/随机化/置信区间，不能计算统一ROAS，也不能将提升归因于Runtime或身份。{refs('S23')}

下一条最有价值证据是**带数据字典和用途开关的Runtime/IAP事件→Vector训练集血缘**，同时有“禁用这类特征”的真实消融。再取得一份SDK token字段并不能完成该证明。
''')

diagram='''```mermaid
flowchart LR
 AC[Axon合法设备与互动类别] -->|A01 官方模型用途| AP[Axon价值预测]
 AI[SDK标识] -->|A02 SDK条件封装| AJ[请求身份上下文]
 AJ -.->|A03 未公开join与特征快照| AF[安装前表示]
 AF -.->|A04 招聘仅间接线索| AP
 AR[游戏实际收入] -->|A05 回调能力| AM[MAX ILRD]
 AM -->|A06 授权共享能力| MM[MMP]
 MM -->|A08 后台授权及映射| AL[伙伴收入事件]
 AL -.->|A10 标签表未知| AP
 AP -->|A11 官方价值出价| AB[报价]
 AB -->|A12 产品与交易接口| AE[拍卖]
 AE -->|A13 仅自身赢输标| FB[反馈]
 FB -->|A14 官方持续学习| AP
 EX[Ad Review或其他bidder用户与出价] -.->|A18 A19 官方排除 此边被禁止| STOP[不得推入Axon训练]
 UC[游戏与玩家行为类别] -->|U02 官方用途| UP[Vector预测]
 UM[授权MMP安装及真实收入] -->|U06 API能力| UL[cohort收入反馈]
 UL -->|U07 官方学习窗口| UP
 UR[Runtime] -.->|U08 具体血缘未知| UP
 UI[IAP与D2C] -->|U09 官方可丰富模型| UP
 UA[UPA或RampID] -.->|U15 U17 未证训练关联| UF[Vector用户表示]
 UF -.->|U10 招聘线索| UP
 UP -->|U11 tROAS动态出价| UB[报价]
 UB -.->|U12 bidding pacing招聘线索| UE[拍卖]
 UE -->|U13 SDK反馈能力| UFB[反馈]
 UFB -->|U14 官方学习用途| UP
```'''

text='''# 身份、行为、价值关联图谱

2026-11-19。实线=在标注范围内的官方用途/API能力；虚线=推断、间接或未知；“官方排除”进入禁止节点，不能误读为训练边。**没有任何边取得独立生产送达/训练日志。**SDK能力实线仍受条件限制。

机器图：[EVIDENCE_GRAPH.json](prediction-system/EVIDENCE_GRAPH.json)；原文含SHA256及行号：[SOURCE_EXCERPTS.json](prediction-system/SOURCE_EXCERPTS.json)。图保存来源时间、证据等级、参与方、权限、生产状态、适用范围和缺失证据。`H1—H5`可按边筛选。

'''+diagram+'\n\n## 逐边证据账本\n\n'
for prefix,title in [('A','AppLovin'),('U','Unity')]:
 text+='### '+title+'\n\n| 边与主张 | 提供方→接收方 | 证据/原始位置 | 权限条件 | 生产与断点 |\n|---|---|---|---|---|\n'
 for e in g['edges']:
  if not e['id'].startswith(prefix):continue
  rr='；'.join(f'[{k}]({S[k]["path"]}):L{S[k]["start_line"]}' for k in e['source_ids'])
  text+=f'| {e["id"]} {e["claim"]} | {e["data_provider"]}→{e["data_receiver"]} | {e["evidence_level"]} {rr} | {e["permission_conditions"]} | 未独立观察生产；{e["missing_evidence"]} |\n'
 text+='\n'
text+='''## 刻意不连接的边

1. MMP收到了游戏事件→MAX EventService：两条独立通路，不能合并。
2. MAX看到了其他网络广告→Axon训练：官方排除Ad Review用途及其他bidder用户/出价数据。
3. UPA登录→RampID→Vector：前后端各有能力不等于连接已证。
4. 电商真实订单→全部手游IAA训练：跨业务用途未证。
5. 身份关联→增量ROAS改善：必须有真实特征消融或合规受控实验。
'''
write('44_身份行为价值关联图谱.md',text)

write('45_关键断点与反证清单.md',f'''
# 关键断点、反证与搜索终止条件

2026-11-19。反证否定特定过强陈述，不等于否定平台所有建模能力。

## 1. 每个核心假设的反面检查

| 假设 | 限制/反证 | 对结论的影响 | 仍值得找的证据 |
|---|---|---|---|
| H1 跨App身份行为有预测力 | AppSet/IDFV有scope与重置、CUID由发布者定义、用户可限制标识；Unity同意与用途独立 | 相同字符串或共封装不能证明跨设备同人；更不能证明增量效益 | 合法历史覆盖/误匹配指标、安装前快照及同样本消融 |
| H2 收入构成标签 | Axon明确排除预测LTV/IAA进入purchase；MAX存在estimated/publisher_defined；Unity需成熟cohort及配置 | 代理值不能装真实收入；收到回调不保证精确结算/进入训练 | ILRD精度过滤、退款/去重、迟到重算和训练标签血缘 |
| H3 关联表示预测 | 招聘/专利不保证生产；UPA和RampID的广告训练连接未证；Axon排除竞争者数据 | 不得声称两家均部署跨App图神经网络/Embedding统一图 | 特征或模型卡、明确产品技术论文/演讲、经授权trace |
| H4 价值→报价→学习 | 官方只定性确认；交易协议不公开预测函数；归因不等于增量 | 不知道pacing/shading/探索/更新延迟，不能把教学公式当平台算法 | 脱敏bid日志+预测值+成熟收入、真实离线/在线实验 |
| H5 两家存在优劣 | 数据披露不等于覆盖、财报增长不等于模型精度；案例非统一竞品试验 | 只能比较已披露产品机制，不能评实际ROAS赢家 | 同国家/素材/预算/成熟度、边际ROAS及归因/增量口径一致的实验 |

直接反证：{refs('S01','S24','S08','S07','S20','S16')}。身份scope及账号/Exchange界限复用[31](31_AppLovin设备身份图谱.md)、[32](32_Unity身份互通与RampID.md)。

## 2. 最关键的八个断点

| 问题 | 可证上限 | 未证部分 |
|---|---|---|
| 不同App行为能否用于模型 | Axon官方跨属性类别用途，Vector游戏/生态与MMP全来源建议 | 某两个App确实进入同一训练任务；同一用户跨App聚合方法 |
| 设备/账号/点击/MMP怎样关联 | SDK标识、归因接口、网站Pixel/CAPI字段 | 服务端命名空间、身份置信度、点击到收入多对一/一对多冲突 |
| IAA是否训练标签 | Unity学习阶段及收入窗口、Axon Ad ROAS产品关联 | 内部表结构、精度清洗、权重和实际作业 |
| 安装前究竟有什么 | 请求上下文和合法历史类别 | event-time水位；不能拿目标App安装后关卡反填首次竞价 |
| 是否Embedding | AppLovin明确招聘方向；Vector行为/推荐建模方向 | Embedding类型、训练样本、维度、跨App共享范围、部署版本 |
| 价值怎样转CPM | 两家官方价值/ROAS动态出价 | 单次转换、平台费率、pacing及竞争价格建模 |
| 去重/延迟/不确定归因 | SDK队列、某些事件幂等接口、Unity成熟窗口 | 整个训练层跨通道去重、迟到校正、SKAN/其他归因加权 |
| 哪些差异明确 | Unity窗口/学习门槛更明确；Axon输入/排除及电商建模更明确 | 差异是否意味着预测优势或数据更多 |

## 3. 本轮公开检索结果与限制

全部URL、HTTP状态、获取UTC和SHA256见[fetches记录](prediction-system/fetches-discovery.json)、[followup](prediction-system/fetches-followup.json)、[targeted](prediction-system/fetches-targeted.json)、[职位发现脚本](prediction-system/discover_unity_jobs.py)。

| 来源类型 | 实际动作与结果 | 是否用于证明核心模型 |
|---|---|---|
| 官方工程/产品文章 | 从AppLovin官方博客索引找到2026-09-16 Ad Review文章；复用Axon说明、Vector/D28/Unite回顾 | 是，按所述用途或排除；营销效果不作独立实验 |
| 官方招聘 | AppLovin公开Greenhouse JSON；Unity官方SSR→Workday公开详情 | D级间接；保存职位日期及描述，不把技能要求当部署 |
| 专利及发明人 | Google Patents公开检索结果→AppLovin US20130159103A1原页；Unity结果含大量动画/渲染噪声 | 前者仅历史构想；后者无有效Vector架构证据，不计入支持 |
| 技术会议/论文 | 搜索涵盖LTV、embeddings、representation、multi-task、delayed feedback、feature store及real-time inference | 未取得明确归属现代Axon/Vector的完整技术模型论文/演讲；既有通用论文仅解释路线 |
| 搜索引擎 | Google200仅跳转提示；Bing RSS200但返回不相关结果 | **全部不作证据**；不将HTTP200当有效检索，不绕过限制 |
| Unity旧招聘API | unity3d/unity两个Greenhouse板404，改由官方careers发现Workday | 已换公开正确来源，不把404当研究阻断 |
| 案例方法 | Unity D28内部配对D7 closed-beta；AppLovin招聘提增量测量需求 | 前者厂商案例方法，后者研究方向；没有我们获得的独立授权生产实验 |

本轮没有新的目标五款游戏AppLovin/Unity实际投放及训练用途记录。SDK、归因枚举、公开招聘和专利均不能替代此证据。

## 4. 不再重复的工作与最高价值下一步

停止增加普通SDK清单、同类OpenRTB字段和没有有效搜索结果的重复请求。优先寻找**授权、脱敏、可追溯的“安装前特征快照—归因安装—逐笔实际收入—训练样本—报价/实验结果”技术案例**。这一条能同时缩小H1/H2/H3/H4的断点；更多政策泛称或SDK字段不能。

若只能取得一个非后台公开材料，优先要官方**数据血缘/特征消融或模型卡**，其次才是新专利；没有合法公开或授权来源则保留未知。
''')

write('46_双方预测系统重建与可信度.md',f'''
# 双方预测系统重建与可信度

2026-11-19。可信度按论断与证据适配评估，不给未经校准的概率分数。

## 1. 已直接证实的最小系统

**Axon：**合法设备/网络与互动类别、伙伴/广告主授权数据和自身MAX赢输标→持续预测展示对特定广告主的价值→按目标出价。MAX/IAA ROAS、真实IAP/MMP共享有产品接口关系；电商订单历史明确用于寻找高价值新客。**内部标签表及具体跨来源join仍断开。**{refs('S01','S02','S03','S05','S08','S11')}

**Vector：**游戏/玩家数据类别及授权MMP安装、会话、真实收入→所选窗口和成熟cohort学习→预测收入潜力→tROAS动态出价；IAP/D2C购买数据被官方明确关联到丰富Vector。**具体Runtime字段、账号/受众ID到模型表示仍断开。**{refs('S12','S13','S14','S16','S21','S22')}

两家都不需要在安装前“知道未来收入”。可行含义是用此前已可用的上下文/合法历史，学习过往用户安装后的实际结果，对下一次展示做条件期望估计。目标App本次安装后的行为可训练未来模型，不能泄露到本次安装前特征。

## 2. 间接线索支持什么

| 环节 | Axon侧 | Vector侧 | 可信度 |
|---|---|---|---|
| 用户表示 | 招聘明确representation/Embedding/多任务、排序检索 | Vector Ads Modeling公开用户行为建模 | 研发方向明确；具体结构部署未证 |
| 特征与推断基础设施 | ML Data Platform训练及feature serving | Vector Gamer AI低延迟高吞吐online inference | 团队职责有原文；实际服务拓扑、实现/延迟未证 |
| 出价优化 | 官方价值出价；具体控制算法未披露 | 专项Bidding Science团队、pacing及bid landscape | 产品用途已证；RL/control理论为招聘要求，部署未知 |
| 评估 | 招聘含离线/在线增量与多来源测量 | 招聘含A/B，D28有内部配对方法 | 有实验方向/案例；没有同条件竞争平台实验 |

{refs('S25','S26','S27','S28','S29','S30','S23')}

## 3. 仅为行业合理架构，不能署名为平台实现

**【合理推断】**事件时间一致的特征处理、安装概率与条件价值估计、用户/游戏/创意表示、多任务或序列学习、长尾稳健损失、校准、迟到反馈纠偏、探索/利用及预算控制，都可以构成此类系统。没有证据允许断言Axon/Vector使用MMoE、Transformer、GNN或某个具体特征库。

教学近似：`CPM≈1000×P(安装|展示)×E(窗口真实收入|安装)/目标ROAS×预算/竞争调整`。**不是两家真实公式。**可能直接预测每展示收入，也可能多目标学习；展示价、广告主成本、发布者ILRD与净收入不应混为一数。

## 4. 哪些已被反证或明确限制

- **【官方明确排除】**“Axon拿其他bidder用户/出价和Ad Review用户级输出训练”与现有官方声明冲突。{refs('S01','S24')}
- **【官方明确限制】**把预测LTV、关卡代理值或广告收入当真实IAP purchase回传不符合当前指南。{refs('S08')}
- **【无法确认】**“UPA/RampID/Runtime全部自动进入Vector”“电商全部数据默认训练游戏Axon”没有连接证据；未知不等于已证明隔离。{refs('S20','S21','S37','S38')}
- **【无法确认】**某游戏SDK/事件存在→某广告平台实际收取/使用→提高ROAS，是三次需要独立证据的跳跃。四款静态审计未完成此生产闭环。{refs('S39','S40')}

## 5. 如何验证高价值用户识别，及身份到底增益多少

真实验证至少要时间外留出、按合法实体/设备分组避免泄漏；比较同库存同预算同规则下的上下文、行为、合法关联历史消融；按国家/平台/安装年龄/同意状态检查覆盖与校准。共同报告：成熟收入预测/实际比、分箱校准、Top10%真实高价值召回和收入覆盖、预算利用、CPI、D28实际及边际ROAS。只看安装AUC或高价值召回不足以证明赚钱；归因ROAS不是增量收益。

辅助材料为前一阶段已完成的[81组本地合成实验](ltv/model/output/SUMMARY.md)：三种价值分布×三seed×九训练/压力场景，共用库存/预算/价值/竞价规则。**不属于平台生产证据，也不是训练了身份图谱。**只是给定已合法关联历史特征的假想增益。

相对已有行为特征，增加假想关联历史后的合成ROAS配对变化：普通分布约+2.9%，长尾相关分布约+15.7%，身份无增量信息负对照约−0.06%。这些数值由人为数据生成机制决定；三seed范围不是置信区间，不能估计真实身份图谱增益或两家优劣。排名已区分条件LTV和`pInstall×LTV`实际决策分数，避免常数LTV基线被行序平局低估。真实增益目前仍**【无法确认】**。

## 6. 下一条最值得寻找的证据

**第一优先：一份授权匿名化、具事件时间和特征血缘的真实收入/身份特征消融案例。**应能核对：哪些安装前历史被关联、同意与覆盖、真实IAA/IAP粒度和幂等、模型使用、报价/预算、成熟收入和实验分组。它能把“有数据/有接口”推进到“确实训练及改善”；新专利、招聘或更多SDK字段做不到。

若无此材料，应交付现在的最小可证系统和断点，不把公开材料拼接成一张实际上不存在的已证完整生产架构。
''')

# Source catalogue rendered once, including original URL, dates, product and precise locator.
catalog='# 原始来源及时间目录\n\nA=官方用途，B=SDK/API，D=招聘/专利；本轮没有独立授权生产实验。源码引用的发行来源可沿既有EVIDENCE_INDEX追溯。\n\n'
for s in g['sources']:
 catalog+=f'## {s["id"]} · {s.get("product")}\n\n'
 catalog+=f'- 原文：[{s["path"]}](../{s["path"]})，L{s["start_line"]}—{s["end_line"]}。\n'
 if s.get('url'):catalog+=f'- URL：{s["url"]}\n'
 catalog+=f'- 材料日期：{s.get("source_date")}；复核：{s["reviewed_utc"]}；级别：{s["evidence_priority"]}。\n'
 if s.get('raw_origin'):catalog+=f'- 原始JSON：[{s["raw_origin"]}](../{s["raw_origin"]})；定位：`{s["raw_locator"]}`。\n'
 catalog+=f'- SHA256：`{s["sha256"]}`。\n\n'
(R/'SOURCE_CATALOG.md').write_text(catalog,encoding='utf-8')
print('written reports 41—46 and source catalogue')
