# 与Axon/Vector已证证据的差距矩阵

本轮是公开技术研究和自主架构设计，不是厂商生产逆向复原。未安装/运行解析库、SDK、服务或模型；未访问身份接口、投放端点、真实个人记录；76号程序不改、不重跑。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 第三方开源能力、协议和论文都不归属于Axon或Vector。

本轮没有新取得Axon/Vector官方生产架构映射或匿名日志；只复用72/74/77/78及Adjust限定分析，未重复招聘、专利、隐私泛搜或合作名单。新增开源/论文/协议原件是独立参考技术证据，不是厂商证据升级。

| 缺口 | 自主参考能力 | Axon现有边界 | Vector现有边界 | 仍需原件 |
|---|---|---|---|---|
| G01 命名空间 | NS可显式tenant/issuer/app/partner/grain | Adjust本地UUID/OS与external传输入口；Axon实际resolver输出UNKNOWN | UPA组织/项目账号及Exchange/RampID产品披露；Vector解析scope UNKNOWN | 经核验的resolver组件/版本与命名空间、实体粒度/结果契约；AM01–06；IG72S02/03/05；IV74S02；EC78S01 |
| G02 确定性账号跨设备 | DR经自有认证仅建account-device | 账号接口不证明Axon接收或匹配 | Unity Authentication/UPA不证明Ads/Vector接收账号关系 | 实际认证映射回执+指定接收产品收妥记录，合法用途；IG72S02/03；AM06；EC78S01 |
| G03 概率匹配与质量 | 可比较FS/监督评分/拒识，未执行 | 没有Axon指定身份匹配模型/校准契约 | LiveRamp matchConfidence规范不等于Vector采用该评分 | 指定产品真实quality语义、代表性校准和误并控制；不能用招聘代替；SIR01–09；IV74S05；77结论 |
| G04 graph解析/合并拆分 | RG版本化边、冲突约束和可撤销membership | 个人图谱组件/合并拆分未获生产证据 | Exchange合作不披露Vector内部graph | 真实resolver输出、图版本和跨系统引用映射；SIR04/07/18/19；IG72S05；EC78S01 |
| G05 实际接收 | ResolutionReceipt与ReceiverReceipt分离 | 广告ID/历史用途披露≠指定Axon收妥本次解析输出 | Exchange官方能力≠Vector实际接收 | 同一解析输出引用→指定Axon/Vector receiver成功回执及时间；IV74S09；IG72S05；EC78S01/04 |
| G06 事件与收入归属 | EL幂等账本及触点/安装/收益分键 | Adjust构包/回调与有界去重不证明Axon训练label | LevelPlay/Unity客户端链不证明Vector训练label | MMP实际接收/partner mapping+成熟收入revision及平台receipt；AM07–15；71/78既有边界 |
| G07 特征物化/时间 | FS双时态+consumer_available门控 | AppLovin用户表示岗位仅团队线索 | Vector训练管道岗位仅工程职责 | 真实feature group/graph/model版本、as-of、availability及特征绑定；S25；PE77S04；SIR11/12；EC78S01 |
| G08 指定价值模型实际读取 | ConsumerReceipt非空输入、inference和decision引用 | C_graph.Axon UNKNOWN | C_graph.Vector UNKNOWN | 权利方可核验实际读取，不是物化/接口/静态bool；active/shadow分开；EC78S01/04；76契约只作原则复用 |
| G09 撤销/删除传播 | CD阻断+图/特征/训练影响per-sink确认 | 未获指定Axon跨层删除与模型影响确认 | 未获指定Vector跨层删除与模型影响确认 | scope/epoch/生效时刻/覆盖与缺失sink、缓存/快照/模型处置；AM15–20；EC78S01；SIR17 |
| G10 个人身份独立价值增益 | 等预算M0–M4消融设计，无真实结果 | D UNKNOWN；预测效果不能反推架构 | D UNKNOWN；披露细节多不等于技术更强 | 合法完整分母/收入、固定容量/训练量/策略的真实对照；74/78结论；本轮LTV接口设计 |
| G11 证据真实性/可引用权 | PA哈希+来源、签认/独立复核；不造日志 | 未取得新授权生产材料 | 未取得新授权生产材料 | 出具者权限、原件/匿名引用、独立核验与环境范围；EC78S01/04 |
| G12 公开研究上限 | 参考架构设计完成≠生产验证启动 | 不因未找到而断言没有图谱 | 不因未找到而排除纯群体/共享参数 | 等待明确授权新原始证据；无新材料保持STOP；77/78停止条件 |

## 不能跳过的三条链

1. resolver输出的实体粒度、结果类型、版本和授权可审查；返回ID不等于既有图实体匹配成功，账号/家庭不等于自然人。
2. 同一输出的跨系统引用必须映射到指定Axon或Vector产品的实际接收回执；Unity Exchange不替代Vector，Adjust请求不替代广告平台接收。
3. 指定价值模型实际非空读取、graph/feature/model版本及广告机会决策引用；物化、查询和shadow分数不得充active消费。要论D再单独做真实独立增益对照。

一份开源实现加一份平台岗位说明，不能拼成上述生产链。当前既不能证明个人级图谱是优势来源，也不能排除只靠上下文、聚合cohort或共享参数产生类似效果。UNKNOWN不是否定存在。

## 最小后续路径

自有实现的契约原型属于另一条工程线，可先验证NS/账号边/撤销/双时态并明确offline-only；本轮没有开发它。厂商取证没有已确认可执行的新渠道，继续STOP，不创建79号。等待权利方允许独立复核的匿名“解析输出→指定产品收妥→模型非空读取→决策trace”材料，或明确指定产品的授权沙箱及schema。仅给SDK版本、岗位、专利、增长案例或ID列表不足恢复。
