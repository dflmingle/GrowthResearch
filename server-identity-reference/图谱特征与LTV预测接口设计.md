# 图谱特征与LTV预测接口设计

本轮是公开技术研究和自主架构设计，不是厂商生产逆向复原。未安装/运行解析库、SDK、服务或模型；未访问身份接口、投放端点、真实个人记录；76号程序不改、不重跑。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 第三方开源能力、协议和论文都不归属于Axon或Vector。

## 两个必须分开的契约

`GetFeatureBundle(entity_scope, as_of, read_at, purpose, consumer_product, model_version, policy_epoch)`只返回合法且当时可用的特征及血缘。`RecordConsumerReceipt(...)`另证指定模型非空读取，关联inference、机会和active/shadow/unused决策。成功物化、特征查询或非空JSON均不等于模型实际消费；模型消费也不等于独立增益。

拟议契约见[REFERENCE_CONTRACTS.json](REFERENCE_CONTRACTS.json)。缺身份授权时可采用明确不含个人跨App关系的上下文/群体基线；必须记录fallback_reason，不能把fallback算作图谱消费成功。禁止在报告里用示例字段伪装平台实际训练列。

| 特征组 | 输入与身份要求 | 时间门槛 | 缺失/风险 |
|---|---|---|---|
| F0 当前上下文 | 获授权应用/场景上下文；无跨App个人关系 | 决策前生成并送达 | 不推断隐含同人身份，不用指纹绕过退出 |
| F1 同游戏历史 | 稳定合法安装/账号scope与源事件 | 前缀事件及本地/接收方available_at均≤as_of | ID重置、无观测不等于零消费 |
| F2 跨游戏聚合prior | 合法汇总、cohort定义、最小群体及披露控制；不需个人跨App键 | 聚合快照训练截止与发布时间≤as_of | 稀小群体可能泄露；target测试标签不能参与统计 |
| F3 共享参数表示 | 训练数据权利、源/目标游戏分组、版本；不需个人共享ID | 训练样本/标签成熟后部署，部署≤as_of | 参数可含隐私风险，需独立用途/删除影响审计；共享参数非个人图谱 |
| F4 经关系授权的历史 | 合法typed关系、scope、实际源事件；模型资格与当前epoch | 关系当时已知+有效、源历史当时已知、特征当时可用 | 错误桥接、共享账号、跨设备标签污染；必须记录证据和缺失原因 |
| FQ 关系质量元数据 | method/quality_scope/relationship_age/冲突状态 | 对应关系和质量版本已知 | 未校准分数不得伪装概率；不输出原始身份给模型 |

## Feast可复用和不能自动满足的部分

所固定Feast文档说明默认point-in-time仅约束event timestamp；created_timestamp默认用于同事件时间去重，回填/更正可能回看泄漏。`filter_by_created_timestamp=True`可增加created≤entity时间，但文档明确NULL会排除，且不是每个offline store支持（SIR11/12）。这不是对历史版本或所有底层实现的保证，本轮未运行任何后端。

要将它用于本设计，必须核验所选后端/版本，且证明created时间确实代表指定产品在线可用时间，否则独立显式过滤consumer_available_at；同时验证关系known-at、graph epoch、用途和撤销。Feast entity/join key本身不认证身份（SIR13），在线latest特征也不能替代历史as-of。特征时间正确不自动意味着标签和关系时间正确。

## 收入与标签接口

`RevenueLabelSpec`需明确游戏、install cohort、观察分母、币种、退款/税/平台费、IAA精度、IAP核验、归因/增量范围、D7/D28窗口及mature_at/watermark。标签以实际成熟收入构建，不拿代理事件或模型预测作真实金额。未来未观察到交易、缺采、退出观察与真实零收入分开；未知收入不可补0。

IAA按有契约的经济展示/账本键及revision聚合，不能按广告请求或load回调数计收入；IAP订单/退款独立幂等。金额转换保留原币种/汇率时点。标签可在预测后成熟，这是合法监督目标；但训练标签必须在下一阶段预测前成熟，任何未来标签都不能倒灌成当次特征。

## 独立增益实验的准入设计（本轮不训练）

M0当前上下文；M1加同游戏历史；M2加跨游戏聚合prior；M3在等样本/容量/训练预算下共享参数；M4在M3可比条件上加入合法个人级关系历史。M2/M3须分别对照与消融，不能将更多训练数据的收益全部归给身份图谱。M4额外与等历史量、等维度的非个人聚合特征比较；身份缺失/错误/关系漂移单列。

按实体簇隔离及时间外测试，跨游戏leave-one-game-out、目标游戏冷启动窗口预注册；候选生成/匹配阈值/校准只在训练/验证决定。图关系和所有源特征以预测时已知版本重放，不使用测试未来关系/标签。纯时间外与新实体泛化是不同任务，不能强行同时满足而悄悄更换总体。

指标：匹配Precision/Recall、False Merge Rate=FP/(TP+FP)、FPR=FP/(FP+TN)、False Split定义分母、簇B-cubed或成对指标、候选召回；金额MAE/RMSE/MedianAE、Recall@10%、Top10金额捕获、概率与金额校准。置信区间按真实独立实体/簇而非逐事件bootstrap；边/簇误差都需报告。没有真实成本/完整机会/控制器对照，不报告竞价ROAS或盈利。

## C_graph与D

自有架构可记录一次模型读取，但只能证明自有系统；要证明Axon/Vector，须权利方的resolver输出、指定产品收妥、图谱/模型版本、非空实际输入、source/available/read/decision时点、权限及可核验trace（78F01–F10）。D还需要固定样本/模型/策略的真实消融或受控实验；公开开源模型、匹配准确率、厂商总增长均不能替代。
