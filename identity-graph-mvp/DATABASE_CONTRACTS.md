# SQLite Schema与数据契约

本系统是自主的本地合成工程MVP，不是Axon/Vector逆向复现，不证明真实自然人身份、生产模型消费或LTV增益。仅使用Python标准库和SQLite；未启动MAX/LevelPlay、外部身份接口、广告网络或真实用户数据。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 00—78、76程序与既有研究证据不修改，主索引/证据图也不追加。
| 数据库 | 表 | 职责 |
|---|---|---|
| state.sqlite | audit_log | 有序SHA256链 |
| state.sqlite | coverage | COMPLETE/MISSING/EXITED观察声明 |
| state.sqlite | edge_revisions | 关系来源/scope/置信度/有效/观察/可用/撤销/版本 |
| state.sqlite | entities | 分粒度实体和合成token/tombstone |
| state.sqlite | events | 事件幂等、时钟和修订 |
| state.sqlite | feature_bundles | 派生特征和血缘/权限/graph版本 |
| state.sqlite | ledger | 经济主键、金额micros、currency、IAA/IAP及更正 |
| state.sqlite | meta | 本地环境和图版本 |
| state.sqlite | namespace_mappings | 显式账号namespace映射许可，不是实体合并 |
| state.sqlite | namespaces | 作用域注册 |
| state.sqlite | outbox | 与事件同事务的本地待处理记录，不发送 |
| state.sqlite | training_snapshots | 仅合成训练血缘，不训练 |
| privacy.sqlite | auth_nonces | 认证重放拒绝和app/account/purpose范围 |
| privacy.sqlite | control_meta | 单调epoch、ID计数和删键摘要 |
| privacy.sqlite | deletion_sinks | 逐sink确认/未确认 |
| privacy.sqlite | deletions | 删除范围、状态和训练影响 |
| privacy.sqlite | erased_entities | 删除扩展实体的控制tombstone |
| privacy.sqlite | policies | 授权/撤销effective与observed和epoch |

实际建表语句在identity_mvp/schema.sql和control_schema.sql；DATABASE_SCHEMA.json从本轮实际运行的demo数据库PRAGMA导出，不是手写虚拟结构。源研究数据契约原字节保留在contracts/，作为参考，不宣称完整实现厂商schema或全部参考扩展。

## API契约

| 入口 | 必需输入 | 输出/拒绝 |
|---|---|---|
| namespaces.register/create | synthetic issuer、typed scope、syn token | namespace/entity引用；UNKNOWN_SCOPE拒绝 |
| resolver.login | 本地签名assertion、issuer/aud、account/app/device、nonce、iat/exp、purpose | ACCOUNT_RELATION_ESTABLISHED；错签名/时效/重放拒绝；无person升级 |
| graph.add/revoke/reset_device | typed端点、synth来源、scope、confidence/quality、有效/可用时间 | ACTIVE/CANDIDATE/CONFLICT或修订；账号边需认证回执 |
| events.ingest | app、source/event instance、revision、UTC时钟、可选明确account/economic key | ACCEPTED/DUPLICATE_EVENT/DUPLICATE_LEDGER；冲突拒绝 |
| features.compute/read | subject、as_of/since、purpose、当前clock | 观察金额/缺失状态、lineage、bundle或拒绝；不输出预测LTV |
| policy.set/delete/acknowledge | subject scope、有效时点、source、合成sink | epoch、删除逐sink状态；未确认不报完成 |
| audit.verify/assess_chain | hash链或独立匿名证据包 | 本地链一致性/UNTRUSTED/NOT_IDENTIFIABLE；所有厂商结论保持UNKNOWN |

时间统一为整数UTC epoch秒，拒绝浮点/负值/未来预测时点和本地available_at倒填。有效区间为[valid_from,valid_to)，撤销/到期从边界时刻起拒绝；可用时点≤预测as_of，当前授权必须在实际read时成立。模拟时钟仅前进，代码不调用真实服务时钟。

金额使用integer micros，不用浮点；币种分别汇总，多币种没有汇率就返回MIXED_CURRENCY/总额null。ledger唯一键(app_ref,source,economic_key,revision)，修订必须串到前一revision；事件唯一键(tenant,app_ref,source,event_id,revision)。相同幂等键不同payload报冲突，不能静默改值。

无事件且观察完整才可返回revenue_micros=0；缺采/退出/不完整时该字段null，observed_revenue_micros只代表已观察账本金额，不是完整LTV。coverage为合成声明，无自动证明真实观察完整性的能力。App/Person/Account与Event/Edge永不混用主键。

落盘隐私：本MVP只存合成token；删除清当前token/payload/amount及所有bundle，但保留合成引用与审计链。没有真实PII vault、密钥管理或介质擦除。外部回执只是带synth来源的本地声明；源码使用者不应把它当真实第三方删除/独立审核证明。
