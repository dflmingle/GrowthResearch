# 72身份审计与73独立实验

本目录保存新72身份专题和73实验的原始公开来源、哈希、预注册、代码及结果。此前access72的六份报告和00—71全部保留。主证据图位于`../prediction-system/EVIDENCE_GRAPH.json`；72自包含图位于根目录`72_跨应用身份关联证据图.json`。

## 实际完成范围

- 身份审计复用103 AAR、67 sources.jar；没有新增SDK下载、生产测试或真实标识采集。30类标识、19组SDK/服务的覆盖程度逐项说明，并非全部SDK都已完整逆向。
- A TalkingData：STOP，仅取得Kaggle数据/规则网页壳。
- B BPID：Apache-2.0、原作者明确合成，完整ZIP已校验；42行基线/压力结果。未使用1M无标签blocking档案捏造真实实体簇。
- C Criteo：STOP，未下载行数据；用途资格和标签成熟时间外切分未通过。
- D：完全独立生成器，360行逐种子结果；不是游戏收入、平台生产图谱或真实ROAS。

## 复现与校验

使用Python 3、numpy1.26.4、pandas2.2.2、scikit-learn1.5.1、scipy1.13.1。没有在线训练依赖。原始BPID.zip只读保留；不输出档案值、不连接其他数据源。

实验脚本拒绝覆盖已有结果。要重新实验，请复制**整个本目录**到独立的新位置，保留来源、预注册和代码，再将副本中的旧`results/`移为独立归档；不要删除本工作目录的历史结果。随后在副本运行：

```powershell
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
python -X utf8 src/bpid_match.py
python -X utf8 src/bpid_fs.py
python -X utf8 src/synthetic_value.py
```

`bpid_fs.py`是预注册之后独立冻结的补充，原因和范围见`PROTOCOL_AMENDMENT_FS.md`；原始协议和结果未改。不能重跑后挑最好种子。`build_evidence.py`/`build_tables.py`/`write_results.py`是本轮生成器，运行会更新本轮衍生文件，不用于改写旧历史报告。`update_graph.py`从冻结基线追加本轮对象；`validate.py`复核文件、图引用、切分和结果一致性，不重新训练。

```powershell
python -X utf8 identity72-experiments73/validate.py
```

以上校验命令从仓库根目录运行。`VALIDATION.json`报告最终状态；`ARTIFACT_MANIFEST.json`记录脚本、协议和结果哈希。文件存在或校验PASS不等于真实生产接收/匹配/训练，E5/E6仍然未知。

## 文件索引

- `SOURCE_CATALOG.md`、`SOURCE_EVIDENCE.json`：官方原文、URL、摘录、哈希和许可边界。
- `CODE_EVIDENCE.json`、`PIXEL_EVIDENCE.json`：复用代码的版本、原包、类/方法和精确位置。
- `REUSED_EVIDENCE.json`：原图对象复用，不改历史来源。
- `IDENTIFIER_INVENTORY.json/csv`、`SDK_CAPABILITY_MATRIX.json`：字段生命周期和服务作用域。
- `DATASET_ADMISSION.json`、`BPID_ARCHIVE_AUDIT.json`：数据准入、MD5/SHA256/CRC。
- `PREREGISTRATION.md`、`PROTOCOL_AMENDMENT_FS.md`：执行前冻结方案。
- `results/B_*.csv/json/npz`、`results/D_*.csv/json`：全部切分、模型和压力条件结果。
- `HISTORY_BEFORE.json`、`EVIDENCE_GRAPH.before.json`、`EVIDENCE_INDEX.before.md`：本轮前基线，只读。

所有真实数据与合成数据、独立机制验证与厂商生产证据分别标记。本轮未新增向外发布、发送邮件或签署协议。
