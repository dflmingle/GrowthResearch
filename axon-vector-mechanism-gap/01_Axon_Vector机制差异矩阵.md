# Axon与Vector机制差异矩阵

本轮结论：**新增厂商身份图谱机制0，新增C_graph消费链证据0。** 复用旧证据并定向核对两个官方仓库的10条近期release notes，没有下载/扫描/启动SDK、没有查询身份或生产广告接口。新公开响应不是新机制，更不是闭源实现已还原。

CONFIRMED只确认表内明确的契约/原文或有界历史代码事实；官方产品说明不是独立生产审计。INFERRED表示有支持但有替代解释。UNKNOWN不表示不存在。实际范围必须同时看product、版本、原件和缺口，不能把Unity其他产品归入Vector。

|层级|Axon|Vector|
|---|---|---|
|身份输入|**CONFIRMED**：Adjust→Axon伙伴契约列出可配置设备/上下文字段；**UNKNOWN**：具体实例是否实际接收、各ID如何映射|**CONFIRMED（邻接产品）**：Unity Ads/UPA存在输入与身份契约；**UNKNOWN（Vector）**：哪些具体身份字段实际接收及作用域映射|
|关系解析|**UNKNOWN**：多ID输入没有给出resolver输出；MG04仅是**INFERRED**的可行解释|**UNKNOWN（Vector）**：UPA组织账号链接、Exchange/RampID激活可**CONFIRMED**，但不构成Vector解析链|
|图谱更新|**UNKNOWN**：没有Axon TTL、冲突、撤销、重建与删除水位的生产契约|**UNKNOWN（Vector）**：UPA link/unlink与冲突契约可**CONFIRMED**，不能移植为Vector图谱更新|
|特征服务|**UNKNOWN**：无graph output→feature group/model版本、available_at与实际消费接口|**UNKNOWN**：无UPA/Exchange解析结果→Vector接收→图谱特征服务的可核验映射|
|价值预测|**CONFIRMED（官方产品用途）**：多日价值分布与广告主价值方向；**UNKNOWN**：特定图谱输入、结构和独立收益|**CONFIRMED（官方产品用途）**：D7/D28预测及cross-game/cohort方向；**UNKNOWN**：聚合、共享参数和个人历史各自贡献|
|竞价消费|**CONFIRMED（官方产品用途）**：实时评估展示、按return goals出价；**UNKNOWN**：图谱读取→指定机会active trace|**CONFIRMED（官方产品用途）**：动态出价与bid-time intelligence；**UNKNOWN**：具体身份解析特征→指定inference→active决策|

逐行机器版见[六层CSV](01_Axon_Vector机制差异矩阵.csv)。每个单元的适用范围和未知生产边独立记录；不能把上表某层CONFIRMED升级成端到端CONFIRMED。

## 六个重点问题的证据落点

|问题|证据|直接事实与边界|
|---|---|---|
|接收哪些标识/作用域？|MG01/02/03、MG05/06/08|MMP伙伴字段和Web第一方入口有契约；SDK多字段是历史客户端能力，非本次发送/收妥。UPA组织/项目账号、Ads机会、Exchange身份分开。具体Vector列仍未知。|
|有何跨App/设备/账号线索？|MG04/05/06|UPA账号跨游戏/设备与显式冲突有直接契约；Exchange受众激活有产品契约。Axon多ID可能后端映射仅推断；两家的个人图谱生产链仍未知。|
|图谱如何更新？|MG07/09/10|能确认账号服务unlink/冲突，不确认Axon/Vector图谱TTL/撤销/删除/重建。Adjust的禁读/离线/删除请求是另一产品的不同阶段。|
|如何从关系生成历史特征？|MG11/12|没有指定Axon/Vector公开图谱特征API或字段级服务契约。通用特征库与自主GraphFeatureService不能补证。|
|是否进入指定价值模型？|MG13/14＋G07/G08|官方有数据类别和产品用途，不等于某关系结果或某列已被某模型版本实际读取。|
|是否进入实际竞价？|MG14/15＋78号F08|预测与竞价的产品用途明确；欠缺特征读取/inference/机会/active决策的权利方核验引用。|

详见[15项机制证据台账](MECHANISM_EVIDENCE.csv)和[原件关联/哈希](EVIDENCE_SOURCE_LINKS.json)。台账包含具体产品、版本、观察、解释、替代解释、未证断点与自主实现用途。

## 本轮真正新增了什么

只新增两份官方公开release-list响应（NEW01/NEW02），共10条release body逐条阅读，见[获取台账](FETCH_MANIFEST.json)、[release review](RELEASE_NOTES_REVIEW.json)。

- AppLovin MAX Unity Plugin `release_8_6_6`（2026-09-15）依赖Android/iOS13.6.4，只提banner位置/Swift Package Manager等修复；不是新身份解析披露。13.6.4已在旧样本审计覆盖，不重扫。
- ironsource-mobile Unity SDK `UnityLevelPlay_9.3.0`（2026-01-20）release body仅说明版本；其余4条也未给身份图谱/模型映射。短说明不能证明该版本内部没有相关变化。

本次仅两次定向公开元数据GET，不是穷尽公开资料。没有新具体映射就停止扩搜，不用职位/专利/隐私政策/旧接口同义词凑证据。未核验核心SDK具体许可前，不新增反编译；发布页可读不等于实现可复制。

初始化时发现研究根目录没有EVIDENCE_GRAPH.json，已如实记录[初始化说明](INITIALIZATION_NOTE.json)。使用实际存在的EVIDENCE_INDEX、原件manifest与版本化差距矩阵，不创建或恢复一个伪历史图，不修改旧索引。

**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。**
