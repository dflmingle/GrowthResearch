# 77号工程证据归档

本轮仅公开资料调查。没有SDK扫描、生产广告/身份请求、模型训练、新模拟或mock。结果是**C_graph零升级**，不是证明图谱不存在。

- [来源目录](SOURCE_CATALOG.md)保存6份正文快照的URL、日期、摘录及SHA256；其中4项真正新来源，2份为旧Workday岗位HTML别名，明确剔除新增计数。
- [全部公开GET记录](FETCH_MANIFEST.json)含21份响应；失败和soft404也保留，不作为正向或否定工程证据。
- [搜索覆盖](SEARCH_COVERAGE.json)记录限定范围、失败与停止条件。
- [来源结构](SOURCE_EVIDENCE.json)、[主张结构](CLAIMS.json)、[别名复核](ALIAS_REVIEW.json)便于机器复核。
- [完整性验证](VALIDATION.json)与[产物哈希](ARTIFACT_MANIFEST.json)记录当前成果及旧文件保留情况。

从项目根目录离线核验：

```powershell
python -X utf8 production77/validate.py
```

验证器不联网、不执行76号mock，只检查哈希、原文、引用、去重、历史保留和主图追加。会更新本轮VALIDATION、ARTIFACT_MANIFEST、ALIAS_REVIEW三个核验文件，不更改历史材料。

`prepare.py`、`fetch.py`和批次JSON为采集过程留档，不应重复运行；`build.py`为一次性打包脚本，主索引已追加后会拒绝重新打包。原始响应不可覆盖。不得以新增抓取时间代替旧岗位的首次发布或模型上线时间。

主图实际路径为`prediction-system/EVIDENCE_GRAPH.json`，沿用项目既有位置，没有在根目录新建另一个同名图。00—76历史编号文件及76号产物由冻结哈希核对。
