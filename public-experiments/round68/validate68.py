"""Read-only historical checks and final round68 evidence integrity report."""
from pathlib import Path
from datetime import datetime, timezone
import ast, csv, hashlib, json, re

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(name):
    return json.loads((OUT / name).read_text(encoding="utf-8-sig"))


def main():
    errors, links = [], 0
    history = read("HISTORY_BEFORE68.json")
    for rel, digest in history.items():
        if rel in {"EVIDENCE_INDEX.md", "prediction-system/EVIDENCE_GRAPH.json"}:
            continue
        if sha(ROOT / rel) != digest:
            errors.append("Historical file changed: " + rel)
    oldindex = (OUT / "EVIDENCE_INDEX.before68.md").read_bytes()
    if not (ROOT / "EVIDENCE_INDEX.md").read_bytes().startswith(oldindex):
        errors.append("Historical index bytes not preserved")
    before = read("EVIDENCE_GRAPH.before68.json")
    graph = json.loads((ROOT / "prediction-system/EVIDENCE_GRAPH.json").read_text(encoding="utf-8-sig"))
    for k in ["nodes", "edges", "sources"]:
        if graph[k][:len(before[k])] != before[k]:
            errors.append("Old graph objects changed: " + k)
        ids = [x["id"] for x in graph[k]]
        if len(ids) != len(set(ids)):
            errors.append("Graph ID collision: " + k)
    for k in before:
        if k not in {"nodes", "edges", "sources"} and graph[k] != before[k]:
            errors.append("Old graph metadata changed: " + k)
    sourceids = {x["id"] for x in graph["sources"]}
    for edge in graph["edges"]:
        if not edge["id"].startswith("PD68"):
            continue
        if not set(edge["source_ids"]) <= sourceids:
            errors.append("Unresolved source ID: " + edge["id"])
        if any(edge["six_layers"].values()):
            errors.append("Dataset audit promoted to production/model layer")
    for source in graph["sources"]:
        if not source["id"].startswith("PD68"):
            continue
        if sha(ROOT / source["path"]) != source["sha256"]:
            errors.append("Source hash mismatch: " + source["id"])
    fetches = []
    for path in OUT.glob("FETCH_LEDGER_*.json"):
        fetches.extend(json.loads(path.read_text(encoding="utf-8")))
    for row in fetches:
        if row.get("path") and sha(ROOT / row["path"]) != row["sha256"]:
            errors.append("Collected source changed: " + row["id"])
    assets = read("ASSET_ACQUISITION.json") + read("ASSET_ELECTRONICS.json")
    for item in assets:
        if item.get("complete") and item.get("path"):
            if sha(ROOT / item["path"]) != item["received_bytes_sha256"]:
                errors.append("Original release changed: " + item["id"])
    with (ROOT / "68_DATASET_CATALOG.csv").open(encoding="utf-8", newline="") as f:
        datasets = list(csv.DictReader(f))
    with (ROOT / "68_EXPERIMENT_ADMISSION_MATRIX.csv").open(encoding="utf-8", newline="") as f:
        admission = list(csv.DictReader(f))
    if len(datasets) != 17 or len(admission) != 6:
        errors.append("Wrong dataset/experiment count")
    if any(row["train_now"].lower() != "false" for row in admission):
        errors.append("Unapproved model training gate")
    jewelry, electronics, journey, vibrent = [
        read(name) for name in ["AUDIT_JEWELRY.json", "AUDIT_ELECTRONICS.json",
                               "AUDIT_JOURNEY.json", "AUDIT_VIBRENT.json"]]
    if jewelry["rows"] != 95911 or jewelry["header_present"] is not False:
        errors.append("Headerless jewelry row-count correction lost")
    if electronics["rows"] != 2633521 or electronics["missing"]["user_id"] != 2069352:
        errors.append("Electronics source DQ changed")
    if electronics["period"]["monthly_rows"]["1970-01"] != 19631:
        errors.append("1970 anomaly hidden")
    if journey["rows"] != 1469307 or journey["households"] != 2469:
        errors.append("Journey full panel not verified")
    if any(table["actual_payment_ledger_present"] for table in vibrent["tables"].values()):
        errors.append("Metadata price promoted to payment")
    deliverables = sorted([p for p in ROOT.glob("68_*") if p.is_file()])
    if len(deliverables) != 5:
        errors.append("Expected exactly five main deliverables")
    for path in deliverables + [OUT / "SOURCE_CATALOG.md"]:
        text = path.read_text(encoding="utf-8")
        if "\ufffd" in text:
            errors.append("Text decoding loss in " + path.name)
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https:", "http:", "#")):
                    continue
                links += 1
                if not (path.parent / target).is_file():
                    errors.append("Broken local link: " + target)
    for path in OUT.glob("*.py"):
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    result = dict(
        status="PASS" if not errors else "FAIL",
        checked_utc=datetime.now(timezone.utc).isoformat(),
        scope="Source/permission/schema/coverage audit, not model/real income/platform effects validation",
        main_deliverables=len(deliverables), dataset_candidates=len(datasets),
        experiment_questions=len(admission), public_url_observations=len(fetches),
        complete_relevant_release_files=sum(bool(a.get("path") and a.get("complete")) for a in assets),
        full_source_domains_with_files=4, partial_prefix_downloads=1,
        historic_file_hashes_preserved=len(history) - 2,
        original_graph_objects_preserved={k: len(before[k]) for k in ["nodes", "edges", "sources"]},
        graph_additions={k: len(graph[k]) - len(before[k]) for k in ["nodes", "edges", "sources"]},
        local_links_checked=links, model_fits=0, training_admissions=0,
        uci_original_data_used=False, individual_keys_or_rows_exported=False,
        cross_source_individual_joins=0, production_ad_or_attribution_requests=0,
        authenticated_cloud_or_private_requests=0,
        raw_release_integrity_checked=True, source_document_hashes_checked=True,
        privacy_note="Only published pseudonymous keys processed source-locally; no real account/advertising identifiers collected",
        final_sha256={p.name: sha(p) for p in deliverables},
        errors=errors,
    )
    (OUT / "VALIDATION68.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "final_sha256"}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
