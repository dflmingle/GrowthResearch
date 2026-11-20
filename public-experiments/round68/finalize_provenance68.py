"""Add exact raw-release origins without changing any historical graph objects."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
graphpath = ROOT / "prediction-system/EVIDENCE_GRAPH.json"
graph = json.loads(graphpath.read_text(encoding="utf-8"))
objects = json.loads((OUT / "NEW_GRAPH_OBJECTS.json").read_text(encoding="utf-8"))
rows = json.loads((OUT / "ASSET_ACQUISITION.json").read_text(encoding="utf-8")) + json.loads(
    (OUT / "ASSET_ELECTRONICS.json").read_text(encoding="utf-8"))
added = []
for row in rows:
    if not row.get("complete") or not row.get("path"):
        continue
    ident = "PD68S_raw_" + row["id"].replace("-", "_")
    assert not any(x["id"] == ident for x in graph["sources"])
    assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["received_bytes_sha256"]
    source = dict(
        id=ident, path=row["path"], sha256=row["received_bytes_sha256"], url=row["url"],
        source_date=row["observed_utc"], http_status=row["status"],
        evidence_level="【公开原始发行物完整下载证实】",
        scope="Local-only original release; not raw user-key publication, game revenue or trained-model evidence",
        permission_conditions="Source-specific conditions in 68_DATASET_LICENSE_AUDIT.md; no external personal joins",
        production_actual_proven=False, observed_target_game_delivery=False, server_model_training=False,
        raw_release_complete=True, user_rows_exported_to_report=False,
    )
    graph["sources"].append(source)
    objects["sources"].append(source)
    graph["public_data_round68"]["new_source_ids"].append(ident)
    added.append(ident)
audit_to_raw = {
    "PD68E2": ["PD68S_raw_completejourney"],
    "PD68E3": ["PD68S_raw_jewelry", "PD68S_raw_electronics"],
    "PD68E4": ["PD68S_raw_vibrent_orders", "PD68S_raw_vibrent_plans", "PD68S_raw_vibrent_spot"],
}
for edges in [graph["edges"], objects["edges"]]:
    for edge in edges:
        if edge["id"] in audit_to_raw:
            edge["source_ids"].extend(audit_to_raw[edge["id"]])
graph["public_data_round68"]["raw_release_sources_hash_verified"] = len(added)
graphpath.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "NEW_GRAPH_OBJECTS.json").write_text(json.dumps(objects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
corrections = """# 第68号读取与语义纠正记录

本轮未训练模型。下列问题在正式审计前纠正，不修改原件、不删除记录：

1. **珠宝无表头。**初步默认read_csv会把第一条交易解释成列名，并显示95,910行；正式audit_jewelry使用header=None和字符串键，保留95,911行。只将可验证的c0当时间，c3/c7/c8业务位置继续标为假设，未冒充发布者字典。
2. **Vibrent是分号CSV。**初步默认逗号读取只得到一列；正式审计sep=';'，恢复4/4/3列。套餐字段pricing.pricePerMonth.amount依旧是价格元数据，不是用户扣款。
3. **RDS时间类型。**本地rdata没有POSIXct/POSIXt构造器，返回底层epoch秒并给出warning。正式审计保留warning，用明确unit='s'转为UTC表示；没有从其他数据猜业务时区或改写原秒值。
4. **解析成功不代表业务日期正确。**电子表所有时间能被解析，但19,631行落在1970年，另有2020年记录，且卡片覆盖期不一致。invalid_times=0只表示解析器无NaT；报告明确保留异常并停止训练。
5. **零记录不同于真实零。**全年all-purchase说明和字段无缺失不能证明每户观察连续；无记录日期也不自动证明采集故障。当前没有客户风险集/退出/漏采契约，因此没有凭最长日期计算成熟真实零标签。

以上纠正全部体现在AUDIT_*.json和68号报告；没有用测试表现选择读法，也没有产生“修复后模型更好”的结果。
"""
path = OUT / "DATA_READING_CORRECTIONS.md"
assert not path.exists()
path.write_text(corrections, encoding="utf-8")
print(json.dumps(dict(raw_release_graph_sources_added=len(added), historical_graph_objects_modified=0)))
