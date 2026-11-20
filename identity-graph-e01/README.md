# E01 账号任务路由与跨App来源分区

仅执行 `axon-vector-mechanism-gap/03_下一轮最小实验方案.md` 的 E01。使用 Python 标准库、原 MVP 合成 fixture 和本目录独立 SQLite；无模型训练、SDK、生产请求或真实身份记录。金额以整数 micros 保存，7/3/99 只是合成账本单位。

## 复现

```powershell
Set-Location D:\GrowthResearch\identity-graph-e01
& 'C:\Users\89trillion\anaconda3\python.exe' -X utf8 run.py
& 'C:\Users\89trillion\anaconda3\python.exe' -X utf8 report.py
```

也可使用能导入 sqlite3 的 Python 3.9+；不需要 pip 安装。`run.py` 每次建立新的 `runs/<UTC>/`，不覆盖已有运行。`--output` 只接受本 E01 目录下尚不存在的路径。`prepare.py` 是已执行过的一次性协议与保护基线冻结工具；不要重新运行或覆盖基线。

## 入口与依赖

`adapter.py` 提供 `TaskAwareAdapter.extract(request)` 与 `reread(request, prior)`。`fixtures.py` 通过原 `SyntheticWorld`、resolver、graph、events、policy 构造测试；`run.py` 使用 unittest 运行断言；`counterexamples.py` 故意破坏正确输出，独立的 fixture 等式检查器必须识别这些错误。

只读导入：`../identity-graph-mvp/identity_mvp/system.py`、`fixtures.py`，以及 `../identity-graph-ltv-lab/lab/adapter.py`。身份解析、签名认证、授权、有效关系选择、经济修订/去重、可见账本及 bundle 失效，均由原系统负责。本目录不提供替代 resolver 或账本规则。

## 输入和输出契约

输入严格包含 `task_ref`、`target_install_ref`、`subject_type=account`、`auth_receipt`、`prediction_at`、`since_at`、`purpose`、`authorization_context`。后者含本地环境、同一 purpose 和源 App 名称 allowlist。裸 `account_ref` 被拒绝。预测时刻必须等于当前合成时钟，防止后物化值倒填历史。

认证回执是原 resolver 已接受的 `auth_nonces` 记录引用，绑定 account/目标安装/purpose；适配器再通过原 policy 与 graph 检查当前有效关系。**这只是可信本地合成调用中的回执引用，不是可向不可信远程调用方开放的 bearer token 或真实 SSO 实现。** 原 assertion 的 60 秒 TTL 是登录证明的接收期限，不被伪造成会话期限。后续读取以原关系、权限和删除状态为准。

`OK` 返回 `cross_app_history`、`target_app_history`，包含逐币种有符号观察金额、完整金额或 null、观察状态、缺失理由、来源安装及账本/事件/coverage 引用；同时保存原 account 总额、lineage、图版本、policy epoch、实际可用时间、认证及来源审计。目标 App 依据产品 namespace 的 App 字段分类，同产品重装仍属于目标历史，不把安装实例变化误作跨App。

`out_of_task_scope` 是原 account API 已批准、但不在任务选择范围内的本地审计分区；allowlist 仅缩小分类选择，不是授权凭证。当前接口返回原 account 级审计元数据，不能直接作为面向不同权限远程租户的最小化数据 API。

`DENIED` 表示任务绑定或原权限/关系不可用；`UNSUPPORTED_PARTITION` 表示原 API 的逐条来源不足或不一致，该子目标停止，金额返回 null，绝不扫描整个账本补齐。缺失观察不能声明完整零值。部分分区观察完整性保守继承原 account API 的完整性限制。

`reread` 不把旧输出当可继续消费的能力；它重新绑定当前任务并调用原 features.read，原 bundle 失效就拒绝。已经导出的普通 JSON 不能被远程召回或擦除，调用者不得跳过 reread 使用旧值；本实验不声称实现外部删除或分布式原子交接。

## 证据文件

运行目录包含 PARAMETERS、源码哈希、unittest 原始日志、逐例 CASE.json、MVP 哈希链审计、最终政策、SQLite 原始状态及控制库、CASE_RESULTS.csv、SUMMARY、历史完整性检查和全部运行产物哈希。首轮失败记录保留，不覆盖为 PASS。`LATEST_RUN.json` 指向最近一次真实执行；报告由 `report.py` 读取其结果生成，不能先填 PASS。

本地运行使用 audit hook 拒绝 socket 连接、解析、绑定、发送及新子进程；它是额外的进程内防误操作，不是操作系统沙箱或独立网络抓包证明。代码本身没有广告/身份网络客户端。未修改主索引或证据图。

## 固定边界

C_graph.Axon = UNKNOWN；C_graph.Vector = UNKNOWN；D = UNKNOWN；原生产取证 = STOP。本地通过只支持 E01 的账号粒度路由和来源分区工程行为，不证明自然人跨设备识别，不证明厂商生产消费，不报告预测增益，也不授权启动 E02/E03。
