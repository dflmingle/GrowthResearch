# 七组件与14条规则的工程映射

本系统是自主的本地合成工程MVP，不是Axon/Vector逆向复现，不证明真实自然人身份、生产模型消费或LTV增益。仅使用Python标准库和SQLite；未启动MAX/LevelPlay、外部身份接口、广告网络或真实用户数据。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 00—78、76程序与既有研究证据不修改，主索引/证据图也不追加。
| 组件 | 已实现机制 | 验收 |
|---|---|---|
| IdentityNamespaceRegistry | 命名空间/实体注册、scope未知拒识、显式映射许可，不自动做同人合并 | V01/V02 |
| DeterministicIdentityResolver | 本地合成HMAC凭证、issuer/audience/有效期与nonce校验；仅账号控制关系 | V03/V04/R13/R15 |
| ConfidenceAwareRelationshipGraph | typed边、候选隔离、cannot-link、修订撤销/拆分和标识重置 | V05–V08/R01/R02/R17 |
| TemporalEventLinker | 事件幂等、经济主键与修订、事务outbox、多时钟与观察覆盖 | V09–V12/R05/R06/R08/R19 |
| ConsentAndDeletionManager | 独立控制epoch、撤销、device→app实例删除传播、逐sink确认、恢复时清理 | V14–V17/R11/R14/R20 |
| GraphFeatureService | 按账号/设备/应用实例限定遍历，防共享设备污染，as-of与当前权限/版本双门控 | V04/V07/V08/V11–V14/R03/R17 |
| ProvenanceAuditLog | 哈希链与独立形状/引用/产品/时间判定；缺证不可识别、来源不足不可信 | V18–V20/R09/R10/R16 |

## 核心不变量

Person、Account、Device、App Instance分别是实体粒度；Event是不可混用的事件实例；Identity Edge是独立、有版本的关系。另保留household粒度以避免与person混淆。本MVP不建立任何person自动推断关系。

命名空间键包括tenant、issuer、app、sector、entity_type、scope和version。相同裸token不跨命名空间比较；显式映射权限也不是同人证据。所有issuer和标识输入限synthetic:/syn:，事件/来源限synth:。这只是合成输入防误用护栏，不是生产安全隔离。

认证只使用公开、固定种子的本地HMAC密钥，绝不能作为真实认证服务。nonce和范围保存在独立privacy.sqlite；graph公开写账号边必须引用已认证且scope匹配的回执。Account→多Device和Device→多Account允许存在，但feature不能沿共享设备扩散到另一个账号。

candidate_same_entity无论分数多高都不激活。same_device用于合成已知设备别名的显式声明，可构造可撤销连通视图；不是概率候选传递闭包。加入cannot-link先检查约束，迟到约束可隔离已存在错误边。原始edge revisions保留；撤销改变当前视图而非不可逆union。

事件发生、接收、本地观察、消费者可用时间分别保存。只读取当时已知关系和经济修订；原始经济时间用于窗口，更正按已知版本选最新净额，不把所有revision相加。未来available_at被排除。历史重放在今天物化，不允许伪造过去的active消费。

授权epoch与graph_version全局保守失效：任何源数据/关系变化可清除全部旧bundle，牺牲性能以降低MVP遗漏失效风险。实际read还核对当前授权及边有效/撤销/到期状态，即使时钟变化而未写新图，也不能消费过期关系。

## 删除与恢复

privacy.sqlite独立保存撤销、删除、key tombstone、nonce和单调ID计数；state.sqlite保存图/事件/特征。支持的备份/恢复只回滚state，之后按保留的控制状态重放删除/失效。若操作员同时回滚/丢失privacy.sqlite，当前MVP不能保证防复活，必须STOP，详见风险。

设备删除覆盖其已知App Instance及其事件/账本/outbox，绝不沿账号扩展到其他设备；账号删除只清其明确归属的记录，保留另一个账号在共享设备上的数据。派生bundle采取全局清空。删除输出逐sink状态；未确认导出为ACK_PENDING；关联已训模型的合成血缘标记MODEL_ERASURE_UNKNOWN，不伪称参数已遗忘。

上述是逻辑清理与局部恢复协议，不能证明磁盘取证级擦除、真实partner执行或训练权重遗忘。不存在真实外部export/训练服务；相关状态是合成契约测试。

| 原规则 | 实现 | 测试/限制 |
|---|---|---|
| R01 | NS | V01/V02 |
| R02 | DR | V03/R15 |
| R03 | PA | V18派生ID反例 |
| R04 | RG | V05 |
| R05 | RG | V06/R01 |
| R06 | DR/FS | V04 |
| R07 | RG/CD | R02 |
| R08 | RG/FS | V07 |
| R09 | EL/FS | V08–V13/R06/R19 |
| R10 | CD/FS | V14/R20 |
| R11 | CD | V15/V16/R14 |
| R12 | CD | V17 |
| R13 | PA/CD | V20/R09；仅合成元数据，不证明真实删除合规 |
| R14 | PA | V18–V20/R10/R16 |
