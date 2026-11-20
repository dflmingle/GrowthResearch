# E02 异步出队、重试与权限交接验证

独立目录，仅本地合成数据、Python 标准库、SQLite 和内存假 sink。只执行 E02；不执行 E03、不训练模型、不启动 SDK、不调用任何广告或身份服务。

## 复现

```powershell
Set-Location D:\GrowthResearch\identity-graph-e02
& 'C:\Users\89trillion\anaconda3\python.exe' -X utf8 run.py
& 'C:\Users\89trillion\anaconda3\python.exe' -X utf8 report.py
```

Python 3.10+，无新增 pip 依赖。固定 seed=780241。`run.py` 每次创建 `runs/<UTC>/` 新目录；可用 `--output runs/my-new-run` 指定尚不存在的本目录内路径。拒绝覆盖旧运行。`prepare.py` 已用于冻结历史基线和协议，不能覆盖重跑。

## 文件与入口

|文件|职责|
|---|---|
|machine.py|HandoffMachine、Job、MemorySink、E02 哈希链日志|
|fixtures.py|通过原 SyntheticWorld、resolver、events、graph 和 policy 构造合成输入|
|counterexamples.py|三种故意错误实现及独立 fixture 观察器，不进入正确状态机|
|run.py|unittest、可控时钟干预、逐例保存、历史保护及运行产物哈希|
|report.py|只读取真实执行结果生成报告和验收映射|
|PROTOCOL.json|测试执行前冻结的范围与一致性假设|
|REUSED_SOURCES.json|只读复用的原文件版本 SHA256|

`HandoffMachine.enqueue(outbox_ref, e01_request)` 只接收原 outbox 引用和 E01 账号任务请求。先调用只读复用的 E01 adapter，经原 resolver 回执绑定和原 account API 审核，再建立本地任务。裸账号不能代替认证回执。任务只保存来源引用、哈希、E01 bundle 与已批准 lineage，不复制原 payload 到新持久队列。

调用 `claim(job)`、`deliver(job)` 或便捷 `run(job)`。`fail_before=True` 注入接收前失败；`lose_ack=True` 在内存接收后丢失本地 ACK；`before_commit` 只在准备与最终临界区之间运行，专用于受控干预，绝不在最终临界区运行用户回调。

## 六种状态

`QUEUED → CLAIMED → REVALIDATING → LOCAL_ACK` 是合法成功路径。检查失败到 `CANCELLED`。接收前失败或本地 ACK 丢失到 `RETRY_PENDING`，重试必须重新 claim 和校验。终态不重放。原 MVP outbox 的 `LOCAL_ONLY_PENDING` 不会被适配器改写成“第三方已发送”；生命周期变化造成的原删除处理仍由原 policy 执行。

每次 claim、retry、pre-handoff 调用原 policy/graph，并调用 E01 `reread` 验证旧 bundle 当前仍可读。最终交接在写锁内再次调用原 policy、graph、E01 task binding 及原经济版本可见性 API。失效 bundle 不重新计算替换，不用旧 epoch 掩盖撤销。因原全局失效导致无关变更也取消，是保守行为；选择性缓存优化属于未执行的 E03。

## 权限四个维度

1. collection：原事件入库和 E01 账号来源审核的历史事实，并非永久使用许可。
2. transmission：本地任务 `transmission_enabled` 只能禁用本地交接，不能授予原 policy 没有的权限。它不是厂商传输协议或新造的合法处理依据。
3. purpose：任务、认证回执、源事件及原 policy 必须为同一用途；其他 purpose 不得复用旧任务。
4. delete：使用原独立控制库的 `policy.deleted`、原 tombstone 和 reconcile；state 恢复不能回滚控制库。

## 可证明的成功范围

仅支持可信单线程、原 `ManualClock`、固定内存 sink、进程不中断的本地调度。最终权限读取到内存 receipt 插入之间没有让出执行权、用户回调或时钟推进，同时持有原两库的 `BEGIN IMMEDIATE` 写锁。线性化点是内存 receipt 插入，不是两个数据库的提交；读锁区最后 rollback 仅释放锁。

外部 sink、持久化/重启保证、既存事务、锁获取失败或不支持的执行边界，输出 **ATOMIC_HANDOFF_UNPROVEN** 并取消；不能把“提交前检查过”当分布式原子性证明。详见 TOCTOU_与原子性交接分析.md。

## 幂等与删除边界

原事件和账本去重仍由原 MVP 负责。假 sink 使用原经济身份 `(app_ref, source, economic_key, revision)` 作为接收 receipt 的幂等键，不另建经济账本，不把两个不同 revision 累加当新收入。相同接收重试只返回已有 receipt，不能两次接收。同进程 ACK 丢失可复核；进程重启丢失内存不在范围内。

撤权/删除后拒绝新的交接，不冒称撤回已经完成的接收。删除测试把 `synthetic:e02-memory` 登记为额外 sink，原删除案保留该 sink 的待确认状态；本任务不把原本地删除 ACK 自动扩展到它。内存 receipt 是测试审计记录，不是真实个人记录，不证明第三方擦除或模型遗忘。

## 审计及安全约束

每例保存完整输入、预期、实际、状态转换、时间、epoch、关系有效区间、用途/删除结果、取消原因、原 outbox/event/ledger/控制库及原 MVP 哈希链。`ARTIFACT_SHA256.json` 可核验运行文件；`SOURCE_SHA256.json` 对应真实执行时源码。首轮错误保留；不预填 PASS。

运行时 audit hook 拒绝所有 socket 事件和子进程，代码不含 HTTP/SDK 客户端。这是进程内防误调用措施，不是 OS 沙箱或外部网络抓包证明。只读导入历史代码，禁止生成历史目录 pycache。主索引与证据图不修改。

C_graph.Axon = UNKNOWN；C_graph.Vector = UNKNOWN；D = UNKNOWN；原生产取证 = STOP。不创建79号任务。
