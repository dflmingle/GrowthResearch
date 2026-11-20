# 74号身份图谱与买量优势审计

本目录只保存公开契约、来源核验、对照实验设计及证据追加脚本，不训练、不读取新的真实用户资料、不调用生产匹配/广告接口。

- `SOURCE_EVIDENCE.json`：14条正文摘录，原始/最终URL、日期、raw/text SHA256、行号、等级和未知点。
- `REUSED_EVIDENCE.json`：20条历史图来源逐哈希复用。
- `FETCH_MANIFEST.json`、`SEARCH_COVERAGE.json`：30次公开GET及覆盖/失败边界；搜索导航和壳不作生产证据。
- `CLAIMS.json`与根目录74 CSV：A/B/C_id/C_graph/D分别判断，UNKNOWN不解释成不存在。
- `EXPERIMENT_READINESS.json`：未来真实对照准入，当前STOP；没有模型效果。
- `CORRECTIONS.md`：旧导航引用及新正文提取问题，不覆盖历史。
- `HISTORY_BEFORE.json`、`EVIDENCE_GRAPH.before.json`、`EVIDENCE_INDEX.before.md`：修改前基线。
- `VALIDATION.json`、`ARTIFACT_MANIFEST.json`：最终历史保留、来源、图和交付一致性。

从`D:\GrowthResearch`运行`python -X utf8 identity-value74/validate.py`可校验，不重新下载或训练。`fetch.py`保存响应并拒绝覆盖；`build_evidence.py`只生成本轮衍生目录；`update_graph.py`从冻结基线追加本轮图/索引。所有真实用途/关联/投放仍以取得相应授权为前提，公开文档的API示例从未执行。
