# Axon/Vector机制核验与自主能力差距

本轮在独立目录完成A/B两线的证据与工程对照。新增厂商身份机制0，新增C_graph生产证据0；没有新问卷、合作方联系、数据申请、个人数据、SDK扫描/运行、生产请求或模拟/模型训练。

优先交付：

1. [六层机制差异矩阵](01_Axon_Vector机制差异矩阵.md)及[CSV](01_Axon_Vector机制差异矩阵.csv)：身份输入、关系解析、图谱更新、特征服务、价值预测、竞价消费；CONFIRMED严格限定证据作用域。
2. [最值得独立实现的机制](02_最值得复制的机制清单.md)及[CSV](02_最值得复制的机制清单.csv)：排序4项，只有3项进入最小设计，候选评分校准HOLD。
3. [最多三项下一轮方案](03_下一轮最小实验方案.md)：任务主体路由、出队重查权限、shadow选择性失效；全部NOT_EXECUTED。

支撑材料：[15项机制证据台账](MECHANISM_EVIDENCE.csv)、[原件/哈希/定位](EVIDENCE_SOURCE_LINKS.json)、[旧成果复用](REUSED_SOURCES.json)、[两次官方release GET](FETCH_MANIFEST.json)、[10条发布说明的人工复核](RELEASE_NOTES_REVIEW.json)、[状态](STATUS.json)。

A线不能将Unity Player Accounts/Exchange/RampID归给Vector，不能将Adjust机制归给Axon或Vector。公开产品说明确认的是用途，不是特征读取trace。MAX/LevelPlay核心许可仍有准入限制，本轮不新反编译、下载或复制其实现。

B线发现的是现有代码边界，而不是厂商新算法：lab设备路由与MVP账号查询的粒度差别；事务outbox与实际异步交接的差别；全局失效与含负依赖的选择性计划的差别。下一步优先E01，先核对正确来源与主体，再谈任何收益。没有扩写原系统或开发新模块。

本地验证只检查来源/文件/矩阵及计划完整性：[VALIDATION.json](VALIDATION.json)，不验真厂商生产、不执行计划。核验命令：

```powershell
Set-Location D:\GrowthResearch\axon-vector-mechanism-gap
C:\Users\89trillion\anaconda3\python.exe -X utf8 verify_delivery.py
```

获取/矩阵脚本用于本轮首次采集与成文，有覆盖防护，不重跑获取来扩大范围。研究根目录当前没有EVIDENCE_GRAPH.json，记录于INITIALIZATION_NOTE；没有补造历史图，原索引与存在的版本化矩阵均保护。历史保全以PRESERVATION_BASELINE逐文件核验。

**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 仅在新的合规材料满足78号证据链门槛后才重新评估，不创建79号生产取证任务。
