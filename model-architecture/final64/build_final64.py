"""Round 64: bounded synthesis, historical preservation, no network access."""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import shutil
from datetime import datetime, timezone

ROOT = Path(r'D:\GrowthResearch')
OUT = ROOT / 'model-architecture' / 'final64'
NOW = datetime.now(timezone.utc).isoformat()
OUT.mkdir(parents=True, exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(rel, content):
    p = ROOT / rel
    if p.exists():
        raise RuntimeError('Refuse to overwrite existing deliverable: ' + rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + '\n', encoding='utf-8', newline='\n')

def dump(rel, obj):
    write(rel, json.dumps(obj, ensure_ascii=False, indent=2))

graph_path = ROOT / 'prediction-system/EVIDENCE_GRAPH.json'
index_path = ROOT / 'EVIDENCE_INDEX.md'
graph = json.loads(graph_path.read_text(encoding='utf-8-sig'))
old_graph = json.loads(graph_path.read_text(encoding='utf-8-sig'))
old_index = index_path.read_bytes()
protected = sorted([p for p in ROOT.glob('*.md') if re.match(r'\d\d_', p.name) and int(p.name[:2]) <= 63])
protected += [ROOT / 'model-architecture/CLAIM_MATRIX.csv', ROOT / 'EVIDENCE_MANIFEST.json']
history = {p.relative_to(ROOT).as_posix(): sha(p) for p in protected}
dump('model-architecture/final64/HISTORY.before.json', history)
shutil.copyfile(graph_path, OUT / 'EVIDENCE_GRAPH.before.json')
shutil.copyfile(index_path, OUT / 'EVIDENCE_INDEX.before.md')

official_ids = ['MA60S01', 'MA60S02', 'MA60S04', 'MA60S09', 'MA60S10', 'MA60S13', 'MA60S14', 'MA60S17', 'MA60S23', 'MA60S27', 'CT62S08', 'CT62S11', 'RV61S01', 'RV61S03', 'RV61S05', 'RV61S06', 'RV61S15', 'RV61S16']
official = []
for ident in official_ids:
    s = next(s for s in graph['sources'] if s['id'] == ident)
    actual = sha(ROOT / s['path'])
    if actual != s['sha256']:
        raise RuntimeError('Historical source hash mismatch: ' + ident)
    official.append(s)

# These are existing raw/static artifacts, not new runtime observations.
raw_specs = [
 ('F64C01','Car Race','1.348.2 ARMv7','car-race/reused-evidence/monetization-20261117/native/InAppAdvertising__InAppAdvertising.IAAController.OnAdRevenuePaidEvent-24401f8.asm','IAAController.OnAdRevenuePaidEvent; RVA 0x24401f8','正收入累计、国家阈值、Firebase事件与缓存清零'),
 ('F64C02','Car Race','1.348.2 ARMv7','car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Metica__Zego.Advertisement.Metica.AdMeticaDefault.OnShowRevenuePaid-32deaf0.asm','AdMeticaDefault.OnShowRevenuePaid; RVA 0x32deaf0','展示收入业务桥；与C05交叉定位'),
 ('F64C03','Car Race','1.348.2 ARMv7','car-race/reused-evidence/monetization-20261117/native/Zego.Advertisement.Max__Zego.Advertisement.Max.AdRevenueTracking.ImpressionSuccessEvent-32c2988.asm','AdRevenueTracking.ImpressionSuccessEvent; RVA 0x32c2988','独立收入分发实现，非国家阈值到Axon的证明'),
 ('F64C04','Meowdoku','1.25.1 / GRT 1.3.2.0','meowdoku/static/java/classes4.dex/com/learnings/grt/event/LTVManager.java','LTVManager.getLTV/increaseLTV/mergeData; L50-L81','已实现收入累计，不是未来收入预测'),
 ('F64C05','Meowdoku','1.25.1 / GRT 1.3.2.0','meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/BaseGrtEvent.java','BaseGrtEvent.sendEvent; L66-L94','mediaSource/country/livingDay过滤后交BridgeManager'),
 ('F64C06','Meowdoku','1.25.1 / GRT 1.3.2.0','meowdoku/static/java/classes4.dex/com/learnings/grt/event/processor/IaaFbRoasEvent.java','IaaFbRoasEvent.onAdImpression','国家规则、最小值、相对lastReportLTV增量'),
 ('F64C07','Meowdoku','1.25.1 / GRT 1.3.2.0','meowdoku/static/java/classes4.dex/com/learnings/grt/config/ConfigManager.java','ConfigManager; configuration load/version/update','可选配置与生产生效表必须区分'),
 ('F64C08','Meowdoku','1.25.1','meowdoku/static/godot-source/tracker.gd','Tracker; game_start/game_end/ad/guide/subscription events','实际业务埋点；订阅点击不等于已付费'),
 ('F64C09','Rotate Rings','1.2.4 / AppsFlyer 6.17.5','rotate-rings/static/java/classes2.dex/g8/a.java','g8.a.adRevenue; L100-L123','AFAdRevenueData(APPLOVIN_MAX,USD,d)、ad_revenue2/ad_revenue4副本'),
 ('F64C10','Rotate Rings','1.2.4','rotate-rings/static/java/classes6.dex/com/unity3d/player/SDKManager.java','SDKManager.handleAdRevenue; L386; async upload L802','MAX收入callback到AppsFlyer及规则分发'),
 ('F64C11','Rotate Rings','1.2.4','rotate-rings/static/java/classes8.dex/com/unity3d/player/SDKKeybehaviors$evenue.java','upload_revenue / upload_pltv7_byday_bycountry; L1013/L1048','国家×安装日/时长/收入与已触发状态'),
 ('F64C12','Rotate Rings','1.2.4','rotate-rings/static/java/classes9.dex/ta/d.java','ta.d.j(String,int); L4405','国家×day0-6收入门槛表，不是实际CPI或预测值'),
 ('F64C13','Jewel Coloring','1.24.1 / AdWorth config 10.2.3','jewel-coloring/deep/resources/ad_worth_event.json.redacted.json','ad_worth_event.json; extras/events; 90 rules / 31 tables','包内默认规则；非生产热更结果'),
 ('F64C14','Jewel Coloring','1.24.1 ARM64','jewel-coloring/deep/asm/ad__event__AWESendPlatform__sendMsgToPlatform__-1a44350.asm','AWESendPlatform::sendMsgToPlatform; RVA 0x1a44350','平台调用和本地已发状态；非后端ACK'),
 ('F64C15','Jewel Coloring','1.24.1 ARM64','jewel-coloring/deep/asm/ad__event__AWEWorthUpdate__getBeSentWorth_ad__event__AWEWorthSendType__float_-1a3dc50.asm','AWEWorthUpdate::getBeSentWorth; RVA 0x1a3dc50','normal/interval/x100等输出口径分开'),
 ('F64C16','Jewel Coloring','1.24.1','jewel-coloring/deep/resources/decoded-config-provenance.json','raw entry / decoded SHA256 / split / logical resource mapping','原始包条目与解码结果的既有溯源'),
 ('F64C17','four games','MAX 13.2.0 / 13.6.2 / 13.6.3 / 13.6.4','axon/deep/event-callsite-catalog.json','DEX class/method/descriptor/invoke offsets','SDK自动事件与通用桥；未建立具体业务价值直发链'),
 ('F64C18','four games','original game DEX scope','axon/deep/game-scan-summary.json','scan summary; 15/8/14/12 DEX','所查范围内的静态结论，不排除native/反射/热更'),
 ('F64C19','Jewel Coloring','1.24.1 ARM64','jewel-coloring/deep/asm/BulldogSdk___initBaseComponents_BulldogDelegate___int__int__int_-1937ee0.asm','BulldogSdk::_initBaseComponents; RVA 0x1937ee0','Bulldog组件关系；不证明商业所有权'),
]
raw_sources = []
for ident, product, version, rel, loc, scope in raw_specs:
    p = ROOT / rel
    if not p.is_file():
        raise FileNotFoundError(rel)
    raw_sources.append(dict(id=ident, company='target game static evidence', product=product,
        version=version, path=rel, sha256=sha(p), class_method_or_location=loc,
        claim=scope, evidence_level='【游戏代码证实】', evidence_kind='reused static artifact',
        source_date='existing evidence collected 2026-11-17 to 2026-11-19; see original provenance',
        reviewed_utc=NOW, production_actual_proven=False, observed_target_game_delivery=False,
        server_model_training=False, missing_evidence='No runtime delivery, partner settings, server ACK or training lineage'))
dump('model-architecture/final64/SOURCE_LEDGER.json', {'scope':'Existing evidence reverified, no new production evidence or public fetch', 'reviewed_utc':NOW, 'official_source_ids':official_ids, 'sources':official + raw_sources})

main = r'''# 普通游戏盈利跃迁：最终机制判断与证据边界

2026-11-19 · 第64号最终综合。研究对象为Car Race、Meowdoku、Rotate Rings和Jewel Coloring的既有授权样本，以及AppLovin Axon/MAX与Unity Vector/LevelPlay的公开资料和SDK。Amaze GO!缺少可验证包体，不加入四款审计。

**最终判断：普通游戏即使不改玩法，也可能因为买到的玩家、获取价格、每名玩家的变现收益和预算分配改变而跨过盈亏线。现有研究证明了这些机制的部分技术入口与官方产品用途，但没有证明这四款游戏确因Axon或Vector获得盈利性扩量，也无法判断两家模型谁更强。**

本轮是00—63号证据的收束，没有新SDK扫描、公开架构广搜、生产请求或真实用户数据采集。下文“已证”只在标明的层级成立。原始来源URL、位置和重新核对的SHA256见[本轮证据目录](model-architecture/final64/SOURCE_CATALOG.md)与[机器可读账本](model-architecture/final64/SOURCE_LEDGER.json)。没有新增生产证据。

## 1. 读懂结论所需的最小技术背景

游戏既可以是**广告主**，付钱获取新玩家，也可以是**媒体**，向已有玩家展示广告赚钱。Axon和Vector的获客优化负责前者；MAX和LevelPlay的中介、竞价及展示收入回调主要负责后者。两者能通过真实收入反馈衔接，但接入变现SDK不等于启用获客投放。Exchange公开拍卖协议也不等于模型或预算控制器源码。[MA60S02/13、RV61S15/16]

**证据六层不可跳级：**①SDK具备能力；②游戏存在实际业务调用；③请求构造实现可追踪；④生产成功发送；⑤接收端确认接收；⑥进入指定生产训练/决策作业。官方产品声明另行记录，可以证明厂商明确披露某用途，不能代替目标游戏④—⑥的观测。本文所有四款游戏的④—⑥均未取得证据。[20号、49号、58号；F64C17/18]

符号约定：链路图实线表示**注明范围内的静态调用或官方契约**，虚线表示尚未连接的生产或因果环节；实线不表示已观测生产送达。安装后的收入只能作为历史样本标签，不能作为同一次安装前广告机会的已知特征；历史聚合、模型版本及个人历史都必须在该次bid发生前已合法可用。[56号、61—63号]

## 2. 统一因果框架：五条能改变单位经济的路径

| 机制 | 已证技术能力与四款实际调用 | 可配置但未证启用的反馈；未知模型消费 | 可能改变什么 | 最强竞争性解释及可推翻证据 |
|---|---|---|---|---|
| **M1 玩家价值排序改善** | 【官方公开证实】Axon按广告主展示价值/return goal出价；Vector预测D7/D28收入、动态竞价。【游戏代码证实】四款产生收入/参与信号，但未证被上述模型消费 | MMP partner、事件/收入映射、来源范围；逐条接收、特征join、校准、训练和真实排序增益未知 | 买入cohort的成熟LTV、CPI、赢标率；预测更高也可能只令出价更贵 | M4变现提高或M5库存/素材变化。固定素材、国家、库存、预算、变现策略后，价值排序无校准/尾部识别/成熟贡献增益，才会削弱该解释；单次无显著不是证明不存在 |
| **M2 同App自然量/跨渠道历史帮助冷启动** | 【官方公开证实】Unity要求预启动至少两周SDK+未归因postback帮助训练；AppLovin有all-source/organic契约及自愿数据用途。四款MMP入口已证 | 四款全来源授权、开始共享时间、历史可用窗口、实际样本和权重未知；Lifetime不等于补发全部历史 | 冷启动等待、早期校准、低效探索成本；自然量分布差异也可能负迁移 | M3共享先验或素材改善。授权开关/投递记录证明当期没有同App历史共享，可排除“这一路输入解释该活动”；合法holdout才可测增量 |
| **M3 跨游戏聚合知识/模型迁移** | 【官方公开证实】Vector称cross-game patterns、aggregate cohort insights用于bid-time区分玩家；Axon称更多广告主数据帮助模型。【无法确认】具体共享参数或个人历史实现 | B聚合、C共享参数、D个人历史不能混为一谈；四款没有明确生产训练连接 | 新游戏/稀疏数据下的初始先验和样本效率；不保证迁移有效 | M2同App样本已足够。生产数据血缘/模型契约明确不含跨游戏统计和共享权重可排除对应实现；仅关个人ID不能排除B/C |
| **M4 MAX/LevelPlay变现收益提高** | 【SDK代码证实】多网络signal/请求、竞价与回调；【游戏代码证实】四款MAX相关展示收益入口。不能把独立LevelPlay包能力写成四款接入事实 | 真实需求竞争、底价/瀑布/频控生效、填充和价格收益、同类用户留存未知；不是Axon/Vector训练已证 | 同类玩家eCPM、填充/展示率、净ARPDAU与净LTV；多广告可能损伤留存 | M1买来更值钱的人。固定获客cohort的随机变现组若净LTV无改善或留存损失抵消，则反驳“变现足以解释利润”的版本 |
| **M5 素材、国家、预算、目标或归因变化** | 【官方公开证实】目标、国家与预算影响交付；四款有不同业务规则，但没有其campaign变更日志或成本收益 | 活动/素材/地域实际启用和归因窗口未知；报表改进不等于新增净收益 | 点击/安装率、CPI、cohort结构、规模、报表ROAS；口径变化可能只改归因 | M1模型本身改善。日志/锁定配置可排除已固定项；固定归因口径、独立收入对账及随机/地域holdout可排除纯归因重分配 |

表中机制为【合理推断/竞争性解释】，能力锚点为MA60S01/02/04/13/14/17、CT62S08、RV61S05/06/15/16；游戏事实见下一节。**没有为任何机制分配四款增长的因果贡献。**逐游戏×五机制的25行总表见[FINAL_CAUSAL_MATRIX.csv](model-architecture/FINAL_CAUSAL_MATRIX.csv)。实验属于建议，未执行。

### 哪些完全不需要跨App个人身份图谱

- **M2同App全来源学习**可用该App安装/事件与合法归因契约，不必知道某人在其他游戏的终身轨迹。仍需准确的同App事件关联和合法用途。
- **M3聚合统计与共享模型参数**在理论上可只共享cohort先验/参数，不在bid时查询个人跨App历史；但公开材料未唯一识别实际实现，也不能用“聚合”规避原始数据授权。
- **M4变现优化、M5素材/国家/预算优化**均可基于广告位、上下文和聚合结果工作。
- **M1更好的价值排序**可依靠上下文、创意/应用特征、同App历史训练和共享先验改善；个人级跨App历史是可能的额外输入，不是逻辑前提。

【合理推断】上述说明“不依赖D也可成立”，不证明无ID系统能达到两家当前生产效果。【官方公开证实】广告同意与用途限制有效；Axon还明确排除竞争者bid/user数据，Ad Review不供给Axon。不能由中介可见信息推断无限训练权。[MA60S02/23、CT62S11；62号]

## 3. 四款逐案审计：能证到哪里

以下均是既有样本的静态事实，不代表全部历史版本、当前线上配置或实际网络送达。完整逐案审计、会计风险、竞争解释和最小补证清单见[FOUR_GAME_VERDICTS.md](model-architecture/FOUR_GAME_VERDICTS.md)。

### 3.1 Car Race：真实ILRD与国家阈值并存，阈值为Firebase-only

【游戏代码证实】样本1.348.2/MAX13.6.4。`IAAController.OnAdRevenuePaidEvent` RVA **0x24401f8**只处理正收益，更新总收入与缓存；US/T1/T2/T3默认门槛$0.50/$0.30/$0.20/$0.03，达标发Firebase `taichi_*`，value为**本次完整缓存实际金额**后清零。另一独立展示收益链交Adjust/Firebase/TikTok；关卡、会话及前5次激励等是行为信号。默认可被远程覆盖，设备国家不等于投放国家。[F64C01—03；C04—C06；03号]

```mermaid
flowchart LR
 CAd[展示收入回调] -->|游戏代码 C01-03| CIR[真实ILRD分发]
 CIR -->|游戏代码 独立收入链| CM[Adjust SDK / Firebase / TikTok]
 CAd -->|游戏代码 C01| CT[国家累计阈值]
 CT -->|游戏代码 Firebase-only| CF[Firebase事件]
 CM -.->|官方可配置 四款实际开关/送达未知| CN[Axon或Unity接收端]
 CN -.->|无法确认| CP[生产训练与盈利改善]
 CF -.->|无法确认 未建立路由| CN
```

**最有支持的解释：**开发者确实生成真实收益和可解释门槛，具备价值反馈基础；M1/M2是可配置的获客解释，M4是独立变现解释，三者均无因果归属。**不能证明：**国家阈值已送Axon/Vector；通用MAX/Metica `trackEvent`桥被具体业务事件调用；真实获客成本、成熟净LTV、盈利扩量。IAP schema/API不构成真实成交账本。[20号；F64C17/18；02号]

**最小补证：**Adjust实际partner/收入映射和投递记录；阈值/ILRD分账及远程生效版本；同campaign成熟成本收益与接入/素材/变现变更日志。若没有阈值外发映射，应停止将`taichi`解释为两家训练输入。

### 3.2 Meowdoku：时间窗参与代理与GRT配置路由

【游戏代码证实】样本1.25.1/MAX13.2.0/GRT1.3.2.0。Godot `tracker.gd`产生关卡/会话/广告及订阅漏斗；GRT支持安装时间窗、关卡/活跃、来源/国家/安装年龄过滤，再经`BridgeManager.sendEvent`到所选AF/Meta等接收端。`LTVManager.increaseLTV`只把已实现收入加进本地`sp_key_ltv`，不是预测未来。`IaaFbRoasEvent`可按`LTV-lastReportLTV`增量，另有累计和once规则；不能据类名判定生产全开。[F64C04—08；M01—M05]

```mermaid
flowchart LR
 MB[关卡 / 活跃 / 广告回调] -->|游戏代码 C04-08| MG[GRT账本 / 条件 / receiver配置]
 MG -->|游戏代码 按选中接收端| MS[AppsFlyer / Meta等SDK]
 MS -.->|官方契约 partner/金额/来源需授权| MN[Axon或Unity接收端]
 MN -.->|无法确认| MP[模型消费 / 获客改善]
 MD[MAX13.2自动landing等] -->|SDK代码 独立旧协议| MA[AppLovin事件入口]
 MA -.->|无法确认 不是GRT显式直发证明| MP
```

**最有支持的解释：**早期参与代理与配置化价值分发确实存在，可能提高可用信号密度。**不能证明：**代理具有超出D0真实收入/广告次数的独立预测力；当前国家美元门槛、上线接收端、两家训练目标、真实购买/订阅结算与盈利。MAX13.2没有新版结构化Axon分支，但这不排除旧事件或MMP服务端路径。[03/20/22/49号]

**最小补证：**当前GRT生效JSON/版本和接收端列表；AF收入/代理事件对账与partner投递；成熟D28数据中比较D0行为、D0收入及新增GRT特征。自然量共享开关存在不等于当前活动已借此冷启动。

### 3.3 Rotate Rings：标准真实ILRD、重复副本与国家×安装日门槛

【游戏代码证实】样本1.2.4/MAX13.6.2/AF6.17.5。`SDKManager.handleAdRevenue`→`g8.a.adRevenue`构造`AFAdRevenueData(network, APPLOVIN_MAX, USD, d)`，还发`ad_revenue2`和`ad_revenue4`。国家×day0—6规则比较**实际累计收益R**与门槛`T(country,day)`，R>T且当日未报才送value=R；其他组合含美国首日时长≥900秒与非banner收益≥$0.45。`pltv`命名不证明未来收入预测。[F64C09—12；R02—R06；49号]

```mermaid
flowchart LR
 RA[MAX收入callback] -->|游戏代码 C09-10| RS[AppsFlyer标准logAdRevenue]
 RA -->|游戏代码 C09| RD[ad_revenue2 / ad_revenue4副本]
 RA -->|游戏代码 C11-12| RR[国家 / 安装日 / 时长门槛]
 RR -->|游戏代码| RT[AF / Firebase等业务事件]
 RS -.->|需partner/专用收入通道 实际送达未知| RN[Axon或Unity]
 RD -.->|去重/映射未知| RN
 RT -.->|事件映射及消费未知| RN
 RN -.->|无法确认| RP[训练 / 实际ROAS]
```

**最有支持的解释：**四款中这条标准AF收入赋值非常直接，且开发者明显区分早期资格；这是可利用反馈，不是反馈已成功。**不能证明：**三路是否被同一后台重复计算、国家门槛来自真实CPI、跨日累计value是新增收入、Axon/Vector实际优化它，或何种IAP净收入。标准枚举`APPLOVIN_MAX`代表变现来源，不证明AppLovin买量。[F64C09—12]

**最小补证：**三个收入名称的partner映射、幂等规则/投递样本；国家门槛生效版本；逐展示经济事件与跨日累计值分账；同国家成熟cohort真实成本收益。

### 3.4 Jewel Coloring：AdWorth是规则化代理价值系统，不是已证LTV模型

【游戏代码证实】样本1.24.1/MAX13.6.3。Bulldog内AdWorth包内恢复90条默认规则与31张权重表；行为系数、插屏次数/关卡/时长与广告价值账本，经条件树路由Firebase/Meta/Adjust。`AWESendPlatform::sendMsgToPlatform` RVA **0x1a44350**调用后更新本地发送状态；`AWEWorthUpdate::getBeSentWorth` RVA **0x1a3dc50**输出normal/interval/x100等不同口径。默认514把广告价值映射Meta `logPurchase(USD,value)`，**不是用户IAP订单**。来源权重和国家条件代码有能力，但默认90规则未引用来源表且未用直接国家条件，线上热更未知。[F64C13—16/19；09号D01—D07]

```mermaid
flowchart LR
 JA[广告价格/价值回调 与玩家行为] -->|游戏代码 C13-16| JW[AdWorth多key账本 / 系数 / 默认条件树]
 JW -->|游戏代码 平台路由| JF[Firebase / Meta / Adjust]
 JW -->|游戏代码 514为代理| JP[Meta purchase语义事件]
 JF -.->|Adjust partner可配置 实际未知| JN[Axon或Unity]
 JP -.->|未建立自动跨平台路由| JN
 JN -.->|无法确认| JM[训练 / 获客改善]
```

**最有支持的解释：**开发者自定义早期价值筛选/分发比单纯原始事件更复杂；尚未验证复杂性带来成熟LTV增量。**不能证明：**AdWorth直接送MAX EventService；Meta代理purchase是实际购买；来源倍率生产启用；独立机器学习预测未来；由这些规则造成盈利增长。广告价格/回退估计必须与真实结算IAA分开。[09/10/20号]

**最小补证：**实际热更版本、规则×接收端和输出单位；广告展示价格/ILRD/估计回退的precision及对账；Adjust映射/投递与Meta代理分账；成熟收入下的代理消融。无需先获取跨App个人ID。

### 四款共同的硬边界

【无法确认】既有研究没有取得其可核验的Axon/Vector实际投放成本及成熟净收益，也没有目标campaign、训练血缘或授权对照实验。四款均有MAX SDK生命周期自动事件；**未建立具体关卡/GRT/AdWorth/收入规则→MAX EventService→结构化Axon协议的完整显式业务链**。MMP转发是另一路，不因未发现MAX直发而消失，也不因官方支持而自动成立。[F64C17/18；20/22/49/58号]

【无法确认】没有可用的四款实际IAP验单/退款/净额账本。购买API、schema、订阅按钮或代理purchase均不能填补此缺口。没有可靠证据证明它们的价值机制必须依赖跨App个人图谱；也不能从客户端未找到图谱就证明服务端没有。[02/08/09/55号]

## 4. 盈利跃迁的数学与因果边界

**本节公式是独立会计定义与合成示例，不是两家报价公式，不是四款盈利结果。**对同一安装cohort和时间窗口W：

`净LTV_W = 每安装可归属且去重的IAA净收入 + IAP净收入 − 退款/税费/平台费等未提前扣除项`

`每安装贡献_W = 净LTV_W − 实际获客支出/安装数 − 其他每安装可变成本`

不同报表可能将部分费用已净额化，必须记录口径、避免二次扣费；固定成本、现金到账和W之后收入另计。所谓D28 LTV只是28天累计，不是完整终身价值。[61/63号；MA60S10、RV61S03]

| 容易混淆的量 | 最终边界 |
|---|---|
| 预测LTV vs 真实净LTV | 前者是估计，可能误校准；后者需成熟经济事件和对账。预测高不保证收入兑现 |
| 目标ROAS vs 实际ROAS | 前者是控制输入，后者是同口径窗口收入/真实支出，不保证达到目标，也不自动等于利润 |
| 平均ROAS vs 边际扩量ROAS | 存量cohort赚钱不保证下一档预算赚钱；考察Δ净收益/Δ支出及其不确定性，不能只看整体均值 |
| 广告主CPI vs 交易所CPM | 计费层与对象不同；CPM报价、发布者ILRD和广告主每安装成本之间有安装率、费用/结算等边界 |
| 归因收入 vs 增量收入 | 归因分配功劳，不证明用户没广告就不会产生收入；自然量训练数据不能计为该渠道新增回报 |
| 变现改善 vs 获客质量改善 | 前者提高同类玩家收入；后者改变买来的人。两者都能涨LTV，需固定另一侧或因子实验 |
| 大规模投放 vs 盈利 | 花费/安装增长不证明成熟净收益覆盖成本；现金回本还受到账周期与投放先付影响 |

**独立合成例（美元）：**原CPI=0.60、净D28 LTV=0.54、其他可变成本=0，贡献=-0.06。玩法不变：①玩家选择更好让LTV到0.66且CPI仍0.60，贡献+0.06；②LTV仍0.54但CPI到0.48，亦+0.06；③同样玩家由变现改善使LTV到0.66，也会+0.06。观察到+0.06本身无法区分三者。若只是模型把0.54预测为0.66，实际收入没变，贡献仍-0.06。

**扩量反例：**原1000安装、CPI0.60、净LTV0.66，贡献+60；新增1000安装、CPI0.75、净LTV0.60，新增贡献-150，总贡献变-90。规模翻倍不保证盈利。全部是合成算术，既未模拟平台真实精度，也未用于证明四款结果。

**因果标准：**固定或记录素材、国家、库存/隐私覆盖、应用版本、广告策略、目标、预算、归因/收入口径与成熟度；随机/可识别holdout再比较净贡献。前后同时换SDK、素材、目标和国家的一条曲线不足以归因。无全机会日志/选择概率时，不声称离线回放有因果ROAS；无授权真实样本时不报告模型召回、精度或消融增益。[56_数据资产审计；63号；MA60S27]

## 5. Axon与Vector分别可以下什么结论

| 层级 | Axon / AppLovin | Vector / Unity |
|---|---|---|
| A 官方明确能力 | 【官方公开证实】持续使用允许的设备/互动、自身胜负及广告主自愿数据训练；按广告主展示价值/return goal出价；未来多日价值分布为官方措辞；IAA/IAP/Blended产品目标 | 【官方公开证实】D7/D28 IAA/IAP/Hybrid收入目标；国家ROAS动态出价；预启动同App全来源数据帮助训练；cross-game patterns/aggregate cohort insights的bid-time用途；部分预算pacing行为 |
| B SDK/协议入口 | 【SDK代码证实】MAX收入回调、请求/signal及EventService旧/新协议、持久postback；【官方契约】MMP all-source/事件/收入共享 | 【SDK代码证实】Unity Ads Token/历史外层、LevelPlay信号、IAP Insights/Analytics各自通道；【官方契约】MMP收入/未归因共享。IAP/Analytics独立包不证明四款已使用同版本 |
| C 合理未证架构 | 【无法确认】单点/多阶段/显式分布可共存，分布措辞不能唯一选架构；共享表示、尾部损失、风险调价、shading未知 | 【无法确认】同游戏学习最直接；聚合用途有披露，但统计迁移/共享表示/个人历史贡献未拆开；共享网络、loss、精确controller未知 |
| D 缺生产材料 | 四款开关/投递/接收、canonical收入标签、训练集/serving特征与时间水位、出价/实验及成熟净收益 | 同左；另需Insights/Runtime字段到Vector训练用途的明确血缘，不能用同属Unity直接连线 |
| E 无法比较的优势 | 不能证明模型更准、数据更多、单位预算更赚钱或扩量更强 | 披露更具体不等于技术更强；不能用文章细节、SDK数量或增长财报替代同条件实验 |

依据：MA60S01/02/04/09/10/13/14/17/23、CT62S08/11、RV61S01/03/05/06；客户端原方法见20—22、49、53—58号。**Axon最有证据的优势轮廓**是把允许的互动/广告主价值反馈用于广告主特定的实时价值出价；**Vector最有证据的轮廓**是明确收入窗口、同App预启动学习和公开跨游戏聚合用途。它们是产品能力，不是相对优胜裁决。

不能由Axon“value distributions”补出每用户条件分布族/分位数/CVaR；也不能由Vector“cross-game”补出个人Embedding或统一账号图谱。参数共享、聚合迁移、个人历史、同App跨来源分别保留。[61—63号]

## 6. 如果只能取得三份授权材料

这里的“一份”指可独立回答一组问题的授权材料包，不要求原始个人ID。研究键只在授权项目/实验内有效，不请求GAID、手机号或跨应用自然人关联。

| 优先 | 材料包与最小字段 | 能补哪条边；仍不能证明什么 |
|---|---|---|
| **1. partner配置—投递—接收对账包** | 一款授权App的活动/来源共享开关、事件/收入映射与窗口、配置生效时间；去标识事件经济幂等键、事件/可用/发送/接收时间、币种/precision、归因标记、投递状态及接收ACK/错误码 | 区分游戏→MMP→指定网络是否真实送达、全来源是否开、重复和金额语义。MMP HTTP2xx也只证明相应入口确认，不证明后续训练消费 |
| **2. 成熟单位经济与受控实验包** | 同国家/平台/cohort至少完整D28及迟到宽限的支出/安装/留存、去重IAA和验单IAP/退款净额、素材/预算/目标/广告策略/归因变更；固定预算随机/地域holdout和分组规则 | 判断是否真盈利、边际扩量、变现与获客贡献及是否仅归因重分配。无可靠随机/识别条件时只能相关，不凭一张ROAS报表做因果 |
| **3. 平台授权训练—推断—决策血缘与消融包** | canonical label/零值/去重/成熟规则、特征来源/作用域/available_at、训练快照与模型版本/用途、允许的聚合/参数/个人历史边界；去标识bid样本预测输出、控制器/预算状态及固定数据/分数的受控消融 | 区分数据、模型与出价策略优势，识别共享知识还是个人历史、Axon输出是否显式分布。若只获schema而无作业关联/实验，仍不证明具体消费和增量 |

三包应尽量对同一App、时期和实验关联，否则只能分别证明碎片。第1+2包通常比更多客户端逆向先产生实际价值；第3包往往需要平台合作，不以未授权探测替代。

## 7. 达到公开资料上限的事项与停止条件

**现在停止：**重复SDK字段清单、把加密Token当已解特征、从native边界猜训练网络、用同包ID补server join、凭招聘/专利/案例唯一选架构、搜索相同文案试图证明四款盈利。00—63已充分暴露这些断点，本轮不再广搜。

**仍未知的五类核心事实：**①四款具体网络投放/事件映射/生产送达；②真实经济事件如何形成去重、成熟、处理退款的训练标签；③bid-time特征/合法join及B/C/D各自贡献；④预测输出如何经控制器/预算/探索成为报价；⑤同条件增量净收益与边际规模。公开客户端无法补齐服务器ACK之后的血缘，官方能力也不能补齐目标游戏启用状态。

**恢复条件：**取得上述三包之一且明确授权、出现可核验的具体生产技术文档/模型schema/字段用途契约，或有明确新增版本路径能补现有某条未知边。只因营销名称/收入增长/文章更多不恢复扫描。细则见[STOP_AND_RESUME_CRITERIA.md](model-architecture/STOP_AND_RESUME_CRITERIA.md)。

## 8. 给不熟悉前63号报告的读者的最终答案

1. **玩法不变也能过线：**买谁、花多少、同类玩家赚多少和预算投到哪里都会变。靠近盈亏线时有限真实改善即可改变贡献符号；必须与报表变化分开。
2. **不必先有跨App个人图谱：**同App全来源历史、上下文排序、聚合先验/参数共享、变现优化、素材/地域/预算优化都可在不查询个人跨App轨迹下成立。
3. **两家有证据的能力：**Axon公开连接允许数据、持续训练与广告主特定价值出价；Vector公开连接同App预启动样本、D7/D28收入和动态出价，并披露跨游戏聚合用途。没有同条件数据可判技术胜负。
4. **四款能证什么：**Car有真实ILRD与Firebase国家阈值；Meow有GRT早期参与/价值路由；Rotate有标准AF收入及国家安装日规则；Jewel有复杂AdWorth代理分发。均未证指定模型实际消费、真实投放盈利或增长因果。
5. **最值得取得的三包：**partner送达链、成熟净收益受控实验、训练推断决策血缘。先证收入真的发对，再证经济效果，最后辨模型原因。
6. **应停止什么：**用客户端字段继续猜闭源训练、跨游戏身份或四款盈利原因。保留未知边，等待授权生产材料；不用通用机器学习知识制造确定性。

结论等级：平台用途为【官方公开证实】；包内调用为【游戏代码证实/SDK代码证实】；经济解释与实验设计为【合理推断】；四款模型消费、真实导量及盈利贡献为【无法确认】。
'''

write('64_普通游戏盈利跃迁最终机制判断.md', main)

appendix = r'''# 四款游戏最终审计与竞争性解释

2026-11-19。与[64号最终报告](../64_普通游戏盈利跃迁最终机制判断.md)配套，可独立阅读。IAA=向玩家展示广告产生的收入；IAP=玩家真实购买；代理value=开发者规则形成的优化信号，不能未经对账作为收入。真实IAA在这里首先指广告展示收益接口的业务金额，仍保留exact/estimated/publisher-defined及结算差异，**不等于已核银行净收入**。

来源编号的原文件、类/方法、版本与SHA256见[final64证据目录](final64/SOURCE_CATALOG.md)。官方声明、SDK实现、实际业务调用、生产送达、服务器接收、模型训练是不同证据层级。实线为静态/契约范围，虚线为未证连接。

## 1. Car Race · 1.348.2 / MAX13.6.4

| 审计项 | 最终判断与证据 |
|---|---|
| 实际SDK/MMP调用 | 【游戏代码证实】MAX/Metica展示收益桥及Adjust/Firebase/TikTok分发；不是仅SDK名称存在。`AdMeticaDefault.OnShowRevenuePaid` RVA0x32deaf0、`AdRevenueTracking.ImpressionSuccessEvent` RVA0x32c2988。[F64C02/03；C05/C06] |
| 真实IAA链 | 展示收益回调→实际金额→独立收入报告；`IAAController.OnAdRevenuePaidEvent` RVA0x24401f8同时处理总额/缓存。[F64C01] 生产到账、precision、MMP与媒体账单对账未取到 |
| IAP链 | 【游戏代码证实】schema/购买确认方法；【无法确认】真实成交、验单/退款/净额账本。不能将可调用API写成支付结果。[02号C08/C09] |
| 行为/代理链 | 关卡、会话、激励次数；国家taichi门槛是已实现收入的分桶/达标事件，**不是未来预测**。默认US/T1/T2/T3金额0.50/0.30/0.20/0.03，实际缓存超额全部报出后清零。该路径Firebase-only。[F64C01；03号] |
| 去重及会计风险 | 同一经济收入既有ILRD又有阈值副本；两者不能加总。缓存清零不是送达ACK；不证明后台重复计算或正确去重。远程默认值不等于生效值 |
| 同App历史入口 | 【官方公开证实】Adjust→Axon可配all sources，Unity也有partner契约；【无法确认】该游戏授权/启用/回填/生效窗口。[CT62S08；57号] |
| MAX直发与模型消费 | SDK landing等自动事件链已证；Car通用MAX/Metica桥不证明具体关卡/taichi调用它。结构化Axon在13.6.4存在，不证明业务可达/送达。Axon/Vector训练消费未证。[F64C17/18；20号] |
| 成本与成熟收益 | 【无法确认】实际指定平台campaign成本、成熟净D28收入、边际ROAS、增量净收益。无独立证据将增长归因两家平台 |

```mermaid
flowchart LR
 A[展示收益] -->|游戏代码 F64C01-03| B[原始金额分发]
 B -->|游戏代码| C[Adjust / Firebase / TikTok]
 A -->|游戏代码| D[国家缓存与达标]
 D -->|游戏代码 Firebase-only| E[taichi事件]
 C -.->|配置/送达未知| F[指定网络接收]
 E -.->|没有已证路由| F
 F -.->|训练/效果未知| G[盈利获客]
```

**竞争性解释：**最强的是“已有真实价值反馈基础”，而非“国家阈值驱动Axon增长”。M1玩家选择、M2全来源学习、M4变现和M5素材市场都相容；M3无四款级辨识证据。若收益改善仅发生在固定自然量/同一UA cohort的变现随机组，优先支持M4；若平台未收该阈值则排除该条特定输入解释，不能连带排除原始ILRD路径。

**最小补证：**①当前收入partner映射/来源开关/投递接收；②ILRD与taichi的独立事件语义、幂等/精度/远程生效版本；③相同素材/国家的成熟支出收益及随机UA×变现对照。无需真实用户广告ID。

## 2. Meowdoku · 1.25.1 / MAX13.2.0 / GRT1.3.2.0

| 审计项 | 最终判断与证据 |
|---|---|
| 实际业务与SDK | 【游戏代码证实】Godot Tracker→UniKit/Learnings/GRT；GRT `BaseGrtEvent.sendEvent` L66—94过滤后→`BridgeManager.sendEvent`→接收端。接收列表可配置，不能把全部工厂处理器当生产全开。[F64C05/07/08；M01—M05] |
| 真实IAA链 | 广告收入桥/GRT；`LTVManager.getLTV/increaseLTV` L50—65累计`sp_key_ltv`已实现收入。收入金额的原始precision及最终结算未核，不是未来LTV模型。[F64C04] |
| IAP链 | 订阅/购买漏斗与可选IAP规则类型有代码；无真实支付返回、验单、退款及净额事件账本，不以订阅点击或工厂枚举填补。[02号M01；F64C07/08] |
| 代理事件 | 安装时间窗×关卡/活跃分钟；来源/国家/livingDay过滤；IaaFbRoas可增量，LtvEvent可累计/once。名含Fb不代表仅发Meta，接收端由配置选。[F64C04—08；03号] |
| 去重与口径 | 累计value与增量value混加会重复；本地once/lastReportLTV不等于服务端事务ACK；广告完成/奖励不是收入；当前GRT表缺失使实际输出量不可算 |
| 同App历史入口 | AF全来源/organic与partner共享契约可配置；四款实际开关和训练样本未知。不要把unattributed当无法归属或跨游戏个人画像。[57号；MA60S14] |
| MAX直发及消费 | 13.2无新版结构化Axon；有SDK自动旧事件。所查DEX未建立GRT→EventService显式链；不能据此排除服务端MMP或native/反射。[F64C17/18；20号] |
| 成本与成熟收益 | 无实际Axon/Vector成本/成熟净回报/代理消融，不能判断GRT是否比简单D0收入更有预测力 |

```mermaid
flowchart LR
 A[关卡 / 活跃 / 广告收入] -->|游戏代码 F64C04-08| B[GRT时间窗 / 累计 / 过滤]
 B -->|游戏代码 按receiver配置| C[AF / Meta等SDK]
 C -.->|partner与实际投递未知| D[指定网络]
 D -.->|模型用途未知| E[价值排序 / 实际回报]
 F[MAX13.2自动生命周期] -->|SDK代码 独立路径| G[AppLovin旧事件]
```

**竞争性解释：**有证据支持“早期参与与收益分层意图”。更密集代理是否有益取决于真实目标及映射；如果GRT代理只是在已有广告次数/收入上重复编码，不能预设模型得到新信息。M2同App全来源是平台能力，M1/M4仍相容；没有特征/反馈对照不能分配因果。

**最小补证：**①生效GRT JSON/规则版本/receiver/单位；②AF partner配置及真实投递；③成熟D28按D0行为→再加D0真实收入→再加GRT的时间外/授权holdout比较，固定广告策略并保留零收入玩家。

## 3. Rotate Rings · 1.2.4 / MAX13.6.2 / AppsFlyer6.17.5

| 审计项 | 最终判断与证据 |
|---|---|
| 实际业务与MMP | `SDKManager.handleAdRevenue` L386、异步upload L802；`g8.a.adRevenue` L100—123明确调AF `logAdRevenue`，金额USD/d，mediation为APPLOVIN_MAX。[F64C09/10] |
| 真实IAA | 标准AFAdRevenueData直接赋值；还有ad_revenue2和ad_revenue4，不能假定三份独立收益。监听/重试与后台是否重复入账须另验 |
| IAP | 代理档位/命名不是已验证商店支付；无实际IAP订单、验单退款及净额账本。[03/49号] |
| 行为/代理/达标 | 国家×安装day0—6比较R>T，每天一次value=累计R；美国首日≥900秒及≥0.45收益资格；首次插屏资格及固定档位。`ta.d.j`L4405国家表是门槛非CPI/预测。[F64C11/12] |
| 去重与口径 | 同经济展示多路副本，跨日累计R重叠，固定档位/累计/单次金额混用是三种不同风险；不能从风险推断后台已实际重复计收 |
| 同App历史入口 | AF→网络的all-source/事件/专用ad_revenue契约；四款partner配置、金额开关、历史共享和接收未证。[57号、RV61S03] |
| MAX与训练 | APPLOVIN_MAX枚举证明中介来源，不证明获客。13.6.2有结构化分支但无已建立业务直达链；模型消费未知。[F64C17/18；20号] |
| 成本收益 | 无指定获客平台成本、成熟去重净收益和实验。不能把精细国家阈值表当投放或盈利证据 |

```mermaid
flowchart LR
 A[单展示实际收益d] -->|游戏代码 F64C09-10| B[AF标准广告收入]
 A -->|游戏代码| C[ad_revenue2 / 4]
 A -->|游戏代码 F64C11-12| D[国家/安装日/时长资格]
 D -->|游戏代码| E[累计/档位事件]
 B -.->|partner配置及接收未知| F[Axon / Unity]
 C -.->|映射去重未知| F
 E -.->|用途未知| F
 F -.->|无训练或盈利证据| G[实际增量]
```

**竞争性解释：**最强静态证据是标准真实收益到AF入口，以及开发者按早期资格分层；不等于知道广告平台实际选了哪条目标。M1/M2/M4/M5都相容；一个可检验反例是“只改报表映射后ROAS上涨，而独立净收益未变”，这会反驳真实盈利改善而非仅反驳模型。

**最小补证：**①AF三路收入及规则事件映射/幂等/接收；②展示经济事件与跨日累计分账、precision/币种/时间；③固定国家/素材/广告策略的成熟成本收益与目标切换holdout。

## 4. Jewel Coloring · 1.24.1 / MAX13.6.3 / AdWorth10.2.3默认配置

| 审计项 | 最终判断与证据 |
|---|---|
| 组件与实际入口 | 【游戏代码证实】Bulldog初始化AdWorth，原生库规则/账本/系数/路由；不是Adjust标准模块的同名功能。商业所有权未知。[F64C19；09号D02] |
| IAA价值来源 | 广告展示价格/价值进入本地多key账本，真实ILRD、估计/默认bidder价格回退需分开；不能把全部AdWorth数值当结算收入。[F64C13/16；09号] |
| IAP | 默认514按广告价值调用Meta logPurchase；它是代理而非真实付费。未取得真实商店验单退款/净额账本。[F64C13—15] |
| 行为与代理 | 默认90规则/31权重表，登录/时长/最高关/插屏/eCPM/展示率参与；normal、interval、x100等金额语义。来源表和国家条件能力存在，默认90未引用来源表且无直接国家条件。[F64C13；09号] |
| 路由与状态 | Firebase/Meta/Adjust输出；`sendMsgToPlatform`RVA0x1a44350调用后更新本地状态，不是远端ACK；未建立AdWorth→MAX显式业务路由。[F64C14/15/17/18] |
| 去重/会计 | 多key可能复用同经济收入；系数、倍率、累计与间隔不可相加；代理purchase不入真实IAP；没有后端幂等证明，不推断后台实际错误 |
| 同App历史入口 | Adjust全来源共享可配，但只覆盖实际映射事件与条件；不能把Meta/Firebase事件自动画到Adjust或AppLovin。[CT62S08；20/57号] |
| 生产与成本收益 | 无热更生效表、指定模型消费、实际Axon/Vector成本成熟净收入和增量；规则复杂不能证明模型成熟或投放成功 |

```mermaid
flowchart LR
 A[广告价格/收益及行为] -->|游戏代码 F64C13-16| B[AdWorth账本/系数/条件]
 B -->|游戏代码 默认平台规则| C[Firebase / Meta / Adjust]
 B -->|游戏代码 代理value| D[Meta purchase]
 C -.->|仅实际MMP映射可配 送达未知| E[指定网络]
 D -.->|无已证自动转发| E
 E -.->|模型/效果未知| F[实际盈利]
```

**竞争性解释：**更丰富的开发者代理可能提供早期信号，也可能只是重复已实现广告收益/参与度，甚至与广告强度共同引入偏差。它不需要跨App图谱才能执行；默认来源权重未启用不能被扩展为“线上绝不使用”。M1与M4、远程策略及素材变化仍不可辨识。

**最小补证：**①实际热更/路由/输出单位；②广告价格与真实ILRD及结算精度、代理purchase分账和Adjust投递；③成熟真实收入下代理增量、广告强度及留存的受控对照。

## 5. 横向裁决

| 能力或结果 | Car | Meow | Rotate | Jewel |
|---|---|---|---|---|
| 真实展示收益业务入口 | 已定位ILRD | 已定位收入桥/累计 | 已定位AF标准金额 | 已定位价格/价值账本，精度/回退需另分 |
| 开发者早期代理/门槛 | 国家缓存、关卡/激励 | 时间窗参与/GRT | 国家安装日/复合资格 | AdWorth多条件/系数 |
| 所指代理直接到MAX Axon | 未建立 | 未建立 | 未建立 | 未建立 |
| 同App全来源共享 | 官方可配置，启用未知 | 同左 | 同左 | 仅已映射Adjust路径可配置，其他端不自动转发 |
| Axon/Vector实际训练 | 无证据 | 无证据 | 无证据 | 无证据 |
| 指定平台实际盈利扩量 | 无成本/成熟收益证据 | 同左 | 同左 | 同左 |

**最终结论：**能比较的是客户端信号设计，不能排名真实买量能力。最值得自建的机制是语义准确的真实收入账本、可靠幂等和授权MMP回传、少量可解释早期代理与成熟LTV验证，以及获客×变现分开实验；不能照抄国家金额或把广告收益伪装purchase，也无需为此先建跨App个人图谱。[10号、61—64号；MA60S10、RV61S03]
'''
write('model-architecture/FOUR_GAME_VERDICTS.md', appendix)

stop = r'''# 公开研究停止与授权恢复条件

2026-11-19 · 第64号。现阶段可以证明部分客户端路径与官方数据用途，不能独立证明四款目标游戏的服务器消费、闭源模型或盈利因果。停止的是无新增辨识度的逆向/广搜，不是断言这些机制不存在。

| 问题 | 当前可证上限 | 立即停止的低价值动作 | 满足什么才恢复 |
|---|---|---|---|
| MAX结构化Axon业务事件 | 自动事件、通用桥与新版分支已追踪；四款具体价值显式直达链未建 | 再搜默认事件名并写成实际调用；把MMP路径拼到MAX | 具体新增callsite、授权生效桥配置或去标识业务日志，指向一条明确未证边 |
| Token与server feature | 外层构造/历史上下文及隐私门控可见；不透明payload与服务器映射未知 | 猜解密Token字段、抓取真实身份、生产测试 | 官方字段/版本契约，或授权隔离合成测试与对应服务端feature血缘；授权必须覆盖用途 |
| partner共享与投递 | 全来源、映射、金额及窗口契约可查；四款启用未知 | 从SDK存在推断后台开关；把生产HTTP发送实现称送达 | 授权配置快照/生效时点、投递与接收对账。2xx仅解释该入口响应，不外推训练 |
| 真实标签与成熟度 | 可构造IAA/IAP字段；经济事件、退款/去重/成熟生产规则未知 | 把代理、paid+fulfilled、累计与副本求和 | canonical规范及成熟cohort净账本、可用/到达时间、精度/币种与幂等、对账差异 |
| 冷启动与跨游戏 | 同App来源学习有契约；Vector聚合用途有披露；共享参数与个人历史未知 | 用ID共包、招聘或专利唯一选B/C/D | 明确生产模型/特征/聚合schema、权限scope和时间水位；合法禁用统计/共享参数/个人历史的消融 |
| Axon价值分布 | 官方多日价值distributions措辞与决策用途；未证每用户显式分布 | 用复数名词补出PDF、分位数、tail loss或风险出价 | 官方生产输出schema/接口、含定义的技术论文/代码；若要证明风险决策需固定均值改变不确定性的授权对照 |
| Vector Runtime/Insights | IAP/Analytics/Core公开接口止于gateway/native；用途类别有披露 | 把Unity同厂商当训练直连；用字段名猜Vector loss | 明确逐字段接收→授权用途→训练作业的数据血缘，不以未授权测试越过闭源接口 |
| 出价/预算控制 | 目标ROAS、部分公开预算行为与拍卖协议；controller内部未知 | 通用数学公式冒充报价；从第一价格反推shading | 平台授权决策日志/控制契约及固定预测分数的策略对照；OpenRTB不替代控制器 |
| 四款盈利性扩量 | 无实际指定平台成本/成熟净收益或因果实验 | 看下载量、财报或SDK版本倒推预算/盈利 | 同条件成本、成熟净收入、预算档位/素材国家策略和可识别holdout，复核边际而非只看平均 |

恢复材料的共同验收条件：所有者/用途授权明确；去标识研究键只在授权scope内有效；时间与版本对应；事件/available_at/接收时间分开；不请求真实个人ID；原件只读；数据授权不自动授权生产调用；每条边分别记录六层证据，不把前一层升为后一层。

最有价值的三包材料：

1. **partner配置与投递/接收对账包**，先判断收入和来源是否真的送给指定网络。
2. **成熟单位经济与受控实验包**，判断真实净收益/边际扩量及获客、变现、归因之间的贡献。
3. **训练—推断—控制器血缘与消融包**，区分数据、模型、出价策略以及聚合/参数/个人历史。

没有新材料时，保留未知，不继续扩大SDK清单，不重复公共架构检索。出现真正限定产品、日期、生产用途的官方技术材料时，可只复核对应断点，不重启全部研究。材料缺一部分就只更新能支持的层级；不因取得后台截图便宣称训练使用或因果盈利。

依据：[最终报告](../64_普通游戏盈利跃迁最终机制判断.md)、[四款审计](FOUR_GAME_VERDICTS.md)、[61号](../61_收入标签与价值分布预测.md)、[62号](../62_跨游戏知识迁移与冷启动机制.md)、[63号](../63_预测价值到实时竞价与预算约束.md)、[来源账本](final64/SOURCE_LEDGER.json)。本文件是研究设计与停止决策，不是新的生产事实。
'''
write('model-architecture/STOP_AND_RESUME_CRITERIA.md', stop)

catalog = ['# 第64号复用证据目录', '', '本轮只综合既有证据并核对哈希；未下载、未调用生产端点、未获得新生产事实。源码行号按现有反编译文件，RVA按原样本；不是新版游戏的通用地址。历史证据若有编码显示问题，保留原字节，使用可核路径与后续报告解释，不修写原件。', '', '## 官方来源（复用原编号）', '']
for s in official:
    catalog += [f'<a id="{s["id"].lower()}"></a>', f'### {s["id"]}', '',
        '- 【官方公开证实】厂商公开用途/契约；不等于四款已启用或独立生产审计。',
        f'- 原文：{s.get("url", "see original source record")}',
        f'- 日期：{s.get("source_date", "not stated")}',
        f'- 本地：[{s["path"]}](../../{s["path"]})；L{s.get("start_line", "?")}—L{s.get("end_line", "?")}',
        f'- SHA256：`{s["sha256"]}`', '']
catalog += ['## 游戏静态原始位置（新索引，非新证据）', '']
for s in raw_sources:
    catalog += [f'<a id="{s["id"].lower()}"></a>', f'### {s["id"]} · {s["product"]}', '',
        f'- 【游戏代码证实】{s["claim"]}', f'- 样本：{s["version"]}',
        f'- 原始位置：[{s["path"]}](../../{s["path"]})', f'- 类/方法/位置：`{s["class_method_or_location"]}`',
        f'- SHA256：`{s["sha256"]}`', '- 边界：静态实现；生产发送、接收与模型消费未证。原包信息复用SAMPLE_CATALOG及旧证据索引，不修改原包。', '']
catalog += ['## 复用报告与历史修正顺序', '',
    '- Jewel默认配置以09/10号为准：03号当时缺明文配置的限制已补齐；不把03号旧未知继续引用为当前结论。',
    '- MAX事件以20—22号为准：自动事件、默认事件名与游戏显式触发分开；两条MMP/直发路径分开。',
    '- 收入副本与IAP边界见49/53—55号；安装前信号/授权共享见56—58号；架构边界以60—63号及MA60/RV61/CT62原始来源为准。',
    '- 本轮不以供应商案例、招聘、财报、专利或旧合成实验证明四款真实盈利；未追加任何真实效果数值。']
write('model-architecture/final64/SOURCE_CATALOG.md', '\n'.join(catalog))

mechanisms = [
 dict(id='M1',name='玩家价值排序改善',ability='Axon按广告主展示价值/return goals出价；Vector按D7/D28收入动态竞价',config='MMP partner、事件/收入映射、目标与窗口',unknown='真实特征join、校准、训练样本与价值排序增量',metric='成熟cohort净LTV、CPI、win rate、每安装贡献',alternative='M4同类玩家变现收益提高；M5库存/素材/国家变化',falsifier='固定其他条件的授权实验中预测校准/尾部识别/成熟贡献不改善，或该输入未被训练消费',experiment='固定库存/素材/预算/广告策略，价值目标/排序holdout并核对成熟净贡献',refs=['MA60S01','MA60S02','MA60S04','MA60S13']),
 dict(id='M2',name='同App自然量/跨渠道历史冷启动',ability='Unity明确预启动全来源帮助训练；Axon有all-source与自愿共享契约',config='全来源/organic开关、事件窗口、开始共享时点',unknown='四款生效开关、实际历史样本/权重与冷启动增益',metric='学习成本、初始校准、有效样本覆盖、早期净贡献',alternative='M3跨游戏先验；M5素材/预算优化',falsifier='配置/投递证明该期无同App历史输入，可排除该路径解释；零效应实验只约束测试范围',experiment='合法历史共享holdout，保持目标/预算/素材固定，记录可用时间与成熟结果',refs=['MA60S14','CT62S08','MA60S02']),
 dict(id='M3',name='跨游戏聚合知识或模型迁移',ability='Vector披露跨游戏模式/聚合cohort bid-time用途；Axon披露额外广告主数据改善模型',config='需明确合法训练用途与统计/参数/个人历史边界',unknown='实际共享参数、统计与个人历史贡献及四款生产使用',metric='新游戏初始先验、样本效率、低覆盖流量校准',alternative='M2同App历史已足够；M1仅上下文改进',falsifier='授权生产血缘明确隔离对应统计/权重可排除该实现；关闭个人ID不能排除聚合/参数迁移',experiment='同数据/机会预算下分别禁用聚合统计、共享参数和合法个人历史',refs=['MA60S17','MA60S02','MA60S23']),
 dict(id='M4',name='MAX或LevelPlay变现收益改善',ability='多网络竞价/信号/超时/收入回调；四款MAX相关收益入口存在',config='有效需求、底价、广告策略、频次与隐私配置',unknown='同类玩家真实填充/eCPM/净LTV增量及留存抵消',metric='净ARPDAU、填充/展示率、eCPM、成熟净LTV',alternative='M1买来更高价值玩家；M5地区/广告策略改变',falsifier='固定UA cohort的变现随机实验无净LTV提升或留存损失抵消',experiment='UA固定下mediation/广告策略随机组，再做UA目标×变现因子实验',refs=['RV61S15','RV61S16']),
 dict(id='M5',name='素材国家预算目标归因变化',ability='国家tROAS、预算与目标影响交付；归因不等于增量',config='实际素材/国家/目标/预算/归因窗口变更',unknown='四款真实变更日志、成本收益和控制条件',metric='CTR、安装率、CPI、库存结构、报告/真实ROAS、边际净贡献',alternative='M1模型排序改善；M4变现需求改善',falsifier='锁定变更日志和独立净收益对账可排除相应变更或仅归因重分配',experiment='固定口径与成熟cohort，素材/目标/国家分层随机或地域holdout',refs=['RV61S05','RV61S06','MA60S27']),
]
game_calls = {
 'Car Race':('ILRD→Adjust/Firebase/TikTok；国家阈值只到Firebase；关卡/激励里程碑', ['F64C01','F64C02','F64C03','F64C17']),
 'Meowdoku':('Tracker/GRT时间窗与实际收入→配置选择AF/Meta等；线上GRT表未知',['F64C04','F64C05','F64C06','F64C07','F64C08','F64C17']),
 'Rotate Rings':('MAX callback→AF标准logAdRevenue＋ad_revenue2/4；国家安装日/时长规则',['F64C09','F64C10','F64C11','F64C12','F64C17']),
 'Jewel Coloring':('AdWorth账本/行为系数→Firebase/Meta/Adjust；默认90规则；purchase含代理',['F64C13','F64C14','F64C15','F64C16','F64C17']),
}
rows=[]
for game in ['ALL_MECHANISMS'] + list(game_calls):
    for m in mechanisms:
        actual = '四款有收入/行为入口，均无指定模型消费与盈利归因证明' if game == 'ALL_MECHANISMS' else game_calls[game][0]
        # A game call is an input capability, never an assertion that this causal mechanism ran.
        refs = m['refs'] + ([] if game == 'ALL_MECHANISMS' else game_calls[game][1])
        rows.append(dict(claim_id=f'F64-{game.replace(" ","_")}-{m["id"]}',scope=game,mechanism_id=m['id'],mechanism=m['name'],
            evidence_grade='【官方公开证实】能力；【游戏代码证实】入口；【合理推断】因果解释；【无法确认】四款效果',
            verified_technical_ability=m['ability'],verified_game_calls=actual,
            game_call_does_not_prove_mechanism='true',configurable_unverified_feedback=m['config'],unproven_server_consumption=m['unknown'],
            impacted_unit_economics=m['metric'],strongest_competing_explanation=m['alternative'],potential_falsifier=m['falsifier'],
            minimum_authorized_experiment=m['experiment'],requires_cross_app_personal_identity='false; personal-history variant would require specific consent/join evidence',
            production_delivery_proven='false',model_training_proven_for_target_games='false',game_profit_causality_proven='false',
            source_ids=';'.join(refs),source_catalog='model-architecture/final64/SOURCE_CATALOG.md',reviewed_utc=NOW))
csvbuf=io.StringIO(newline='')
writer=csv.DictWriter(csvbuf,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
write('model-architecture/FINAL_CAUSAL_MATRIX.csv',csvbuf.getvalue())

# Append scoped game evidence and unknown production boundaries; do not alter old objects.
new_nodes=[];new_edges=[]
def node(ident,label,stage,company='research synthesis',**kwargs):
    new_nodes.append(dict(id=ident,label=label,stage=stage,company=company,**kwargs))
def edge(ident,src,dst,claim,refs,status='unknown',actual=False,construction=False,missing='Target partner activation, delivery, receipt, training lineage and controlled net profit'):
    available={s['id']:s for s in official+raw_sources}
    evidence=[available[i] for i in refs]
    new_edges.append(dict(id=ident,source=src,target=dst,claim=claim,source_ids=refs,
        status=status,evidence_level='【游戏代码证实】' if actual else ('【合理推断】' if status=='inference' else '【无法确认】'),
        edge_type='final_causal_synthesis',diagram_style='solid' if actual else 'dashed',
        data_provider=src,data_receiver=dst,explicit_call_chain=claim if actual else 'No production call chain asserted',
        class_method_lines=[{'path':s['path'],'class_method_or_location':s.get('class_method_or_location'),'start_line':s.get('start_line'),'end_line':s.get('end_line')} for s in evidence],
        sha256=[{'path':s['path'],'sha256':s['sha256']} for s in evidence],
        six_layers={'sdk_capability':actual,'actual_game_business_callsite':actual,'request_construction_code':construction,
            'production_successful_send':False,'server_received':False,'server_model_training':False},
        permission_conditions='Static existing authorized samples only; live sharing would need advertiser authorization, consent and scoped join; available_at <= bid_time for features',
        applies_to='Existing sample/static path only' if actual else 'Unproven production or causal connection; not a deployment assertion',
        missing_evidence=missing,reviewed_utc=NOW,production_actual_proven=False,observed_target_game_delivery=False,
        independent_production_audit=False,new_production_evidence=False))

for idx,(game,(call,refs)) in enumerate(game_calls.items(),1):
    key=f'F64G{idx}'
    node(key+'_input',game+' 收入/行为输入','game_business',game)
    node(key+'_sdk',game+' 本地已识别平台分发入口','sdk_api',game)
    node(key+'_network',game+' 指定获客网络接收（未证）','unknown_delivery',game,hypothesis_only=True)
    node(key+'_training',game+' 指定模型训练消费（未证）','unknown_training',game,hypothesis_only=True)
    node(key+'_profit',game+' 增量净盈利/边际扩量（未证）','unknown_causal_profit',game,hypothesis_only=True)
    edge(f'F64E{idx:02d}A',key+'_input',key+'_sdk',call,refs,status='proven_scoped_static',actual=True)
    edge(f'F64E{idx:02d}B',key+'_sdk',key+'_network','MMP partner sharing is configurable; this game activation/delivery is unknown',refs+['CT62S08','RV61S03'])
    edge(f'F64E{idx:02d}C',key+'_network',key+'_training','Receiving an event does not prove canonical labels or model consumption',refs+['MA60S02','MA60S14'])
    edge(f'F64E{idx:02d}D',key+'_training',key+'_profit','Even model consumption does not prove incrementality, profitability or sustainable marginal scale',refs+['MA60S27'])

node('F64_profit','普通游戏净贡献跨越盈亏线：解释框架，非四款事实','causal_hypothesis',hypothesis_only=True)
for m in mechanisms:
    nid='F64_'+m['id'];node(nid,m['name'],'competing_causal_mechanism',hypothesis_only=True)
    edge('F64E_'+m['id'],nid,'F64_profit',m['name']+' may change unit economics, but no target-game causal effect is established',m['refs'],status='inference',missing=m['unknown']+'; '+m['experiment'])

existing_ids={n['id'] for n in graph['nodes']}|{e['id'] for e in graph['edges']}|{s['id'] for s in graph['sources']}
for record in new_nodes+new_edges+raw_sources:
    if record['id'] in existing_ids:raise RuntimeError('Duplicate id '+record['id'])
graph['nodes'].extend(new_nodes);graph['edges'].extend(new_edges);graph['sources'].extend(raw_sources)
graph['final_causal_round64']=dict(reviewed_utc=NOW,scope='Final synthesis only; no new production or fetched evidence',
    report='64_普通游戏盈利跃迁最终机制判断.md',causal_matrix='model-architecture/FINAL_CAUSAL_MATRIX.csv',
    source_ledger='model-architecture/final64/SOURCE_LEDGER.json',history_snapshot='model-architecture/final64/EVIDENCE_GRAPH.before.json',
    new_node_ids=[n['id'] for n in new_nodes],new_edge_ids=[e['id'] for e in new_edges],new_source_ids=[s['id'] for s in raw_sources],
    public_research_recommendation='Stop repeated broad SDK/architecture search; resume only with specific new primary or authorized production evidence',
    no_new_production_evidence=True,game_profit_claims_proven=False)
# Keep the old global reviewed timestamp and all historical extension metadata intact.
graph_path.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dump('model-architecture/final64/NEW_EDGES.json',new_edges)

addition = '''\n\n<a id="final64"></a>\n\n## FINAL64 · 普通游戏盈利跃迁最终综合（无新增生产证据）\n\n- [64号独立最终报告](64_普通游戏盈利跃迁最终机制判断.md)\n- [25行因果矩阵：总框架＋四款×五机制](model-architecture/FINAL_CAUSAL_MATRIX.csv)\n- [四款逐案审计及技术链图](model-architecture/FOUR_GAME_VERDICTS.md)\n- [停止与授权恢复条件](model-architecture/STOP_AND_RESUME_CRITERIA.md)\n- [复用原始URL/方法/RVA/SHA256目录](model-architecture/final64/SOURCE_CATALOG.md)\n- [机器可读来源账本](model-architecture/final64/SOURCE_LEDGER.json)\n- [新增关系边](model-architecture/final64/NEW_EDGES.json)\n- [更新前图快照](model-architecture/final64/EVIDENCE_GRAPH.before.json) / [历史文件哈希](model-architecture/final64/HISTORY.before.json)\n- [交付校验](model-architecture/final64/VALIDATION.json)\n\n结论：价值排序、同App全来源历史、跨游戏聚合或参数迁移、变现改善、素材/国家/预算/归因均为竞争性解释；没有四款目标游戏指定模型消费、实际导量盈利或因果增量的新证据。新增图边实线只表静态业务入口；送达/训练/盈利边保留未知。官方原编号MA60/RV61/CT62复用，未改变旧对象；F64C01—F64C19仅为既有静态原件的新索引。\n'''
for s in raw_sources:
    addition += f'\n<a id="{s["id"].lower()}"></a>\n\n- **{s["id"]}** 【游戏代码证实】{s["product"]} / {s["class_method_or_location"]}；[{s["path"]}]({s["path"]})；SHA256 `{s["sha256"]}`；仅静态范围，生产送达/训练/效果未证。\n'
with index_path.open('ab') as f:f.write(addition.encode('utf-8'))

# Report-specific verification; no SDK or production endpoint is executed.
errors=[]
for rel,expected in history.items():
    if sha(ROOT/rel)!=expected:errors.append('Historical bytes changed: '+rel)
for s in official+raw_sources:
    if sha(ROOT/s['path'])!=s['sha256']:errors.append('Source hash mismatch: '+s['id'])
after=json.loads(graph_path.read_text(encoding='utf-8'))
for k in ['nodes','edges','sources']:
    if after[k][:len(old_graph[k])]!=old_graph[k]:errors.append('Historical graph list mutated: '+k)
for k,v in old_graph.items():
    if k not in ['nodes','edges','sources'] and after[k]!=v:errors.append('Historical graph metadata mutated: '+k)
if not index_path.read_bytes().startswith(old_index):errors.append('Index old bytes overwritten')
node_ids={n['id'] for n in after['nodes']};source_ids={s['id'] for s in after['sources']}
for k in ['nodes','edges','sources']:
    ids=[v['id'] for v in after[k]]
    if len(set(ids))!=len(ids):errors.append('Duplicate '+k+' ids')
for e in new_edges:
    if e['source'] not in node_ids or e['target'] not in node_ids:errors.append('Invalid graph endpoint '+e['id'])
    if set(e['source_ids'])-source_ids:errors.append('Invalid source ref '+e['id'])
    if e['six_layers']['production_successful_send'] or e['six_layers']['server_received'] or e['six_layers']['server_model_training']:errors.append('Invalid production promotion '+e['id'])
deliverables=['64_普通游戏盈利跃迁最终机制判断.md','model-architecture/FINAL_CAUSAL_MATRIX.csv','model-architecture/FOUR_GAME_VERDICTS.md','model-architecture/STOP_AND_RESUME_CRITERIA.md','model-architecture/final64/SOURCE_CATALOG.md']
links_checked=0
for rel in deliverables:
    p=ROOT/rel
    txt=p.read_text(encoding='utf-8')
    if '\ufffd' in txt:errors.append('Replacement character in new deliverable '+rel)
    if p.suffix!='.md':continue
    for target in re.findall(r'\]\(([^)]+)\)',txt):
        if target.startswith(('https:','http:','#')):continue
        q=(p.parent/target.split('#')[0]).resolve()
        if not q.is_file():errors.append('Broken local link '+rel+' -> '+target)
        links_checked+=1
with (ROOT/'model-architecture/FINAL_CAUSAL_MATRIX.csv').open(encoding='utf-8',newline='') as f:
    parsed=list(csv.DictReader(f))
if len(parsed)!=25:errors.append('Expected 25 causal rows')
for r in parsed:
    if r['game_profit_causality_proven']!='false':errors.append('Unsupported causal production claim')
validation=dict(status='PASS' if not errors else 'FAIL',reviewed_utc=NOW,
    scope='Artifact/source hash, graph preservation, link and causal-boundary checks only; not platform production evidence',
    primary_deliverables=len(deliverables)-1,causal_rows=len(parsed),games=4,mechanisms=5,
    historical_report_and_matrix_manifest_files_verified=len(history),original_sources_hash_reverified=len(official)+len(raw_sources),
    historical_graph_nodes_preserved=len(old_graph['nodes']),historical_graph_edges_preserved=len(old_graph['edges']),historical_graph_sources_preserved=len(old_graph['sources']),
    new_graph_nodes=len(new_nodes),new_graph_edges=len(new_edges),new_static_source_aliases=len(raw_sources),
    index_original_bytes_preserved=True,local_links_checked=links_checked,
    sdk_executed=False,new_public_downloads=0,production_ad_requests=0,real_identifiers_collected=0,
    new_training_or_profit_production_evidence=False,errors=errors)
dump('model-architecture/final64/VALIDATION.json',validation)
print(json.dumps(validation,ensure_ascii=True,indent=2))
if errors:raise SystemExit(1)
