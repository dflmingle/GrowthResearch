# 78号规范与证据保全

这是身份图谱生产证据的**获取/验收设计**，不是平台证据，也不是生产适配器。当前C_graph、D均UNKNOWN，执行STOP。没有联网、外部申请、真实日志导入、mock/统计实验或76号测试重跑。

- [输入目录](SOURCE_CATALOG.md)：12份已有材料的路径、SHA256和审计代码精确位置。
- [十组拟议字段](CONTRACT_GROUPS.csv)：研究者规范，不冒充厂商schema。
- [10条候选渠道](CHANNEL_MATRIX.csv)：均UNKNOWN，未确认开放合作或联系人。
- [56行对照](MATRIX75_CROSSWALK.csv)：完整保留75号原列，仅追加取证门槛；NOT_EXECUTED。
- [拟议适配器规范](ADAPTER_SPEC.json)：G00—G08与结果分层；未实现、未连接。
- [当前准入](READINESS.json)：无生产包/授权环境/新公开URL，STOP；不创建后续任务。
- [保全核验](VALIDATION.json)和[产物清单](ARTIFACT_MANIFEST.json)：只验证本地文档/引用/历史保留，不验证任何平台事实。

可在项目根目录进行一次只读内容/哈希核验：

```powershell
python -X utf8 acquisition78/validate.py
```

脚本只更新本目录VALIDATION与ARTIFACT_MANIFEST；不导入76号模块、不运行其测试、不联网。`prepare.py`与`finalize.py`为一次性保全/打包脚本，不要重复运行或覆盖历史快照。主图沿用`prediction-system/EVIDENCE_GRAPH.json`。

未来取得实际授权材料后，先审查处理和引用许可，再另行设计/实现只读适配器；不得把真实记录改成offline-mock来通过旧审计器。
