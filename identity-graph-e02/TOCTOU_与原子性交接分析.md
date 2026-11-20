# TOCTOU 与原子性交接分析

## 必须分开的命题

“claim 时许可有效”“最终检查时许可有效”“本地内存接收的线性化点许可有效”“外部服务实际接收有效”“外部删除完成”是不同命题。本工程只对第三项在下列受限执行模型中验证；后两项未执行、未证明。

原系统是 state.sqlite + 独立 privacy.sqlite，二者没有分布式事务。本实现没有修改原 schema，没有 ATTACH 联合提交，没有把假 sink 接入原事务，也没有声称使两库和外部服务原子提交。

## 执行序列

1. 原事件/账本/outbox 原子写入是原 MVP 的已有机制；E02 不重写。
2. E01 adapter 绑定合法合成认证回执，原 account API 批准来源；E02 排队只保存 refs/hash/bundle。
3. claim/retry：原 policy 同时检查收集时及当前许可，原 graph 验证关系，E01 reread 验证旧特征未失效；源事件、用途、outbox 和原经济修订必须仍相符。
4. prepare：再次执行上一步，记录准备时间、epoch 和 graph version。
5. 测试干预点：允许在 prepare 后撤权、删除、推进时钟到到期点或造成锁冲突。
6. 最终边界：仅在约定的单可信线程、固定 ManualClock 和精确 MemorySink 类下，依次获得 privacy 和 state 的 BEGIN IMMEDIATE。无法获得任一锁就取消，已获得的锁 rollback 释放。
7. 锁内只读验证：再次调用原 policy.allowed/require、policy.deleted、graph.active、E01 的只读任务绑定、原 visible_ledger，核验版本和同一来源。**不能在此调用会写 audit/id_counter 并提交的 features.read**；原 features.read 已由步骤4的 E01 reread 调用。通过读同一 bundle 的状态/epoch/graph 并复核当前依赖，建立其许可连续性。
8. 无回调、无 yield、无推进时钟地向内存插入 receipt，或返回同一经济身份已有 receipt。首次插入为本地交接线性化点。之后释放两库写锁，再记录成功/失败日志和 ACK 状态。

## 为什么这比“刚才检查过”强

该临界区内原两库的其他 SQLite 写连接不能提交状态变更；可信单线程调度器不能在最后一次只读验证与内存插入间运行撤权回调或推进模拟时钟。步骤5的撤权/删除会被步骤7看见；即使 epoch 不变，定时撤权/边到期也会被原 policy/graph 的当前时间检查发现。两个数据库不需要共同提交，因为该区间不写它们，真正的接收点只存在于一个进程的内存中。

这是依赖明确运行假设和源码临界区的局部一致性论证，测试仅覆盖定义的干预集合，不是任意代码的形式化验证。用户可修改 Python 对象、安装重入 trace callback、替换时钟、修改原连接或跳过状态机时，假设不再成立；不能以可变 Python 对象充当安全边界。

## 仍然必须拒绝的范围

|情形|结论|
|---|---|
|没有固定单线程、不支持的时钟或 sink|ATOMIC_HANDOFF_UNPROVEN|
|已有不属于交接器的事务|ATOMIC_HANDOFF_UNPROVEN；不擅自提交或回滚调用者事务|
|任一原数据库写锁不可得|ATOMIC_HANDOFF_UNPROVEN；无本地成功接收|
|要求本地磁盘 receipt 与两库共同持久化|ATOMIC_HANDOFF_UNPROVEN|
|要求跨进程/多机状态机一致性或故障恢复|ATOMIC_HANDOFF_UNPROVEN|
|要求 HTTP/SDK/第三方接收或外部删除|STOP，不执行|
|权限、删除、关系、purpose 或来源不合法|CANCELLED，保存具体拒绝原因|

内存接收后、状态日志或 ACK 生成前发生进程崩溃时，本实现不保证恢复，不存在可靠“恰好一次”。本地同进程 ACK 丢失只验证 sink 自身保留 receipt 时重试不重复接收；它不能外推到真实网络 ACK。

## 三种反证实现

enqueue-only：保存入队时合法 frame，撤权后直接接收。

stale-retry-epoch：首次失败后仍使用旧 epoch 的 frame 重试。

check-then-revoke-commit：先检查合法，执行撤权，再接收旧 frame。

三者都实际向独立场景内存 sink 写入错误 receipt；测试观察器立即调用原 policy/graph，按 fixture 的 device/app/account 检查接收当时的合法性，不信任被测实现自报结果。预期必须检测到未经许可接收/旧 epoch；只有发生且被检测的反例才能记为检出 PASS。

撤权前已合法接收的 receipt 单独分类。后续重试禁止继续交接，但不把过去合法接收判成新违规，也不声称能从外部召回数据。

## state 恢复与独立控制库

原 restore_state 只恢复数据文件并执行 policy.reconcile。测试验证删除记录、tombstone、原 policy epoch 保留，outbox payload 被再次清理，当前 claim 被拒绝。重放 reconcile 可能写控制库的处理状态和 SQLite 元信息；文件字节完全相等并非“控制授权未回滚”的正确判据，逻辑授权内容和拒绝结果才是直接判据。报告同时保存前后文件哈希与逻辑快照。

所有 ACK 都是 E02 内存假 sink 的本地观察，不是第三方接收证据。C_graph.Axon、C_graph.Vector、D 均 UNKNOWN，原生产取证 STOP。
