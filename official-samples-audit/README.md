# 官方技术样本与许可审计：首轮交付

已复用并核验**30个版本、47份已有技术包**；22次新增请求仅取官方许可/仓库/发布元数据，新增SDK包下载和功能静态分析均为0。

| 交付 | 文件 |
|---|---|
| 官方样本与许可 | [核验报告](官方样本清单与许可核验.md)；[47行哈希/版本/URL清单](ACQUIRED_SAMPLE_CATALOG.csv) |
| 未取得的官方发布候选 | [发布与下载元数据](OFFICIAL_DOWNLOAD_CANDIDATES.csv)，不将发布方digest当本地验证 |
| 静态分析准入 | [可行性报告](静态分析可行性报告.md)：3份Adjust MIT源码优先；其他范围未自动放行 |
| 身份字段与调用关系 | [关系图](身份字段及调用关系图.md)；[30字段](IDENTITY_FIELD_REUSE_MATRIX.csv)；[10映射](CALL_RELATION_REUSE_MATRIX.csv)，均复用旧证据 |
| 五个机制 | [优先机制与反证](五项优先机制与反证测试.md)；[未执行测试设计](MECHANISM_TEST_DESIGN.csv) |
| 授权与下一轮 | [条件及边界](下一轮授权与测试条件.md)；[当前状态](STATUS.json) |

关键纠错：旧AppLovin适配器“license.txt”实际上是404响应；MAX/Unity公开仓库并未因此获得MIT/Apache许可。Google官方适配器repo有Apache-2.0许可，但不覆盖AppLovin适配器或核心依赖。详细原文、日期和SHA256见[来源目录](SOURCE_CATALOG.md)及[勘误](CORRECTIONS.md)。

C_graph.Axon=UNKNOWN，C_graph.Vector=UNKNOWN，D=UNKNOWN，原生产取证执行=STOP。独立实现设计不能替代厂商生产证据；本轮不展开原型开发。

本地完整性核验：

```powershell
python -X utf8 official-samples-audit/validate.py
```

验证器仅核对文档、旧件/样本哈希、许可摘录及证据引用；不读取功能实现、不启动SDK、模拟或76号测试，不联网。更新本目录VALIDATION及ARTIFACT_MANIFEST，不能把它的PASS解释成许可法律结论或生产模型证明。

prepare/fetch/inventory/build_reports/finalize为本轮留档脚本，不重复采集、不覆盖旧文件。主图沿用prediction-system/EVIDENCE_GRAPH.json；[核验](VALIDATION.json)、[产物清单](ARTIFACT_MANIFEST.json)。
