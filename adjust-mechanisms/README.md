# Adjust限定源码机制验证

本轮仅静态分析OSM034/036/038三份MIT源码，未启动SDK，未发送生产请求，未读取真实第三方身份；未修改76号程序，未创建79号生产取证任务。**C_graph.Axon=UNKNOWN，C_graph.Vector=UNKNOWN，D=UNKNOWN；原生产取证STOP。** Adjust机制不归属于Axon/Vector。

方法：选取111个Java文件条目，逐链阅读并进行文本差分。2486个初始方法定位只是词法辅助，不是完整AST/调用图；Map等泛型返回方法另补定位，精确摘录见CODE_EVIDENCE.json。全部结论限于所列版本、路径和分支；未执行OS权限、网络、崩溃恢复或服务器验证。

| 样本 | 版本 | 原始归档SHA256 |
|---|---|---|
| OSM034 | 5.5.0 | `e76d574c1155d74dbc11db8ee6fd043a10b41062c722e590ac8663f30edd7792` |
| OSM036 | 5.7.0 | `6e92756c8419253619aa57dbf6a7127e6533f8c3fecd42c672f84772d7b8c8be` |
| OSM038 | 5.8.1 | `dfee5dda1f80d86b1e0af56af77e04568f7929462a5fe09ffd6b75254180030b` |

## 交付导航

1. [Adjust身份与归因机制图](Adjust身份与归因机制图.md)
2. [三版本源码差分](三版本源码差分.md)
3. [身份标识生命周期表](身份标识生命周期表.md)
4. [已证实机制与服务端未知清单](已证实机制与服务端未知清单.md)
5. [自主Identity Resolver最小设计建议](自主IdentityResolver最小设计建议.md)
6. [下一阶段授权和测试条件](下一阶段授权和测试条件.md)

附：[版本许可复核](license-review/版本许可复核.md)、[逐版本发现矩阵](FINDINGS.csv)、[完整原文/行号/哈希](CODE_EVIDENCE.json)、[可读代码定位](CODE_LOCATIONS.md)、[最终diff索引](DIFF_INDEX.final.json)、[静态保全验证](VALIDATION.json)。旧diffs/为开发中间产物，正式差分只引用diffs-final及DIFF_INDEX.final.json。

运行复核：`python -X utf8 adjust-mechanisms/validate.py`。这只验证静态证据和历史保全，不加载Java、不连接SDK服务器。build_deliverables.py会重建本轮报告；index_and_validate.py仅追加本轮索引/证据图，不改旧对象。

SAMPLES.json保留盘点时的permission_gate/new_functional_analysis原始值；当前范围见STATUS.json，不能将旧快照当成本轮未开展。归档的HTTP Last-Modified不等于正式发布日期，正式发布日期仍UNKNOWN。
