# Adjust限定源码机制验证

本轮仅静态分析OSM034/036/038三份MIT源码，未启动SDK，未发送生产请求，未读取真实第三方身份；未修改76号程序，未创建79号生产取证任务。**C_graph.Axon=UNKNOWN，C_graph.Vector=UNKNOWN，D=UNKNOWN；原生产取证STOP。** Adjust机制不归属于Axon/Vector。

方法：选取111个Java文件条目，逐链阅读并进行文本差分。2486个初始方法定位只是词法辅助，不是完整AST/调用图；Map等泛型返回方法另补定位，精确摘录见CODE_EVIDENCE.json。全部结论限于所列版本、路径和分支；未执行OS权限、网络、崩溃恢复或服务器验证。


以下是自主参考设计，不复制Adjust实现，不声称厂商采用本架构；本轮只交设计，不开发/运行解析器。

| 模块 | 最小数据与不变量 | 本轮参考 |
|---|---|---|
| Namespace Registry | issuer、tenant、app、entity_type、scope_evidence、版本；未知scope不得全局合并 | AM01–06/14 |
| Identity Resolver | 标识相等只产生候选关系；自有已认证账号可建account-device边，禁止自动升级person/household；不做真实个人概率重识别 | AM02–06 |
| Relationship Store | relation_id、from/to、粒度、evidence、quality_type、valid_from/to、recorded_at、consent_epoch、revoked_at；不破坏性union所有设备 | AM06/15–18 |
| Temporal Event Linker | event_instance_id、event_type、installation、session、occurred_at、received_at、available_at；只链接有证据的事件，不拿请求ID充收入主键 | AM07–14 |
| Consent & Deletion | collection/transmission/purpose分别授权；撤销epoch立即拒读；删除遍历关系、outbox和派生缓存，确认有范围与截止时点 | AM15–18/20 |
| Graph Feature Service | as_of及model/purpose/epoch校验；来源关系、特征materialized_at、available_at；失效/撤销后不得使用旧快照 | AM12/15/20 |
| LTV Feature Consumer | 默认仅空接口；记录非空feature_group、模型版本、decision_trace；真实标签/授权未获准不训练，收益UNKNOWN | AM12/14/22及78号契约 |
| Audit & Provenance | 原件SHA、代码/规则版本、接收/消费独立引用、缺失字段、UNKNOWN判定；mock不升级生产 | AM10–14及76/78原则 |

## 最小模式与解析规则

```text
IdentityKey = (tenant, issuer, namespace_version, entity_type, scoped_value)
Relation = (relation_id, source_key, target_key, relation_type, evidence_id,
            valid_from, valid_to, observed_at, available_at, purpose,
            consent_epoch, revoked_at, quality_type)
Event = (tenant, app, event_instance_id, event_type, install_id, session_id,
         occurred_at, received_at, available_at, consent_epoch, payload_hash)
FeatureRead = (trace_id, model_id, model_version, feature_group, nonempty_count,
               source_relation_ids, graph_version, as_of, read_at, purpose, epoch)
```

标识仅在相同tenant/issuer/namespace和作用域证据成立时比较；设备、安装、账号、人、家庭分别建节点。一个账号可被多人共享，一个人可有多个账号，因此account链接不能自动证明person。仅有模型分数变化时返回不可识别。

时间查询要求occurred_at≤available_at≤决策时刻，关系valid_from/valid_to与撤销时刻同时生效；迟到事件不能倒灌早期决策。数据删除使用tombstone和epoch阻断旧缓存，按来源遍历派生特征，拒绝旧关系重放。

幂等键用(tenant, app, event_instance_id)，事件接受与outbox原子提交；重试具有独立attempt_id，不改变经济事件主键。服务端幂等确认不能由FIFO出队或HTTP200代替。不同事件类型不得复用去重键；订单/退款、广告展示和收入修正分别表达。

## 可复现测试设计（尚未执行）

| 测试 | 自有/合成输入 | 预期 | 反例 |
|---|---|---|---|
| namespace隔离 | 两应用相同字符串但不同issuer/scope | 不合并 | 按裸字符串union必须失败 |
| 账号关系 | 两自有设备经自有账号认证；另一个共享账号 | account-device边，person仍未确定 | 相同账号不能生成已证实person边 |
| 重置 | 撤销旧设备标识epoch，新建测试标识 | 旧关系失效，禁止恢复追踪 | 旧缓存特征读应拒绝 |
| 去重 | 同实例重试、不同类型复用相同业务串、窗口外重放 | 实例幂等且不同业务不误删 | 有限10项缓存不满足持久幂等 |
| 时间 | 迟到收入、晚于决策的特征 | 拒绝早期读 | 仅按occurred_at过滤会泄漏 |
| 删除 | outbox、图边、缓存、特征快照都含待撤销记录 | 每层可核对清理及审计确认 | 只flush队列不算删除完成 |
| UNKNOWN | 删除接收/非空读取/trace任一证据 | 保持不可识别 | 把接口存在当模型消费应拒绝 |

匹配准确率、错误合并/拆分、漂移、查询延迟及撤销传播需合法测试样本和实测；本轮未产生这些数字。对LTV的独立增益需固定样本/容量/时间/预算，聚合学习、共享参数与个人关联分别消融；没有真实授权收入标签不报告收益。
